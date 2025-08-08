"""
Chemical file format support for reading and writing molecular data.

This module provides support for common chemical file formats including:
- MOL files (MDL Molfile format)
- SDF files (Structure Data Format)
- XYZ files (simple coordinate format)
- PDB files (Protein Data Bank format)
"""

import re
from typing import List, Dict, Optional, Any, Union, TextIO
from pathlib import Path
from dataclasses import dataclass
from chemesty.molecules.molecule import Molecule
from chemesty.elements.data_driven_element import DataDrivenElement


@dataclass
class Atom:
    """Represents an atom with coordinates and properties."""
    symbol: str
    x: float
    y: float
    z: float
    charge: int = 0
    mass_difference: int = 0


@dataclass
class Bond:
    """Represents a bond between two atoms."""
    atom1_idx: int
    atom2_idx: int
    bond_type: int = 1  # 1=single, 2=double, 3=triple, 4=aromatic
    stereo: int = 0


@dataclass
class MolecularStructure:
    """Represents a complete molecular structure."""
    atoms: List[Atom]
    bonds: List[Bond]
    title: str = ""
    properties: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


class MOLFileReader:
    """Reader for MDL MOL file format."""
    
    @staticmethod
    def read_mol_file(file_path: Union[str, Path]) -> MolecularStructure:
        """
        Read a MOL file and return a MolecularStructure.
        
        Args:
            file_path: Path to the MOL file
            
        Returns:
            MolecularStructure object
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"MOL file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return MOLFileReader._parse_mol_content(f)
    
    @staticmethod
    def read_mol_string(mol_string: str) -> MolecularStructure:
        """
        Parse a MOL format string and return a MolecularStructure.
        
        Args:
            mol_string: MOL format string
            
        Returns:
            MolecularStructure object
        """
        from io import StringIO
        return MOLFileReader._parse_mol_content(StringIO(mol_string))
    
    @staticmethod
    def _parse_mol_content(file_obj: TextIO) -> MolecularStructure:
        """Parse MOL file content from a file-like object."""
        lines = [line.rstrip('\n\r') for line in file_obj.readlines()]
        
        if len(lines) < 4:
            raise ValueError("Invalid MOL file: too few lines")
        
        # Header block (first 3 lines)
        title = lines[0] if lines[0].strip() else "Untitled"
        # lines[1] is program info, lines[2] is comment - we skip these
        
        # Counts line (4th line)
        counts_line = lines[3]
        if len(counts_line) < 6:
            raise ValueError("Invalid MOL file: malformed counts line")
        
        try:
            num_atoms = int(counts_line[0:3].strip())
            num_bonds = int(counts_line[3:6].strip())
        except ValueError:
            raise ValueError("Invalid MOL file: cannot parse atom/bond counts")
        
        # Atom block
        atoms = []
        atom_start = 4
        for i in range(num_atoms):
            line_idx = atom_start + i
            if line_idx >= len(lines):
                raise ValueError(f"Invalid MOL file: missing atom line {i+1}")
            
            line = lines[line_idx]
            if len(line) < 31:
                raise ValueError(f"Invalid MOL file: malformed atom line {i+1}")
            
            try:
                x = float(line[0:10].strip())
                y = float(line[10:20].strip())
                z = float(line[20:30].strip())
                symbol = line[31:34].strip()
                
                # Optional fields
                mass_diff = int(line[34:36].strip()) if len(line) > 35 and line[34:36].strip() else 0
                charge = int(line[36:39].strip()) if len(line) > 38 and line[36:39].strip() else 0
                
                atoms.append(Atom(symbol, x, y, z, charge, mass_diff))
            except (ValueError, IndexError) as e:
                raise ValueError(f"Invalid MOL file: cannot parse atom line {i+1}: {e}")
        
        # Bond block
        bonds = []
        bond_start = atom_start + num_atoms
        for i in range(num_bonds):
            line_idx = bond_start + i
            if line_idx >= len(lines):
                raise ValueError(f"Invalid MOL file: missing bond line {i+1}")
            
            line = lines[line_idx]
            if len(line) < 9:
                raise ValueError(f"Invalid MOL file: malformed bond line {i+1}")
            
            try:
                atom1 = int(line[0:3].strip()) - 1  # Convert to 0-based indexing
                atom2 = int(line[3:6].strip()) - 1
                bond_type = int(line[6:9].strip())
                stereo = int(line[9:12].strip()) if len(line) > 11 and line[9:12].strip() else 0
                
                if atom1 < 0 or atom1 >= num_atoms or atom2 < 0 or atom2 >= num_atoms:
                    raise ValueError(f"Invalid bond: atom indices out of range")
                
                bonds.append(Bond(atom1, atom2, bond_type, stereo))
            except (ValueError, IndexError) as e:
                raise ValueError(f"Invalid MOL file: cannot parse bond line {i+1}: {e}")
        
        return MolecularStructure(atoms, bonds, title)


class MOLFileWriter:
    """Writer for MDL MOL file format."""
    
    @staticmethod
    def write_mol_file(structure: MolecularStructure, file_path: Union[str, Path]) -> None:
        """
        Write a MolecularStructure to a MOL file.
        
        Args:
            structure: MolecularStructure to write
            file_path: Output file path
        """
        file_path = Path(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            MOLFileWriter._write_mol_content(structure, f)
    
    @staticmethod
    def write_mol_string(structure: MolecularStructure) -> str:
        """
        Convert a MolecularStructure to MOL format string.
        
        Args:
            structure: MolecularStructure to convert
            
        Returns:
            MOL format string
        """
        from io import StringIO
        output = StringIO()
        MOLFileWriter._write_mol_content(structure, output)
        return output.getvalue()
    
    @staticmethod
    def _write_mol_content(structure: MolecularStructure, file_obj: TextIO) -> None:
        """Write MOL content to a file-like object."""
        # Header block
        file_obj.write(f"{structure.title}\n")
        file_obj.write("  Chemesty\n")  # Program info
        file_obj.write("\n")  # Comment line
        
        # Counts line
        num_atoms = len(structure.atoms)
        num_bonds = len(structure.bonds)
        file_obj.write(f"{num_atoms:3d}{num_bonds:3d}  0  0  0  0  0  0  0  0999 V2000\n")
        
        # Atom block
        for atom in structure.atoms:
            file_obj.write(f"{atom.x:10.4f}{atom.y:10.4f}{atom.z:10.4f} {atom.symbol:<3s}")
            file_obj.write(f"{atom.mass_difference:2d}{atom.charge:3d}  0  0  0  0  0  0  0  0  0  0\n")
        
        # Bond block
        for bond in structure.bonds:
            atom1 = bond.atom1_idx + 1  # Convert to 1-based indexing
            atom2 = bond.atom2_idx + 1
            file_obj.write(f"{atom1:3d}{atom2:3d}{bond.bond_type:3d}{bond.stereo:3d}  0  0  0\n")
        
        # End marker
        file_obj.write("M  END\n")


class SDFFileReader:
    """Reader for Structure Data Format (SDF) files."""
    
    @staticmethod
    def read_sdf_file(file_path: Union[str, Path]) -> List[MolecularStructure]:
        """
        Read an SDF file and return a list of MolecularStructure objects.
        
        Args:
            file_path: Path to the SDF file
            
        Returns:
            List of MolecularStructure objects
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"SDF file not found: {file_path}")
        
        structures = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split by $$$$ delimiter
        mol_blocks = content.split('$$$$')
        
        for mol_block in mol_blocks:
            mol_block = mol_block.strip()
            if not mol_block:
                continue
            
            # Parse the MOL part and properties
            lines = mol_block.split('\n')
            
            # Find the end of the MOL block (M  END)
            mol_end_idx = -1
            for i, line in enumerate(lines):
                if line.strip() == 'M  END':
                    mol_end_idx = i
                    break
            
            if mol_end_idx == -1:
                continue  # Skip malformed entries
            
            # Parse MOL part
            mol_content = '\n'.join(lines[:mol_end_idx + 1])
            try:
                structure = MOLFileReader.read_mol_string(mol_content)
            except ValueError:
                continue  # Skip malformed MOL blocks
            
            # Parse properties
            properties = {}
            i = mol_end_idx + 1
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith('>'):
                    # Property header
                    prop_match = re.match(r'>\s*<(.+?)>', line)
                    if prop_match:
                        prop_name = prop_match.group(1)
                        i += 1
                        if i < len(lines):
                            prop_value = lines[i].strip()
                            properties[prop_name] = prop_value
                i += 1
            
            structure.properties.update(properties)
            structures.append(structure)
        
        return structures


class SDFFileWriter:
    """Writer for Structure Data Format (SDF) files."""
    
    @staticmethod
    def write_sdf_file(structures: List[MolecularStructure], file_path: Union[str, Path]) -> None:
        """
        Write a list of MolecularStructure objects to an SDF file.
        
        Args:
            structures: List of MolecularStructure objects
            file_path: Output file path
        """
        file_path = Path(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, structure in enumerate(structures):
                # Write MOL block
                mol_content = MOLFileWriter.write_mol_string(structure)
                f.write(mol_content)
                
                # Write properties
                for prop_name, prop_value in structure.properties.items():
                    f.write(f">  <{prop_name}>\n")
                    f.write(f"{prop_value}\n\n")
                
                # Write delimiter (except for last structure)
                if i < len(structures) - 1:
                    f.write("$$$$\n")


class XYZFileReader:
    """Reader for XYZ coordinate files."""
    
    @staticmethod
    def read_xyz_file(file_path: Union[str, Path]) -> MolecularStructure:
        """
        Read an XYZ file and return a MolecularStructure.
        
        Args:
            file_path: Path to the XYZ file
            
        Returns:
            MolecularStructure object (without bonds)
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"XYZ file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if len(lines) < 2:
            raise ValueError("Invalid XYZ file: too few lines")
        
        try:
            num_atoms = int(lines[0])
        except ValueError:
            raise ValueError("Invalid XYZ file: cannot parse atom count")
        
        title = lines[1] if len(lines) > 1 else "Untitled"
        
        atoms = []
        for i in range(num_atoms):
            line_idx = i + 2
            if line_idx >= len(lines):
                raise ValueError(f"Invalid XYZ file: missing atom line {i+1}")
            
            parts = lines[line_idx].split()
            if len(parts) < 4:
                raise ValueError(f"Invalid XYZ file: malformed atom line {i+1}")
            
            try:
                symbol = parts[0]
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                atoms.append(Atom(symbol, x, y, z))
            except (ValueError, IndexError) as e:
                raise ValueError(f"Invalid XYZ file: cannot parse atom line {i+1}: {e}")
        
        return MolecularStructure(atoms, [], title)


class XYZFileWriter:
    """Writer for XYZ coordinate files."""
    
    @staticmethod
    def write_xyz_file(structure: MolecularStructure, file_path: Union[str, Path]) -> None:
        """
        Write a MolecularStructure to an XYZ file.
        
        Args:
            structure: MolecularStructure to write
            file_path: Output file path
        """
        file_path = Path(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{len(structure.atoms)}\n")
            f.write(f"{structure.title}\n")
            
            for atom in structure.atoms:
                f.write(f"{atom.symbol} {atom.x:.6f} {atom.y:.6f} {atom.z:.6f}\n")


# Convenience functions
def read_molecule_file(file_path: Union[str, Path]) -> Union[MolecularStructure, List[MolecularStructure]]:
    """
    Read a molecular structure file, automatically detecting the format.
    
    Args:
        file_path: Path to the molecular structure file
        
    Returns:
        MolecularStructure for single-molecule formats (MOL, XYZ)
        List[MolecularStructure] for multi-molecule formats (SDF)
        
    Raises:
        ValueError: If the file format is not supported
        FileNotFoundError: If the file doesn't exist
    """
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()
    
    if suffix == '.mol':
        return MOLFileReader.read_mol_file(file_path)
    elif suffix == '.sdf':
        return SDFFileReader.read_sdf_file(file_path)
    elif suffix == '.xyz':
        return XYZFileReader.read_xyz_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def write_molecule_file(structure: Union[MolecularStructure, List[MolecularStructure]], 
                       file_path: Union[str, Path]) -> None:
    """
    Write molecular structure(s) to a file, automatically detecting the format.
    
    Args:
        structure: MolecularStructure or list of structures to write
        file_path: Output file path
        
    Raises:
        ValueError: If the file format is not supported
    """
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()
    
    if suffix == '.mol':
        if isinstance(structure, list):
            if len(structure) != 1:
                raise ValueError("MOL format supports only single molecules")
            structure = structure[0]
        MOLFileWriter.write_mol_file(structure, file_path)
    elif suffix == '.sdf':
        if not isinstance(structure, list):
            structure = [structure]
        SDFFileWriter.write_sdf_file(structure, file_path)
    elif suffix == '.xyz':
        if isinstance(structure, list):
            if len(structure) != 1:
                raise ValueError("XYZ format supports only single molecules")
            structure = structure[0]
        XYZFileWriter.write_xyz_file(structure, file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def structure_to_molecule(structure: MolecularStructure) -> Molecule:
    """
    Convert a MolecularStructure to a Molecule object.
    
    Args:
        structure: MolecularStructure to convert
        
    Returns:
        Molecule object
        
    Note:
        This is a basic conversion that creates a molecular formula
        from the atoms. More sophisticated conversion would require
        additional chemical analysis.
    """
    # Count atoms by element
    element_counts = {}
    for atom in structure.atoms:
        element_counts[atom.symbol] = element_counts.get(atom.symbol, 0) + 1
    
    # Create molecular formula
    formula_parts = []
    for symbol in sorted(element_counts.keys()):
        count = element_counts[symbol]
        if count == 1:
            formula_parts.append(symbol)
        else:
            formula_parts.append(f"{symbol}{count}")
    
    formula = ''.join(formula_parts)
    
    # Create molecule with the formula
    molecule = Molecule(formula=formula)
    
    # Add any properties from the structure
    for prop_name, prop_value in structure.properties.items():
        setattr(molecule, prop_name, prop_value)
    
    return molecule