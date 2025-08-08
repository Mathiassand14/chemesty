#!/usr/bin/env python3
"""
Script to download real molecules from PubChem and store them in a local database.

This script uses the chemesty.data.download module to download a dataset of
real molecules from PubChem, with validation to ensure they are realistic
chemical compounds.
"""

import os
import sys
import time
from chemesty.data.download import download_dataset

def main():
    """Download a dataset of real molecules from PubChem."""
    print("Starting download of real molecules from PubChem...")
    
    # Download 1 million compounds from PubChem
    # Set force_update=True to ensure we download even if the database already exists
    db_path = download_dataset(
        source='pubchem',
        max_compounds=1000000,  # Download 1 million compounds as requested
        n_jobs=-1,              # Use all available processors
        force_update=True       # Force update even if database exists
    )
    
    print(f"Database created at {db_path}")
    
    # Verify the number of compounds in the database
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.execute('SELECT COUNT(*) FROM molecules')
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Database contains {count} molecules")
    
    # Sample some molecules to verify they are real
    if count > 0:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute('SELECT name, formula, molecular_weight FROM molecules LIMIT 10')
        print("\nSample molecules in the database:")
        print("Name\t\tFormula\t\tMolecular Weight")
        print("-" * 60)
        for row in cursor:
            print(f"{row[0]}\t{row[1]}\t\t{row[2]}")
        conn.close()

if __name__ == "__main__":
    main()