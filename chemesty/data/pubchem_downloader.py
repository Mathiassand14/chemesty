"""
Module for downloading chemical compounds from PubChem.

This module provides functions for downloading chemical compounds from PubChem
using the PubChemPy library and storing them in a local SQLite database.
"""

import os
import time
import sqlite3
import logging
import pubchempy as pcp
from typing import List, Dict, Any, Optional, Tuple
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pubchem_download.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("pubchem_downloader")

def create_checkpoint_file(checkpoint_file: str, batch_id: int) -> None:
    """
    Create or update a checkpoint file with the current batch ID.
    
    Args:
        checkpoint_file: Path to the checkpoint file
        batch_id: Current batch ID
    """
    with open(checkpoint_file, 'w') as f:
        f.write(str(batch_id))
    logger.info(f"Updated checkpoint file with batch ID {batch_id}")

def read_checkpoint_file(checkpoint_file: str) -> int:
    """
    Read the batch ID from a checkpoint file.
    
    Args:
        checkpoint_file: Path to the checkpoint file
        
    Returns:
        Batch ID from the checkpoint file, or 0 if the file doesn't exist
    """
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                batch_id = int(f.read().strip())
                logger.info(f"Resuming from batch ID {batch_id}")
                return batch_id
        except Exception as e:
            logger.error(f"Error reading checkpoint file: {e}")
    
    logger.info("Starting from batch ID 0")
    return 0

def convert_pubchem_compound(compound: pcp.Compound) -> Dict[str, Any]:
    """
    Convert a PubChemPy Compound object to a dictionary for database storage.
    
    Args:
        compound: PubChemPy Compound object
        
    Returns:
        Dictionary containing compound data
    """
    # Extract properties from the compound
    data = {
        'name': getattr(compound, 'iupac_name', None),
        'smiles': getattr(compound, 'canonical_smiles', None),
        'formula': getattr(compound, 'molecular_formula', None),
        'molecular_weight': getattr(compound, 'molecular_weight', None),
        'inchi': getattr(compound, 'inchi', None),
        'logp': getattr(compound, 'xlogp', None),
        'num_atoms': None,
        'num_rings': None
    }
    
    # Try to get additional properties
    try:
        if hasattr(compound, 'atoms'):
            data['num_atoms'] = len(compound.atoms)
        
        if hasattr(compound, 'elements'):
            # Count unique elements
            data['num_elements'] = len(set(atom.element for atom in compound.atoms))
    except Exception as e:
        logger.warning(f"Error extracting additional properties for CID {compound.cid}: {e}")
    
    return data

def download_compounds_batch(cids: List[int], max_retries: int = 3, retry_delay: int = 5) -> List[Dict[str, Any]]:
    """
    Download a batch of compounds from PubChem by CID.
    
    Args:
        cids: List of compound IDs to download
        max_retries: Maximum number of retries for failed downloads
        retry_delay: Delay in seconds between retries
        
    Returns:
        List of dictionaries containing compound data
    """
    compounds_data = []
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Download compounds from PubChem
            compounds = pcp.get_compounds(cids, 'cid')
            
            # Convert compounds to dictionaries
            for compound in compounds:
                compound_data = convert_pubchem_compound(compound)
                compound_data['cid'] = compound.cid
                compounds_data.append(compound_data)
            
            # If we got here, the download was successful
            break
            
        except Exception as e:
            retry_count += 1
            logger.warning(f"Error downloading compounds batch (attempt {retry_count}/{max_retries}): {e}")
            
            if retry_count < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to download compounds batch after {max_retries} attempts")
                # Return any compounds we managed to download
                break
    
    return compounds_data

