"""
Molecular orbital analysis and visualization.

This module provides tools for analyzing and visualizing molecular orbitals
from quantum chemistry calculations.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from chemesty.molecules.file_formats import MolecularStructure, Atom


class MolecularOrbitals:
    """
    Molecular orbital analysis and visualization.
    
    This class provides methods for analyzing molecular orbitals,
    calculating orbital properties, and creating visualizations.
    """
    
    def __init__(self, structure: MolecularStructure, orbital_data: Dict[str, Any]):
        """
        Initialize molecular orbitals.
        
        Args:
            structure: Molecular structure
            orbital_data: Dictionary containing orbital information
        """
        self.structure = structure
        self.orbital_data = orbital_data
        self.orbital_energies = orbital_data.get('orbital_energies', [])
        self.n_electrons = orbital_data.get('n_electrons', 0)
        self.n_orbitals = len(self.orbital_energies)
        
        # Calculate orbital occupations
        self.occupations = self._calculate_occupations()
        
        # Identify frontier orbitals
        self.homo_index = self._find_homo_index()
        self.lumo_index = self._find_lumo_index()
    
    def _calculate_occupations(self) -> List[float]:
        """Calculate orbital occupations."""
        occupations = []
        electrons_remaining = self.n_electrons
        
        for i, energy in enumerate(self.orbital_energies):
            if electrons_remaining >= 2:
                occupations.append(2.0)
                electrons_remaining -= 2
            elif electrons_remaining == 1:
                occupations.append(1.0)
                electrons_remaining -= 1
            else:
                occupations.append(0.0)
        
        return occupations
    
    def _find_homo_index(self) -> Optional[int]:
        """Find the index of the HOMO (Highest Occupied Molecular Orbital)."""
        for i in range(len(self.occupations) - 1, -1, -1):
            if self.occupations[i] > 0:
                return i
        return None
    
    def _find_lumo_index(self) -> Optional[int]:
        """Find the index of the LUMO (Lowest Unoccupied Molecular Orbital)."""
        for i, occupation in enumerate(self.occupations):
            if occupation == 0:
                return i
        return None
    
    def get_homo_energy(self) -> Optional[float]:
        """Get HOMO energy."""
        if self.homo_index is not None:
            return self.orbital_energies[self.homo_index]
        return None
    
    def get_lumo_energy(self) -> Optional[float]:
        """Get LUMO energy."""
        if self.lumo_index is not None:
            return self.orbital_energies[self.lumo_index]
        return None
    
    def get_homo_lumo_gap(self) -> Optional[float]:
        """Get HOMO-LUMO gap."""
        homo = self.get_homo_energy()
        lumo = self.get_lumo_energy()
        
        if homo is not None and lumo is not None:
            return lumo - homo
        return None
    
    def get_occupied_orbitals(self) -> List[Tuple[int, float, float]]:
        """
        Get list of occupied orbitals.
        
        Returns:
            List of tuples (index, energy, occupation)
        """
        occupied = []
        for i, (energy, occupation) in enumerate(zip(self.orbital_energies, self.occupations)):
            if occupation > 0:
                occupied.append((i, energy, occupation))
        return occupied
    
    def get_virtual_orbitals(self) -> List[Tuple[int, float, float]]:
        """
        Get list of virtual (unoccupied) orbitals.
        
        Returns:
            List of tuples (index, energy, occupation)
        """
        virtual = []
        for i, (energy, occupation) in enumerate(zip(self.orbital_energies, self.occupations)):
            if occupation == 0:
                virtual.append((i, energy, occupation))
        return virtual
    
    def plot_energy_levels(self, figsize: Tuple[float, float] = (8, 10),
                          show_occupations: bool = True,
                          highlight_frontier: bool = True) -> Figure:
        """
        Plot molecular orbital energy levels.
        
        Args:
            figsize: Figure size (width, height)
            show_occupations: Whether to show orbital occupations
            highlight_frontier: Whether to highlight HOMO/LUMO
            
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot energy levels
        for i, (energy, occupation) in enumerate(zip(self.orbital_energies, self.occupations)):
            # Determine color based on occupation
            if occupation == 2.0:
                color = 'blue'
                alpha = 0.8
            elif occupation == 1.0:
                color = 'orange'
                alpha = 0.8
            else:
                color = 'red'
                alpha = 0.4
            
            # Highlight frontier orbitals
            if highlight_frontier:
                if i == self.homo_index:
                    color = 'green'
                    alpha = 1.0
                elif i == self.lumo_index:
                    color = 'purple'
                    alpha = 1.0
            
            # Draw energy level
            ax.hlines(energy, 0, 1, colors=color, alpha=alpha, linewidth=3)
            
            # Add orbital index
            ax.text(1.05, energy, f'{i+1}', va='center', fontsize=8)
            
            # Add occupation if requested
            if show_occupations:
                ax.text(-0.05, energy, f'{occupation:.1f}', ha='right', va='center', fontsize=8)
        
        # Add HOMO-LUMO gap annotation
        if self.homo_index is not None and self.lumo_index is not None:
            homo_energy = self.orbital_energies[self.homo_index]
            lumo_energy = self.orbital_energies[self.lumo_index]
            gap = lumo_energy - homo_energy
            
            # Draw gap arrow
            ax.annotate('', xy=(0.5, lumo_energy), xytext=(0.5, homo_energy),
                       arrowprops=dict(arrowstyle='<->', color='black', lw=2))
            
            # Add gap label
            gap_center = (homo_energy + lumo_energy) / 2
            ax.text(0.5, gap_center, f'Gap: {gap:.2f} eV', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Formatting
        ax.set_xlim(-0.2, 1.3)
        ax.set_ylabel('Energy (eV)')
        ax.set_title('Molecular Orbital Energy Levels')
        ax.set_xticks([])
        ax.grid(True, alpha=0.3)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], color='blue', lw=3, label='Doubly occupied'),
            plt.Line2D([0], [0], color='orange', lw=3, label='Singly occupied'),
            plt.Line2D([0], [0], color='red', lw=3, alpha=0.4, label='Virtual')
        ]
        
        if highlight_frontier:
            legend_elements.extend([
                plt.Line2D([0], [0], color='green', lw=3, label='HOMO'),
                plt.Line2D([0], [0], color='purple', lw=3, label='LUMO')
            ])
        
        ax.legend(handles=legend_elements, loc='upper right')
        
        return fig
    
    def plot_orbital_density(self, orbital_index: int,
                           figsize: Tuple[float, float] = (10, 8),
                           grid_size: int = 50) -> Figure:
        """
        Plot orbital electron density (simplified 2D projection).
        
        Args:
            orbital_index: Index of orbital to plot
            figsize: Figure size (width, height)
            grid_size: Grid resolution for density plot
            
        Returns:
            Matplotlib Figure object
        """
        if orbital_index < 0 or orbital_index >= len(self.orbital_energies):
            raise ValueError(f"Invalid orbital index: {orbital_index}")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Get atomic positions
        if not self.structure.atoms:
            ax.text(0.5, 0.5, 'No atoms to display', ha='center', va='center',
                   transform=ax.transAxes, fontsize=14)
            return fig
        
        x_coords = [atom.x for atom in self.structure.atoms]
        y_coords = [atom.y for atom in self.structure.atoms]
        
        # Create grid
        if x_coords and y_coords:
            x_min, x_max = min(x_coords) - 2, max(x_coords) + 2
            y_min, y_max = min(y_coords) - 2, max(y_coords) + 2
        else:
            x_min, x_max, y_min, y_max = -2, 2, -2, 2
        
        x_grid = np.linspace(x_min, x_max, grid_size)
        y_grid = np.linspace(y_min, y_max, grid_size)
        X, Y = np.meshgrid(x_grid, y_grid)
        
        # Calculate simplified orbital density
        density = self._calculate_orbital_density_2d(orbital_index, X, Y)
        
        # Plot density
        contour = ax.contourf(X, Y, density, levels=20, cmap='RdYlBu_r', alpha=0.7)
        ax.contour(X, Y, density, levels=10, colors='black', alpha=0.3, linewidths=0.5)
        
        # Add colorbar
        cbar = plt.colorbar(contour, ax=ax)
        cbar.set_label('Electron Density')
        
        # Plot atoms
        for i, atom in enumerate(self.structure.atoms):
            ax.scatter(atom.x, atom.y, s=200, c='white', edgecolors='black', linewidth=2)
            ax.text(atom.x, atom.y, atom.symbol, ha='center', va='center',
                   fontsize=12, fontweight='bold')
        
        # Formatting
        ax.set_xlabel('X (Å)')
        ax.set_ylabel('Y (Å)')
        ax.set_title(f'Orbital {orbital_index + 1} Density '
                    f'(Energy: {self.orbital_energies[orbital_index]:.2f} eV)')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def _calculate_orbital_density_2d(self, orbital_index: int, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        """
        Calculate simplified 2D orbital density.
        
        This is a very simplified implementation for demonstration.
        Real orbital densities would require proper basis functions and coefficients.
        """
        density = np.zeros_like(X)
        
        # Simple Gaussian-based approximation
        for atom in self.structure.atoms:
            # Distance from each grid point to atom
            r_squared = (X - atom.x)**2 + (Y - atom.y)**2
            
            # Orbital-dependent parameters
            if orbital_index < len(self.structure.atoms):
                # Core-like orbitals (more localized)
                sigma = 0.5
                amplitude = 1.0
            else:
                # Valence-like orbitals (more delocalized)
                sigma = 1.0
                amplitude = 0.5
            
            # Add Gaussian contribution
            contribution = amplitude * np.exp(-r_squared / (2 * sigma**2))
            
            # Add some orbital character (simplified)
            if orbital_index % 2 == 1:
                # Add some p-character (directional)
                contribution *= np.cos(np.arctan2(Y - atom.y, X - atom.x))
            
            density += contribution
        
        # Add some interference patterns for molecular orbitals
        if len(self.structure.atoms) > 1:
            for i, atom1 in enumerate(self.structure.atoms):
                for j, atom2 in enumerate(self.structure.atoms[i+1:], i+1):
                    # Distance between atoms
                    bond_length = np.sqrt((atom1.x - atom2.x)**2 + (atom1.y - atom2.y)**2)
                    if bond_length > 0:
                        # Add bonding/antibonding character
                        r1 = np.sqrt((X - atom1.x)**2 + (Y - atom1.y)**2)
                        r2 = np.sqrt((X - atom2.x)**2 + (Y - atom2.y)**2)
                        
                        # Bonding (constructive) or antibonding (destructive)
                        if orbital_index % 2 == 0:
                            # Bonding
                            interference = 0.3 * np.exp(-(r1 + r2 - bond_length)**2 / bond_length)
                        else:
                            # Antibonding
                            interference = -0.2 * np.exp(-(r1 - r2)**2 / bond_length)
                        
                        density += interference
        
        return density
    
    def plot_dos(self, figsize: Tuple[float, float] = (10, 6),
                 broadening: float = 0.1) -> Figure:
        """
        Plot Density of States (DOS).
        
        Args:
            figsize: Figure size (width, height)
            broadening: Gaussian broadening for DOS peaks
            
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if not self.orbital_energies:
            ax.text(0.5, 0.5, 'No orbital data available', ha='center', va='center',
                   transform=ax.transAxes, fontsize=14)
            return fig
        
        # Create energy grid
        e_min = min(self.orbital_energies) - 2
        e_max = max(self.orbital_energies) + 2
        energy_grid = np.linspace(e_min, e_max, 1000)
        
        # Calculate DOS
        dos = np.zeros_like(energy_grid)
        
        for energy, occupation in zip(self.orbital_energies, self.occupations):
            # Gaussian broadening
            gaussian = np.exp(-(energy_grid - energy)**2 / (2 * broadening**2))
            gaussian /= np.sqrt(2 * np.pi) * broadening
            
            # Weight by occupation
            dos += occupation * gaussian
        
        # Plot DOS
        ax.fill_between(energy_grid, dos, alpha=0.7, color='blue', label='Total DOS')
        ax.plot(energy_grid, dos, 'b-', linewidth=2)
        
        # Mark orbital positions
        for i, (energy, occupation) in enumerate(zip(self.orbital_energies, self.occupations)):
            if occupation > 0:
                ax.axvline(energy, color='red', alpha=0.5, linestyle='--')
        
        # Mark HOMO and LUMO
        if self.homo_index is not None:
            homo_energy = self.orbital_energies[self.homo_index]
            ax.axvline(homo_energy, color='green', linewidth=2, label='HOMO')
        
        if self.lumo_index is not None:
            lumo_energy = self.orbital_energies[self.lumo_index]
            ax.axvline(lumo_energy, color='purple', linewidth=2, label='LUMO')
        
        # Formatting
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel('Density of States')
        ax.set_title('Density of States')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def analyze_orbital_character(self, orbital_index: int) -> Dict[str, Any]:
        """
        Analyze the character of a specific orbital.
        
        Args:
            orbital_index: Index of orbital to analyze
            
        Returns:
            Dictionary with orbital character analysis
        """
        if orbital_index < 0 or orbital_index >= len(self.orbital_energies):
            raise ValueError(f"Invalid orbital index: {orbital_index}")
        
        energy = self.orbital_energies[orbital_index]
        occupation = self.occupations[orbital_index]
        
        # Determine orbital type
        if occupation > 0:
            orbital_type = 'occupied'
        else:
            orbital_type = 'virtual'
        
        # Determine if it's a frontier orbital
        is_homo = (orbital_index == self.homo_index)
        is_lumo = (orbital_index == self.lumo_index)
        
        # Estimate orbital character (simplified)
        if orbital_index < len(self.structure.atoms):
            character = 'core-like'
        elif orbital_index < 2 * len(self.structure.atoms):
            character = 'valence'
        else:
            character = 'virtual/Rydberg'
        
        return {
            'index': orbital_index,
            'energy': energy,
            'occupation': occupation,
            'type': orbital_type,
            'character': character,
            'is_homo': is_homo,
            'is_lumo': is_lumo,
            'is_frontier': is_homo or is_lumo
        }
    
    def get_orbital_summary(self) -> Dict[str, Any]:
        """
        Get summary of all orbitals.
        
        Returns:
            Dictionary with orbital summary
        """
        occupied = self.get_occupied_orbitals()
        virtual = self.get_virtual_orbitals()
        
        summary = {
            'total_orbitals': self.n_orbitals,
            'n_electrons': self.n_electrons,
            'n_occupied': len(occupied),
            'n_virtual': len(virtual),
            'homo_index': self.homo_index,
            'lumo_index': self.lumo_index,
            'homo_energy': self.get_homo_energy(),
            'lumo_energy': self.get_lumo_energy(),
            'homo_lumo_gap': self.get_homo_lumo_gap(),
            'energy_range': (min(self.orbital_energies), max(self.orbital_energies)) if self.orbital_energies else None,
            'occupied_orbitals': occupied,
            'virtual_orbitals': virtual[:10]  # Show first 10 virtual orbitals
        }
        
        return summary