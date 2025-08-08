# Molecule Database

This document describes the implementation of a database containing common molecules like CO2, NaCl, MgCl2, and others.

## Overview

The molecule database is implemented using SQLite and the `MoleculeDatabase` class from the Chemesty library. The database stores information about molecules including:

- Name
- SMILES representation
- Chemical formula
- Molecular weight
- Number of atoms
- Other properties (volume, density, etc.)

## Scripts

Three scripts have been created to manage and interact with the database:

1. `common_molecules.py`: Adds common molecules to the database
2. `display_molecules.py`: Displays and searches for molecules in the database
3. `download_dataset.py`: Downloads a large dataset of molecules from online sources

### Adding Molecules to the Database

The `common_molecules.py` script adds a list of common molecules to the database. The script:

1. Initializes a `MoleculeDatabase` with a database file named "common_molecules.db"
2. Checks if the molecules are already in the database by searching for their formulas
3. Adds only the molecules that aren't already in the database
4. Prints statistics about the database

The list of molecules includes:

- Carbon Dioxide (CO2)
- Sodium Chloride (NaCl)
- Magnesium Chloride (MgCl2)
- Water (H2O)
- Ammonia (NH3)
- Methane (CH4)
- Hydrogen Peroxide (H2O2)
- Calcium Carbonate (CaCO3)
- Potassium Chloride (KCl)
- Sulfuric Acid (H2SO4)
- Nitric Acid (HNO3)
- Hydrochloric Acid (HCl)
- Sodium Hydroxide (NaOH)
- Calcium Oxide (CaO)
- Magnesium Oxide (MgO)

### Displaying and Searching for Molecules

The `display_molecules.py` script provides functions to:

1. Display all molecules in the database with their properties (formula, name, molecular weight, SMILES)
2. Search for molecules by formula or name

### Downloading Molecules from Online Sources

The `download_dataset.py` script allows you to download a large dataset of molecules from online sources like PubChem and ChEMBL. This gives you access to thousands or even millions of molecules for educational purposes and exam preparation.

The script:

1. Downloads molecule data from PubChem (default) or ChEMBL
2. Processes the data in parallel for better performance
3. Stores the molecules in a SQLite database
4. Provides statistics about the downloaded dataset

#### Command-line Options

The script supports several command-line options:

- `--source`: Source of the dataset (`pubchem` or `chembl`, default: `pubchem`)
- `--max-compounds`: Maximum number of compounds to download (default: 100000)
- `--output`: Path to the output SQLite database file (default: `molecule_dataset.db`)
- `--n-jobs`: Number of parallel jobs to run. -1 means using all processors (default: -1)
- `--no-force-update`: Do not force update if the database already exists (by default, the database will be updated even if it already exists)

## Usage Examples

### Adding Molecules to the Database

```bash
python common_molecules.py
```

Output:
```
Added 15 new molecules to the database.
Database contains 15 molecules.
```

### Downloading Molecules from Online Sources

```bash
# Download 1000 molecules from PubChem
python download_dataset.py --max-compounds 1000 --output pubchem_molecules.db
```

Output:
```
Starting download from pubchem...
Maximum compounds: 1000
Output database: pubchem_molecules.db
Number of parallel jobs: -1
Force update: True
Downloading 1000 compounds from PubChem in 1 batches using 8 processes...
Processing batch chunk 0-1 of 1...
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 8 concurrent workers.
[Parallel(n_jobs=-1)]: Done 1 tasks | elapsed: 2.5s
Inserting compounds from batches 0-1 into the database...
Processing batches: 100%|█████████████████████████| 1/1 [00:00<00:00, 45.63it/s]
PubChem subset downloaded and stored in ./pubchem_molecules.db
Database contains 1000 molecules

Download completed in 3.21 seconds
Dataset downloaded and stored in ./pubchem_molecules.db
Database contains 1000 molecules
Database size: 0.25 MB

Example usage:
  python display_molecules.py --db-path ./pubchem_molecules.db
  python search_molecules.py --db-path ./pubchem_molecules.db --formula 'C6H6'
```

### Displaying and Searching for Molecules

#### Displaying Molecules from the Default Database

```bash
python display_molecules.py
```