def insert_compounds_batch(db_path: str, compounds_data: List[Dict[str, Any]]) -> int:
    """
    Insert a batch of compounds into the database.
    
    Args:
        db_path: Path to the SQLite database
        compounds_data: List of dictionaries containing compound data
        
    Returns:
        Number of compounds inserted
    """
    if not compounds_data:
        return 0
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Start a transaction
        conn.execute('BEGIN TRANSACTION')
        
        # Insert each compound
        inserted_count = 0
        for compound in compounds_data:
            cursor.execute('''
            INSERT OR IGNORE INTO molecules
            (name, smiles, formula, molecular_weight, inchi, logp, num_atoms, num_rings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                compound.get('name'),
                compound.get('smiles'),
                compound.get('formula'),
                compound.get('molecular_weight'),
                compound.get('inchi'),
                compound.get('logp'),
                compound.get('num_atoms'),
                compound.get('num_rings')
            ))
            
            if cursor.rowcount > 0:
                inserted_count += 1
        
        # Commit the transaction
        conn.commit()
        
        return inserted_count
        
    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        logger.error(f"Error inserting compounds batch: {e}")
        return 0
        
    finally:
        # Close the connection
        conn.close()

def download_pubchem_compounds(
    db_path: str,
    start_cid: int = 1,
    max_compounds: int = 1000000,
    batch_size: int = 100,
    force_update: bool = True,
    max_retries: int = 3,
    retry_delay: int = 5,
    sleep_time: float = 0.1
) -> Tuple[int, int]:
    """
    Download compounds from PubChem and store them in a SQLite database.
    
    Args:
        db_path: Path to the SQLite database
        start_cid: CID to start downloading from
        max_compounds: Maximum number of compounds to download
        batch_size: Number of compounds to download in each batch
        force_update: Whether to force update if the database already exists
        max_retries: Maximum number of retries for failed downloads
        retry_delay: Delay in seconds between retries
        sleep_time: Time to sleep between batches to avoid overwhelming the API
        
    Returns:
        Tuple of (total compounds downloaded, total compounds in database)
    """
    # Create the database if it doesn't exist
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the molecules table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS molecules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        smiles TEXT UNIQUE,
        formula TEXT,
        molecular_weight REAL,
        inchi TEXT,
        logp REAL,
        num_atoms INTEGER,
        num_rings INTEGER
    )
    ''')
    
    # Create indexes for faster lookups
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_formula ON molecules(formula)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON molecules(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mw ON molecules(molecular_weight)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_smiles ON molecules(smiles)')
    
    # Check if the database already has data
    cursor.execute('SELECT COUNT(*) FROM molecules')
    count = cursor.fetchone()[0]
    
    if count > 0 and not force_update:
        logger.info(f"Database already contains {count} molecules")
        logger.info("Use force_update=True to add more compounds")
        conn.close()
        return 0, count
    
    # Close the connection so it doesn't interfere with batch processing
    conn.close()
    
    # Calculate the number of batches
    end_cid = start_cid + max_compounds - 1
    num_batches = (max_compounds + batch_size - 1) // batch_size
    
    # Check if we can resume from a checkpoint
    checkpoint_file = f"{db_path}.checkpoint"
    start_batch = read_checkpoint_file(checkpoint_file)
    
    # Calculate the actual start CID based on the checkpoint
    start_cid = start_cid + start_batch * batch_size
    
    logger.info(f"Downloading compounds from PubChem (CIDs {start_cid}-{end_cid})")
    logger.info(f"Using batch size of {batch_size} compounds")
    logger.info(f"Total batches: {num_batches}")
    logger.info(f"Starting from batch {start_batch}")
    
    # Download compounds in batches
    total_downloaded = 0
    total_inserted = 0
    
    try:
        for batch_id in tqdm(range(start_batch, num_batches), desc="Downloading batches"):
            # Calculate the CID range for this batch
            batch_start_cid = start_cid + (batch_id - start_batch) * batch_size
            batch_end_cid = min(batch_start_cid + batch_size - 1, end_cid)
            
            # Generate the list of CIDs for this batch
            batch_cids = list(range(batch_start_cid, batch_end_cid + 1))
            
            logger.info(f"Downloading batch {batch_id} (CIDs {batch_start_cid}-{batch_end_cid})")
            
            # Download the batch
            compounds_data = download_compounds_batch(batch_cids, max_retries, retry_delay)
            total_downloaded += len(compounds_data)
            
            # Insert the batch into the database
            inserted = insert_compounds_batch(db_path, compounds_data)
            total_inserted += inserted
            
            logger.info(f"Batch {batch_id}: Downloaded {len(compounds_data)} compounds, inserted {inserted} new compounds")
            
            # Update the checkpoint
            create_checkpoint_file(checkpoint_file, batch_id + 1)
            
            # Sleep to avoid overwhelming the API
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        logger.warning("Download interrupted by user")
    except Exception as e:
        logger.error(f"Error downloading compounds: {e}")
    
    # Get the final count of compounds in the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM molecules')
    final_count = cursor.fetchone()[0]
    conn.close()
    
    logger.info(f"Download completed: Downloaded {total_downloaded} compounds, inserted {total_inserted} new compounds")
    logger.info(f"Database now contains {final_count} molecules")
    
    return total_inserted, final_count

def download_dataset(
    source: str = 'pubchem',
    db_path: Optional[str] = None,
    max_compounds: int = 1000000,
    start_cid: int = 1,
    batch_size: int = 100,
    force_update: bool = True
) -> str:
    """
    Download a chemical dataset from the specified source.
    
    This is a convenience function that calls the appropriate download function
    based on the source parameter.
    
    Args:
        source: Source of the dataset ('pubchem' only for now)
        db_path: Path to the SQLite database file. If None, uses the default path.
        max_compounds: Maximum number of compounds to download.
        start_cid: CID to start downloading from (for PubChem only)
        batch_size: Number of compounds to download in each batch (for PubChem only)
        force_update: If True, download and add compounds even if the database already has data.
        
    Returns:
        Path to the SQLite database file.
    """
    if db_path is None:
        # Use default path in the package data directory
        package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(package_dir, 'data', 'molecules.db')
    
    if source.lower() == 'pubchem':
        download_pubchem_compounds(
            db_path=db_path,
            start_cid=start_cid,
            max_compounds=max_compounds,
            batch_size=batch_size,
            force_update=force_update
        )
    else:
        logger.error(f"Unsupported source: {source}")
        logger.info("Currently only 'pubchem' is supported")
    
    return db_path