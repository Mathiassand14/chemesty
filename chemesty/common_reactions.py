"""
Script to add common chemical reactions to the database.

This script creates a database of common chemical reactions including combustion,
acid-base, redox, and other types of reactions that are commonly studied in chemistry.
"""

from chemesty.data.reaction_database import ReactionDatabase
from chemesty.reactions.reaction import Reaction
from chemesty.molecules.molecule import Molecule

# Define common chemical reactions with their properties
# Each reaction is defined with reactants, products, name, and optional conditions
COMMON_REACTIONS = [
    # Combustion Reactions
    {
        'name': 'Methane Combustion',
        'reactants': [
            {'formula': 'CH4', 'coefficient': 1.0},
            {'formula': 'O2', 'coefficient': 2.0}
        ],
        'products': [
            {'formula': 'CO2', 'coefficient': 1.0},
            {'formula': 'H2O', 'coefficient': 2.0}
        ],
        'type': 'combustion'
    },
    {
        'name': 'Ethane Combustion',
        'reactants': [
            {'formula': 'C2H6', 'coefficient': 1.0},
            {'formula': 'O2', 'coefficient': 3.5}
        ],
        'products': [
            {'formula': 'CO2', 'coefficient': 2.0},
            {'formula': 'H2O', 'coefficient': 3.0}
        ],
        'type': 'combustion'
    },
    {
        'name': 'Propane Combustion',
        'reactants': [
            {'formula': 'C3H8', 'coefficient': 1.0},
            {'formula': 'O2', 'coefficient': 5.0}
        ],
        'products': [
            {'formula': 'CO2', 'coefficient': 3.0},
            {'formula': 'H2O', 'coefficient': 4.0}
        ],
        'type': 'combustion'
    },
    {
        'name': 'Butane Combustion',
        'reactants': [
            {'formula': 'C4H10', 'coefficient': 1.0},
            {'formula': 'O2', 'coefficient': 6.5}
        ],
        'products': [
            {'formula': 'CO2', 'coefficient': 4.0},
            {'formula': 'H2O', 'coefficient': 5.0}
        ],
        'type': 'combustion'
    },
    
    # Acid-Base Reactions
    {
        'name': 'Hydrochloric Acid and Sodium Hydroxide',
        'reactants': [
            {'formula': 'HCl', 'coefficient': 1.0},
            {'formula': 'NaOH', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'NaCl', 'coefficient': 1.0},
            {'formula': 'H2O', 'coefficient': 1.0}
        ],
        'type': 'acid_base'
    },
    {
        'name': 'Sulfuric Acid and Sodium Hydroxide',
        'reactants': [
            {'formula': 'H2SO4', 'coefficient': 1.0},
            {'formula': 'NaOH', 'coefficient': 2.0}
        ],
        'products': [
            {'formula': 'Na2SO4', 'coefficient': 1.0},
            {'formula': 'H2O', 'coefficient': 2.0}
        ],
        'type': 'neutralization'
    },
    {
        'name': 'Nitric Acid and Potassium Hydroxide',
        'reactants': [
            {'formula': 'HNO3', 'coefficient': 1.0},
            {'formula': 'KOH', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'KNO3', 'coefficient': 1.0},
            {'formula': 'H2O', 'coefficient': 1.0}
        ],
        'type': 'acid_base'
    },
    {
        'name': 'Acetic Acid and Sodium Hydroxide',
        'reactants': [
            {'formula': 'CH3COOH', 'coefficient': 1.0},
            {'formula': 'NaOH', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'CH3COONa', 'coefficient': 1.0},
            {'formula': 'H2O', 'coefficient': 1.0}
        ],
        'type': 'acid_base'
    },
    
    # Redox Reactions
    {
        'name': 'Hydrogen and Oxygen',
        'reactants': [
            {'formula': 'H2', 'coefficient': 2.0},
            {'formula': 'O2', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'H2O', 'coefficient': 2.0}
        ],
        'type': 'redox'
    },
    {
        'name': 'Hydrogen and Fluorine',
        'reactants': [
            {'formula': 'H2', 'coefficient': 1.0},
            {'formula': 'F2', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'HF', 'coefficient': 2.0}
        ],
        'type': 'redox'
    },
    {
        'name': 'Iron and Oxygen',
        'reactants': [
            {'formula': 'Fe', 'coefficient': 4.0},
            {'formula': 'O2', 'coefficient': 3.0}
        ],
        'products': [
            {'formula': 'Fe2O3', 'coefficient': 2.0}
        ],
        'type': 'redox'
    },
    {
        'name': 'Zinc and Copper Sulfate',
        'reactants': [
            {'formula': 'Zn', 'coefficient': 1.0},
            {'formula': 'CuSO4', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'ZnSO4', 'coefficient': 1.0},
            {'formula': 'Cu', 'coefficient': 1.0}
        ],
        'type': 'single_replacement'
    },
    
    # Precipitation Reactions
    {
        'name': 'Silver Nitrate and Sodium Chloride',
        'reactants': [
            {'formula': 'AgNO3', 'coefficient': 1.0},
            {'formula': 'NaCl', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'AgCl', 'coefficient': 1.0, 'phase': 's'},
            {'formula': 'NaNO3', 'coefficient': 1.0}
        ],
        'type': 'precipitation'
    },
    {
        'name': 'Lead Nitrate and Potassium Iodide',
        'reactants': [
            {'formula': 'Pb(NO3)2', 'coefficient': 1.0},
            {'formula': 'KI', 'coefficient': 2.0}
        ],
        'products': [
            {'formula': 'PbI2', 'coefficient': 1.0, 'phase': 's'},
            {'formula': 'KNO3', 'coefficient': 2.0}
        ],
        'type': 'precipitation'
    },
    {
        'name': 'Barium Chloride and Sodium Sulfate',
        'reactants': [
            {'formula': 'BaCl2', 'coefficient': 1.0},
            {'formula': 'Na2SO4', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'BaSO4', 'coefficient': 1.0, 'phase': 's'},
            {'formula': 'NaCl', 'coefficient': 2.0}
        ],
        'type': 'precipitation'
    },
    
    # Synthesis Reactions
    {
        'name': 'Hydrogen and Nitrogen',
        'reactants': [
            {'formula': 'N2', 'coefficient': 1.0},
            {'formula': 'H2', 'coefficient': 3.0}
        ],
        'products': [
            {'formula': 'NH3', 'coefficient': 2.0}
        ],
        'type': 'synthesis',
        'conditions': {'catalyst': 'Fe', 'temperature': 450, 'pressure': 200}
    },
    {
        'name': 'Carbon and Oxygen',
        'reactants': [
            {'formula': 'C', 'coefficient': 1.0},
            {'formula': 'O2', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'CO2', 'coefficient': 1.0}
        ],
        'type': 'synthesis'
    },
    {
        'name': 'Sodium and Chlorine',
        'reactants': [
            {'formula': 'Na', 'coefficient': 2.0},
            {'formula': 'Cl2', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'NaCl', 'coefficient': 2.0}
        ],
        'type': 'synthesis'
    },
    
    # Decomposition Reactions
    {
        'name': 'Hydrogen Peroxide Decomposition',
        'reactants': [
            {'formula': 'H2O2', 'coefficient': 2.0}
        ],
        'products': [
            {'formula': 'H2O', 'coefficient': 2.0},
            {'formula': 'O2', 'coefficient': 1.0}
        ],
        'type': 'decomposition',
        'conditions': {'catalyst': 'MnO2'}
    },
    {
        'name': 'Calcium Carbonate Decomposition',
        'reactants': [
            {'formula': 'CaCO3', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'CaO', 'coefficient': 1.0},
            {'formula': 'CO2', 'coefficient': 1.0}
        ],
        'type': 'decomposition',
        'conditions': {'temperature': 825}
    },
    {
        'name': 'Ammonium Nitrate Decomposition',
        'reactants': [
            {'formula': 'NH4NO3', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'N2O', 'coefficient': 1.0},
            {'formula': 'H2O', 'coefficient': 2.0}
        ],
        'type': 'decomposition',
        'conditions': {'temperature': 200}
    },
    
    # Double Replacement Reactions
    {
        'name': 'Sodium Carbonate and Calcium Chloride',
        'reactants': [
            {'formula': 'Na2CO3', 'coefficient': 1.0},
            {'formula': 'CaCl2', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'CaCO3', 'coefficient': 1.0, 'phase': 's'},
            {'formula': 'NaCl', 'coefficient': 2.0}
        ],
        'type': 'double_replacement'
    },
    {
        'name': 'Potassium Iodide and Lead Nitrate',
        'reactants': [
            {'formula': 'KI', 'coefficient': 2.0},
            {'formula': 'Pb(NO3)2', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'PbI2', 'coefficient': 1.0, 'phase': 's'},
            {'formula': 'KNO3', 'coefficient': 2.0}
        ],
        'type': 'double_replacement'
    },
    
    # Hydrolysis Reactions
    {
        'name': 'Ethyl Acetate Hydrolysis',
        'reactants': [
            {'formula': 'CH3COOC2H5', 'coefficient': 1.0},
            {'formula': 'H2O', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'CH3COOH', 'coefficient': 1.0},
            {'formula': 'C2H5OH', 'coefficient': 1.0}
        ],
        'type': 'hydrolysis',
        'conditions': {'catalyst': 'H+'}
    },
    {
        'name': 'Sucrose Hydrolysis',
        'reactants': [
            {'formula': 'C12H22O11', 'coefficient': 1.0},
            {'formula': 'H2O', 'coefficient': 1.0}
        ],
        'products': [
            {'formula': 'C6H12O6', 'coefficient': 1.0},  # Glucose
            {'formula': 'C6H12O6', 'coefficient': 1.0}   # Fructose
        ],
        'type': 'hydrolysis',
        'conditions': {'catalyst': 'H+'}
    }
]