Output:
```
Database: common_molecules.db
Total molecules: 45
Database size: 0.04 MB
--------------------------------------------------------------------------------
Formula    Name                      Molecular Weight     SMILES
--------------------------------------------------------------------------------
CH4        Methane                   16.04                C
CO2        Carbon Dioxide            44.01                O=C=O
CaCO3      Calcium Carbonate         100.09               [Ca+2].[C+0]([O-])([O-])=O
CaO        Calcium Oxide             56.08                [Ca+2].[O-2]
H2O        Water                     18.02                O
H2O2       Hydrogen Peroxide         34.01                OO
H2SO4      Sulfuric Acid             98.08                O=S(=O)(O)O
HCl        Hydrochloric Acid         36.46                [H+].[Cl-]
HNO3       Nitric Acid               63.01                O=[N+]([O-])O
KCl        Potassium Chloride        74.55                [K+].[Cl-]
MgCl2      Magnesium Chloride        95.21                [Mg+2].[Cl-].[Cl-]
MgO        Magnesium Oxide           40.30                [Mg+2].[O-2]
NH3        Ammonia                   17.03                N
NaCl       Sodium Chloride           58.44                [Na+].[Cl-]
NaOH       Sodium Hydroxide          40.00                [Na+].[OH-]
...
```

#### Displaying Molecules from a Downloaded Dataset

```bash
python display_molecules.py --db-path pubchem_molecules.db
```

Output:
```
Database: pubchem_molecules.db
Total molecules: 1000
Database size: 0.25 MB
--------------------------------------------------------------------------------
Formula    Name                      Molecular Weight     SMILES
--------------------------------------------------------------------------------
C10H20O5   Compound_10               100.10               C10H20O5
C11H22O5   Compound_11               100.11               C11H22O5
C12H24O6   Compound_12               100.12               C12H24O6
...
```

#### Searching for Molecules

Search in the default database:
```bash
python display_molecules.py --search "Sodium"
```

Output:
```
Results for name search 'Sodium':
  NaCl - Sodium Chloride (58.44)
  NaOH - Sodium Hydroxide (40.00)
  Na2CO3 - Sodium Carbonate (105.99)
  NaHCO3 - Sodium Bicarbonate (84.01)
```

Search in a downloaded dataset:
```bash
python display_molecules.py --db-path pubchem_molecules.db --search "C10"
```

Output:
```
Results for formula search 'C10':
  C10H20O5 - Compound_10 (100.10)
  C100H200O50 - Compound_100 (101.00)
```

## Programmatic Usage

### Using the MoleculeDatabase Class

You can use the `MoleculeDatabase` class directly in your code to work with either the default database or a downloaded dataset:

```python
from chemesty.data.database import MoleculeDatabase

# Initialize the database (default or downloaded)
db = MoleculeDatabase("common_molecules.db")  # or "pubchem_molecules.db"

# Search for a molecule by formula
results = db.search_by_formula("CO2")
for molecule in results:
    print(f"Found: {molecule['name']}")

# Close the database connection
db.close()
```

### Downloading Datasets Programmatically

You can also download datasets programmatically using the `download_dataset` function:

```python
from chemesty.data.download import download_dataset

# Download 10,000 molecules from PubChem
db_path = download_dataset(
    source="pubchem",
    db_path="programmatic_download.db",
    max_compounds=10000,
    n_jobs=-1,  # Use all available processors
    force_update=True
)

print(f"Dataset downloaded to {db_path}")

# Now use the downloaded dataset
from chemesty.data.database import MoleculeDatabase
db = MoleculeDatabase(db_path)

# Get database statistics
stats = db.get_database_stats()
print(f"Downloaded {stats['molecule_count']} molecules")
print(f"Database size: {stats['database_size_mb']:.2f} MB")

# Close the database connection
db.close()
```

## Extending the Database

### Adding More Molecules Manually

To add more molecules to the default database, you can modify the `COMMON_MOLECULES` list in the `common_molecules.py` script and run it again. The script will only add molecules that aren't already in the database.

### Downloading More Molecules

For a much larger collection of molecules, use the `download_dataset.py` script with a higher value for the `--max-compounds` parameter. For example, to download 1 million molecules:

```bash
python download_dataset.py --max-compounds 1000000 --output large_dataset.db
```

This will give you access to a vast collection of molecules for educational purposes and exam preparation.