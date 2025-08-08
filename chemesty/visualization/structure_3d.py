"""
3D molecular structure rendering with advanced visualization techniques.

This module provides specialized 3D rendering capabilities with support for
different molecular representations and interactive 3D displays.
"""

from typing import Dict, List, Tuple, Optional, Union, Any
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math
from chemesty.molecules.molecule import Molecule
from chemesty.molecules.file_formats import MolecularStructure, Atom, Bond


class Structure3DRenderer:
    """
    Specialized 3D molecular structure renderer.
    
    This class provides advanced 3D rendering with different molecular
    representations including ball-and-stick, space-filling, and wireframe models.
    """
    
    def __init__(self, style: str = 'ball_and_stick'):
        """
        Initialize the 3D renderer.
        
        Args:
            style: Rendering style ('ball_and_stick', 'space_filling', 'wireframe', 'stick')
        """
        self.style = style
        self.bond_radius = 0.1  # Radius for cylindrical bonds
        self.bond_resolution = 8  # Number of segments for bond cylinders
        
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
            'Fe': '#E06633',  # Orange-red
            'default': '#FF1493'  # Hot pink
        }
        
        # Van der Waals radii in Angstroms
        self.vdw_radii = {
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
        
        # Covalent radii for ball-and-stick representation
        self.covalent_radii = {
            'H': 0.31,
            'C': 0.76,
            'N': 0.71,
            'O': 0.66,
            'F': 0.57,
            'Cl': 0.99,
            'Br': 1.14,
            'I': 1.33,
            'P': 1.07,
            'S': 1.05,
            'default': 0.80
        }
    
    def render(self, structure: MolecularStructure,
               figsize: Tuple[float, float] = (10, 8),
               show_labels: bool = True,
               show_bonds: bool = True,
               alpha: float = 0.8) -> Figure:
        """
        Render a 3D molecular structure.
        
        Args:
            structure: MolecularStructure to render
            figsize: Figure size (width, height)
            show_labels: Whether to show atom labels
            show_bonds: Whether to show bonds
            alpha: Transparency level (0-1)
            
        Returns:
            Matplotlib Figure object with 3D plot
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        if not structure.atoms:
            ax.text(0.5, 0.5, 0.5, 'No structure to display', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            return fig
        
        # Get or generate coordinates
        coords = self._get_coordinates(structure)
        
        # Render based on style
        if self.style == 'ball_and_stick':
            self._render_ball_and_stick(ax, structure, coords, show_labels, show_bonds, alpha)
        elif self.style == 'space_filling':
            self._render_space_filling(ax, structure, coords, show_labels, alpha)
        elif self.style == 'wireframe':
            self._render_wireframe(ax, structure, coords, show_labels)
        elif self.style == 'stick':
            self._render_stick(ax, structure, coords, show_labels)
        else:
            # Default to ball and stick
            self._render_ball_and_stick(ax, structure, coords, show_labels, show_bonds, alpha)
        
        # Set up the plot
        self._setup_3d_plot(ax, coords, structure.title)
        
        return fig
    
    def _get_coordinates(self, structure: MolecularStructure) -> List[Tuple[float, float, float]]:
        """Get or generate 3D coordinates for atoms."""
        coords = [(atom.x, atom.y, atom.z) for atom in structure.atoms]
        
        # Check if coordinates are meaningful
        if all(x == 0 and y == 0 and z == 0 for x, y, z in coords):
            coords = self._generate_3d_layout(structure)
        
        return coords
    
    def _generate_3d_layout(self, structure: MolecularStructure) -> List[Tuple[float, float, float]]:
        """Generate 3D layout for molecules without coordinates."""
        n_atoms = len(structure.atoms)
        
        if n_atoms == 0:
            return []
        elif n_atoms == 1:
            return [(0.0, 0.0, 0.0)]
        elif n_atoms == 2:
            return [(0.0, 0.0, 0.0), (1.5, 0.0, 0.0)]
        else:
            # Generate a 3D spiral layout
            t = np.linspace(0, 4 * np.pi, n_atoms)
            radius = 2.0
            height_scale = 0.5
            
            coords = []
            for i, ti in enumerate(t):
                x = radius * np.cos(ti)
                y = radius * np.sin(ti)
                z = ti * height_scale
                coords.append((float(x), float(y), float(z)))
            
            return coords
    
    def _render_ball_and_stick(self, ax, structure: MolecularStructure,
                              coords: List[Tuple[float, float, float]],
                              show_labels: bool, show_bonds: bool, alpha: float) -> None:
        """Render in ball-and-stick style."""
        # Draw bonds first (behind atoms)
        if show_bonds and structure.bonds:
            self._draw_bonds_3d(ax, structure, coords)
        
        # Draw atoms as spheres
        for i, atom in enumerate(structure.atoms):
            if i < len(coords):
                x, y, z = coords[i]
                color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
                radius = self.covalent_radii.get(atom.symbol, self.covalent_radii['default'])
                
                # Create sphere
                u = np.linspace(0, 2 * np.pi, 20)
                v = np.linspace(0, np.pi, 20)
                sphere_x = radius * np.outer(np.cos(u), np.sin(v)) + x
                sphere_y = radius * np.outer(np.sin(u), np.sin(v)) + y
                sphere_z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + z
                
                ax.plot_surface(sphere_x, sphere_y, sphere_z, color=color, alpha=alpha)
                
                if show_labels:
                    ax.text(x, y, z + radius + 0.2, atom.symbol, 
                           fontsize=10, ha='center', va='center')
    
    def _render_space_filling(self, ax, structure: MolecularStructure,
                             coords: List[Tuple[float, float, float]],
                             show_labels: bool, alpha: float) -> None:
        """Render in space-filling (CPK) style."""
        for i, atom in enumerate(structure.atoms):
            if i < len(coords):
                x, y, z = coords[i]
                color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
                radius = self.vdw_radii.get(atom.symbol, self.vdw_radii['default'])
                
                # Create sphere with van der Waals radius
                u = np.linspace(0, 2 * np.pi, 30)
                v = np.linspace(0, np.pi, 30)
                sphere_x = radius * np.outer(np.cos(u), np.sin(v)) + x
                sphere_y = radius * np.outer(np.sin(u), np.sin(v)) + y
                sphere_z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + z
                
                ax.plot_surface(sphere_x, sphere_y, sphere_z, color=color, alpha=alpha)
                
                if show_labels:
                    ax.text(x, y, z + radius + 0.3, atom.symbol, 
                           fontsize=8, ha='center', va='center')
    
    def _render_wireframe(self, ax, structure: MolecularStructure,
                         coords: List[Tuple[float, float, float]],
                         show_labels: bool) -> None:
        """Render in wireframe style."""
        # Draw bonds only
        if structure.bonds:
            self._draw_bonds_3d(ax, structure, coords, style='wireframe')
        
        # Draw atoms as points
        for i, atom in enumerate(structure.atoms):
            if i < len(coords):
                x, y, z = coords[i]
                color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
                
                ax.scatter([x], [y], [z], c=color, s=50, alpha=0.8)
                
                if show_labels:
                    ax.text(x, y, z + 0.3, atom.symbol, 
                           fontsize=10, ha='center', va='center')
    
    def _render_stick(self, ax, structure: MolecularStructure,
                     coords: List[Tuple[float, float, float]],
                     show_labels: bool) -> None:
        """Render in stick style (bonds only, no atom spheres)."""
        # Draw bonds
        if structure.bonds:
            self._draw_bonds_3d(ax, structure, coords, style='stick')
        
        # Draw small markers at atom positions
        for i, atom in enumerate(structure.atoms):
            if i < len(coords):
                x, y, z = coords[i]
                color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
                
                ax.scatter([x], [y], [z], c=color, s=20, alpha=0.8)
                
                if show_labels:
                    ax.text(x, y, z + 0.2, atom.symbol, 
                           fontsize=8, ha='center', va='center')
    
    def _draw_bonds_3d(self, ax, structure: MolecularStructure,
                      coords: List[Tuple[float, float, float]],
                      style: str = 'cylinder') -> None:
        """Draw bonds in 3D."""
        for bond in structure.bonds:
            if (bond.atom1_idx < len(coords) and bond.atom2_idx < len(coords)):
                x1, y1, z1 = coords[bond.atom1_idx]
                x2, y2, z2 = coords[bond.atom2_idx]
                
                if style == 'wireframe':
                    # Simple line
                    ax.plot([x1, x2], [y1, y2], [z1, z2], 'k-', linewidth=1, alpha=0.6)
                elif style == 'stick':
                    # Thicker line
                    ax.plot([x1, x2], [y1, y2], [z1, z2], 'k-', linewidth=3, alpha=0.8)
                else:
                    # Cylinder (simplified as thick line for now)
                    linewidth = 4 if bond.bond_type == 1 else 6 if bond.bond_type == 2 else 8
                    alpha = 0.7
                    
                    if bond.bond_type == 2:
                        # Double bond - draw two parallel lines
                        self._draw_double_bond_3d(ax, x1, y1, z1, x2, y2, z2)
                    elif bond.bond_type == 3:
                        # Triple bond - draw three parallel lines
                        self._draw_triple_bond_3d(ax, x1, y1, z1, x2, y2, z2)
                    else:
                        # Single bond
                        ax.plot([x1, x2], [y1, y2], [z1, z2], 'k-', 
                               linewidth=linewidth, alpha=alpha)
    
    def _draw_double_bond_3d(self, ax, x1: float, y1: float, z1: float,
                            x2: float, y2: float, z2: float) -> None:
        """Draw a double bond in 3D."""
        # Calculate bond vector
        bond_vec = np.array([x2 - x1, y2 - y1, z2 - z1])
        bond_length = np.linalg.norm(bond_vec)
        
        if bond_length > 0:
            # Normalize bond vector
            bond_unit = bond_vec / bond_length
            
            # Find a perpendicular vector
            if abs(bond_unit[2]) < 0.9:
                perp = np.cross(bond_unit, [0, 0, 1])
            else:
                perp = np.cross(bond_unit, [1, 0, 0])
            
            perp = perp / np.linalg.norm(perp) * 0.1
            
            # Draw two parallel lines
            p1_start = np.array([x1, y1, z1]) + perp
            p1_end = np.array([x2, y2, z2]) + perp
            p2_start = np.array([x1, y1, z1]) - perp
            p2_end = np.array([x2, y2, z2]) - perp
            
            ax.plot([p1_start[0], p1_end[0]], [p1_start[1], p1_end[1]], 
                   [p1_start[2], p1_end[2]], 'k-', linewidth=4, alpha=0.7)
            ax.plot([p2_start[0], p2_end[0]], [p2_start[1], p2_end[1]], 
                   [p2_start[2], p2_end[2]], 'k-', linewidth=4, alpha=0.7)
    
    def _draw_triple_bond_3d(self, ax, x1: float, y1: float, z1: float,
                            x2: float, y2: float, z2: float) -> None:
        """Draw a triple bond in 3D."""
        # Draw center line
        ax.plot([x1, x2], [y1, y2], [z1, z2], 'k-', linewidth=4, alpha=0.7)
        
        # Calculate bond vector
        bond_vec = np.array([x2 - x1, y2 - y1, z2 - z1])
        bond_length = np.linalg.norm(bond_vec)
        
        if bond_length > 0:
            # Normalize bond vector
            bond_unit = bond_vec / bond_length
            
            # Find two perpendicular vectors
            if abs(bond_unit[2]) < 0.9:
                perp1 = np.cross(bond_unit, [0, 0, 1])
            else:
                perp1 = np.cross(bond_unit, [1, 0, 0])
            
            perp1 = perp1 / np.linalg.norm(perp1) * 0.15
            perp2 = np.cross(bond_unit, perp1)
            perp2 = perp2 / np.linalg.norm(perp2) * 0.15
            
            # Draw two additional parallel lines
            for perp in [perp1, perp2]:
                p_start = np.array([x1, y1, z1]) + perp
                p_end = np.array([x2, y2, z2]) + perp
                ax.plot([p_start[0], p_end[0]], [p_start[1], p_end[1]], 
                       [p_start[2], p_end[2]], 'k-', linewidth=3, alpha=0.7)
    
    def _setup_3d_plot(self, ax, coords: List[Tuple[float, float, float]], title: str) -> None:
        """Set up the 3D plot appearance."""
        if coords:
            x_coords = [x for x, y, z in coords]
            y_coords = [y for x, y, z in coords]
            z_coords = [z for x, y, z in coords]
            
            # Set equal aspect ratio
            max_range = max(
                max(x_coords) - min(x_coords) if x_coords else 1,
                max(y_coords) - min(y_coords) if y_coords else 1,
                max(z_coords) - min(z_coords) if z_coords else 1
            )
            
            mid_x = (max(x_coords) + min(x_coords)) * 0.5 if x_coords else 0
            mid_y = (max(y_coords) + min(y_coords)) * 0.5 if y_coords else 0
            mid_z = (max(z_coords) + min(z_coords)) * 0.5 if z_coords else 0
            
            margin = max_range * 0.1
            ax.set_xlim(mid_x - max_range/2 - margin, mid_x + max_range/2 + margin)
            ax.set_ylim(mid_y - max_range/2 - margin, mid_y + max_range/2 + margin)
            ax.set_zlim(mid_z - max_range/2 - margin, mid_z + max_range/2 + margin)
        
        ax.set_xlabel('X (Å)')
        ax.set_ylabel('Y (Å)')
        ax.set_zlabel('Z (Å)')
        ax.set_title(title or 'Molecular Structure', fontsize=14)
        
        # Set viewing angle
        ax.view_init(elev=20, azim=45)
    
    def create_animation(self, structure: MolecularStructure,
                        rotation_frames: int = 36,
                        figsize: Tuple[float, float] = (10, 8)) -> List[Figure]:
        """
        Create an animation by rotating the molecule.
        
        Args:
            structure: MolecularStructure to animate
            rotation_frames: Number of frames for full rotation
            figsize: Figure size (width, height)
            
        Returns:
            List of Figure objects for animation frames
        """
        frames = []
        
        for i in range(rotation_frames):
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='3d')
            
            if structure.atoms:
                coords = self._get_coordinates(structure)
                
                # Render the structure
                if self.style == 'ball_and_stick':
                    self._render_ball_and_stick(ax, structure, coords, True, True, 0.8)
                elif self.style == 'space_filling':
                    self._render_space_filling(ax, structure, coords, True, 0.8)
                elif self.style == 'wireframe':
                    self._render_wireframe(ax, structure, coords, True)
                else:
                    self._render_stick(ax, structure, coords, True)
                
                self._setup_3d_plot(ax, coords, structure.title)
                
                # Set rotation angle
                angle = i * 360 / rotation_frames
                ax.view_init(elev=20, azim=angle)
            
            frames.append(fig)
            plt.close(fig)  # Close to save memory
        
        return frames
    
    def render_molecular_surface(self, structure: MolecularStructure,
                                figsize: Tuple[float, float] = (10, 8),
                                surface_type: str = 'vdw') -> Figure:
        """
        Render molecular surface.
        
        Args:
            structure: MolecularStructure to render
            figsize: Figure size (width, height)
            surface_type: Type of surface ('vdw', 'solvent_accessible')
            
        Returns:
            Matplotlib Figure object
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        if not structure.atoms:
            ax.text(0.5, 0.5, 0.5, 'No structure to display', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            return fig
        
        coords = self._get_coordinates(structure)
        
        # For simplicity, render as overlapping spheres
        # In a full implementation, this would use proper surface algorithms
        for i, atom in enumerate(structure.atoms):
            if i < len(coords):
                x, y, z = coords[i]
                color = self.atom_colors.get(atom.symbol, self.atom_colors['default'])
                
                if surface_type == 'vdw':
                    radius = self.vdw_radii.get(atom.symbol, self.vdw_radii['default'])
                else:  # solvent_accessible
                    radius = self.vdw_radii.get(atom.symbol, self.vdw_radii['default']) + 1.4
                
                # Create sphere
                u = np.linspace(0, 2 * np.pi, 20)
                v = np.linspace(0, np.pi, 20)
                sphere_x = radius * np.outer(np.cos(u), np.sin(v)) + x
                sphere_y = radius * np.outer(np.sin(u), np.sin(v)) + y
                sphere_z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + z
                
                ax.plot_surface(sphere_x, sphere_y, sphere_z, color=color, alpha=0.3)
        
        self._setup_3d_plot(ax, coords, f'{surface_type.upper()} Surface: {structure.title}')
        return fig
    
    def create_stereo_pair(self, structure: MolecularStructure,
                          figsize: Tuple[float, float] = (16, 6),
                          eye_separation: float = 5.0) -> Figure:
        """
        Create a stereo pair for 3D viewing.
        
        Args:
            structure: MolecularStructure to render
            figsize: Figure size (width, height)
            eye_separation: Angle separation between views
            
        Returns:
            Matplotlib Figure with stereo pair
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, 
                                      subplot_kw={'projection': '3d'})
        
        if not structure.atoms:
            for ax in [ax1, ax2]:
                ax.text(0.5, 0.5, 0.5, 'No structure to display', 
                       ha='center', va='center', transform=ax.transAxes, fontsize=14)
            return fig
        
        coords = self._get_coordinates(structure)
        
        # Render on both axes
        for ax in [ax1, ax2]:
            if self.style == 'ball_and_stick':
                self._render_ball_and_stick(ax, structure, coords, True, True, 0.8)
            elif self.style == 'space_filling':
                self._render_space_filling(ax, structure, coords, True, 0.8)
            elif self.style == 'wireframe':
                self._render_wireframe(ax, structure, coords, True)
            else:
                self._render_stick(ax, structure, coords, True)
            
            self._setup_3d_plot(ax, coords, structure.title)
        
        # Set different viewing angles for stereo effect
        ax1.view_init(elev=20, azim=45 - eye_separation/2)
        ax2.view_init(elev=20, azim=45 + eye_separation/2)
        
        ax1.set_title('Left Eye')
        ax2.set_title('Right Eye')
        
        plt.tight_layout()
        return fig