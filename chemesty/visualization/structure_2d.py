"""
2D molecular structure rendering with advanced layout algorithms.

This module provides specialized 2D rendering capabilities with support for
chemical structure conventions and automatic layout generation.
"""

from typing import Dict, List, Tuple, Optional, Union
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
import math
from chemesty.molecules.molecule import Molecule
from chemesty.molecules.file_formats import MolecularStructure, Atom, Bond


class Structure2DRenderer:
    """
    Specialized 2D molecular structure renderer.
    
    This class provides advanced 2D rendering with chemical structure
    conventions, automatic layout algorithms, and publication-quality output.
    """
    
    def __init__(self):
        """Initialize the 2D renderer."""
        self.bond_length = 1.5  # Standard bond length in display units
        self.bond_width = 2.0   # Bond line width
        self.atom_font_size = 12
        self.title_font_size = 14
        
        # Chemical drawing conventions
        self.wedge_bond_width = 0.3
        self.dash_bond_segments = 10
        
        # Atom colors (CPK coloring scheme)
        self.atom_colors = {
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
            'default': '#FF1493'  # Hot pink
        }
        
        # Atom radii for display
        self.atom_radii = {
            'H': 0.4,
            'C': 0.6,
            'N': 0.6,
            'O': 0.6,
            'F': 0.5,
            'Cl': 0.8,
            'Br': 0.9,
            'I': 1.0,
            'P': 0.8,
            'S': 0.8,
            'default': 0.6
        }
    
    def render(self, structure: MolecularStructure, 
               figsize: Tuple[float, float] = (8, 6),
               show_hydrogens: bool = True,
               show_carbon_labels: bool = False,
               show_atom_indices: bool = False) -> Figure:
        """
        Render a 2D molecular structure.
        
        Args:
            structure: MolecularStructure to render
            figsize: Figure size (width, height)
            show_hydrogens: Whether to show hydrogen atoms
            show_carbon_labels: Whether to show carbon atom labels
            show_atom_indices: Whether to show atom indices
            
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if not structure.atoms:
            ax.text(0.5, 0.5, 'No structure to display', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            return fig
        
        # Get or generate coordinates
        coords = self._get_coordinates(structure)
        
        # Filter atoms if needed
        visible_atoms = self._filter_atoms(structure.atoms, show_hydrogens)
        visible_indices = [i for i, atom in enumerate(structure.atoms) 
                          if atom in visible_atoms]
        
        # Draw bonds first (behind atoms)
        self._draw_bonds(ax, structure, coords, visible_indices)
        
        # Draw atoms
        self._draw_atoms(ax, structure.atoms, coords, visible_indices,
                        show_carbon_labels, show_atom_indices)
        
        # Set up the plot
        self._setup_plot(ax, coords, structure.title)
        
        return fig
    
    def _get_coordinates(self, structure: MolecularStructure) -> List[Tuple[float, float]]:
        """Get or generate 2D coordinates for atoms."""
        coords = [(atom.x, atom.y) for atom in structure.atoms]
        
        # Check if coordinates are meaningful
        if all(x == 0 and y == 0 for x, y in coords):
            coords = self._generate_layout(structure)
        
        return coords
    
    def _generate_layout(self, structure: MolecularStructure) -> List[Tuple[float, float]]:
        """Generate 2D layout using force-directed algorithm."""
        n_atoms = len(structure.atoms)
        
        if n_atoms == 0:
            return []
        elif n_atoms == 1:
            return [(0.0, 0.0)]
        elif n_atoms == 2:
            return [(0.0, 0.0), (self.bond_length, 0.0)]
        
        # Initialize with random positions
        np.random.seed(42)  # For reproducible layouts
        coords = [(np.random.uniform(-2, 2), np.random.uniform(-2, 2)) 
                 for _ in range(n_atoms)]
        
        # Apply force-directed layout
        coords = self._force_directed_layout(structure, coords)
        
        return coords
    
    def _force_directed_layout(self, structure: MolecularStructure, 
                              initial_coords: List[Tuple[float, float]],
                              iterations: int = 100) -> List[Tuple[float, float]]:
        """Apply force-directed layout algorithm."""
        coords = np.array(initial_coords)
        
        # Build adjacency list from bonds
        adjacency = [[] for _ in range(len(structure.atoms))]
        for bond in structure.bonds:
            if (bond.atom1_idx < len(structure.atoms) and 
                bond.atom2_idx < len(structure.atoms)):
                adjacency[bond.atom1_idx].append(bond.atom2_idx)
                adjacency[bond.atom2_idx].append(bond.atom1_idx)
        
        for iteration in range(iterations):
            forces = np.zeros_like(coords)
            
            # Repulsive forces between all atoms
            for i in range(len(coords)):
                for j in range(i + 1, len(coords)):
                    diff = coords[i] - coords[j]
                    dist = np.linalg.norm(diff)
                    if dist > 0:
                        # Repulsive force
                        force_mag = 0.1 / (dist ** 2)
                        force_dir = diff / dist
                        forces[i] += force_mag * force_dir
                        forces[j] -= force_mag * force_dir
            
            # Attractive forces for bonded atoms
            for i, neighbors in enumerate(adjacency):
                for j in neighbors:
                    if i < j:  # Avoid double counting
                        diff = coords[j] - coords[i]
                        dist = np.linalg.norm(diff)
                        if dist > 0:
                            # Spring force toward ideal bond length
                            ideal_dist = self.bond_length
                            force_mag = 0.01 * (dist - ideal_dist)
                            force_dir = diff / dist
                            forces[i] += force_mag * force_dir
                            forces[j] -= force_mag * force_dir
            
            # Apply forces with damping
            damping = 0.9
            coords += forces * damping
        
        return [(float(x), float(y)) for x, y in coords]
    
    def _filter_atoms(self, atoms: List[Atom], show_hydrogens: bool) -> List[Atom]:
        """Filter atoms based on display preferences."""
        if show_hydrogens:
            return atoms
        else:
            return [atom for atom in atoms if atom.symbol != 'H']
    
    def _draw_bonds(self, ax, structure: MolecularStructure, 
                   coords: List[Tuple[float, float]], 
                   visible_indices: List[int]) -> None:
        """Draw bonds between atoms."""
        visible_set = set(visible_indices)
        
        for bond in structure.bonds:
            if (bond.atom1_idx in visible_set and bond.atom2_idx in visible_set):
                x1, y1 = coords[bond.atom1_idx]
                x2, y2 = coords[bond.atom2_idx]
                
                if bond.bond_type == 1:
                    self._draw_single_bond(ax, x1, y1, x2, y2)
                elif bond.bond_type == 2:
                    self._draw_double_bond(ax, x1, y1, x2, y2)
                elif bond.bond_type == 3:
                    self._draw_triple_bond(ax, x1, y1, x2, y2)
                else:
                    # Aromatic or other bond types
                    self._draw_aromatic_bond(ax, x1, y1, x2, y2)
    
    def _draw_single_bond(self, ax, x1: float, y1: float, x2: float, y2: float) -> None:
        """Draw a single bond."""
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=self.bond_width)
    
    def _draw_double_bond(self, ax, x1: float, y1: float, x2: float, y2: float) -> None:
        """Draw a double bond."""
        # Calculate perpendicular offset
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            offset_x = -dy / length * 0.1
            offset_y = dx / length * 0.1
            
            # Draw two parallel lines
            ax.plot([x1 + offset_x, x2 + offset_x], [y1 + offset_y, y2 + offset_y], 
                   'k-', linewidth=self.bond_width)
            ax.plot([x1 - offset_x, x2 - offset_x], [y1 - offset_y, y2 - offset_y], 
                   'k-', linewidth=self.bond_width)
    
    def _draw_triple_bond(self, ax, x1: float, y1: float, x2: float, y2: float) -> None:
        """Draw a triple bond."""
        # Calculate perpendicular offset
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            offset_x = -dy / length * 0.15
            offset_y = dx / length * 0.15
            
            # Draw three parallel lines
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=self.bond_width)
            ax.plot([x1 + offset_x, x2 + offset_x], [y1 + offset_y, y2 + offset_y], 
                   'k-', linewidth=self.bond_width)
            ax.plot([x1 - offset_x, x2 - offset_x], [y1 - offset_y, y2 - offset_y], 
                   'k-', linewidth=self.bond_width)
    
    def _draw_aromatic_bond(self, ax, x1: float, y1: float, x2: float, y2: float) -> None:
        """Draw an aromatic bond (dashed line)."""
        ax.plot([x1, x2], [y1, y2], 'k--', linewidth=self.bond_width, alpha=0.7)
    
    def _draw_atoms(self, ax, atoms: List[Atom], coords: List[Tuple[float, float]],
                   visible_indices: List[int], show_carbon_labels: bool,
                   show_atom_indices: bool) -> None:
        """Draw atoms with labels."""
        for i in visible_indices:
            atom = atoms[i]
            x, y = coords[i]
            
            # Determine if we should show the label
            show_label = (atom.symbol != 'C' or show_carbon_labels or 
                         atom.symbol == 'H')
            
            if show_label:
                color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
                
                # Draw atom circle (background for text)
                if atom.symbol != 'H':  # Don't draw circles for hydrogens
                    radius = self.atom_radii.get(atom.symbol, self.atom_radii['default'])
                    circle = patches.Circle((x, y), radius, facecolor='white', 
                                          edgecolor=color, linewidth=1, alpha=0.8)
                    ax.add_patch(circle)
                
                # Draw atom label
                ax.text(x, y, atom.symbol, ha='center', va='center',
                       fontsize=self.atom_font_size, fontweight='bold', color='black')
                
                # Draw atom index if requested
                if show_atom_indices:
                    ax.text(x + 0.3, y + 0.3, str(i), ha='left', va='bottom',
                           fontsize=8, color='gray')
    
    def _setup_plot(self, ax, coords: List[Tuple[float, float]], title: str) -> None:
        """Set up the plot appearance."""
        if coords:
            x_coords = [x for x, y in coords]
            y_coords = [y for x, y in coords]
            
            margin = 1.0
            ax.set_xlim(min(x_coords) - margin, max(x_coords) + margin)
            ax.set_ylim(min(y_coords) - margin, max(y_coords) + margin)
        
        ax.set_aspect('equal')
        ax.set_title(title or 'Molecular Structure', fontsize=self.title_font_size)
        ax.axis('off')  # Hide axes for cleaner appearance
    
    def render_skeletal_formula(self, structure: MolecularStructure,
                               figsize: Tuple[float, float] = (8, 6)) -> Figure:
        """
        Render a skeletal formula (line-angle formula).
        
        Args:
            structure: MolecularStructure to render
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if not structure.atoms:
            ax.text(0.5, 0.5, 'No structure to display', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            return fig
        
        coords = self._get_coordinates(structure)
        
        # In skeletal formulas, we typically don't show carbon or hydrogen labels
        # Only show heteroatoms and carbons with special properties
        
        # Draw bonds
        for bond in structure.bonds:
            if (bond.atom1_idx < len(coords) and bond.atom2_idx < len(coords)):
                x1, y1 = coords[bond.atom1_idx]
                x2, y2 = coords[bond.atom2_idx]
                
                if bond.bond_type == 1:
                    ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2)
                elif bond.bond_type == 2:
                    self._draw_double_bond(ax, x1, y1, x2, y2)
                elif bond.bond_type == 3:
                    self._draw_triple_bond(ax, x1, y1, x2, y2)
                else:
                    ax.plot([x1, x2], [y1, y2], 'k--', linewidth=2, alpha=0.7)
        
        # Draw only heteroatoms and special carbons
        for i, atom in enumerate(structure.atoms):
            if i < len(coords):
                x, y = coords[i]
                
                # Show non-carbon atoms and carbons with charges or special properties
                if (atom.symbol != 'C' and atom.symbol != 'H') or atom.charge != 0:
                    ax.text(x, y, atom.symbol, ha='center', va='center',
                           fontsize=self.atom_font_size, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
                    
                    # Show charge if present
                    if atom.charge != 0:
                        charge_str = f"{'+' if atom.charge > 0 else ''}{atom.charge}"
                        ax.text(x + 0.3, y + 0.3, charge_str, ha='left', va='bottom',
                               fontsize=8, fontweight='bold')
        
        self._setup_plot(ax, coords, structure.title)
        return fig
    
    def create_reaction_scheme(self, reactants: List[MolecularStructure],
                              products: List[MolecularStructure],
                              figsize: Tuple[float, float] = (15, 6)) -> Figure:
        """
        Create a reaction scheme showing reactants and products.
        
        Args:
            reactants: List of reactant structures
            products: List of product structures
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib Figure showing the reaction scheme
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        total_molecules = len(reactants) + len(products)
        if total_molecules == 0:
            ax.text(0.5, 0.5, 'No molecules to display', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            return fig
        
        # Calculate positions for molecules
        reactant_width = 0.4 / max(1, len(reactants))
        product_width = 0.4 / max(1, len(products))
        
        # Draw reactants
        for i, reactant in enumerate(reactants):
            x_center = 0.1 + i * reactant_width
            self._draw_molecule_in_subplot(ax, reactant, x_center, 0.5, reactant_width * 0.8)
            
            # Add "+" between reactants
            if i < len(reactants) - 1:
                ax.text(x_center + reactant_width/2, 0.5, '+', 
                       ha='center', va='center', fontsize=16, fontweight='bold',
                       transform=ax.transAxes)
        
        # Draw arrow
        ax.annotate('', xy=(0.7, 0.5), xytext=(0.6, 0.5),
                   arrowprops=dict(arrowstyle='->', lw=3, color='black'),
                   xycoords='axes fraction', textcoords='axes fraction')
        
        # Draw products
        for i, product in enumerate(products):
            x_center = 0.8 + i * product_width
            self._draw_molecule_in_subplot(ax, product, x_center, 0.5, product_width * 0.8)
            
            # Add "+" between products
            if i < len(products) - 1:
                ax.text(x_center + product_width/2, 0.5, '+', 
                       ha='center', va='center', fontsize=16, fontweight='bold',
                       transform=ax.transAxes)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Reaction Scheme', fontsize=16, fontweight='bold')
        
        return fig
    
    def _draw_molecule_in_subplot(self, ax, structure: MolecularStructure,
                                 x_center: float, y_center: float, width: float) -> None:
        """Draw a molecule within a subplot region."""
        if not structure.atoms:
            return
        
        coords = self._get_coordinates(structure)
        if not coords:
            return
        
        # Scale and center the molecule
        x_coords = [x for x, y in coords]
        y_coords = [y for x, y in coords]
        
        if x_coords and y_coords:
            # Calculate bounds
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            # Scale to fit in the allocated space
            x_range = x_max - x_min if x_max != x_min else 1
            y_range = y_max - y_min if y_max != y_min else 1
            scale = min(width / x_range, 0.3 / y_range) * 0.8
            
            # Transform coordinates
            scaled_coords = []
            for x, y in coords:
                scaled_x = x_center + (x - (x_min + x_max)/2) * scale
                scaled_y = y_center + (y - (y_min + y_max)/2) * scale
                scaled_coords.append((scaled_x, scaled_y))
            
            # Draw bonds
            for bond in structure.bonds:
                if (bond.atom1_idx < len(scaled_coords) and 
                    bond.atom2_idx < len(scaled_coords)):
                    x1, y1 = scaled_coords[bond.atom1_idx]
                    x2, y2 = scaled_coords[bond.atom2_idx]
                    ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1, 
                           transform=ax.transAxes)
            
            # Draw atoms (only heteroatoms)
            for i, atom in enumerate(structure.atoms):
                if i < len(scaled_coords) and atom.symbol not in ['C', 'H']:
                    x, y = scaled_coords[i]
                    ax.text(x, y, atom.symbol, ha='center', va='center',
                           fontsize=8, fontweight='bold', transform=ax.transAxes,
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))