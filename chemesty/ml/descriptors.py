"""
Molecular descriptors for machine learning applications.

This module provides tools for calculating molecular descriptors and features
that can be used as input for machine learning models.
"""

from typing import Dict, List, Optional, Any, Union
import numpy as np
import math
from chemesty.molecules.molecule import Molecule
from chemesty.molecules.file_formats import MolecularStructure, Atom


class MolecularDescriptors:
    """
    Calculator for molecular descriptors and features.
    
    This class provides methods for calculating various molecular descriptors
    that are commonly used in machine learning applications for chemical
    property prediction.
    """
    
    def __init__(self):
        """Initialize the molecular descriptors calculator."""
        self.descriptor_names = [
            'molecular_weight',
            'num_atoms',
            'num_heavy_atoms',
            'num_bonds',
            'num_aromatic_atoms',
            'num_heteroatoms',
            'formal_charge',
            'num_rotatable_bonds',
            'num_h_donors',
            'num_h_acceptors',
            'tpsa',  # Topological Polar Surface Area
            'logp',  # Partition coefficient
            'num_rings',
            'num_aromatic_rings',
            'num_saturated_rings',
            'molecular_refractivity',
            'balaban_j',
            'bertz_ct',  # Complexity index
            'chi0v',  # Connectivity indices
            'chi1v',
            'kappa1',  # Kappa shape indices
            'kappa2',
            'kappa3'
        ]
    
    def calculate_all_descriptors(self, molecule: Union[Molecule, MolecularStructure]) -> Dict[str, float]:
        """
        Calculate all available molecular descriptors.
        
        Args:
            molecule: Molecule or MolecularStructure to analyze
            
        Returns:
            Dictionary containing all calculated descriptors
        """
        descriptors = {}
        
        # Convert to standard format if needed
        if isinstance(molecule, Molecule):
            structure = self._molecule_to_structure(molecule)
        else:
            structure = molecule
        
        # Calculate basic descriptors
        descriptors['molecular_weight'] = self.calculate_molecular_weight(structure)
        descriptors['num_atoms'] = self.calculate_num_atoms(structure)
        descriptors['num_heavy_atoms'] = self.calculate_num_heavy_atoms(structure)
        descriptors['num_bonds'] = self.calculate_num_bonds(structure)
        descriptors['num_heteroatoms'] = self.calculate_num_heteroatoms(structure)
        descriptors['formal_charge'] = self.calculate_formal_charge(structure)
        
        # Calculate topological descriptors
        descriptors['num_rotatable_bonds'] = self.calculate_num_rotatable_bonds(structure)
        descriptors['num_h_donors'] = self.calculate_num_h_donors(structure)
        descriptors['num_h_acceptors'] = self.calculate_num_h_acceptors(structure)
        descriptors['tpsa'] = self.calculate_tpsa(structure)
        descriptors['num_rings'] = self.calculate_num_rings(structure)
        
        # Calculate physicochemical descriptors
        descriptors['logp'] = self.calculate_logp(structure)
        descriptors['molecular_refractivity'] = self.calculate_molecular_refractivity(structure)
        
        # Calculate connectivity and shape descriptors
        descriptors['balaban_j'] = self.calculate_balaban_j(structure)
        descriptors['bertz_ct'] = self.calculate_bertz_ct(structure)
        descriptors['chi0v'] = self.calculate_chi0v(structure)
        descriptors['chi1v'] = self.calculate_chi1v(structure)
        descriptors['kappa1'] = self.calculate_kappa1(structure)
        descriptors['kappa2'] = self.calculate_kappa2(structure)
        descriptors['kappa3'] = self.calculate_kappa3(structure)
        
        # Set placeholder values for complex descriptors
        descriptors['num_aromatic_atoms'] = self.estimate_aromatic_atoms(structure)
        descriptors['num_aromatic_rings'] = self.estimate_aromatic_rings(structure)
        descriptors['num_saturated_rings'] = max(0, descriptors['num_rings'] - descriptors['num_aromatic_rings'])
        
        return descriptors
    
    def calculate_molecular_weight(self, structure: MolecularStructure) -> float:
        """Calculate molecular weight."""
        from chemesty.elements import get_element_by_symbol
        
        total_weight = 0.0
        for atom in structure.atoms:
            element = get_element_by_symbol(atom.symbol)
            total_weight += element.atomic_mass
        
        return total_weight
    
    def calculate_num_atoms(self, structure: MolecularStructure) -> int:
        """Calculate total number of atoms."""
        return len(structure.atoms)
    
    def calculate_num_heavy_atoms(self, structure: MolecularStructure) -> int:
        """Calculate number of heavy atoms (non-hydrogen)."""
        return sum(1 for atom in structure.atoms if atom.symbol != 'H')
    
    def calculate_num_bonds(self, structure: MolecularStructure) -> int:
        """Calculate number of bonds."""
        return len(structure.bonds)
    
    def calculate_num_heteroatoms(self, structure: MolecularStructure) -> int:
        """Calculate number of heteroatoms (non-carbon, non-hydrogen)."""
        return sum(1 for atom in structure.atoms if atom.symbol not in ['C', 'H'])
    
    def calculate_formal_charge(self, structure: MolecularStructure) -> int:
        """Calculate total formal charge."""
        return sum(atom.charge for atom in structure.atoms)
    
    def calculate_num_rotatable_bonds(self, structure: MolecularStructure) -> int:
        """Estimate number of rotatable bonds."""
        # Simplified estimation based on single bonds between heavy atoms
        rotatable = 0
        for bond in structure.bonds:
            if bond.bond_type == 1:  # Single bond
                atom1 = structure.atoms[bond.atom1_idx]
                atom2 = structure.atoms[bond.atom2_idx]
                if atom1.symbol != 'H' and atom2.symbol != 'H':
                    rotatable += 1
        
        return max(0, rotatable - self.calculate_num_rings(structure))
    
    def calculate_num_h_donors(self, structure: MolecularStructure) -> int:
        """Estimate number of hydrogen bond donors."""
        donors = 0
        for atom in structure.atoms:
            if atom.symbol in ['N', 'O', 'S']:
                # Count attached hydrogens (simplified)
                h_count = sum(1 for bond in structure.bonds 
                             for idx in [bond.atom1_idx, bond.atom2_idx]
                             if idx < len(structure.atoms) and 
                             structure.atoms[idx].symbol == 'H')
                donors += min(h_count, 1)  # Simplified counting
        
        return donors
    
    def calculate_num_h_acceptors(self, structure: MolecularStructure) -> int:
        """Estimate number of hydrogen bond acceptors."""
        return sum(1 for atom in structure.atoms if atom.symbol in ['N', 'O', 'F'])
    
    def calculate_tpsa(self, structure: MolecularStructure) -> float:
        """Estimate Topological Polar Surface Area."""
        # Simplified TPSA calculation based on polar atoms
        tpsa = 0.0
        polar_contributions = {
            'N': 23.79,  # Basic nitrogen contribution
            'O': 23.06,  # Basic oxygen contribution
            'S': 25.30,  # Basic sulfur contribution
            'P': 23.85   # Basic phosphorus contribution
        }
        
        for atom in structure.atoms:
            if atom.symbol in polar_contributions:
                tpsa += polar_contributions[atom.symbol]
        
        return tpsa
    
    def calculate_logp(self, structure: MolecularStructure) -> float:
        """Estimate partition coefficient (LogP)."""
        # Simplified LogP estimation using atomic contributions
        logp_contributions = {
            'C': 0.20,
            'H': 0.23,
            'N': -0.85,
            'O': -0.64,
            'S': 0.17,
            'P': 0.13,
            'F': -0.38,
            'Cl': 0.06,
            'Br': 0.20,
            'I': 0.60
        }
        
        logp = 0.0
        for atom in structure.atoms:
            logp += logp_contributions.get(atom.symbol, 0.0)
        
        return logp
    
    def calculate_num_rings(self, structure: MolecularStructure) -> int:
        """Estimate number of rings using Euler's formula."""
        if not structure.bonds:
            return 0
        
        # Simple ring detection: rings = edges - vertices + connected_components
        num_vertices = len(structure.atoms)
        num_edges = len(structure.bonds)
        
        # Assume single connected component for simplicity
        num_rings = max(0, num_edges - num_vertices + 1)
        
        return num_rings
    
    def calculate_molecular_refractivity(self, structure: MolecularStructure) -> float:
        """Estimate molecular refractivity."""
        # Simplified calculation using atomic contributions
        refractivity_contributions = {
            'C': 2.503,
            'H': 1.028,
            'N': 2.134,
            'O': 1.580,
            'S': 7.591,
            'P': 4.841,
            'F': 1.108,
            'Cl': 5.853,
            'Br': 8.741,
            'I': 13.900
        }
        
        refractivity = 0.0
        for atom in structure.atoms:
            refractivity += refractivity_contributions.get(atom.symbol, 2.0)
        
        return refractivity
    
    def calculate_balaban_j(self, structure: MolecularStructure) -> float:
        """Calculate Balaban J index (simplified)."""
        if len(structure.atoms) <= 1:
            return 0.0
        
        # Simplified calculation based on molecular size
        n_atoms = len(structure.atoms)
        n_bonds = len(structure.bonds)
        
        if n_bonds == 0:
            return 0.0
        
        # Simplified Balaban index approximation
        return n_bonds / (n_atoms - 1) if n_atoms > 1 else 0.0
    
    def calculate_bertz_ct(self, structure: MolecularStructure) -> float:
        """Calculate Bertz complexity index (simplified)."""
        n_atoms = len(structure.atoms)
        n_bonds = len(structure.bonds)
        n_hetero = self.calculate_num_heteroatoms(structure)
        
        # Simplified complexity based on size and diversity
        complexity = n_atoms + n_bonds + n_hetero * 2
        
        return float(complexity)
    
    def calculate_chi0v(self, structure: MolecularStructure) -> float:
        """Calculate 0th order valence connectivity index."""
        if not structure.atoms:
            return 0.0
        
        # Simplified calculation based on atom types
        chi0v = 0.0
        for atom in structure.atoms:
            if atom.symbol == 'C':
                chi0v += 1.0
            elif atom.symbol in ['N', 'O']:
                chi0v += 0.5
            else:
                chi0v += 0.25
        
        return chi0v
    
    def calculate_chi1v(self, structure: MolecularStructure) -> float:
        """Calculate 1st order valence connectivity index."""
        if not structure.bonds:
            return 0.0
        
        # Simplified calculation based on bonds
        chi1v = 0.0
        for bond in structure.bonds:
            # Simple contribution based on bond type
            chi1v += 1.0 / math.sqrt(bond.bond_type)
        
        return chi1v
    
    def calculate_kappa1(self, structure: MolecularStructure) -> float:
        """Calculate 1st order kappa shape index."""
        n_atoms = len(structure.atoms)
        if n_atoms <= 2:
            return 0.0
        
        # Simplified kappa calculation
        return float(n_atoms * (n_atoms - 1) ** 2) / (2 * len(structure.bonds)) ** 2 if structure.bonds else 0.0
    
    def calculate_kappa2(self, structure: MolecularStructure) -> float:
        """Calculate 2nd order kappa shape index."""
        n_atoms = len(structure.atoms)
        if n_atoms <= 3:
            return 0.0
        
        # Simplified kappa2 calculation
        return float((n_atoms - 1) * (n_atoms - 2) ** 2) / (len(structure.bonds) + 1) ** 2 if structure.bonds else 0.0
    
    def calculate_kappa3(self, structure: MolecularStructure) -> float:
        """Calculate 3rd order kappa shape index."""
        n_atoms = len(structure.atoms)
        if n_atoms <= 4:
            return 0.0
        
        # Simplified kappa3 calculation
        return float((n_atoms - 2) * (n_atoms - 3) ** 2) / (len(structure.bonds) + 2) ** 2 if structure.bonds else 0.0
    
    def estimate_aromatic_atoms(self, structure: MolecularStructure) -> int:
        """Estimate number of aromatic atoms (simplified)."""
        # Very simplified estimation based on carbon atoms in rings
        num_rings = self.calculate_num_rings(structure)
        carbon_atoms = sum(1 for atom in structure.atoms if atom.symbol == 'C')
        
        # Rough estimate: assume some carbons are aromatic if rings exist
        return min(carbon_atoms, num_rings * 6) if num_rings > 0 else 0
    
    def estimate_aromatic_rings(self, structure: MolecularStructure) -> int:
        """Estimate number of aromatic rings (simplified)."""
        total_rings = self.calculate_num_rings(structure)
        # Simple heuristic: assume half of rings are aromatic
        return max(0, total_rings // 2)
    
    def _molecule_to_structure(self, molecule: Molecule) -> MolecularStructure:
        """Convert Molecule to MolecularStructure."""
        atoms = []
        atom_idx = 0
        
        for element, count in molecule.elements.items():
            for i in range(count):
                atoms.append(Atom(
                    symbol=element.symbol,
                    x=atom_idx * 1.5,  # Simple linear arrangement
                    y=0.0,
                    z=0.0
                ))
                atom_idx += 1
        
        return MolecularStructure(atoms=atoms, bonds=[])
    
    def get_descriptor_names(self) -> List[str]:
        """Get list of all available descriptor names."""
        return self.descriptor_names.copy()
    
    def calculate_descriptor_matrix(self, molecules: List[Union[Molecule, MolecularStructure]]) -> np.ndarray:
        """
        Calculate descriptor matrix for multiple molecules.
        
        Args:
            molecules: List of molecules to analyze
            
        Returns:
            2D numpy array where rows are molecules and columns are descriptors
        """
        if not molecules:
            return np.array([])
        
        descriptor_matrix = []
        
        for molecule in molecules:
            descriptors = self.calculate_all_descriptors(molecule)
            # Ensure consistent ordering
            descriptor_vector = [descriptors[name] for name in self.descriptor_names]
            descriptor_matrix.append(descriptor_vector)
        
        return np.array(descriptor_matrix)