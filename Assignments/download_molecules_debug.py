#!/usr/bin/env python3
"""
Debug script to download real molecules from PubChem and store them in a local database.

This script includes additional debugging output and clears existing database
before downloading a small number of compounds for testing.
"""

import os
import sys
import time
import sqlite3
from chemesty.data.download import download_dataset

def clear_database_and_checkpoint():
    """Clear the existing database and checkpoint file."""
    # Get the default database path
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(package_dir, 'data', 'molecules.db')
    checkpoint_file = f"{db_path}.checkpoint"
    
    # Remove the database file if it exists
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Remove the checkpoint file if it exists
    if os.path.exists(checkpoint_file):
        print(f"Removing existing checkpoint file: {checkpoint_file}")
        os.remove(checkpoint_file)
    
    return db_path

def main():
    """Download a small dataset of real molecules from PubChem for testing."""
    print("Starting debug download of real molecules from PubChem...")
    
    # Clear existing database and checkpoint file
    db_path = clear_database_and_checkpoint()
    
    # Download a small number of compounds for testing
    print("Downloading a small number of compounds for testing...")
    db_path = download_dataset(
        source='pubchem',
        max_compounds=100,  # Small number for testing
        n_jobs=1,           # Single process for easier debugging
        force_update=True   # Force update even if database exists
    )
    
    print(f"Database created at {db_path}")
    
    # Verify the number of compounds in the database
    conn = sqlite3.connect(db_path)
    cursor = conn.execute('SELECT COUNT(*) FROM molecules')
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Database contains {count} molecules")
    
    # Sample all molecules to verify they are real
    if count > 0:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute('SELECT name, formula, molecular_weight, smiles FROM molecules')
        print("\nMolecules in the database:")
        print("Name\t\tFormula\t\tMolecular Weight\tSMILES")
        print("-" * 80)
        for row in cursor:
            print(f"{row[0]}\t{row[1]}\t\t{row[2]}\t\t{row[3][:30]}...")
        conn.close()

if __name__ == "__main__":
    main()