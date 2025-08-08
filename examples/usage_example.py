"""
Usage examples for the Chemesty package.
"""

from chemesty.elements.element_factory import ElementFactory
from chemesty.molecules.molecule import Molecule
from chemesty.data.database import MoleculeDatabase

def element_examples():
    """Examples of working with elements."""
    print("=== Element Examples ===")
    
    # Get elements by symbol
    H = ElementFactory.get_element("H")
    O = ElementFactory.get_element("O")
    C = ElementFactory.get_element("C")
    
    # Get elements by atomic number
    iron = ElementFactory.get_element_by_number(26)
    gold = ElementFactory.get_element_by_number(79)
    
    # Print element information
    print(f"Hydrogen: {H}")
    print(f"Atomic number: {H.atomic_number}")
    print(f"Atomic mass: {H.atomic_mass}")
    print(f"Electron configuration: {H.electron_configuration}")
    print(f"Electron shells: {H.electron_shells}")
    print(f"Electronegativity: {H.electronegativity}")
    print(f"Atomic radius: {H.atomic_radius} pm")
    print(f"Density: {H.density_value} g/cm³")
    print(f"Volume: {H.volume_value:.2f} Å³")
    print(f"Is metal: {H.is_metal()}")
    print()
    
    print(f"Iron: {iron}")
    print(f"Symbol: {iron.symbol}")
    print(f"Atomic mass: {iron.atomic_mass}")
    print(f"Category: {iron.category}")
    print(f"Is metal: {iron.is_metal()}")
    print()
    
    print(f"Gold: {gold}")
    print(f"Symbol: {gold.symbol}")
    print(f"Atomic mass: {gold.atomic_mass}")
    print(f"Density: {gold.density_value} g/cm³")
    print(f"Is metal: {gold.is_metal()}")
    print()

def molecule_examples():
    """Examples of working with molecules."""
    print("=== Molecule Examples ===")
    
    # Get elements
    H = ElementFactory.get_element("H")
    O = ElementFactory.get_element("O")
    C = ElementFactory.get_element("C")
    
    # Create water molecule using addition and multiplication
    water = 2 * H + O
    print(f"Water: {water}")
    print(f"Molecular formula: {water.molecular_formula}")
    print(f"Molecular weight: {water.molecular_weight:.3f}")
    print(f"Elements: {[(e.symbol, count) for e, count in water.elements.items()]}")
    print()
    
    # Create methane molecule
    methane = C + 4 * H
    print(f"Methane: {methane}")
    print(f"Molecular formula: {methane.molecular_formula}")
    print(f"Molecular weight: {methane.molecular_weight:.3f}")
    print()
    
    # Create glucose molecule
    glucose = 6 * C + 12 * H + 6 * O
    print(f"Glucose: {glucose}")
    print(f"Molecular formula: {glucose.molecular_formula}")
    print(f"Empirical formula: {glucose.empirical_formula}")
    print(f"Molecular weight: {glucose.molecular_weight:.3f}")
    print(f"Element count: {glucose.element_count}")
    print(f"Atom count: {glucose.atom_count}")
    print()
    
    # Create molecule from formula
    ethanol = Molecule(formula="C2H6O")
    print(f"Ethanol: {ethanol}")
    print(f"Molecular formula: {ethanol.molecular_formula}")
    print(f"Molecular weight: {ethanol.molecular_weight:.3f}")
    print()
    
    # Create molecule from SMILES
    aspirin = Molecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O")
    print(f"Aspirin: {aspirin}")
    print(f"Molecular formula: {aspirin.molecular_formula}")
    print(f"Molecular weight: {aspirin.molecular_weight:.3f}")
    print()

def database_examples():
    """Examples of working with the molecule database."""
    print("=== Database Examples ===")
    print("Note: These examples require a downloaded database.")
    print("Run 'python -m chemesty.data.download' to download the database first.")
    print()
    
    try:
        # Initialize the database
        db = MoleculeDatabase()
        
        # Search by formula
        print("Searching for molecules with formula C6H12O6...")
        results = db.search_by_formula("C6H12O6")
        print(f"Found {len(results)} molecules")
        for i, (mol_id, name, smiles) in enumerate(results[:5]):
            print(f"{i+1}. {name} (ID: {mol_id})")
        print()
        
        # Search by name
        print("Searching for molecules with 'aspirin' in the name...")
        results = db.search_by_name("aspirin")
        print(f"Found {len(results)} molecules")
        for i, (mol_id, name, smiles) in enumerate(results[:5]):
            print(f"{i+1}. {name} (ID: {mol_id})")
        print()
        
        # Search by molecular weight
        print("Searching for molecules with molecular weight around 180.16...")
        results = db.search_by_molecular_weight(180.16, tolerance=0.1)
        print(f"Found {len(results)} molecules")
        for i, (mol_id, name, smiles, mw) in enumerate(results[:5]):
            print(f"{i+1}. {name} (ID: {mol_id}, MW: {mw:.3f})")
        print()
        
        # Close the database
        db.close()
    except Exception as e:
        print(f"Error accessing database: {e}")
        print("Make sure to download the database first using 'python -m chemesty.data.download'")

if __name__ == "__main__":
    print("Chemesty Package Usage Examples")
    print("==============================")
    print()
    
    element_examples()
    print()
    
    molecule_examples()
    print()
    
    database_examples()