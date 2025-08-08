#!/usr/bin/env python3
"""
Script to download a large dataset of molecules from online sources.

This script downloads millions of real molecules from PubChem and stores them in a local
SQLite database for use in chemistry education and exams.
"""

import os
import argparse
import time
import sqlite3
from chemesty.data.pubchem_downloader import download_dataset

def main():
    """Download a chemical dataset from PubChem."""
    parser = argparse.ArgumentParser(
        description='Download a large dataset of molecules from PubChem'
    )
    
    parser.add_argument(
        '--source', 
        choices=['pubchem'], 
        default='pubchem',
        help='Source of the dataset (currently only pubchem is supported)'
    )
    
    parser.add_argument(
        '--max-compounds', 
        type=int, 
        default=1000000,
        help='Maximum number of compounds to download (default: 1000000)'
    )
    
    parser.add_argument(
        '--start-cid', 
        type=int, 
        default=1,
        help='CID to start downloading from (default: 1)'
    )
    
    parser.add_argument(
        '--batch-size', 
        type=int, 
        default=100,
        help='Number of compounds to download in each batch (default: 100)'
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        default='chemesty/data/molecule_dataset.db',
        help='Path to the output SQLite database file (default: chemesty/data/molecule_dataset.db)'
    )
    
    parser.add_argument(
        '--no-force-update', 
        action='store_false',
        dest='force_update',
        help='Do not force update if the database already exists (default: force update)'
    )
    
    args = parser.parse_args()
    
    print(f"Starting download from {args.source}...")
    print(f"Maximum compounds: {args.max_compounds}")
    print(f"Starting CID: {args.start_cid}")
    print(f"Batch size: {args.batch_size}")
    print(f"Output database: {args.output}")
    print(f"Force update: {args.force_update}")
    
    start_time = time.time()
    
    # Ensure the database path is properly formatted
    output_path = args.output
    # If the path doesn't include a directory component, add './' to indicate current directory
    if os.path.dirname(output_path) == '':
        output_path = os.path.join('.', output_path)
    
    # Download the dataset
    db_path = download_dataset(
        source=args.source,
        db_path=output_path,
        max_compounds=args.max_compounds,
        start_cid=args.start_cid,
        batch_size=args.batch_size,
        force_update=args.force_update
    )
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\nDownload completed in {elapsed_time:.2f} seconds")
    print(f"Dataset downloaded and stored in {db_path}")
    
    # Connect to the database to get statistics
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
    
    print(f"Database contains {count} molecules")
    print(f"Database size: {db_size:.2f} MB")
    
    # Close the connection
    conn.close()
    
    print("\nExample usage:")
    print(f"  python chemesty/display_molecules.py --db-path {db_path}")
    print(f"  python chemesty/display_molecules.py --db-path {db_path} --search 'C6H6'")

if __name__ == "__main__":
    main()