def create_reaction_from_dict(reaction_data):
    """
    Create a Reaction object from a dictionary.
    
    Args:
        reaction_data: Dictionary containing reaction data
        
    Returns:
        Reaction object
    """
    # Create a new reaction
    reaction = Reaction(
        name=reaction_data.get('name'),
        temperature=reaction_data.get('temperature'),
        pressure=reaction_data.get('pressure')
    )
    
    # Add reactants
    for reactant_data in reaction_data.get('reactants', []):
        reaction.add_reactant(
            molecule=reactant_data['formula'],
            coefficient=reactant_data.get('coefficient', 1.0),
            phase=reactant_data.get('phase'),
            is_catalyst=reactant_data.get('is_catalyst', False)
        )
    
    # Add products
    for product_data in reaction_data.get('products', []):
        reaction.add_product(
            molecule=product_data['formula'],
            coefficient=product_data.get('coefficient', 1.0),
            phase=product_data.get('phase')
        )
    
    # Add conditions
    if 'conditions' in reaction_data:
        for key, value in reaction_data['conditions'].items():
            reaction.conditions[key] = value
    
    # Add catalyst as a reactant if specified in conditions
    if 'conditions' in reaction_data and 'catalyst' in reaction_data['conditions']:
        catalyst = reaction_data['conditions']['catalyst']
        reaction.add_reactant(
            molecule=catalyst,
            coefficient=1.0,
            is_catalyst=True
        )
    
    return reaction

def main():
    """Add common reactions to the database."""
    # Initialize the database
    db_path = "chemesty/data/common_reactions.db"
    db = ReactionDatabase(db_path)
    
    # Create reaction objects from the data
    reactions = []
    for reaction_data in COMMON_REACTIONS:
        reaction = create_reaction_from_dict(reaction_data)
        reactions.append(reaction)
    
    # Add reactions to the database
    reaction_ids = db.batch_add_reactions(reactions)
    
    # Print database statistics
    stats = db.get_database_stats()
    print(f"Added {len(reaction_ids)} reactions to the database.")
    print(f"Database contains {stats['reaction_count']} reactions.")
    print(f"Reaction types: {', '.join(db.get_reaction_types())}")
    
    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()