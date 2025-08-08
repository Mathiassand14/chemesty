#!/usr/bin/env python3
"""
Script to verify that the updated implementation correctly downloads real molecules from PubChem.

This script tests the updated download_batch function with a small batch of compounds
and verifies that real molecules are downloaded instead of dummy data.
"""

import os
import sys
import sqlite3
from chemesty.data.download import download_batch, create_database, insert_compounds

def verify_implementation():
    """Verify that the updated implementation correctly downloads real molecules."""
    print("Verifying updated implementation for downloading real molecules from PubChem...")
    
    # Parameters for a small test batch
    batch_id = 0
    batch_size = 5  # Small batch for quick testing
    max_compounds = 5
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    
    print(f"Testing with batch_id={batch_id}, batch_size={batch_size}, max_compounds={max_compounds}")
    
    # Call the updated download_batch function
    batch_id, compounds = download_batch(batch_id, batch_size, max_compounds, base_url)
    
    print(f"\nDownload complete. Retrieved {len(compounds)} compounds.")
    
    # Check if we got real molecules
    if compounds:
        print("\nCompound details:")
        for i, compound in enumerate(compounds):
            print(f"\nCompound {i+1}:")
            for key, value in compound.items():
                print(f"  {key}: {value}")
            
            # Check if this looks like a dummy compound
            is_dummy = (
                compound['name'].startswith('Compound_') or
                compound['formula'].startswith(f"C{i+1}H{(i+1)*2}O{(i+1)//2}")
            )
            
            if is_dummy:
                print("  WARNING: This appears to be dummy data!")
            else:
                print("  SUCCESS: This appears to be real molecule data!")
    else:
        print("No compounds retrieved. Implementation verification failed.")
        return
    
    # Create a test database to store the compounds
    db_path = os.path.join(os.getcwd(), "../chemesty/data/verify_pubchem.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = create_database(db_path)
    conn.close()
    
    # Insert the compounds into the database
    insert_compounds(db_path, compounds)
    
    # Verify the database
    conn = sqlite3.connect(db_path)
    cursor = conn.execute('SELECT COUNT(*) FROM molecules')
    count = cursor.fetchone()[0]
    print(f"\nTest database contains {count} molecules")
    
    # Sample the molecules
    if count > 0:
        cursor = conn.execute('SELECT name, formula, molecular_weight, smiles FROM molecules')
        print("\nMolecules in the test database:")
        for row in cursor:
            print(f"Name: {row[0]}")
            print(f"Formula: {row[1]}")
            print(f"Molecular Weight: {row[2]}")
            print(f"SMILES: {row[3]}")
            print("-" * 40)
    
    conn.close()
    
    print(f"\nVerification complete. Test database created at {db_path}")
    
    # Summary
    real_count = sum(1 for c in compounds if not c['name'].startswith('Compound_'))
    dummy_count = len(compounds) - real_count
    
    print(f"\nSUMMARY:")
    print(f"Total compounds: {len(compounds)}")
    print(f"Real molecules: {real_count}")
    print(f"Dummy molecules: {dummy_count}")
    
    if real_count > 0:
        print("\nSUCCESS: The implementation is correctly downloading real molecules from PubChem!")
    else:
        print("\nFAILURE: The implementation is still generating dummy data.")

if __name__ == "__main__":
    verify_implementation()