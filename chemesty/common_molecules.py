"""
Script to add common molecules to the database.

This script creates a database of common molecules including CO2, NaCl, MgCl2, etc.
"""

from chemesty.data.database import MoleculeDatabase

# Define common molecules with their properties
# Format: name, SMILES, formula, molecular_weight
COMMON_MOLECULES = [
    # Basic Inorganic Compounds - Common in General Chemistry
    {
        'name': 'Carbon Dioxide',
        'smiles': 'O=C=O',
        'formula': 'CO2',
        'molecular_weight': 44.01,
        'num_atoms': 3
    },
    {
        'name': 'Sodium Chloride',
        'smiles': '[Na+].[Cl-]',
        'formula': 'NaCl',
        'molecular_weight': 58.44,
        'num_atoms': 2
    },
    {
        'name': 'Magnesium Chloride',
        'smiles': '[Mg+2].[Cl-].[Cl-]',
        'formula': 'MgCl2',
        'molecular_weight': 95.21,
        'num_atoms': 3
    },
    {
        'name': 'Water',
        'smiles': 'O',
        'formula': 'H2O',
        'molecular_weight': 18.02,
        'num_atoms': 3
    },
    {
        'name': 'Ammonia',
        'smiles': 'N',
        'formula': 'NH3',
        'molecular_weight': 17.03,
        'num_atoms': 4
    },
    {
        'name': 'Methane',
        'smiles': 'C',
        'formula': 'CH4',
        'molecular_weight': 16.04,
        'num_atoms': 5
    },
    {
        'name': 'Hydrogen Peroxide',
        'smiles': 'OO',
        'formula': 'H2O2',
        'molecular_weight': 34.01,
        'num_atoms': 4
    },
    {
        'name': 'Calcium Carbonate',
        'smiles': '[Ca+2].[C+0]([O-])([O-])=O',
        'formula': 'CaCO3',
        'molecular_weight': 100.09,
        'num_atoms': 5
    },
    {
        'name': 'Potassium Chloride',
        'smiles': '[K+].[Cl-]',
        'formula': 'KCl',
        'molecular_weight': 74.55,
        'num_atoms': 2
    },
    {
        'name': 'Sulfuric Acid',
        'smiles': 'O=S(=O)(O)O',
        'formula': 'H2SO4',
        'molecular_weight': 98.08,
        'num_atoms': 7
    },
    {
        'name': 'Nitric Acid',
        'smiles': 'O=[N+]([O-])O',
        'formula': 'HNO3',
        'molecular_weight': 63.01,
        'num_atoms': 5
    },
    {
        'name': 'Hydrochloric Acid',
        'smiles': '[H+].[Cl-]',
        'formula': 'HCl',
        'molecular_weight': 36.46,
        'num_atoms': 2
    },
    {
        'name': 'Sodium Hydroxide',
        'smiles': '[Na+].[OH-]',
        'formula': 'NaOH',
        'molecular_weight': 40.00,
        'num_atoms': 3
    },
    {
        'name': 'Calcium Oxide',
        'smiles': '[Ca+2].[O-2]',
        'formula': 'CaO',
        'molecular_weight': 56.08,
        'num_atoms': 2
    },
    {
        'name': 'Magnesium Oxide',
        'smiles': '[Mg+2].[O-2]',
        'formula': 'MgO',
        'molecular_weight': 40.30,
        'num_atoms': 2
    },
    
    # Additional Inorganic Compounds - Common in Exams
    {
        'name': 'Ammonium Chloride',
        'smiles': '[NH4+].[Cl-]',
        'formula': 'NH4Cl',
        'molecular_weight': 53.49,
        'num_atoms': 6
    },
    {
        'name': 'Potassium Permanganate',
        'smiles': '[K+].[Mn+7].[O-].[O-].[O-].[O-]',
        'formula': 'KMnO4',
        'molecular_weight': 158.03,
        'num_atoms': 6
    },
    {
        'name': 'Sodium Carbonate',
        'smiles': '[Na+].[Na+].[C+0]([O-])([O-])=O',
        'formula': 'Na2CO3',
        'molecular_weight': 105.99,
        'num_atoms': 6
    },
    {
        'name': 'Potassium Dichromate',
        'smiles': '[K+].[K+].[Cr+6].[Cr+6].[O-].[O-].[O-].[O-].[O-].[O-].[O-]',
        'formula': 'K2Cr2O7',
        'molecular_weight': 294.18,
        'num_atoms': 11
    },
    {
        'name': 'Copper Sulfate',
        'smiles': '[Cu+2].[O-]S(=O)(=O)[O-]',
        'formula': 'CuSO4',
        'molecular_weight': 159.61,
        'num_atoms': 6
    },
    {
        'name': 'Phosphoric Acid',
        'smiles': 'O=P(O)(O)O',
        'formula': 'H3PO4',
        'molecular_weight': 97.99,
        'num_atoms': 8
    },
    {
        'name': 'Sodium Bicarbonate',
        'smiles': '[Na+].[O]C([O-])=O',
        'formula': 'NaHCO3',
        'molecular_weight': 84.01,
        'num_atoms': 6
    },
    {
        'name': 'Calcium Hydroxide',
        'smiles': '[Ca+2].[OH-].[OH-]',
        'formula': 'Ca(OH)2',
        'molecular_weight': 74.09,
        'num_atoms': 5
    },
    {
        'name': 'Aluminum Oxide',
        'smiles': '[Al+3].[Al+3].[O-2].[O-2].[O-2]',
        'formula': 'Al2O3',
        'molecular_weight': 101.96,
        'num_atoms': 5
    },
    {
        'name': 'Iron(III) Chloride',
        'smiles': '[Fe+3].[Cl-].[Cl-].[Cl-]',
        'formula': 'FeCl3',
        'molecular_weight': 162.20,
        'num_atoms': 4
    },
    
    # Simple Organic Compounds - Common in Organic Chemistry Exams
    {
        'name': 'Ethanol',
        'smiles': 'CCO',
        'formula': 'C2H6O',
        'molecular_weight': 46.07,
        'num_atoms': 9
    },
    {
        'name': 'Acetic Acid',
        'smiles': 'CC(=O)O',
        'formula': 'C2H4O2',
        'molecular_weight': 60.05,
        'num_atoms': 8
    },
    {
        'name': 'Acetone',
        'smiles': 'CC(=O)C',
        'formula': 'C3H6O',
        'molecular_weight': 58.08,
        'num_atoms': 10
    },
    {
        'name': 'Formaldehyde',
        'smiles': 'C=O',
        'formula': 'CH2O',
        'molecular_weight': 30.03,
        'num_atoms': 4
    },
    {
        'name': 'Methanol',
        'smiles': 'CO',
        'formula': 'CH4O',
        'molecular_weight': 32.04,
        'num_atoms': 6
    },
    {
        'name': 'Benzene',
        'smiles': 'c1ccccc1',
        'formula': 'C6H6',
        'molecular_weight': 78.11,
        'num_atoms': 12
    },
    {
        'name': 'Toluene',
        'smiles': 'Cc1ccccc1',
        'formula': 'C7H8',
        'molecular_weight': 92.14,
        'num_atoms': 15
    },
    {
        'name': 'Ethylene',
        'smiles': 'C=C',
        'formula': 'C2H4',
        'molecular_weight': 28.05,
        'num_atoms': 6
    },
    {
        'name': 'Acetylene',
        'smiles': 'C#C',
        'formula': 'C2H2',
        'molecular_weight': 26.04,
        'num_atoms': 4
    },
    {
        'name': 'Propane',
        'smiles': 'CCC',
        'formula': 'C3H8',
        'molecular_weight': 44.10,
        'num_atoms': 11
    },
    
    # Biochemically Relevant Molecules - Common in Biochemistry Exams
    {
        'name': 'Glucose',
        'smiles': 'C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O)O)O)O)O',
        'formula': 'C6H12O6',
        'molecular_weight': 180.16,
        'num_atoms': 24
    },
    {
        'name': 'Glycine',
        'smiles': 'NCC(=O)O',
        'formula': 'C2H5NO2',
        'molecular_weight': 75.07,
        'num_atoms': 10
    },
    {
        'name': 'Alanine',
        'smiles': 'C[C@H](C(=O)O)N',
        'formula': 'C3H7NO2',
        'molecular_weight': 89.09,
        'num_atoms': 13
    },
    {
        'name': 'Urea',
        'smiles': 'NC(=O)N',
        'formula': 'CH4N2O',
        'molecular_weight': 60.06,
        'num_atoms': 8
    },
    {
        'name': 'Lactic Acid',
        'smiles': 'C[C@H](C(=O)O)O',
        'formula': 'C3H6O3',
        'molecular_weight': 90.08,
        'num_atoms': 12
    },
    
    # Additional Molecules for Demonstrating Chemical Principles
    {
        'name': 'Ozone',
        'smiles': 'O=[O+][O-]',
        'formula': 'O3',
        'molecular_weight': 48.00,
        'num_atoms': 3
    },
    {
        'name': 'Hydrogen Gas',
        'smiles': '[H][H]',
        'formula': 'H2',
        'molecular_weight': 2.02,
        'num_atoms': 2
    },
    {
        'name': 'Oxygen Gas',
        'smiles': 'O=O',
        'formula': 'O2',
        'molecular_weight': 32.00,
        'num_atoms': 2
    },
    {
        'name': 'Nitrogen Gas',
        'smiles': 'N#N',
        'formula': 'N2',
        'molecular_weight': 28.01,
        'num_atoms': 2
    },
    {
        'name': 'Carbon Monoxide',
        'smiles': '[C-]#[O+]',
        'formula': 'CO',
        'molecular_weight': 28.01,
        'num_atoms': 2
    }
]

def main():
    """Add common molecules to the database."""
    # Initialize the database
    db_path = "common_molecules.db"
    db = MoleculeDatabase(db_path)
    
    # Check if molecules are already in the database
    formulas = [mol['formula'] for mol in COMMON_MOLECULES]
    existing_molecules = db.batch_get_molecules(formulas, search_type='formula')
    
    # Filter out molecules that are already in the database
    molecules_to_add = []
    for i, mol in enumerate(COMMON_MOLECULES):
        if existing_molecules[i] is None:
            molecules_to_add.append(mol)
    
    # Add molecules to the database
    if molecules_to_add:
        db.batch_add_molecules(molecules_to_add)
        print(f"Added {len(molecules_to_add)} new molecules to the database.")
    else:
        print("All common molecules are already in the database.")
    
    # Print database statistics
    stats = db.get_database_stats()
    print(f"Database contains {stats['molecule_count']} molecules.")
    
    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()