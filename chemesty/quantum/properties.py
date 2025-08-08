"""
Quantum mechanical property calculations.

This module provides tools for calculating various quantum mechanical
properties from electronic structure calculations.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import math
from chemesty.molecules.file_formats import MolecularStructure, Atom


class QuantumProperties:
    """
    Calculator for quantum mechanical properties.
    
    This class provides methods for calculating various quantum mechanical
    properties from electronic structure data.
    """
    
    def __init__(self, structure: MolecularStructure, calculation_results: Dict[str, Any]):
        """
        Initialize quantum properties calculator.
        
        Args:
            structure: Molecular structure
            calculation_results: Results from quantum chemistry calculation
        """
        self.structure = structure
        self.results = calculation_results
        
        # Physical constants
        self.bohr_to_angstrom = 0.529177
        self.hartree_to_ev = 27.211
        self.debye_to_au = 0.393456
        self.speed_of_light = 137.036  # in atomic units
    
    def calculate_dipole_moment(self, method: str = 'mulliken') -> Dict[str, Any]:
        """
        Calculate electric dipole moment.
        
        Args:
            method: Method for calculating dipole moment ('mulliken', 'esp')
            
        Returns:
            Dictionary with dipole moment information
        """
        if method == 'mulliken':
            dipole = self._calculate_mulliken_dipole()
        elif method == 'esp':
            dipole = self._calculate_esp_dipole()
        else:
            raise ValueError(f"Unknown dipole calculation method: {method}")
        
        # Calculate magnitude
        magnitude = np.linalg.norm(dipole)
        
        # Convert to Debye
        magnitude_debye = magnitude / self.debye_to_au
        
        return {
            'method': method,
            'dipole_vector': dipole.tolist(),
            'magnitude_au': magnitude,
            'magnitude_debye': magnitude_debye,
            'x_component': dipole[0],
            'y_component': dipole[1],
            'z_component': dipole[2]
        }
    
    def _calculate_mulliken_dipole(self) -> np.ndarray:
        """Calculate dipole moment using Mulliken population analysis."""
        dipole = np.array([0.0, 0.0, 0.0])
        
        # Nuclear contribution
        for atom in self.structure.atoms:
            atomic_numbers = {
                'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
                'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20
            }
            charge = atomic_numbers.get(atom.symbol, 1)
            position = np.array([atom.x, atom.y, atom.z])
            dipole += charge * position
        
        # Electronic contribution (simplified)
        # In a real implementation, this would use the density matrix
        center_of_charge = self._calculate_electronic_center()
        n_electrons = self.results.get('n_electrons', 0)
        dipole -= n_electrons * center_of_charge
        
        return dipole
    
    def _calculate_esp_dipole(self) -> np.ndarray:
        """Calculate dipole moment using electrostatic potential fitting."""
        # Simplified ESP-based dipole calculation
        return self._calculate_mulliken_dipole() * 1.1  # Rough correction factor
    
    def _calculate_electronic_center(self) -> np.ndarray:
        """Calculate center of electronic charge (simplified)."""
        center = np.array([0.0, 0.0, 0.0])
        total_weight = 0.0
        
        for atom in self.structure.atoms:
            # Weight by number of electrons
            atomic_numbers = {
                'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
                'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20
            }
            weight = atomic_numbers.get(atom.symbol, 1)
            position = np.array([atom.x, atom.y, atom.z])
            
            center += weight * position
            total_weight += weight
        
        if total_weight > 0:
            center /= total_weight
        
        return center
    
    def calculate_polarizability(self) -> Dict[str, Any]:
        """
        Calculate molecular polarizability (simplified estimation).
        
        Returns:
            Dictionary with polarizability information
        """
        # Very simplified polarizability calculation
        # Real implementation would require response calculations
        
        volume = self._estimate_molecular_volume()
        n_electrons = self.results.get('n_electrons', 0)
        
        # Rough estimation based on molecular volume and electron count
        alpha_iso = 0.1 * volume + 0.05 * n_electrons
        
        # Estimate anisotropy (simplified)
        alpha_xx = alpha_iso * (1.0 + 0.1 * np.random.normal())
        alpha_yy = alpha_iso * (1.0 + 0.1 * np.random.normal())
        alpha_zz = alpha_iso * (1.0 + 0.1 * np.random.normal())
        
        alpha_tensor = np.array([
            [alpha_xx, 0.0, 0.0],
            [0.0, alpha_yy, 0.0],
            [0.0, 0.0, alpha_zz]
        ])
        
        return {
            'isotropic_polarizability': alpha_iso,
            'polarizability_tensor': alpha_tensor.tolist(),
            'alpha_xx': alpha_xx,
            'alpha_yy': alpha_yy,
            'alpha_zz': alpha_zz,
            'anisotropy': np.std([alpha_xx, alpha_yy, alpha_zz])
        }
    
    def calculate_hyperpolarizability(self) -> Dict[str, Any]:
        """
        Calculate first hyperpolarizability (simplified estimation).
        
        Returns:
            Dictionary with hyperpolarizability information
        """
        # Very simplified hyperpolarizability calculation
        polarizability = self.calculate_polarizability()
        alpha_iso = polarizability['isotropic_polarizability']
        
        # Rough estimation
        beta_iso = 0.01 * alpha_iso**1.5
        
        return {
            'isotropic_hyperpolarizability': beta_iso,
            'method': 'simplified_estimation'
        }
    
    def calculate_ionization_potential(self) -> Dict[str, Any]:
        """
        Calculate ionization potential using Koopmans' theorem.
        
        Returns:
            Dictionary with ionization potential information
        """
        homo_energy = self.results.get('homo_energy')
        
        if homo_energy is None:
            return {'error': 'HOMO energy not available'}
        
        # Koopmans' theorem: IP = -E_HOMO
        ip_koopmans = -homo_energy
        
        # Estimate relaxation correction (simplified)
        relaxation_correction = 0.1 * abs(homo_energy)
        ip_corrected = ip_koopmans - relaxation_correction
        
        return {
            'koopmans_ip': ip_koopmans,
            'corrected_ip': ip_corrected,
            'relaxation_correction': relaxation_correction,
            'homo_energy': homo_energy,
            'method': 'koopmans_theorem'
        }
    
    def calculate_electron_affinity(self) -> Dict[str, Any]:
        """
        Calculate electron affinity using Koopmans' theorem.
        
        Returns:
            Dictionary with electron affinity information
        """
        lumo_energy = self.results.get('lumo_energy')
        
        if lumo_energy is None:
            return {'error': 'LUMO energy not available'}
        
        # Koopmans' theorem: EA = -E_LUMO
        ea_koopmans = -lumo_energy
        
        # Estimate relaxation correction (simplified)
        relaxation_correction = 0.1 * abs(lumo_energy)
        ea_corrected = ea_koopmans + relaxation_correction
        
        return {
            'koopmans_ea': ea_koopmans,
            'corrected_ea': ea_corrected,
            'relaxation_correction': relaxation_correction,
            'lumo_energy': lumo_energy,
            'method': 'koopmans_theorem'
        }
    
    def calculate_chemical_hardness(self) -> Dict[str, Any]:
        """
        Calculate chemical hardness and related descriptors.
        
        Returns:
            Dictionary with chemical hardness information
        """
        ip_result = self.calculate_ionization_potential()
        ea_result = self.calculate_electron_affinity()
        
        if 'error' in ip_result or 'error' in ea_result:
            return {'error': 'Cannot calculate hardness without IP and EA'}
        
        ip = ip_result['corrected_ip']
        ea = ea_result['corrected_ea']
        
        # Chemical hardness: η = (IP - EA) / 2
        hardness = (ip - ea) / 2
        
        # Chemical potential: μ = -(IP + EA) / 2
        chemical_potential = -(ip + ea) / 2
        
        # Electronegativity (Mulliken): χ = (IP + EA) / 2
        electronegativity = (ip + ea) / 2
        
        # Softness: S = 1 / (2η)
        softness = 1 / (2 * hardness) if hardness != 0 else float('inf')
        
        return {
            'chemical_hardness': hardness,
            'chemical_potential': chemical_potential,
            'electronegativity_mulliken': electronegativity,
            'softness': softness,
            'ionization_potential': ip,
            'electron_affinity': ea
        }
    
    def calculate_fukui_functions(self) -> Dict[str, Any]:
        """
        Calculate Fukui functions (simplified estimation).
        
        Returns:
            Dictionary with Fukui function information
        """
        # Simplified Fukui function calculation
        # Real implementation would require finite difference calculations
        
        homo_energy = self.results.get('homo_energy', 0)
        lumo_energy = self.results.get('lumo_energy', 0)
        
        # Estimate Fukui functions based on frontier orbital energies
        f_plus = abs(lumo_energy) / (abs(homo_energy) + abs(lumo_energy) + 1e-6)
        f_minus = abs(homo_energy) / (abs(homo_energy) + abs(lumo_energy) + 1e-6)
        f_zero = (f_plus + f_minus) / 2
        
        return {
            'f_plus': f_plus,      # Nucleophilic attack
            'f_minus': f_minus,    # Electrophilic attack
            'f_zero': f_zero,      # Radical attack
            'method': 'frontier_orbital_approximation'
        }
    
    def calculate_nmr_shieldings(self) -> Dict[str, Any]:
        """
        Calculate NMR chemical shieldings (simplified estimation).
        
        Returns:
            Dictionary with NMR shielding information
        """
        shieldings = {}
        
        for i, atom in enumerate(self.structure.atoms):
            # Very simplified shielding calculation
            # Real implementation would require GIAO or similar methods
            
            if atom.symbol == 'H':
                # Typical proton shielding range
                base_shielding = 30.0
                environment_factor = self._estimate_chemical_environment(i)
                shielding = base_shielding + environment_factor * 5.0
            elif atom.symbol == 'C':
                # Typical carbon shielding range
                base_shielding = 180.0
                environment_factor = self._estimate_chemical_environment(i)
                shielding = base_shielding + environment_factor * 20.0
            else:
                # Default for other atoms
                base_shielding = 100.0
                environment_factor = self._estimate_chemical_environment(i)
                shielding = base_shielding + environment_factor * 10.0
            
            shieldings[f'{atom.symbol}_{i+1}'] = {
                'atom_index': i,
                'atom_symbol': atom.symbol,
                'shielding_ppm': shielding,
                'chemical_shift_ppm': self._shielding_to_chemical_shift(atom.symbol, shielding)
            }
        
        return {
            'method': 'simplified_estimation',
            'shieldings': shieldings
        }
    
    def _estimate_chemical_environment(self, atom_index: int) -> float:
        """Estimate chemical environment factor for an atom."""
        if atom_index >= len(self.structure.atoms):
            return 0.0
        
        atom = self.structure.atoms[atom_index]
        environment_factor = 0.0
        
        # Consider nearby atoms
        for i, other_atom in enumerate(self.structure.atoms):
            if i == atom_index:
                continue
            
            distance = np.sqrt(
                (atom.x - other_atom.x)**2 +
                (atom.y - other_atom.y)**2 +
                (atom.z - other_atom.z)**2
            )
            
            if distance < 3.0:  # Within 3 Angstroms
                # Electronegativity effect
                electronegativity = {
                    'H': 2.20, 'C': 2.55, 'N': 3.04, 'O': 3.44, 'F': 3.98,
                    'Cl': 3.16, 'Br': 2.96, 'I': 2.66, 'S': 2.58, 'P': 2.19
                }
                
                other_en = electronegativity.get(other_atom.symbol, 2.5)
                atom_en = electronegativity.get(atom.symbol, 2.5)
                
                # Distance-weighted electronegativity difference
                weight = 1.0 / (distance + 0.1)
                environment_factor += weight * (other_en - atom_en)
        
        return environment_factor
    
    def _shielding_to_chemical_shift(self, atom_symbol: str, shielding: float) -> float:
        """Convert shielding to chemical shift using reference values."""
        # Reference shieldings (simplified)
        references = {
            'H': 31.8,    # TMS reference
            'C': 182.1,   # TMS reference
            'N': 244.0,   # Nitromethane reference
            'O': 287.0,   # Water reference
            'F': 188.0,   # CFCl3 reference
            'P': 266.0    # 85% H3PO4 reference
        }
        
        reference = references.get(atom_symbol, 0.0)
        return reference - shielding
    
    def _estimate_molecular_volume(self) -> float:
        """Estimate molecular volume."""
        if not self.structure.atoms:
            return 0.0
        
        # Simple estimation based on van der Waals radii
        vdw_radii = {
            'H': 1.20, 'C': 1.70, 'N': 1.55, 'O': 1.52, 'F': 1.47,
            'Cl': 1.75, 'Br': 1.85, 'I': 1.98, 'P': 1.80, 'S': 1.80
        }
        
        total_volume = 0.0
        for atom in self.structure.atoms:
            radius = vdw_radii.get(atom.symbol, 1.5)
            volume = (4/3) * np.pi * radius**3
            total_volume += volume
        
        # Apply packing factor for molecular volume
        packing_factor = 0.74  # Face-centered cubic packing
        return total_volume * packing_factor
    
    def calculate_vibrational_frequencies(self) -> Dict[str, Any]:
        """
        Calculate vibrational frequencies (simplified estimation).
        
        Returns:
            Dictionary with vibrational frequency information
        """
        n_atoms = len(self.structure.atoms)
        n_modes = 3 * n_atoms - 6  # Non-linear molecule
        
        if n_atoms == 2:
            n_modes = 1  # Diatomic molecule
        elif n_atoms == 1:
            n_modes = 0  # Atomic
        
        # Generate simplified vibrational frequencies
        frequencies = []
        
        for i in range(n_modes):
            # Rough estimation based on bond types and masses
            if i < n_atoms - 1:  # Stretching modes
                base_freq = 3000.0  # cm^-1
                variation = np.random.normal(0, 500)
                freq = max(500, base_freq + variation)
            else:  # Bending modes
                base_freq = 1500.0  # cm^-1
                variation = np.random.normal(0, 300)
                freq = max(200, base_freq + variation)
            
            frequencies.append(freq)
        
        frequencies.sort(reverse=True)
        
        # Calculate zero-point energy
        zpe = sum(frequencies) * 0.5 * 1.44e-4  # Convert to eV
        
        return {
            'frequencies_cm1': frequencies,
            'n_modes': n_modes,
            'zero_point_energy_ev': zpe,
            'method': 'simplified_estimation'
        }
    
    def calculate_thermodynamic_properties(self, temperature: float = 298.15) -> Dict[str, Any]:
        """
        Calculate thermodynamic properties at given temperature.
        
        Args:
            temperature: Temperature in Kelvin
            
        Returns:
            Dictionary with thermodynamic properties
        """
        # Get vibrational frequencies
        vib_result = self.calculate_vibrational_frequencies()
        frequencies = vib_result['frequencies_cm1']
        
        # Constants
        kb = 8.617e-5  # Boltzmann constant in eV/K
        h = 4.136e-15  # Planck constant in eV·s
        c = 2.998e10   # Speed of light in cm/s
        
        # Calculate partition functions and thermodynamic quantities
        # Electronic contribution (ground state)
        q_elec = 1.0
        
        # Translational contribution (ideal gas)
        mass = self._estimate_molecular_mass()  # in amu
        mass_kg = mass * 1.66054e-27  # Convert to kg
        
        # Rotational contribution (simplified)
        q_rot = temperature  # Very simplified
        
        # Vibrational contribution
        q_vib = 1.0
        u_vib = 0.0  # Internal energy
        cv_vib = 0.0  # Heat capacity
        
        for freq in frequencies:
            if freq > 0:
                theta_vib = h * c * freq / kb  # Vibrational temperature
                x = theta_vib / temperature
                
                if x < 50:  # Avoid overflow
                    exp_x = np.exp(x)
                    q_vib *= 1.0 / (1.0 - np.exp(-x))
                    u_vib += theta_vib / (exp_x - 1.0)
                    cv_vib += x**2 * exp_x / (exp_x - 1.0)**2
        
        u_vib *= kb
        cv_vib *= kb
        
        # Total internal energy
        u_total = 1.5 * kb * temperature + u_vib  # Translational + vibrational
        
        # Heat capacity
        cv_total = 1.5 * kb + cv_vib  # Translational + vibrational
        cp_total = cv_total + kb  # Cp = Cv + R for ideal gas
        
        # Entropy (simplified)
        s_total = kb * (np.log(q_elec * q_rot * q_vib) + 1.5 * np.log(temperature))
        
        return {
            'temperature_k': temperature,
            'internal_energy_ev': u_total,
            'heat_capacity_cv_ev_k': cv_total,
            'heat_capacity_cp_ev_k': cp_total,
            'entropy_ev_k': s_total,
            'zero_point_energy_ev': vib_result['zero_point_energy_ev'],
            'method': 'ideal_gas_approximation'
        }
    
    def _estimate_molecular_mass(self) -> float:
        """Estimate molecular mass in amu."""
        atomic_masses = {
            'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
            'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
            'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
            'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078
        }
        
        total_mass = 0.0
        for atom in self.structure.atoms:
            mass = atomic_masses.get(atom.symbol, 12.0)  # Default to carbon
            total_mass += mass
        
        return total_mass
    
    def get_property_summary(self) -> Dict[str, Any]:
        """
        Get summary of all calculated properties.
        
        Returns:
            Dictionary with property summary
        """
        summary = {}
        
        try:
            summary['dipole_moment'] = self.calculate_dipole_moment()
        except Exception as e:
            summary['dipole_moment'] = {'error': str(e)}
        
        try:
            summary['polarizability'] = self.calculate_polarizability()
        except Exception as e:
            summary['polarizability'] = {'error': str(e)}
        
        try:
            summary['ionization_potential'] = self.calculate_ionization_potential()
        except Exception as e:
            summary['ionization_potential'] = {'error': str(e)}
        
        try:
            summary['electron_affinity'] = self.calculate_electron_affinity()
        except Exception as e:
            summary['electron_affinity'] = {'error': str(e)}
        
        try:
            summary['chemical_hardness'] = self.calculate_chemical_hardness()
        except Exception as e:
            summary['chemical_hardness'] = {'error': str(e)}
        
        try:
            summary['thermodynamic_properties'] = self.calculate_thermodynamic_properties()
        except Exception as e:
            summary['thermodynamic_properties'] = {'error': str(e)}
        
        return summary