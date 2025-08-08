# Million Molecules Downloader

This document provides instructions for downloading millions of real molecules from PubChem using the Million Molecules Downloader tool.

## Overview

The Million Molecules Downloader is a specialized tool designed for downloading very large datasets (millions of molecules) from PubChem. It includes advanced features such as:

- Efficient batch processing
- Resumable downloads
- Detailed progress reporting
- System resource monitoring
- Database optimization
- Disk space checking

This tool allows you to create a comprehensive database of real chemical compounds for educational purposes, research, or exam preparation.

## Requirements

- Python 3.6 or higher
- PubChemPy library
- SQLite3
- At least 10GB of free disk space (for 1 million molecules)
- Stable internet connection

## Installation

The Million Molecules Downloader is included in the Chemesty package. No additional installation is required if you have already installed Chemesty.

## Usage

### Basic Usage

To download 1 million molecules from PubChem:

```bash
python million_molecules.py
```

This will download 1 million molecules from PubChem, starting from CID 1, and store them in a SQLite database named `million_molecules.db`.

### Advanced Usage

You can customize the download process using various command-line options:

```bash
python million_molecules.py --output custom_database.db --num-molecules 2000000 --start-cid 1000 --batch-size 200
```

#### Command-line Options

- `--output`: Path to the output SQLite database file (default: `million_molecules.db`)
- `--num-molecules`: Number of molecules to download (default: 1,000,000)
- `--start-cid`: CID to start downloading from (default: 1)
- `--batch-size`: Number of compounds to download in each batch (default: 100)
- `--no-force-update`: Do not force update if the database already exists (default: force update)
- `--no-optimize`: Do not optimize the database after download (default: optimize)
- `--required-space`: Required free disk space in GB (default: 10)
- `--monitor-interval`: Interval in seconds between resource monitoring checks (default: 60)

### Resuming Interrupted Downloads

If the download is interrupted (e.g., due to network issues or system shutdown), you can resume it by running the same command again. The downloader will automatically detect the checkpoint file and continue from where it left off.

```bash
python million_molecules.py --output my_database.db
```

## Performance Expectations

Based on our testing, here are the performance expectations for downloading molecules from PubChem:

- **Download Speed**: Approximately 14.5 molecules per second
- **Average Size per Molecule**: About 655 bytes
- **Estimated Time for 1 Million Molecules**: About 19 hours
- **Estimated Database Size for 1 Million Molecules**: About 655 MB

These metrics may vary depending on your internet connection speed, system resources, and PubChem server load.

## Disk Space Requirements

The Million Molecules Downloader checks if there's enough disk space available before starting the download. By default, it requires at least 10GB of free space for a download of 1 million molecules.

You can adjust this requirement using the `--required-space` option:

```bash
python million_molecules.py --required-space 20
```

## System Resource Monitoring

The downloader monitors CPU and memory usage during the download process. This information is logged to the `million_molecules_download.log` file and can be used to diagnose performance issues.

## Database Optimization

After the download is complete, the downloader optimizes the database for better performance by:

- Setting appropriate SQLite pragmas
- Analyzing tables for query optimization
- Vacuuming the database to reclaim space and defragment
- Updating statistics

You can disable this optimization using the `--no-optimize` option if you prefer to optimize the database manually or if you're planning to add more molecules later.

## Troubleshooting

### Download is Too Slow

If the download is too slow, you can try:

1. Increasing the batch size (e.g., `--batch-size 200`)
2. Checking your internet connection
3. Running the download during off-peak hours

### Download Keeps Getting Interrupted

If the download keeps getting interrupted, you can:

1. Check your internet connection stability
2. Reduce the batch size (e.g., `--batch-size 50`)
3. Run the download in smaller chunks (e.g., download 100,000 molecules at a time)

### Not Enough Disk Space

If you don't have enough disk space, you can:

1. Free up disk space by removing unnecessary files
2. Use a different drive with more free space
3. Reduce the number of molecules to download

### Database is Corrupted

If the database becomes corrupted, you can:

1. Delete the database file and the checkpoint file
2. Start the download again
3. If the problem persists, try using a different output location

## Example Queries

Once you have downloaded the molecules, you can query the database using the `display_molecules.py` script:

```bash
# Display all molecules in the database
python display_molecules.py --db-path million_molecules.db

# Search for molecules by formula
python display_molecules.py --db-path million_molecules.db --search "C6H6"

# Search for molecules by name
python display_molecules.py --db-path million_molecules.db --search "benzene"
```

You can also use the database programmatically:

```python
from chemesty.data.database import MoleculeDatabase

# Initialize the database
db = MoleculeDatabase("million_molecules.db")

# Search for molecules by formula
results = db.search_by_formula("C6H6")
for molecule in results:
    print(f"Found: {molecule['name']} ({molecule['formula']})")

# Search for molecules by name
results = db.search_by_name("benzene")
for molecule in results:
    print(f"Found: {molecule['name']} ({molecule['formula']})")

# Close the database connection
db.close()
```

## Advanced Database Usage

### Optimizing the Database Manually

If you want to optimize the database manually, you can use the following SQL commands:

```sql
PRAGMA cache_size = 100000;  -- Increase cache size to 100MB
PRAGMA temp_store = MEMORY;  -- Store temp tables in memory
PRAGMA journal_mode = WAL;   -- Use Write-Ahead Logging
PRAGMA synchronous = NORMAL; -- Balance safety and performance
PRAGMA mmap_size = 1073741824; -- Use memory mapping (1GB)
ANALYZE;                     -- Analyze tables for query optimization
VACUUM;                      -- Reclaim space and defragment
PRAGMA optimize;             -- Update statistics
```

### Creating Custom Indexes

If you frequently search by specific properties, you can create custom indexes to improve performance:

```sql
-- Create an index on molecular weight
CREATE INDEX idx_molecular_weight ON molecules(molecular_weight);

-- Create an index on logP
CREATE INDEX idx_logp ON molecules(logp);

-- Create an index on number of atoms
CREATE INDEX idx_num_atoms ON molecules(num_atoms);
```

## Conclusion

The Million Molecules Downloader provides a powerful and flexible way to download millions of real molecules from PubChem. With its advanced features like resumable downloads, progress tracking, and database optimization, it makes it easy to create a comprehensive database of chemical compounds for educational purposes, research, or exam preparation.

For more information about the molecule database and how to use it, see the [Molecule Database README](MOLECULE_DATABASE_README.md).