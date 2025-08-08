"""
Specific quantum chemistry method implementations.

This module provides implementations of specific quantum chemistry methods
including Hartree-Fock and Density Functional Theory.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import math
from chemesty.molecules.file_formats import MolecularStructure, Atom
from chemesty.quantum.basis_sets import BasisSetManager, BasisFunction


class HartreeFock:
    """
    Hartree-Fock method implementation.
    
    This class provides a simplified implementation of the Hartree-Fock
    self-consistent field method for electronic structure calculations.
    """
    
    def __init__(self, basis_set: str = 'sto-3g', max_iterations: int = 100,
                 convergence_threshold: float = 1e-6):
        """
        Initialize Hartree-Fock calculator.
        
        Args:
            basis_set: Basis set to use for calculations
            max_iterations: Maximum number of SCF iterations
            convergence_threshold: Energy convergence threshold
        """
        self.basis_set_name = basis_set
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.basis_manager = BasisSetManager()
        
        # SCF data
        self.basis_functions = []
        self.overlap_matrix = None
        self.core_hamiltonian = None
        self.density_matrix = None
        self.fock_matrix = None
        self.orbital_energies = []
        self.orbital_coefficients = None
        self.total_energy = 0.0
        self.converged = False
        self.scf_energies = []
    
    def calculate(self, structure: MolecularStructure, 
                 charge: int = 0, multiplicity: int = 1) -> Dict[str, Any]:
        """
        Perform Hartree-Fock calculation.
        
        Args:
            structure: Molecular structure
            charge: Total charge of the system
            multiplicity: Spin multiplicity (2S + 1)
            
        Returns:
            Dictionary containing calculation results
        """
        # Generate basis functions
        self.basis_functions = self.basis_manager.generate_basis_functions(
            structure, self.basis_set_name
        )
        
        n_basis = len(self.basis_functions)
        n_electrons = self._count_electrons(structure, charge)
        
        if n_basis == 0:
            raise ValueError("No basis functions generated")
        
        # Calculate one-electron integrals
        self.overlap_matrix = self.basis_manager.calculate_overlap_matrix(self.basis_functions)
        self.core_hamiltonian = self._calculate_core_hamiltonian(structure)
        
        # Initial guess for density matrix
        self.density_matrix = self._initial_guess_density(n_electrons)
        
        # SCF iterations
        self.scf_energies = []
        previous_energy = 0.0
        
        for iteration in range(self.max_iterations):
            # Build Fock matrix
            self.fock_matrix = self._build_fock_matrix()
            
            # Solve generalized eigenvalue problem: FC = SCE
            self.orbital_energies, self.orbital_coefficients = self._solve_roothaan_equations()
            
            # Build new density matrix
            new_density = self._build_density_matrix(n_electrons)
            
            # Calculate total energy
            self.total_energy = self._calculate_total_energy(structure)
            self.scf_energies.append(self.total_energy)
            
            # Check convergence
            energy_change = abs(self.total_energy - previous_energy)
            density_change = np.max(np.abs(new_density - self.density_matrix))
            
            if energy_change < self.convergence_threshold and density_change < self.convergence_threshold:
                self.converged = True
                break
            
            # Update density matrix with damping
            damping_factor = 0.5
            self.density_matrix = (damping_factor * new_density + 
                                 (1 - damping_factor) * self.density_matrix)
            previous_energy = self.total_energy
        
        # Calculate properties
        results = self._compile_results(structure, charge, multiplicity, n_electrons)
        
        return results
    
    def _count_electrons(self, structure: MolecularStructure, charge: int) -> int:
        """Count total number of electrons."""
        atomic_numbers = {
            'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
            'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
            'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20
        }
        
        total_electrons = 0
        for atom in structure.atoms:
            total_electrons += atomic_numbers.get(atom.symbol, 0)
        
        return total_electrons - charge
    
    def _calculate_core_hamiltonian(self, structure: MolecularStructure) -> np.ndarray:
        """Calculate core Hamiltonian matrix (simplified)."""
        n_basis = len(self.basis_functions)
        h_core = np.zeros((n_basis, n_basis))
        
        # Kinetic energy + nuclear attraction (simplified)
        for i in range(n_basis):
            for j in range(n_basis):
                bf_i = self.basis_functions[i]
                bf_j = self.basis_functions[j]
                
                # Kinetic energy integral (simplified)
                kinetic = self._kinetic_energy_integral(bf_i, bf_j)
                
                # Nuclear attraction integral (simplified)
                nuclear = self._nuclear_attraction_integral(bf_i, bf_j, structure)
                
                h_core[i, j] = kinetic + nuclear
        
        return h_core
    
    def _kinetic_energy_integral(self, bf_i: BasisFunction, bf_j: BasisFunction) -> float:
        """Calculate kinetic energy integral (simplified)."""
        # Very simplified kinetic energy calculation
        overlap = self.basis_manager._calculate_overlap_integral(bf_i, bf_j)
        
        # Rough approximation based on exponents
        alpha_i = bf_i.exponent
        alpha_j = bf_j.exponent
        
        kinetic = 0.5 * (alpha_i + alpha_j) * overlap
        
        return kinetic
    
    def _nuclear_attraction_integral(self, bf_i: BasisFunction, bf_j: BasisFunction,
                                   structure: MolecularStructure) -> float:
        """Calculate nuclear attraction integral (simplified)."""
        atomic_numbers = {
            'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
            'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
            'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20
        }
        
        nuclear_attraction = 0.0
        overlap = self.basis_manager._calculate_overlap_integral(bf_i, bf_j)
        
        for atom in structure.atoms:
            z = atomic_numbers.get(atom.symbol, 1)
            atom_pos = np.array([atom.x, atom.y, atom.z])
            
            # Distance from basis function centers to nucleus
            r_i = np.linalg.norm(bf_i.center - atom_pos)
            r_j = np.linalg.norm(bf_j.center - atom_pos)
            
            # Simplified nuclear attraction
            if r_i + r_j > 0:
                nuclear_attraction -= z * overlap / (1 + r_i + r_j)
        
        return nuclear_attraction
    
    def _initial_guess_density(self, n_electrons: int) -> np.ndarray:
        """Generate initial guess for density matrix."""
        n_basis = len(self.basis_functions)
        density = np.zeros((n_basis, n_basis))
        
        # Simple core guess - put electrons in lowest basis functions
        n_occupied = min(n_electrons // 2, n_basis)
        
        for i in range(n_occupied):
            density[i, i] = 2.0  # Doubly occupied
        
        # Handle odd electron
        if n_electrons % 2 == 1 and n_occupied < n_basis:
            density[n_occupied, n_occupied] = 1.0
        
        return density
    
    def _build_fock_matrix(self) -> np.ndarray:
        """Build Fock matrix."""
        # F = H_core + G
        # where G is the two-electron contribution
        
        fock = self.core_hamiltonian.copy()
        
        # Add two-electron terms (simplified)
        n_basis = len(self.basis_functions)
        
        for i in range(n_basis):
            for j in range(n_basis):
                g_ij = 0.0
                
                for k in range(n_basis):
                    for l in range(n_basis):
                        # Coulomb integral (simplified)
                        coulomb = self._two_electron_integral(i, j, k, l)
                        
                        # Exchange integral (simplified)
                        exchange = self._two_electron_integral(i, k, j, l)
                        
                        g_ij += self.density_matrix[k, l] * (coulomb - 0.5 * exchange)
                
                fock[i, j] += g_ij
        
        return fock
    
    def _two_electron_integral(self, i: int, j: int, k: int, l: int) -> float:
        """Calculate two-electron integral (simplified)."""
        bf_i = self.basis_functions[i]
        bf_j = self.basis_functions[j]
        bf_k = self.basis_functions[k]
        bf_l = self.basis_functions[l]
        
        # Very simplified two-electron integral
        # Real implementation would use proper integral evaluation
        
        # Distance-based approximation
        r_ij = np.linalg.norm(bf_i.center - bf_j.center)
        r_kl = np.linalg.norm(bf_k.center - bf_l.center)
        r_centers = np.linalg.norm((bf_i.center + bf_j.center)/2 - (bf_k.center + bf_l.center)/2)
        
        # Simplified integral based on overlaps and distances
        overlap_ij = self.basis_manager._calculate_overlap_integral(bf_i, bf_j)
        overlap_kl = self.basis_manager._calculate_overlap_integral(bf_k, bf_l)
        
        integral = overlap_ij * overlap_kl / (1 + r_centers + 0.1)
        
        return integral
    
    def _solve_roothaan_equations(self) -> Tuple[np.ndarray, np.ndarray]:
        """Solve Roothaan equations FC = SCE."""
        try:
            # Generalized eigenvalue problem
            eigenvalues, eigenvectors = np.linalg.eigh(self.fock_matrix, self.overlap_matrix)
            
            # Sort by eigenvalue
            idx = np.argsort(eigenvalues)
            eigenvalues = eigenvalues[idx]
            eigenvectors = eigenvectors[:, idx]
            
            return eigenvalues, eigenvectors
        
        except np.linalg.LinAlgError:
            # Fallback to regular eigenvalue problem
            eigenvalues, eigenvectors = np.linalg.eigh(self.fock_matrix)
            idx = np.argsort(eigenvalues)
            return eigenvalues[idx], eigenvectors[:, idx]
    
    def _build_density_matrix(self, n_electrons: int) -> np.ndarray:
        """Build density matrix from orbital coefficients."""
        n_basis = len(self.basis_functions)
        density = np.zeros((n_basis, n_basis))
        
        n_occupied = n_electrons // 2
        
        for i in range(n_basis):
            for j in range(n_basis):
                for k in range(min(n_occupied, n_basis)):
                    density[i, j] += 2.0 * self.orbital_coefficients[i, k] * self.orbital_coefficients[j, k]
        
        # Handle odd electron (simplified)
        if n_electrons % 2 == 1 and n_occupied < n_basis:
            for i in range(n_basis):
                for j in range(n_basis):
                    density[i, j] += self.orbital_coefficients[i, n_occupied] * self.orbital_coefficients[j, n_occupied]
        
        return density
    
    def _calculate_total_energy(self, structure: MolecularStructure) -> float:
        """Calculate total electronic energy."""
        # E = Tr(P * (H + F)) / 2 + V_nn
        electronic_energy = 0.5 * np.trace(self.density_matrix @ (self.core_hamiltonian + self.fock_matrix))
        
        # Nuclear repulsion
        nuclear_repulsion = self._calculate_nuclear_repulsion(structure)
        
        return electronic_energy + nuclear_repulsion
    
    def _calculate_nuclear_repulsion(self, structure: MolecularStructure) -> float:
        """Calculate nuclear-nuclear repulsion energy."""
        atomic_numbers = {
            'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
            'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
            'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20
        }
        
        repulsion = 0.0
        
        for i, atom1 in enumerate(structure.atoms):
            for j, atom2 in enumerate(structure.atoms[i+1:], i+1):
                z1 = atomic_numbers.get(atom1.symbol, 1)
                z2 = atomic_numbers.get(atom2.symbol, 1)
                
                distance = np.sqrt(
                    (atom1.x - atom2.x)**2 +
                    (atom1.y - atom2.y)**2 +
                    (atom1.z - atom2.z)**2
                )
                
                if distance > 0:
                    repulsion += z1 * z2 / distance
        
        return repulsion
    
    def _compile_results(self, structure: MolecularStructure, charge: int, 
                        multiplicity: int, n_electrons: int) -> Dict[str, Any]:
        """Compile calculation results."""
        n_occupied = n_electrons // 2
        
        results = {
            'method': 'Hartree-Fock',
            'basis_set': self.basis_set_name,
            'total_energy': self.total_energy,
            'electronic_energy': self.total_energy - self._calculate_nuclear_repulsion(structure),
            'nuclear_repulsion': self._calculate_nuclear_repulsion(structure),
            'orbital_energies': self.orbital_energies.tolist(),
            'n_electrons': n_electrons,
            'n_basis_functions': len(self.basis_functions),
            'converged': self.converged,
            'scf_iterations': len(self.scf_energies),
            'scf_energies': self.scf_energies,
            'charge': charge,
            'multiplicity': multiplicity
        }
        
        # Add HOMO/LUMO information
        if len(self.orbital_energies) > 0:
            if n_occupied > 0:
                results['homo_energy'] = self.orbital_energies[n_occupied - 1]
                results['homo_index'] = n_occupied - 1
            
            if n_occupied < len(self.orbital_energies):
                results['lumo_energy'] = self.orbital_energies[n_occupied]
                results['lumo_index'] = n_occupied
                
                if n_occupied > 0:
                    results['homo_lumo_gap'] = results['lumo_energy'] - results['homo_energy']
        
        return results


class DFT:
    """
    Density Functional Theory implementation.
    
    This class provides a simplified implementation of DFT calculations
    using common exchange-correlation functionals.
    """
    
    def __init__(self, functional: str = 'b3lyp', basis_set: str = 'sto-3g',
                 max_iterations: int = 100, convergence_threshold: float = 1e-6):
        """
        Initialize DFT calculator.
        
        Args:
            functional: Exchange-correlation functional ('lda', 'pbe', 'b3lyp')
            basis_set: Basis set to use for calculations
            max_iterations: Maximum number of SCF iterations
            convergence_threshold: Energy convergence threshold
        """
        self.functional = functional.lower()
        self.basis_set_name = basis_set
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        
        # Initialize Hartree-Fock calculator for base functionality
        self.hf_calculator = HartreeFock(basis_set, max_iterations, convergence_threshold)
        
        # DFT-specific parameters
        self.exchange_correlation_energy = 0.0
        self.exchange_energy = 0.0
        self.correlation_energy = 0.0
    
    def calculate(self, structure: MolecularStructure, 
                 charge: int = 0, multiplicity: int = 1) -> Dict[str, Any]:
        """
        Perform DFT calculation.
        
        Args:
            structure: Molecular structure
            charge: Total charge of the system
            multiplicity: Spin multiplicity (2S + 1)
            
        Returns:
            Dictionary containing calculation results
        """
        # Start with Hartree-Fock calculation as base
        hf_results = self.hf_calculator.calculate(structure, charge, multiplicity)
        
        # Add DFT corrections
        self._calculate_exchange_correlation(structure)
        
        # Update total energy with XC contribution
        dft_energy = hf_results['total_energy'] + self.exchange_correlation_energy
        
        # Compile DFT results
        results = hf_results.copy()
        results.update({
            'method': f'DFT ({self.functional.upper()})',
            'functional': self.functional,
            'total_energy': dft_energy,
            'exchange_correlation_energy': self.exchange_correlation_energy,
            'exchange_energy': self.exchange_energy,
            'correlation_energy': self.correlation_energy,
            'hf_energy': hf_results['total_energy']
        })
        
        return results
    
    def _calculate_exchange_correlation(self, structure: MolecularStructure) -> None:
        """Calculate exchange-correlation energy."""
        if self.functional == 'lda':
            self._calculate_lda_xc(structure)
        elif self.functional == 'pbe':
            self._calculate_pbe_xc(structure)
        elif self.functional == 'b3lyp':
            self._calculate_b3lyp_xc(structure)
        else:
            raise ValueError(f"Unsupported functional: {self.functional}")
    
    def _calculate_lda_xc(self, structure: MolecularStructure) -> None:
        """Calculate LDA exchange-correlation energy."""
        # Very simplified LDA implementation
        n_electrons = self.hf_calculator._count_electrons(structure, 0)
        
        # Rough LDA exchange energy: E_x = -C_x * n^(4/3)
        c_x = 0.7386  # Exchange constant
        self.exchange_energy = -c_x * (n_electrons ** (4/3))
        
        # Rough LDA correlation energy
        self.correlation_energy = -0.1 * n_electrons * np.log(n_electrons + 1)
        
        self.exchange_correlation_energy = self.exchange_energy + self.correlation_energy
    
    def _calculate_pbe_xc(self, structure: MolecularStructure) -> None:
        """Calculate PBE exchange-correlation energy."""
        # Start with LDA
        self._calculate_lda_xc(structure)
        
        # Add gradient corrections (simplified)
        n_electrons = self.hf_calculator._count_electrons(structure, 0)
        gradient_correction = -0.05 * n_electrons * np.sqrt(n_electrons)
        
        self.exchange_correlation_energy += gradient_correction
    
    def _calculate_b3lyp_xc(self, structure: MolecularStructure) -> None:
        """Calculate B3LYP exchange-correlation energy."""
        # B3LYP mixing parameters
        a0 = 0.20  # Exact exchange mixing
        ax = 0.72  # Slater exchange
        ac = 0.81  # VWN correlation
        
        # Start with LDA
        self._calculate_lda_xc(structure)
        
        # Get HF exchange energy (simplified)
        n_electrons = self.hf_calculator._count_electrons(structure, 0)
        hf_exchange = -0.5 * n_electrons * np.log(n_electrons + 1)
        
        # B3LYP mixing
        self.exchange_energy = (a0 * hf_exchange + 
                               (1 - a0) * ax * self.exchange_energy)
        
        self.correlation_energy *= ac
        
        self.exchange_correlation_energy = self.exchange_energy + self.correlation_energy
    
    def get_functional_info(self) -> Dict[str, Any]:
        """Get information about the current functional."""
        functional_info = {
            'lda': {
                'name': 'Local Density Approximation',
                'type': 'local',
                'description': 'Simple local functional based on uniform electron gas'
            },
            'pbe': {
                'name': 'Perdew-Burke-Ernzerhof',
                'type': 'gga',
                'description': 'Generalized gradient approximation functional'
            },
            'b3lyp': {
                'name': 'Becke 3-parameter Lee-Yang-Parr',
                'type': 'hybrid',
                'description': 'Hybrid functional with exact exchange mixing'
            }
        }
        
        return functional_info.get(self.functional, {'name': 'Unknown', 'type': 'unknown'})


def compare_methods(structure: MolecularStructure, methods: List[str],
                   basis_set: str = 'sto-3g', charge: int = 0, 
                   multiplicity: int = 1) -> Dict[str, Any]:
    """
    Compare different quantum chemistry methods on the same system.
    
    Args:
        structure: Molecular structure
        methods: List of method names ('hf', 'lda', 'pbe', 'b3lyp')
        basis_set: Basis set to use
        charge: Total charge
        multiplicity: Spin multiplicity
        
    Returns:
        Dictionary with comparison results
    """
    results = {}
    
    for method in methods:
        try:
            if method.lower() == 'hf':
                calculator = HartreeFock(basis_set)
            else:
                calculator = DFT(method, basis_set)
            
            method_results = calculator.calculate(structure, charge, multiplicity)
            results[method] = method_results
            
        except Exception as e:
            results[method] = {'error': str(e)}
    
    # Add comparison summary
    if len(results) > 1:
        energies = {}
        for method, result in results.items():
            if 'total_energy' in result:
                energies[method] = result['total_energy']
        
        if energies:
            min_energy = min(energies.values())
            max_energy = max(energies.values())
            
            results['comparison'] = {
                'energy_range': max_energy - min_energy,
                'lowest_energy_method': min(energies, key=energies.get),
                'highest_energy_method': max(energies, key=energies.get),
                'energies': energies
            }
    
    return results