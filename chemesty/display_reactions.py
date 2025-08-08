"""
Script to display chemical reactions in the database.

This script lists all reactions in the database with their properties and
provides search functionality based on various criteria.
"""

from chemesty.data.reaction_database import ReactionDatabase
import argparse
import textwrap

def display_all_reactions(db_path, limit=100):
    """
    Display all reactions in the database.
    
    Args:
        db_path: Path to the database file
        limit: Maximum number of reactions to display
    """
    try:
        # Initialize the database
        db = ReactionDatabase(db_path)
        
        # Get database statistics
        stats = db.get_database_stats()
        print(f"Database: {db_path}")
        print(f"Total reactions: {stats['reaction_count']}")
        print(f"Total reactants: {stats['reactant_count']}")
        print(f"Total products: {stats['product_count']}")
        print(f"Database size: {stats['database_size_mb']:.2f} MB")
        
        # Get reaction type counts
        print("\nReaction Types:")
        for reaction_type, count in stats['reaction_type_counts'].items():
            print(f"  {reaction_type}: {count}")
        
        print("\n" + "-" * 80)
        
        # Get all reactions
        reactions = db.get_all_reactions(limit=limit)
        
        if not reactions:
            print("No reactions found in the database.")
            db.close()
            return
        
        # Display reactions in a formatted table
        print(f"{'ID':<5} {'Name':<30} {'Type':<20} {'Equation':<50}")
        print("-" * 105)
        
        for i, reaction in enumerate(reactions):
            # Format the equation to fit in the table
            equation = str(reaction)
            if len(equation) > 50:
                equation = equation[:47] + "..."
            
            # Format the name to fit in the table
            name = reaction.name or f"Reaction {i+1}"
            if len(name) > 30:
                name = name[:27] + "..."
            
            print(f"{i+1:<5} {name:<30} {reaction.type:<20} {equation:<50}")
        
        # Close the database connection
        db.close()
        
    except Exception as e:
        print(f"Error displaying reactions: {e}")

def display_reaction_details(db_path, reaction_id):
    """
    Display detailed information about a specific reaction.
    
    Args:
        db_path: Path to the database file
        reaction_id: ID of the reaction to display
    """
    try:
        # Initialize the database
        db = ReactionDatabase(db_path)
        
        # Get the reaction
        reaction = db.get_reaction_by_id(reaction_id)
        
        if not reaction:
            print(f"Reaction with ID {reaction_id} not found.")
            db.close()
            return
        
        # Display reaction details
        print("\n" + "=" * 80)
        print(f"Reaction ID: {reaction_id}")
        print(f"Name: {reaction.name or 'Unnamed reaction'}")
        print(f"Type: {reaction.type}")
        print(f"Balanced: {'Yes' if reaction.is_balanced() else 'No'}")
        print(f"Equation: {reaction}")
        
        # Display reactants
        print("\nReactants:")
        for reactant in reaction.reactants:
            catalyst_str = " (catalyst)" if reactant.is_catalyst else ""
            print(f"  {reactant.coefficient:.2g} {reactant.molecule.molecular_formula}{catalyst_str}")
        
        # Display products
        print("\nProducts:")
        for product in reaction.products:
            print(f"  {product.coefficient:.2g} {product.molecule.molecular_formula}")
        
        # Display conditions
        if reaction.temperature or reaction.pressure or reaction.conditions:
            print("\nConditions:")
            if reaction.temperature:
                print(f"  Temperature: {reaction.temperature} K")
            if reaction.pressure:
                print(f"  Pressure: {reaction.pressure} atm")
            for key, value in reaction.conditions.items():
                print(f"  {key}: {value}")
        
        # Display element balance
        print("\nElement Balance:")
        element_balance = reaction.get_element_balance()
        for element, balance in element_balance.items():
            status = "Balanced" if abs(balance) < 1e-6 else "Unbalanced"
            print(f"  {element}: {balance:.6f} ({status})")
        
        print("=" * 80)
        
        # Close the database connection
        db.close()
        
    except Exception as e:
        print(f"Error displaying reaction details: {e}")

def search_reactions(db_path, reaction_type=None, reactant=None, product=None, name=None, balanced_only=False, limit=100):
    """
    Search for reactions based on various criteria.
    
    Args:
        db_path: Path to the database file
        reaction_type: Type of reaction to search for
        reactant: Reactant formula to search for
        product: Product formula to search for
        name: Name to search for
        balanced_only: Whether to return only balanced reactions
        limit: Maximum number of results to return
    """
    try:
        # Initialize the database
        db = ReactionDatabase(db_path)
        
        # Search for reactions
        reactions = db.search_reactions(
            reaction_type=reaction_type,
            reactant_formula=reactant,
            product_formula=product,
            name=name,
            balanced_only=balanced_only,
            limit=limit
        )
        
        if not reactions:
            print("No reactions found matching the search criteria.")
            db.close()
            return
        
        # Display search results
        print(f"\nFound {len(reactions)} reactions matching the search criteria:")
        print("-" * 80)
        
        for i, reaction in enumerate(reactions):
            # Format the equation to fit in the display
            equation = str(reaction)
            equation = textwrap.fill(equation, width=70, subsequent_indent="  ")
            
            # Display the reaction
            print(f"{i+1}. {reaction.name or 'Unnamed reaction'} ({reaction.type})")
            print(f"   {equation}")
            print()
        
        # Close the database connection
        db.close()
        
    except Exception as e:
        print(f"Error searching for reactions: {e}")

def main():
    """Main function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Display and search for chemical reactions')
    parser.add_argument('--db-path', type=str, default="chemesty/data/common_reactions.db",
                        help='Path to the SQLite database file (default: chemesty/data/common_reactions.db)')
    parser.add_argument('--limit', type=int, default=100,
                        help='Maximum number of reactions to display (default: 100)')
    
    # Search options
    search_group = parser.add_argument_group('Search options')
    search_group.add_argument('--reaction-id', type=int,
                             help='Display details for a specific reaction ID')
    search_group.add_argument('--type', type=str,
                             help='Search for reactions of a specific type')
    search_group.add_argument('--reactant', type=str,
                             help='Search for reactions with a specific reactant')
    search_group.add_argument('--product', type=str,
                             help='Search for reactions with a specific product')
    search_group.add_argument('--name', type=str,
                             help='Search for reactions with a specific name')
    search_group.add_argument('--balanced-only', action='store_true',
                             help='Only show balanced reactions')
    
    args = parser.parse_args()
    
    # If a specific reaction ID is provided, display its details
    if args.reaction_id:
        display_reaction_details(args.db_path, args.reaction_id)
        return
    
    # If search options are provided, perform a search
    if args.type or args.reactant or args.product or args.name or args.balanced_only:
        search_reactions(
            args.db_path,
            reaction_type=args.type,
            reactant=args.reactant,
            product=args.product,
            name=args.name,
            balanced_only=args.balanced_only,
            limit=args.limit
        )
        return
    
    # Otherwise, display all reactions
    display_all_reactions(args.db_path, args.limit)
    
    # Example searches
    if args.db_path == "chemesty/data/common_reactions.db":
        print("\nExample searches:")
        print("\n1. Search for combustion reactions:")
        search_reactions(args.db_path, reaction_type="combustion", limit=3)
        
        print("\n2. Search for reactions involving water as a product:")
        search_reactions(args.db_path, product="H2O", limit=3)
        
        print("\n3. Search for acid-base reactions:")
        search_reactions(args.db_path, reaction_type="acid_base", limit=3)

if __name__ == "__main__":
    main()