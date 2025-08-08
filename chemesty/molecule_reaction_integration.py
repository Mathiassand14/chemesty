"""
Script to demonstrate integration between molecule and reaction databases.

This script shows how to search for molecules and then find reactions involving those molecules,
providing a comprehensive tool for chemistry education and research.
"""

from chemesty.data.database import MoleculeDatabase
from chemesty.data.reaction_database import ReactionDatabase
import argparse

def find_reactions_for_molecule(molecule_formula, molecule_db_path, reaction_db_path):
    """
    Find reactions involving a specific molecule.
    
    Args:
        molecule_formula: Formula of the molecule to search for
        molecule_db_path: Path to the molecule database
        reaction_db_path: Path to the reaction database
    """
    # Initialize the databases
    molecule_db = MoleculeDatabase(molecule_db_path)
    reaction_db = ReactionDatabase(reaction_db_path)
    
    # Search for the molecule
    molecules = molecule_db.search_by_formula(molecule_formula)
    
    if not molecules:
        print(f"No molecules found with formula '{molecule_formula}'")
        molecule_db.close()
        reaction_db.close()
        return
    
    # Display the molecule information
    print(f"Found {len(molecules)} molecules with formula '{molecule_formula}':")
    for molecule in molecules:
        print(f"  {molecule['name']} ({molecule_formula})")
        if 'molecular_weight' in molecule and molecule['molecular_weight'] is not None:
            print(f"  Molecular weight: {molecule['molecular_weight']:.2f}")
        if 'density_value' in molecule and molecule['density_value'] is not None:
            print(f"  Density: {molecule['density_value']:.4f} g/cm³")
        print()
    
    # Search for reactions where the molecule is a reactant
    reactant_reactions = reaction_db.search_reactions(reactant_formula=molecule_formula)
    
    if reactant_reactions:
        print(f"Found {len(reactant_reactions)} reactions where '{molecule_formula}' is a reactant:")
        for i, reaction in enumerate(reactant_reactions):
            print(f"{i+1}. {reaction.name} ({reaction.type})")
            print(f"   {reaction}")
            print()
    else:
        print(f"No reactions found where '{molecule_formula}' is a reactant")
    
    # Search for reactions where the molecule is a product
    product_reactions = reaction_db.search_reactions(product_formula=molecule_formula)
    
    if product_reactions:
        print(f"Found {len(product_reactions)} reactions where '{molecule_formula}' is a product:")
        for i, reaction in enumerate(product_reactions):
            print(f"{i+1}. {reaction.name} ({reaction.type})")
            print(f"   {reaction}")
            print()
    else:
        print(f"No reactions found where '{molecule_formula}' is a product")
    
    # Close the database connections
    molecule_db.close()
    reaction_db.close()

def find_molecules_for_reaction_type(reaction_type, molecule_db_path, reaction_db_path):
    """
    Find molecules involved in reactions of a specific type.
    
    Args:
        reaction_type: Type of reaction to search for
        molecule_db_path: Path to the molecule database
        reaction_db_path: Path to the reaction database
    """
    # Initialize the databases
    molecule_db = MoleculeDatabase(molecule_db_path)
    reaction_db = ReactionDatabase(reaction_db_path)
    
    # Search for reactions of the specified type
    reactions = reaction_db.search_reactions(reaction_type=reaction_type)
    
    if not reactions:
        print(f"No reactions found of type '{reaction_type}'")
        molecule_db.close()
        reaction_db.close()
        return
    
    print(f"Found {len(reactions)} reactions of type '{reaction_type}':")
    
    # Collect all unique molecules involved in these reactions
    reactant_formulas = set()
    product_formulas = set()
    
    for reaction in reactions:
        print(f"  {reaction.name}: {reaction}")
        
        for reactant in reaction.reactants:
            if not reactant.is_catalyst:
                reactant_formulas.add(reactant.molecule.molecular_formula)
        
        for product in reaction.products:
            product_formulas.add(product.molecule.molecular_formula)
    
    print("\nMolecules involved as reactants:")
    for formula in sorted(reactant_formulas):
        molecules = molecule_db.search_by_formula(formula)
        if molecules:
            for molecule in molecules:
                print(f"  {molecule['name']} ({formula})")
                if 'molecular_weight' in molecule and molecule['molecular_weight'] is not None:
                    print(f"  Molecular weight: {molecule['molecular_weight']:.2f}")
                if 'density_value' in molecule and molecule['density_value'] is not None:
                    print(f"  Density: {molecule['density_value']:.4f} g/cm³")
                print()
        else:
            print(f"  {formula} (not found in molecule database)")
            print()
    
    print("\nMolecules involved as products:")
    for formula in sorted(product_formulas):
        molecules = molecule_db.search_by_formula(formula)
        if molecules:
            for molecule in molecules:
                print(f"  {molecule['name']} ({formula})")
                if 'molecular_weight' in molecule and molecule['molecular_weight'] is not None:
                    print(f"  Molecular weight: {molecule['molecular_weight']:.2f}")
                if 'density_value' in molecule and molecule['density_value'] is not None:
                    print(f"  Density: {molecule['density_value']:.4f} g/cm³")
                print()
        else:
            print(f"  {formula} (not found in molecule database)")
            print()
    
    # Close the database connections
    molecule_db.close()
    reaction_db.close()

def main():
    """Main function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Demonstrate integration between molecule and reaction databases'
    )
    
    parser.add_argument(
        '--molecule-db', 
        type=str, 
        default="chemesty/data/common_molecules.db",
        help='Path to the molecule database file (default: chemesty/data/common_molecules.db)'
    )
    
    parser.add_argument(
        '--reaction-db', 
        type=str, 
        default="chemesty/data/common_reactions.db",
        help='Path to the reaction database file (default: chemesty/data/common_reactions.db)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Subparser for finding reactions for a molecule
    molecule_parser = subparsers.add_parser(
        'molecule', 
        help='Find reactions involving a specific molecule'
    )
    molecule_parser.add_argument(
        'formula', 
        type=str,
        help='Formula of the molecule to search for'
    )
    
    # Subparser for finding molecules for a reaction type
    reaction_parser = subparsers.add_parser(
        'reaction-type', 
        help='Find molecules involved in reactions of a specific type'
    )
    reaction_parser.add_argument(
        'type', 
        type=str,
        help='Type of reaction to search for'
    )
    
    args = parser.parse_args()
    
    # If no command is provided, show examples
    if args.command is None:
        print("Examples of integration between molecule and reaction databases:")
        print("\n1. Find reactions involving water (H2O):")
        find_reactions_for_molecule(
            "H2O", 
            args.molecule_db, 
            args.reaction_db
        )
        
        print("\n2. Find molecules involved in combustion reactions:")
        find_molecules_for_reaction_type(
            "combustion", 
            args.molecule_db, 
            args.reaction_db
        )
        
        return
    
    # Run the appropriate command
    if args.command == 'molecule':
        find_reactions_for_molecule(
            args.formula, 
            args.molecule_db, 
            args.reaction_db
        )
    elif args.command == 'reaction-type':
        find_molecules_for_reaction_type(
            args.type, 
            args.molecule_db, 
            args.reaction_db
        )

if __name__ == "__main__":
    main()