#!/usr/bin/env python3
"""
Script to download millions of molecules from PubChem.

This script is specifically designed for downloading very large datasets
(millions of molecules) from PubChem with optimized parameters, detailed
progress reporting, and system resource monitoring.
"""

import os
import sys
import time
import argparse
import sqlite3
import logging
import shutil
import psutil
from datetime import datetime, timedelta
from tqdm import tqdm
from chemesty.data.pubchem_downloader import download_pubchem_compounds

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("million_molecules_download.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("million_molecules")

def check_disk_space(path, required_gb=10):
    """
    Check if there's enough disk space available.
    
    Args:
        path: Path to check disk space for
        required_gb: Required disk space in GB
        
    Returns:
        True if there's enough disk space, False otherwise
    """
    # Get the disk usage statistics
    disk_usage = shutil.disk_usage(path)
    free_space_gb = disk_usage.free / (1024 * 1024 * 1024)  # Convert to GB
    
    logger.info(f"Checking disk space at {path}")
    logger.info(f"Free space: {free_space_gb:.2f} GB")
    logger.info(f"Required space: {required_gb} GB")
    
    if free_space_gb < required_gb:
        logger.error(f"Not enough disk space. Need at least {required_gb} GB, but only {free_space_gb:.2f} GB available.")
        return False
    
    logger.info("Sufficient disk space available.")
    return True

def estimate_database_size(num_molecules, avg_molecule_size_kb=2):
    """
    Estimate the database size based on the number of molecules.
    
    Args:
        num_molecules: Number of molecules to download
        avg_molecule_size_kb: Average size per molecule in KB
        
    Returns:
        Estimated database size in GB
    """
    estimated_size_kb = num_molecules * avg_molecule_size_kb
    estimated_size_gb = estimated_size_kb / (1024 * 1024)  # Convert to GB
    
    # Add some overhead for indexes, etc.
    estimated_size_gb *= 1.5
    
    return estimated_size_gb

def estimate_download_time(num_molecules, molecules_per_second=40):
    """
    Estimate the download time based on the number of molecules.
    
    Args:
        num_molecules: Number of molecules to download
        molecules_per_second: Average download rate in molecules per second
        
    Returns:
        Estimated download time as a timedelta
    """
    seconds = num_molecules / molecules_per_second
    return timedelta(seconds=seconds)

def monitor_resources(interval=60):
    """
    Monitor system resources during the download.
    
    Args:
        interval: Interval in seconds between resource checks
    """
    # Get initial resource usage
    initial_cpu = psutil.cpu_percent(interval=1)
    initial_memory = psutil.virtual_memory().percent
    
    logger.info(f"Initial CPU usage: {initial_cpu}%")
    logger.info(f"Initial memory usage: {initial_memory}%")
    
    # Start monitoring in a separate thread
    import threading
    stop_monitoring = threading.Event()
    
    def monitor_thread():
        while not stop_monitoring.is_set():
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            logger.info(f"CPU usage: {cpu_percent}%")
            logger.info(f"Memory usage: {memory_percent}%")
            
            # Sleep for the specified interval
            time.sleep(interval)
    
    # Start the monitoring thread
    thread = threading.Thread(target=monitor_thread)
    thread.daemon = True
    thread.start()
    
    return stop_monitoring

def optimize_database(db_path):
    """
    Optimize the database for better performance.
    
    Args:
        db_path: Path to the SQLite database
    """
    logger.info(f"Optimizing database {db_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Set performance optimization pragmas
        cursor.execute('PRAGMA cache_size = 100000')  # Increase cache size to 100MB
        cursor.execute('PRAGMA temp_store = MEMORY')  # Store temp tables in memory
        cursor.execute('PRAGMA journal_mode = WAL')   # Use Write-Ahead Logging
        cursor.execute('PRAGMA synchronous = NORMAL') # Balance safety and performance
        cursor.execute('PRAGMA mmap_size = 1073741824') # Use memory mapping (1GB)
        
        # Analyze tables for query optimization
        cursor.execute('ANALYZE')
        
        # Vacuum to reclaim space and defragment
        logger.info("Vacuuming database (this may take a while)...")
        cursor.execute('VACUUM')
        
        # Update statistics
        cursor.execute('PRAGMA optimize')
        
        logger.info("Database optimization completed.")
        
    except Exception as e:
        logger.error(f"Error optimizing database: {e}")
    finally:
        conn.close()

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Download millions of molecules from PubChem'
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        default='chemesty/data/million_molecules.db',
        help='Path to the output SQLite database file (default: chemesty/data/million_molecules.db)'
    )
    
    parser.add_argument(
        '--num-molecules', 
        type=int, 
        default=1000000,
        help='Number of molecules to download (default: 1,000,000)'
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
        '--no-force-update', 
        action='store_false',
        dest='force_update',
        help='Do not force update if the database already exists (default: force update)'
    )
    
    parser.add_argument(
        '--no-optimize', 
        action='store_false',
        dest='optimize',
        help='Do not optimize the database after download (default: optimize)'
    )
    
    parser.add_argument(
        '--required-space', 
        type=int, 
        default=10,
        help='Required free disk space in GB (default: 10)'
    )
    
    parser.add_argument(
        '--monitor-interval', 
        type=int, 
        default=60,
        help='Interval in seconds between resource monitoring checks (default: 60)'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print("=" * 80)
    print("MILLION MOLECULES DOWNLOADER".center(80))
    print("=" * 80)
    
    # Print configuration
    print(f"Output database: {args.output}")
    print(f"Number of molecules: {args.num_molecules:,}")
    print(f"Starting CID: {args.start_cid}")
    print(f"Batch size: {args.batch_size}")
    print(f"Force update: {args.force_update}")
    print(f"Optimize database: {args.optimize}")
    print(f"Required disk space: {args.required_space} GB")
    print(f"Resource monitoring interval: {args.monitor_interval} seconds")
    print("-" * 80)
    
    # Ensure the database path is properly formatted
    output_path = args.output
    if os.path.dirname(output_path) == '':
        output_path = os.path.join('.', output_path)
    
    # Estimate database size and download time
    estimated_size = estimate_database_size(args.num_molecules)
    estimated_time = estimate_download_time(args.num_molecules)
    
    print(f"Estimated database size: {estimated_size:.2f} GB")
    print(f"Estimated download time: {estimated_time}")
    print("-" * 80)
    
    # Check if there's enough disk space
    if not check_disk_space(os.path.dirname(output_path) or '.', args.required_space):
        print("Error: Not enough disk space available.")
        sys.exit(1)
    
    # Confirm with the user
    if args.num_molecules >= 1000000:
        confirm = input("You are about to download a very large dataset. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Download cancelled.")
            sys.exit(0)
    
    # Start resource monitoring
    stop_monitoring = monitor_resources(args.monitor_interval)
    
    # Start the download
    start_time = time.time()
    print(f"Starting download at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)
    
    try:
        # Download the compounds
        total_inserted, final_count = download_pubchem_compounds(
            db_path=output_path,
            start_cid=args.start_cid,
            max_compounds=args.num_molecules,
            batch_size=args.batch_size,
            force_update=args.force_update
        )
        
        # Stop resource monitoring
        stop_monitoring.set()
        
        # Calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_timedelta = timedelta(seconds=elapsed_time)
        
        print("-" * 80)
        print(f"Download completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Elapsed time: {elapsed_timedelta}")
        print(f"Downloaded and inserted {total_inserted:,} new molecules")
        print(f"Database now contains {final_count:,} molecules")
        
        # Get database size
        conn = sqlite3.connect(output_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA page_count')
        page_count = cursor.fetchone()[0]
        cursor.execute('PRAGMA page_size')
        page_size = cursor.fetchone()[0]
        db_size_mb = page_count * page_size / (1024 * 1024)  # Size in MB
        conn.close()
        
        print(f"Database size: {db_size_mb:.2f} MB ({db_size_mb/1024:.2f} GB)")
        
        # Optimize the database if requested
        if args.optimize:
            print("-" * 80)
            print("Optimizing database...")
            optimize_database(output_path)
        
        print("-" * 80)
        print("Example usage:")
        print(f"  python display_molecules.py --db-path {output_path}")
        print(f"  python display_molecules.py --db-path {output_path} --search 'C6H6'")
        print("=" * 80)
        
    except KeyboardInterrupt:
        # Stop resource monitoring
        stop_monitoring.set()
        
        print("\nDownload interrupted by user.")
        print("You can resume the download later by running the script again.")
        print("The checkpoint file will be used to continue from where you left off.")
        sys.exit(1)
    except Exception as e:
        # Stop resource monitoring
        stop_monitoring.set()
        
        print(f"\nError during download: {e}")
        print("Check the log file for more details.")
        logger.error(f"Error during download: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()