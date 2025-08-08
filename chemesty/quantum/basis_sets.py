"""
Basis set management for quantum chemistry calculations.

This module provides tools for managing and working with quantum chemistry
basis sets including Gaussian-type orbitals and Slater-type orbitals.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import math
from chemesty.molecules.file_formats import MolecularStructure, Atom


class BasisFunction:
    """
    Represents a single basis function (Gaussian or Slater type).
    """
    
    def __init__(self, center: Tuple[float, float, float], 
                 angular_momentum: Tuple[int, int, int],
                 exponent: float, coefficient: float = 1.0,
                 function_type: str = 'gaussian'):
        """
        Initialize a basis function.
        
        Args:
            center: Center coordinates (x, y, z)
            angular_momentum: Angular momentum quantum numbers (l, m, n)
            exponent: Orbital exponent
            coefficient: Contraction coefficient
            function_type: Type of function ('gaussian' or 'slater')
        """
        self.center = np.array(center)
        self.angular_momentum = angular_momentum
        self.exponent = exponent
        self.coefficient = coefficient
        self.function_type = function_type
        
        # Calculate normalization constant
        self.normalization = self._calculate_normalization()
    
    def _calculate_normalization(self) -> float:
        """Calculate normalization constant for the basis function."""
        l, m, n = self.angular_momentum
        alpha = self.exponent
        
        if self.function_type == 'gaussian':
            # Normalization for Gaussian-type orbitals
            norm = (2 * alpha / np.pi)**(3/4)
            norm *= (4 * alpha)**(l + m + n) / 2
            norm *= math.sqrt(math.factorial(2*l - 1) * math.factorial(2*m - 1) * math.factorial(2*n - 1))
            norm /= math.sqrt(math.factorial(l) * math.factorial(m) * math.factorial(n))
        else:
            # Normalization for Slater-type orbitals (simplified)
            norm = (2 * alpha)**(l + m + n + 1.5)
            norm *= math.sqrt(math.factorial(l + m + n))
        
        return norm
    
    def evaluate(self, point: np.ndarray) -> float:
        """
        Evaluate the basis function at a given point.
        
        Args:
            point: Coordinates where to evaluate (x, y, z)
            
        Returns:
            Value of the basis function at the point
        """
        r = point - self.center
        x, y, z = r
        l, m, n = self.angular_momentum
        
        if self.function_type == 'gaussian':
            # Gaussian-type orbital
            r_squared = np.dot(r, r)
            radial = np.exp(-self.exponent * r_squared)
            angular = (x**l) * (y**m) * (z**n)
            return self.coefficient * self.normalization * radial * angular
        else:
            # Slater-type orbital
            r_magnitude = np.linalg.norm(r)
            if r_magnitude == 0:
                return 0.0 if (l + m + n) > 0 else self.coefficient * self.normalization
            
            radial = (r_magnitude**(l + m + n)) * np.exp(-self.exponent * r_magnitude)
            angular = (x**l) * (y**m) * (z**n) / (r_magnitude**(l + m + n))
            return self.coefficient * self.normalization * radial * angular


class BasisSetManager:
    """
    Manager for quantum chemistry basis sets.
    
    This class provides tools for loading, managing, and working with
    various quantum chemistry basis sets.
    """
    
    def __init__(self):
        """Initialize the basis set manager."""
        self.basis_sets = {}
        self.loaded_basis_sets = {}
        
        # Initialize built-in basis sets
        self._initialize_builtin_basis_sets()
    
    def _initialize_builtin_basis_sets(self) -> None:
        """Initialize built-in basis set definitions."""
        # STO-3G basis set (minimal basis)
        self.basis_sets['sto-3g'] = {
            'description': 'STO-3G minimal basis set',
            'type': 'gaussian',
            'elements': {
                'H': {
                    'shells': [
                        {
                            'type': 's',
                            'exponents': [3.42525091, 0.62391373, 0.16885540],
                            'coefficients': [0.15432897, 0.53532814, 0.44463454]
                        }
                    ]
                },
                'He': {
                    'shells': [
                        {
                            'type': 's',
                            'exponents': [6.36242139, 1.15892300, 0.31364979],
                            'coefficients': [0.15432897, 0.53532814, 0.44463454]
                        }
                    ]
                },
                'C': {
                    'shells': [
                        {
                            'type': 's',
                            'exponents': [71.6168370, 13.0450960, 3.5305122],
                            'coefficients': [0.15432897, 0.53532814, 0.44463454]
                        },
                        {
                            'type': 's',
                            'exponents': [2.9412494, 0.6834831, 0.2222899],
                            'coefficients': [-0.09996723, 0.39951283, 0.70011547]
                        },
                        {
                            'type': 'p',
                            'exponents': [2.9412494, 0.6834831, 0.2222899],
                            'coefficients': [0.15591627, 0.60768372, 0.39195739]
                        }
                    ]
                },
                'N': {
                    'shells': [
                        {
                            'type': 's',
                            'exponents': [99.1061690, 18.0523120, 4.8856602],
                            'coefficients': [0.15432897, 0.53532814, 0.44463454]
                        },
                        {
                            'type': 's',
                            'exponents': [3.7804559, 0.8784966, 0.2857144],
                            'coefficients': [-0.09996723, 0.39951283, 0.70011547]
                        },
                        {
                            'type': 'p',
                            'exponents': [3.7804559, 0.8784966, 0.2857144],
                            'coefficients': [0.15591627, 0.60768372, 0.39195739]
                        }
                    ]
                },
                'O': {
                    'shells': [
                        {
                            'type': 's',
                            'exponents': [130.7093200, 23.8088610, 6.4436083],
                            'coefficients': [0.15432897, 0.53532814, 0.44463454]
                        },
                        {
                            'type': 's',
                            'exponents': [5.0331513, 1.1695961, 0.3803890],
                            'coefficients': [-0.09996723, 0.39951283, 0.70011547]
                        },
                        {
                            'type': 'p',
                            'exponents': [5.0331513, 1.1695961, 0.3803890],
                            'coefficients': [0.15591627, 0.60768372, 0.39195739]
                        }
                    ]
                }
            }
        }
        
        # 6-31G basis set (split-valence)
        self.basis_sets['6-31g'] = {
            'description': '6-31G split-valence basis set',
            'type': 'gaussian',
            'elements': {
                'H': {
                    'shells': [
                        {
                            'type': 's',
                            'exponents': [18.7311370, 2.8253937, 0.6401217],
                            'coefficients': [0.03349460, 0.23472695, 0.81375733]
                        },
                        {
                            'type': 's',
                            'exponents': [0.1612778],
                            'coefficients': [1.0]
                        }
                    ]
                },
                'C': {
                    'shells': [
                        {
                            'type': 's',
                            'exponents': [3047.5249000, 457.3695100, 103.9486900, 29.2101550, 9.2866630, 3.1639270],
                            'coefficients': [0.0018347, 0.0140373, 0.0688426, 0.2321844, 0.4679413, 0.3623120]
                        },
                        {
                            'type': 's',
                            'exponents': [7.8682724, 1.8812885, 0.5442493],
                            'coefficients': [-0.1193324, 0.1608542, 1.1434564]
                        },
                        {
                            'type': 's',
                            'exponents': [0.1687144],
                            'coefficients': [1.0]
                        },
                        {
                            'type': 'p',
                            'exponents': [7.8682724, 1.8812885, 0.5442493],
                            'coefficients': [0.0689991, 0.3164240, 0.7443083]
                        },
                        {
                            'type': 'p',
                            'exponents': [0.1687144],
                            'coefficients': [1.0]
                        }
                    ]
                }
            }
        }
    
    def get_basis_set(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get basis set definition by name.
        
        Args:
            name: Name of the basis set
            
        Returns:
            Basis set definition dictionary or None if not found
        """
        return self.basis_sets.get(name.lower())
    
    def list_available_basis_sets(self) -> List[str]:
        """
        List all available basis sets.
        
        Returns:
            List of basis set names
        """
        return list(self.basis_sets.keys())
    
    def generate_basis_functions(self, structure: MolecularStructure, 
                                basis_set_name: str) -> List[BasisFunction]:
        """
        Generate basis functions for a molecular structure.
        
        Args:
            structure: Molecular structure
            basis_set_name: Name of the basis set to use
            
        Returns:
            List of basis functions
        """
        basis_set = self.get_basis_set(basis_set_name)
        if basis_set is None:
            raise ValueError(f"Basis set '{basis_set_name}' not found")
        
        basis_functions = []
        
        for atom in structure.atoms:
            atom_basis = basis_set['elements'].get(atom.symbol)
            if atom_basis is None:
                raise ValueError(f"Basis set '{basis_set_name}' does not support element '{atom.symbol}'")
            
            center = (atom.x, atom.y, atom.z)
            
            for shell in atom_basis['shells']:
                shell_type = shell['type']
                exponents = shell['exponents']
                coefficients = shell['coefficients']
                
                # Generate angular momentum combinations for the shell
                angular_momenta = self._get_angular_momentum_combinations(shell_type)
                
                for l, m, n in angular_momenta:
                    for exp, coeff in zip(exponents, coefficients):
                        bf = BasisFunction(
                            center=center,
                            angular_momentum=(l, m, n),
                            exponent=exp,
                            coefficient=coeff,
                            function_type=basis_set['type']
                        )
                        basis_functions.append(bf)
        
        return basis_functions
    
    def _get_angular_momentum_combinations(self, shell_type: str) -> List[Tuple[int, int, int]]:
        """
        Get angular momentum combinations for a shell type.
        
        Args:
            shell_type: Type of shell ('s', 'p', 'd', 'f')
            
        Returns:
            List of (l, m, n) tuples
        """
        if shell_type == 's':
            return [(0, 0, 0)]
        elif shell_type == 'p':
            return [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        elif shell_type == 'd':
            return [
                (2, 0, 0), (0, 2, 0), (0, 0, 2),
                (1, 1, 0), (1, 0, 1), (0, 1, 1)
            ]
        elif shell_type == 'f':
            return [
                (3, 0, 0), (0, 3, 0), (0, 0, 3),
                (2, 1, 0), (2, 0, 1), (1, 2, 0),
                (0, 2, 1), (1, 0, 2), (0, 1, 2),
                (1, 1, 1)
            ]
        else:
            raise ValueError(f"Unsupported shell type: {shell_type}")
    
    def calculate_overlap_matrix(self, basis_functions: List[BasisFunction]) -> np.ndarray:
        """
        Calculate overlap matrix between basis functions.
        
        Args:
            basis_functions: List of basis functions
            
        Returns:
            Overlap matrix
        """
        n_basis = len(basis_functions)
        overlap_matrix = np.zeros((n_basis, n_basis))
        
        for i, bf_i in enumerate(basis_functions):
            for j, bf_j in enumerate(basis_functions):
                overlap_matrix[i, j] = self._calculate_overlap_integral(bf_i, bf_j)
        
        return overlap_matrix
    
    def _calculate_overlap_integral(self, bf_i: BasisFunction, bf_j: BasisFunction) -> float:
        """
        Calculate overlap integral between two basis functions (simplified).
        
        Args:
            bf_i: First basis function
            bf_j: Second basis function
            
        Returns:
            Overlap integral value
        """
        if bf_i.function_type != bf_j.function_type:
            return 0.0  # Different function types don't overlap
        
        # Simplified overlap calculation for Gaussian functions
        if bf_i.function_type == 'gaussian':
            return self._gaussian_overlap(bf_i, bf_j)
        else:
            return self._slater_overlap(bf_i, bf_j)
    
    def _gaussian_overlap(self, bf_i: BasisFunction, bf_j: BasisFunction) -> float:
        """Calculate overlap between two Gaussian basis functions."""
        # Distance between centers
        R = bf_i.center - bf_j.center
        R_squared = np.dot(R, R)
        
        # Exponents
        alpha_i = bf_i.exponent
        alpha_j = bf_j.exponent
        
        # Angular momentum
        l_i, m_i, n_i = bf_i.angular_momentum
        l_j, m_j, n_j = bf_j.angular_momentum
        
        # Gaussian product theorem
        gamma = alpha_i + alpha_j
        
        # Exponential factor
        exp_factor = np.exp(-alpha_i * alpha_j * R_squared / gamma)
        
        # Angular momentum integrals (simplified)
        if (l_i, m_i, n_i) == (l_j, m_j, n_j) and np.allclose(R, 0):
            # Same function at same center
            angular_factor = 1.0
        elif (l_i, m_i, n_i) == (l_j, m_j, n_j):
            # Same angular momentum, different centers
            angular_factor = np.exp(-R_squared / 4)
        else:
            # Different angular momentum
            angular_factor = 0.1 * np.exp(-R_squared / 2)
        
        # Normalization and coefficients
        overlap = (bf_i.coefficient * bf_j.coefficient * 
                  bf_i.normalization * bf_j.normalization *
                  exp_factor * angular_factor)
        
        return overlap
    
    def _slater_overlap(self, bf_i: BasisFunction, bf_j: BasisFunction) -> float:
        """Calculate overlap between two Slater basis functions (simplified)."""
        # Very simplified Slater overlap calculation
        R = bf_i.center - bf_j.center
        R_magnitude = np.linalg.norm(R)
        
        # Simplified exponential decay with distance
        overlap = (bf_i.coefficient * bf_j.coefficient * 
                  bf_i.normalization * bf_j.normalization *
                  np.exp(-0.5 * (bf_i.exponent + bf_j.exponent) * R_magnitude))
        
        return overlap
    
    def get_basis_set_info(self, basis_set_name: str) -> Dict[str, Any]:
        """
        Get information about a basis set.
        
        Args:
            basis_set_name: Name of the basis set
            
        Returns:
            Dictionary with basis set information
        """
        basis_set = self.get_basis_set(basis_set_name)
        if basis_set is None:
            return {'error': f"Basis set '{basis_set_name}' not found"}
        
        info = {
            'name': basis_set_name,
            'description': basis_set.get('description', 'No description'),
            'type': basis_set.get('type', 'unknown'),
            'supported_elements': list(basis_set.get('elements', {}).keys()),
            'total_elements': len(basis_set.get('elements', {}))
        }
        
        # Count total functions
        total_functions = 0
        for element, element_data in basis_set.get('elements', {}).items():
            for shell in element_data.get('shells', []):
                shell_type = shell['type']
                n_contractions = len(shell.get('exponents', []))
                n_angular = len(self._get_angular_momentum_combinations(shell_type))
                total_functions += n_contractions * n_angular
        
        info['functions_per_element'] = {}
        for element, element_data in basis_set.get('elements', {}).items():
            element_functions = 0
            for shell in element_data.get('shells', []):
                shell_type = shell['type']
                n_contractions = len(shell.get('exponents', []))
                n_angular = len(self._get_angular_momentum_combinations(shell_type))
                element_functions += n_contractions * n_angular
            info['functions_per_element'][element] = element_functions
        
        return info
    
    def count_basis_functions(self, structure: MolecularStructure, 
                            basis_set_name: str) -> Dict[str, Any]:
        """
        Count basis functions for a molecular structure.
        
        Args:
            structure: Molecular structure
            basis_set_name: Name of the basis set
            
        Returns:
            Dictionary with function counts
        """
        basis_set = self.get_basis_set(basis_set_name)
        if basis_set is None:
            return {'error': f"Basis set '{basis_set_name}' not found"}
        
        total_functions = 0
        functions_by_element = {}
        functions_by_atom = []
        
        for i, atom in enumerate(structure.atoms):
            atom_basis = basis_set['elements'].get(atom.symbol)
            if atom_basis is None:
                continue
            
            atom_functions = 0
            for shell in atom_basis['shells']:
                shell_type = shell['type']
                n_contractions = len(shell.get('exponents', []))
                n_angular = len(self._get_angular_momentum_combinations(shell_type))
                atom_functions += n_contractions * n_angular
            
            total_functions += atom_functions
            functions_by_atom.append({
                'atom_index': i,
                'element': atom.symbol,
                'functions': atom_functions
            })
            
            if atom.symbol not in functions_by_element:
                functions_by_element[atom.symbol] = 0
            functions_by_element[atom.symbol] += atom_functions
        
        return {
            'total_functions': total_functions,
            'functions_by_element': functions_by_element,
            'functions_by_atom': functions_by_atom,
            'basis_set': basis_set_name
        }
    
    def add_custom_basis_set(self, name: str, basis_set_data: Dict[str, Any]) -> None:
        """
        Add a custom basis set.
        
        Args:
            name: Name for the basis set
            basis_set_data: Basis set definition
        """
        self.basis_sets[name.lower()] = basis_set_data
    
    def export_basis_functions_xyz(self, basis_functions: List[BasisFunction], 
                                  filename: str) -> None:
        """
        Export basis function centers to XYZ format for visualization.
        
        Args:
            basis_functions: List of basis functions
            filename: Output filename
        """
        with open(filename, 'w') as f:
            f.write(f"{len(basis_functions)}\n")
            f.write("Basis function centers\n")
            
            for i, bf in enumerate(basis_functions):
                x, y, z = bf.center
                l, m, n = bf.angular_momentum
                shell_type = 's' if (l, m, n) == (0, 0, 0) else 'p' if max(l, m, n) == 1 else 'd'
                f.write(f"{shell_type} {x:.6f} {y:.6f} {z:.6f}\n")