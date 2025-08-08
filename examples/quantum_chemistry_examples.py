"""
Quantum Chemistry Examples for Chemesty.

This module demonstrates how to use Chemesty's quantum chemistry capabilities
including orbital calculations, basis sets, and molecular properties.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chemesty.molecules.molecule import Molecule
from chemesty.utils.progress import progress_context, molecule_progress
from chemesty.utils.errors import with_error_handling, QuantumError

try:
    from chemesty.quantum.orbitals import MolecularOrbitals
    from chemesty.quantum.basis_sets import BasisSetManager
    from chemesty.quantum.properties import QuantumProperties
    QUANTUM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Quantum chemistry modules not available: {e}")
    print("Some examples will be skipped.")
    QUANTUM_AVAILABLE = False


@with_error_handling("quantum orbital calculation")
def orbital_examples():
    """Examples of molecular orbital calculations."""
    print("=== Molecular Orbital Examples ===")
    
    if not QUANTUM_AVAILABLE:
        print("Quantum chemistry modules not available. Skipping orbital examples.")
        return
    
    # Create simple molecules
    molecules = [
        Molecule(formula="H2"),
        Molecule(formula="H2O"),
        Molecule(formula="CH4"),
        Molecule(formula="NH3")
    ]
    
    print("Calculating molecular orbitals for various molecules...")
    
    with progress_context(total=len(molecules), desc="Calculating orbitals", unit="molecules") as progress:
        for mol in molecules:
            try:
                # Create molecular orbital calculator
                mo_calc = MolecularOrbitals(mol)
                
                # Calculate orbitals with different basis sets
                print(f"\n{mol.molecular_formula}:")
                
                # STO-3G basis set (minimal)
                mo_calc.set_basis_set("STO-3G")
                homo_lumo = mo_calc.calculate_homo_lumo()
                
                if homo_lumo:
                    homo_energy, lumo_energy = homo_lumo
                    gap = lumo_energy - homo_energy
                    print(f"  STO-3G basis:")
                    print(f"    HOMO energy: {homo_energy:.4f} eV")
                    print(f"    LUMO energy: {lumo_energy:.4f} eV")
                    print(f"    HOMO-LUMO gap: {gap:.4f} eV")
                
                # 6-31G basis set (larger)
                try:
                    mo_calc.set_basis_set("6-31G")
                    homo_lumo_631g = mo_calc.calculate_homo_lumo()
                    
                    if homo_lumo_631g:
                        homo_631g, lumo_631g = homo_lumo_631g
                        gap_631g = lumo_631g - homo_631g
                        print(f"  6-31G basis:")
                        print(f"    HOMO energy: {homo_631g:.4f} eV")
                        print(f"    LUMO energy: {lumo_631g:.4f} eV")
                        print(f"    HOMO-LUMO gap: {gap_631g:.4f} eV")
                except Exception as e:
                    print(f"    6-31G calculation failed: {e}")
                
                # Get orbital information
                orbital_info = mo_calc.get_orbital_info()
                if orbital_info:
                    print(f"  Total orbitals: {orbital_info.get('total_orbitals', 'N/A')}")
                    print(f"  Occupied orbitals: {orbital_info.get('occupied_orbitals', 'N/A')}")
                
            except Exception as e:
                print(f"  Error calculating orbitals for {mol.molecular_formula}: {e}")
            
            progress.update(1)


@with_error_handling("basis set management")
def basis_set_examples():
    """Examples of working with basis sets."""
    print("\n=== Basis Set Examples ===")
    
    if not QUANTUM_AVAILABLE:
        print("Quantum chemistry modules not available. Skipping basis set examples.")
        return
    
    # Create basis set manager
    basis_manager = BasisSetManager()
    
    # List available basis sets
    available_sets = basis_manager.list_available_basis_sets()
    print("Available basis sets:")
    for basis_set in available_sets[:10]:  # Show first 10
        print(f"  - {basis_set}")
    
    if len(available_sets) > 10:
        print(f"  ... and {len(available_sets) - 10} more")
    
    # Get information about specific basis sets
    common_basis_sets = ["STO-3G", "6-31G", "6-31G*", "cc-pVDZ"]
    
    print("\nBasis set information:")
    for basis_name in common_basis_sets:
        try:
            info = basis_manager.get_basis_set_info(basis_name)
            if info:
                print(f"  {basis_name}:")
                print(f"    Description: {info.get('description', 'N/A')}")
                print(f"    Type: {info.get('type', 'N/A')}")
                print(f"    Elements supported: {len(info.get('elements', []))} elements")
        except Exception as e:
            print(f"  {basis_name}: Information not available ({e})")
    
    # Demonstrate basis set selection for different elements
    print("\nBasis set recommendations:")
    elements = ["H", "C", "N", "O", "F"]
    
    for element in elements:
        try:
            recommended = basis_manager.recommend_basis_set(element, accuracy="medium")
            print(f"  {element}: {recommended}")
        except Exception as e:
            print(f"  {element}: No recommendation available ({e})")


@with_error_handling("quantum property calculation")
def quantum_properties_examples():
    """Examples of calculating quantum properties."""
    print("\n=== Quantum Properties Examples ===")
    
    if not QUANTUM_AVAILABLE:
        print("Quantum chemistry modules not available. Skipping property examples.")
        return
    
    # Create molecules for property calculations
    molecules = [
        ("Water", Molecule(formula="H2O")),
        ("Methane", Molecule(formula="CH4")),
        ("Ammonia", Molecule(formula="NH3")),
        ("Carbon dioxide", Molecule(formula="CO2"))
    ]
    
    print("Calculating quantum properties...")
    
    with progress_context(total=len(molecules), desc="Calculating properties", unit="molecules") as progress:
        for name, mol in molecules:
            try:
                print(f"\n{name} ({mol.molecular_formula}):")
                
                # Create quantum properties calculator
                qp_calc = QuantumProperties(mol)
                
                # Calculate dipole moment
                try:
                    dipole = qp_calc.calculate_dipole_moment()
                    if dipole is not None:
                        print(f"  Dipole moment: {dipole:.4f} Debye")
                except Exception as e:
                    print(f"  Dipole moment: Calculation failed ({e})")
                
                # Calculate polarizability
                try:
                    polarizability = qp_calc.calculate_polarizability()
                    if polarizability is not None:
                        print(f"  Polarizability: {polarizability:.4f} Å³")
                except Exception as e:
                    print(f"  Polarizability: Calculation failed ({e})")
                
                # Calculate ionization potential
                try:
                    ip = qp_calc.calculate_ionization_potential()
                    if ip is not None:
                        print(f"  Ionization potential: {ip:.4f} eV")
                except Exception as e:
                    print(f"  Ionization potential: Calculation failed ({e})")
                
                # Calculate electron affinity
                try:
                    ea = qp_calc.calculate_electron_affinity()
                    if ea is not None:
                        print(f"  Electron affinity: {ea:.4f} eV")
                except Exception as e:
                    print(f"  Electron affinity: Calculation failed ({e})")
                
                # Calculate molecular volume
                try:
                    volume = qp_calc.calculate_molecular_volume()
                    if volume is not None:
                        print(f"  Molecular volume: {volume:.2f} Å³")
                except Exception as e:
                    print(f"  Molecular volume: Calculation failed ({e})")
                
            except Exception as e:
                print(f"  Error calculating properties for {name}: {e}")
            
            progress.update(1)


def energy_calculation_examples():
    """Examples of energy calculations."""
    print("\n=== Energy Calculation Examples ===")
    
    if not QUANTUM_AVAILABLE:
        print("Quantum chemistry modules not available. Skipping energy examples.")
        return
    
    # Simple molecules for energy comparison
    molecules = [
        ("Hydrogen", Molecule(formula="H2")),
        ("Water", Molecule(formula="H2O")),
        ("Methane", Molecule(formula="CH4"))
    ]
    
    print("Comparing energies with different methods...")
    
    methods = ["HF", "DFT", "MP2"]  # Different quantum methods
    
    for name, mol in molecules:
        print(f"\n{name} ({mol.molecular_formula}):")
        
        for method in methods:
            try:
                # This would use the quantum chemistry backend
                # In a real implementation, this would interface with PySCF or similar
                print(f"  {method} method: Calculation would be performed here")
                # energy = calculate_energy(mol, method=method, basis="6-31G")
                # print(f"  {method} energy: {energy:.6f} Hartree")
            except Exception as e:
                print(f"  {method} method: Not available ({e})")


def advanced_quantum_examples():
    """Examples of advanced quantum chemistry features."""
    print("\n=== Advanced Quantum Chemistry Examples ===")
    
    if not QUANTUM_AVAILABLE:
        print("Quantum chemistry modules not available. Skipping advanced examples.")
        return
    
    print("Advanced features (conceptual examples):")
    
    # Geometry optimization example
    print("\n1. Geometry Optimization:")
    print("   - Start with initial molecular geometry")
    print("   - Optimize structure to find minimum energy conformation")
    print("   - Calculate vibrational frequencies")
    print("   - Verify that structure is a true minimum (no imaginary frequencies)")
    
    # Transition state search
    print("\n2. Transition State Search:")
    print("   - Define reaction coordinate")
    print("   - Search for saddle point on potential energy surface")
    print("   - Calculate activation energy")
    print("   - Perform intrinsic reaction coordinate (IRC) calculations")
    
    # Excited state calculations
    print("\n3. Excited State Calculations:")
    print("   - Calculate electronic excitation energies")
    print("   - Determine oscillator strengths")
    print("   - Predict UV-Vis absorption spectrum")
    print("   - Calculate fluorescence properties")
    
    # Solvent effects
    print("\n4. Solvent Effects:")
    print("   - Use polarizable continuum model (PCM)")
    print("   - Calculate solvation energies")
    print("   - Compare gas phase vs. solution properties")
    print("   - Model specific solvent interactions")


def main():
    """Run all quantum chemistry examples."""
    print("Chemesty Quantum Chemistry Examples")
    print("==================================")
    
    if not QUANTUM_AVAILABLE:
        print("\n⚠️  Note: Quantum chemistry modules are not fully available.")
        print("Install additional dependencies for full functionality:")
        print("  pip install pyscf openmm")
        print()
    
    try:
        orbital_examples()
        basis_set_examples()
        quantum_properties_examples()
        energy_calculation_examples()
        advanced_quantum_examples()
        
        print("\n✅ Quantum chemistry examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error running quantum chemistry examples: {e}")
        print("This may be due to missing dependencies or configuration issues.")


if __name__ == "__main__":
    main()