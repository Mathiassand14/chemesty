"""
Script to display molecules in the database.

This script lists all molecules in the database with their properties.
"""

from chemesty.data.database import MoleculeDatabase
import sqlite3
import argparse

def display_all_molecules(db_path):
    """Display all molecules in the database."""
    try:
        # Try using MoleculeDatabase first
        try:
            db = MoleculeDatabase(db_path)
            
            # Get database statistics
            stats = db.get_database_stats()
            print(f"Database: {db_path}")
            print(f"Total molecules: {stats['molecule_count']}")
            print(f"Database size: {stats['database_size_mb']:.2f} MB")
            
            # Close the database connection
            db.close()
        except Exception as e:
            # If MoleculeDatabase fails, get basic stats directly
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get the number of molecules
            cursor.execute('SELECT COUNT(*) FROM molecules')
            count = cursor.fetchone()[0]
            
            # Get the database size
            cursor.execute('PRAGMA page_count')
            page_count = cursor.fetchone()[0]
            cursor.execute('PRAGMA page_size')
            page_size = cursor.fetchone()[0]
            db_size = page_count * page_size / (1024 * 1024)  # Size in MB
            
            print(f"Database: {db_path}")
            print(f"Total molecules: {count}")
            print(f"Database size: {db_size:.2f} MB")
            
            conn.close()
        
        print("\n" + "-" * 80)
        
        # Connect directly to the database to get all molecules
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all molecules ordered by formula
        cursor.execute("""
        SELECT * FROM molecules
        ORDER BY formula
        """)
        
        molecules = cursor.fetchall()
        
        # Get column names to handle different database schemas
        columns = [column[0] for column in cursor.description]
        
        # Display molecules in a formatted table
        header = f"{'Formula':<10} {'Name':<25}"
        if 'molecular_weight' in columns:
            header += f" {'Molecular Weight':<20}"
        header += f" {'SMILES':<30}"
        print(header)
        print("-" * 80)
        
        for mol in molecules:
            # Handle different database schemas
            formula = mol['formula'] if 'formula' in columns else 'N/A'
            name = mol['name'][:24] if 'name' in columns else 'N/A'
            smiles = mol['smiles'][:30] if 'smiles' in columns else 'N/A'
            
            line = f"{formula:<10} {name:<25}"
            if 'molecular_weight' in columns:
                mw = mol['molecular_weight'] if mol['molecular_weight'] is not None else 0.0
                line += f" {mw:<20.2f}"
            line += f" {smiles:<30}"
            print(line)
        
        # Close connections
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error displaying molecules: {e}")

def search_molecule(db_path, search_term):
    """Search for a molecule by formula or name."""
    try:
        # Connect directly to the database for more control over the query
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get column names to handle different database schemas
        cursor.execute("SELECT * FROM molecules LIMIT 1")
        columns = [column[0] for column in cursor.description]
        
        # Search by formula if the column exists
        formula_results = []
        if 'formula' in columns:
            cursor.execute("""
            SELECT * FROM molecules
            WHERE formula LIKE ?
            """, (f"%{search_term}%",))
            
            formula_results = cursor.fetchall()
            if formula_results:
                print(f"\nResults for formula search '{search_term}':")
                for mol in formula_results:
                    result_str = f"  {mol['formula']} - {mol['name']}"
                    if 'molecular_weight' in columns and mol['molecular_weight'] is not None:
                        result_str += f" ({mol['molecular_weight']:.2f})"
                    print(result_str)
        
        # Search by name if the column exists
        name_results = []
        if 'name' in columns:
            cursor.execute("""
            SELECT * FROM molecules
            WHERE name LIKE ?
            """, (f"%{search_term}%",))
            
            name_results = cursor.fetchall()
            # Only show name results that weren't already shown in formula results
            unique_name_results = []
            if formula_results and 'formula' in columns:
                formula_set = {mol['formula'] for mol in formula_results}
                unique_name_results = [mol for mol in name_results if mol['formula'] not in formula_set]
            else:
                unique_name_results = name_results
                
            if unique_name_results:
                print(f"\nResults for name search '{search_term}':")
                for mol in unique_name_results:
                    result_str = f"  {mol['formula'] if 'formula' in columns else 'N/A'} - {mol['name']}"
                    if 'molecular_weight' in columns and mol['molecular_weight'] is not None:
                        result_str += f" ({mol['molecular_weight']:.2f})"
                    print(result_str)
        
        # Search by SMILES if the column exists and no other results were found
        if not formula_results and not name_results and 'smiles' in columns:
            cursor.execute("""
            SELECT * FROM molecules
            WHERE smiles LIKE ?
            """, (f"%{search_term}%",))
            
            smiles_results = cursor.fetchall()
            if smiles_results:
                print(f"\nResults for SMILES search '{search_term}':")
                for mol in smiles_results:
                    result_str = f"  {mol['formula'] if 'formula' in columns else 'N/A'} - "
                    result_str += f"{mol['name'] if 'name' in columns else 'N/A'}"
                    if 'molecular_weight' in columns and mol['molecular_weight'] is not None:
                        result_str += f" ({mol['molecular_weight']:.2f})"
                    print(result_str)
        
        if not formula_results and not name_results and not ('smiles' in columns and cursor.rowcount > 0):
            print(f"No molecules found matching '{search_term}'")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error searching for molecules: {e}")

def main():
    """Main function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Display molecules in the database')
    parser.add_argument('--db-path', type=str, default="chemesty/data/common_molecules.db",
                        help='Path to the SQLite database file (default: chemesty/data/common_molecules.db)')
    parser.add_argument('--search', type=str, default=None,
                        help='Search term for molecules (optional)')
    args = parser.parse_args()
    
    # Display all molecules if no search term is provided
    if args.search is None:
        display_all_molecules(args.db_path)
        
        # Example searches only for the default database
        if args.db_path == "common_molecules.db":
            print("\nExample searches:")
            search_molecule(args.db_path, "CO2")
            search_molecule(args.db_path, "NaCl")
            search_molecule(args.db_path, "Sodium")
    else:
        # Perform the requested search
        search_molecule(args.db_path, args.search)

if __name__ == "__main__":
    main()