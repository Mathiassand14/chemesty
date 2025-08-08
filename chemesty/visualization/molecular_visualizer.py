"""
Core molecular visualization class.

This module provides the main interface for visualizing molecular structures
with support for both 2D and 3D rendering.
"""

from typing import Optional, Dict, Any, Union, List, Tuple
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
import numpy as np
from chemesty.molecules.molecule import Molecule
from chemesty.molecules.file_formats import MolecularStructure, Atom, Bond


class MolecularVisualizer:
    """
    Main class for molecular visualization.
    
    This class provides a unified interface for creating 2D and 3D
    visualizations of molecular structures.
    """
    
    def __init__(self, style: str = 'default'):
        """
        Initialize the molecular visualizer.
        
        Args:
            style: Visualization style ('default', 'ball_and_stick', 'space_filling')
        """
        self.style = style
        self.atom_colors = self._get_default_atom_colors()
        self.atom_radii = self._get_default_atom_radii()
        self.bond_colors = {'single': 'black', 'double': 'red', 'triple': 'blue', 'aromatic': 'green'}
        
    def _get_default_atom_colors(self) -> Dict[str, str]:
        """Get default CPK atom colors."""
        return {
            'H': '#FFFFFF',   # White
            'C': '#909090',   # Gray
            'N': '#3050F8',   # Blue
            'O': '#FF0D0D',   # Red
            'F': '#90E050',   # Green
            'Cl': '#1FF01F',  # Green
            'Br': '#A62929',  # Brown
            'I': '#940094',   # Purple
            'P': '#FF8000',   # Orange
            'S': '#FFFF30',   # Yellow
            'B': '#FFB5B5',   # Pink
            'Fe': '#E06633',  # Orange-red
            'default': '#FF1493'  # Hot pink for unknown elements
        }
    
    def _get_default_atom_radii(self) -> Dict[str, float]:
        """Get default van der Waals radii in Angstroms."""
        return {
            'H': 1.20,
            'C': 1.70,
            'N': 1.55,
            'O': 1.52,
            'F': 1.47,
            'Cl': 1.75,
            'Br': 1.85,
            'I': 1.98,
            'P': 1.80,
            'S': 1.80,
            'default': 1.50
        }
    
    def visualize_2d(self, molecule: Union[Molecule, MolecularStructure], 
                     figsize: Tuple[int, int] = (8, 6),
                     show_labels: bool = True,
                     show_bonds: bool = True) -> Figure:
        """
        Create a 2D visualization of a molecule.
        
        Args:
            molecule: Molecule or MolecularStructure to visualize
            figsize: Figure size (width, height)
            show_labels: Whether to show atom labels
            show_bonds: Whether to show bonds
            
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if isinstance(molecule, Molecule):
            # Convert Molecule to a simple structure for visualization
            structure = self._molecule_to_structure(molecule)
        else:
            structure = molecule
        
        if not structure.atoms:
            ax.text(0.5, 0.5, 'No atoms to display', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=14)
            return fig
        
        # Extract coordinates
        x_coords = [atom.x for atom in structure.atoms]
        y_coords = [atom.y for atom in structure.atoms]
        
        # If all coordinates are zero, generate a simple layout
        if all(x == 0 for x in x_coords) and all(y == 0 for y in y_coords):
            x_coords, y_coords = self._generate_2d_layout(structure)
        
        # Draw bonds first (so they appear behind atoms)
        if show_bonds and structure.bonds:
            self._draw_bonds_2d(ax, structure, x_coords, y_coords)
        
        # Draw atoms
        for i, atom in enumerate(structure.atoms):
            color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
            radius = self.atom_radii.get(atom.symbol, self.atom_radii['default']) * 0.3
            
            circle = patches.Circle((x_coords[i], y_coords[i]), radius, 
                                  facecolor=color, edgecolor='black', linewidth=1)
            ax.add_patch(circle)
            
            if show_labels:
                ax.text(x_coords[i], y_coords[i], atom.symbol, 
                       ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Set equal aspect ratio and adjust limits
        ax.set_aspect('equal')
        if x_coords and y_coords:
            margin = 2.0
            ax.set_xlim(min(x_coords) - margin, max(x_coords) + margin)
            ax.set_ylim(min(y_coords) - margin, max(y_coords) + margin)
        
        ax.set_title(f'2D Structure: {structure.title or "Molecule"}')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def _molecule_to_structure(self, molecule: Molecule) -> MolecularStructure:
        """Convert a Molecule to a MolecularStructure for visualization."""
        atoms = []
        atom_index = 0
        
        # Create atoms from the molecule's element composition
        for element, count in molecule.elements.items():
            for i in range(count):
                atoms.append(Atom(element.symbol, 0.0, 0.0, 0.0))
                atom_index += 1
        
        # Create a simple structure without bonds for now
        return MolecularStructure(atoms, [], molecule.molecular_formula)
    
    def _generate_2d_layout(self, structure: MolecularStructure) -> Tuple[List[float], List[float]]:
        """Generate a simple 2D layout for molecules without coordinates."""
        n_atoms = len(structure.atoms)
        
        if n_atoms == 1:
            return [0.0], [0.0]
        elif n_atoms == 2:
            return [0.0, 2.0], [0.0, 0.0]
        else:
            # Arrange atoms in a circle
            angles = np.linspace(0, 2 * np.pi, n_atoms, endpoint=False)
            radius = max(2.0, n_atoms * 0.5)
            x_coords = [radius * np.cos(angle) for angle in angles]
            y_coords = [radius * np.sin(angle) for angle in angles]
            return x_coords, y_coords
    
    def _draw_bonds_2d(self, ax, structure: MolecularStructure, 
                       x_coords: List[float], y_coords: List[float]) -> None:
        """Draw bonds in 2D visualization."""
        for bond in structure.bonds:
            if bond.atom1_idx < len(x_coords) and bond.atom2_idx < len(x_coords):
                x1, y1 = x_coords[bond.atom1_idx], y_coords[bond.atom1_idx]
                x2, y2 = x_coords[bond.atom2_idx], y_coords[bond.atom2_idx]
                
                # Determine bond color and style
                if bond.bond_type == 1:
                    color = self.bond_colors['single']
                    linewidth = 2
                elif bond.bond_type == 2:
                    color = self.bond_colors['double']
                    linewidth = 3
                elif bond.bond_type == 3:
                    color = self.bond_colors['triple']
                    linewidth = 4
                else:
                    color = self.bond_colors['aromatic']
                    linewidth = 2
                
                ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth, alpha=0.8)
    
    def visualize_3d(self, molecule: Union[Molecule, MolecularStructure],
                     figsize: Tuple[int, int] = (10, 8),
                     show_labels: bool = True,
                     show_bonds: bool = True) -> Figure:
        """
        Create a 3D visualization of a molecule.
        
        Args:
            molecule: Molecule or MolecularStructure to visualize
            figsize: Figure size (width, height)
            show_labels: Whether to show atom labels
            show_bonds: Whether to show bonds
            
        Returns:
            Matplotlib Figure object with 3D plot
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        if isinstance(molecule, Molecule):
            structure = self._molecule_to_structure(molecule)
        else:
            structure = molecule
        
        if not structure.atoms:
            ax.text(0.5, 0.5, 0.5, 'No atoms to display', ha='center', va='center')
            return fig
        
        # Extract coordinates
        x_coords = [atom.x for atom in structure.atoms]
        y_coords = [atom.y for atom in structure.atoms]
        z_coords = [atom.z for atom in structure.atoms]
        
        # If all coordinates are zero, generate a simple 3D layout
        if (all(x == 0 for x in x_coords) and all(y == 0 for y in y_coords) and 
            all(z == 0 for z in z_coords)):
            x_coords, y_coords, z_coords = self._generate_3d_layout(structure)
        
        # Draw bonds first
        if show_bonds and structure.bonds:
            self._draw_bonds_3d(ax, structure, x_coords, y_coords, z_coords)
        
        # Draw atoms
        for i, atom in enumerate(structure.atoms):
            color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
            size = self.atom_radii.get(atom.symbol, self.atom_radii['default']) * 100
            
            ax.scatter(x_coords[i], y_coords[i], z_coords[i], 
                      c=color, s=size, alpha=0.8, edgecolors='black')
            
            if show_labels:
                ax.text(x_coords[i], y_coords[i], z_coords[i], atom.symbol,
                       fontsize=8, ha='center', va='center')
        
        ax.set_xlabel('X (Å)')
        ax.set_ylabel('Y (Å)')
        ax.set_zlabel('Z (Å)')
        ax.set_title(f'3D Structure: {structure.title or "Molecule"}')
        
        return fig
    
    def _generate_3d_layout(self, structure: MolecularStructure) -> Tuple[List[float], List[float], List[float]]:
        """Generate a simple 3D layout for molecules without coordinates."""
        n_atoms = len(structure.atoms)
        
        if n_atoms == 1:
            return [0.0], [0.0], [0.0]
        elif n_atoms == 2:
            return [0.0, 2.0], [0.0, 0.0], [0.0, 0.0]
        else:
            # Arrange atoms in a 3D spiral
            t = np.linspace(0, 4 * np.pi, n_atoms)
            radius = 2.0
            x_coords = [radius * np.cos(ti) for ti in t]
            y_coords = [radius * np.sin(ti) for ti in t]
            z_coords = [ti * 0.5 for ti in t]
            return x_coords, y_coords, z_coords
    
    def _draw_bonds_3d(self, ax, structure: MolecularStructure,
                       x_coords: List[float], y_coords: List[float], z_coords: List[float]) -> None:
        """Draw bonds in 3D visualization."""
        for bond in structure.bonds:
            if bond.atom1_idx < len(x_coords) and bond.atom2_idx < len(x_coords):
                x1, y1, z1 = x_coords[bond.atom1_idx], y_coords[bond.atom1_idx], z_coords[bond.atom1_idx]
                x2, y2, z2 = x_coords[bond.atom2_idx], y_coords[bond.atom2_idx], z_coords[bond.atom2_idx]
                
                # Determine bond color and style
                if bond.bond_type == 1:
                    color = self.bond_colors['single']
                    linewidth = 2
                elif bond.bond_type == 2:
                    color = self.bond_colors['double']
                    linewidth = 3
                elif bond.bond_type == 3:
                    color = self.bond_colors['triple']
                    linewidth = 4
                else:
                    color = self.bond_colors['aromatic']
                    linewidth = 2
                
                ax.plot([x1, x2], [y1, y2], [z1, z2], color=color, linewidth=linewidth, alpha=0.8)
    
    def save_visualization(self, fig: Figure, filename: Union[str, Path],
                          dpi: int = 300, format: str = 'png') -> None:
        """
        Save a visualization to file.
        
        Args:
            fig: Matplotlib Figure to save
            filename: Output filename
            dpi: Resolution in dots per inch
            format: Output format ('png', 'svg', 'pdf', 'eps')
        """
        fig.savefig(filename, dpi=dpi, format=format, bbox_inches='tight')
    
    def create_comparison_plot(self, molecules: List[Union[Molecule, MolecularStructure]],
                              titles: Optional[List[str]] = None,
                              figsize: Tuple[int, int] = (15, 5)) -> Figure:
        """
        Create a comparison plot of multiple molecules.
        
        Args:
            molecules: List of molecules to compare
            titles: Optional titles for each molecule
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib Figure with subplots
        """
        n_molecules = len(molecules)
        if n_molecules == 0:
            raise ValueError("At least one molecule is required")
        
        fig, axes = plt.subplots(1, n_molecules, figsize=figsize)
        if n_molecules == 1:
            axes = [axes]
        
        for i, (molecule, ax) in enumerate(zip(molecules, axes)):
            if isinstance(molecule, Molecule):
                structure = self._molecule_to_structure(molecule)
            else:
                structure = molecule
            
            # Create 2D visualization on this subplot
            x_coords = [atom.x for atom in structure.atoms]
            y_coords = [atom.y for atom in structure.atoms]
            
            if all(x == 0 for x in x_coords) and all(y == 0 for y in y_coords):
                x_coords, y_coords = self._generate_2d_layout(structure)
            
            # Draw bonds
            if structure.bonds:
                self._draw_bonds_2d(ax, structure, x_coords, y_coords)
            
            # Draw atoms
            for j, atom in enumerate(structure.atoms):
                color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
                radius = self.atom_radii.get(atom.symbol, self.atom_radii['default']) * 0.3
                
                circle = patches.Circle((x_coords[j], y_coords[j]), radius,
                                      facecolor=color, edgecolor='black', linewidth=1)
                ax.add_patch(circle)
                ax.text(x_coords[j], y_coords[j], atom.symbol,
                       ha='center', va='center', fontsize=8, fontweight='bold')
            
            ax.set_aspect('equal')
            if x_coords and y_coords:
                margin = 1.5
                ax.set_xlim(min(x_coords) - margin, max(x_coords) + margin)
                ax.set_ylim(min(y_coords) - margin, max(y_coords) + margin)
            
            title = titles[i] if titles and i < len(titles) else f'Molecule {i+1}'
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig