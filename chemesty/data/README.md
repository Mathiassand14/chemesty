# Chemesty Data Module

This module provides functionality for downloading, storing, and accessing chemical data.

## Overview

The data module includes:

- Functions for downloading chemical datasets from ChEMBL and PubChem
- A database interface for storing and retrieving molecule data
- A molecule lookup mechanism for finding molecules by various criteria

## Usage

### Downloading Datasets

```python
from chemesty.data import download_chembl_dataset, download_pubchem_subset

# Download the ChEMBL dataset (default)
download_chembl_dataset()

# Or download a subset of PubChem compounds
download_pubchem_subset(max_compounds=5000)
```

### Looking Up Molecules

```python
from chemesty.data import lookup_molecule, MoleculeLookup

# Simple lookup using the convenience function
molecules = lookup_molecule("aspirin")
for molecule in molecules:
    print(f"{molecule.molecular_formula} - {molecule}")

# More advanced lookups using the MoleculeLookup class
with MoleculeLookup() as lookup:
    # Look up by formula
    molecules = lookup.lookup_by_formula("C9H8O4")

    # Look up by name
    molecules = lookup.lookup_by_name("aspirin")

    # Look up by molecular weight
    molecules = lookup.lookup_by_molecular_weight(180.16, tolerance=0.1)

    # Look up by volume (in cubic angstroms)
    molecules = lookup.lookup_by_volume(250.0, tolerance_percent=10.0)

    # Look up by density (in g/cm³)
    molecules = lookup.lookup_by_density(1.3, tolerance_percent=10.0)

    # Look up by molar volume (in cm³/mol)
    molecules = lookup.lookup_by_molar_volume(130.0, tolerance_percent=10.0)

    # Look up by substructure
    molecules = lookup.lookup_by_substructure("c1ccccc1")  # Benzene ring

    # Look up similar molecules
    similar_molecules = lookup.lookup_similar_molecules("CC(=O)OC1=CC=CC=C1C(=O)O")  # Aspirin
    for molecule, similarity in similar_molecules:
        print(f"{molecule.molecular_formula} - {molecule} (similarity: {similarity:.2f})")

    # Access volume and other attributes of molecules
    for molecule in molecules:
        print(f"Volume: {molecule.volume_value:.2f} Å³")
        print(f"Density: {molecule.density_value:.4f} g/cm³")
        print(f"Molar Volume: {molecule.molar_volume:.2f} cm³/mol")
```

## Database Schema

The molecule database uses the following schema:

```sql
CREATE TABLE molecules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    smiles TEXT UNIQUE,
    formula TEXT,
    molecular_weight REAL,
    inchi TEXT,
    logp REAL,
    num_atoms INTEGER,
    num_rings INTEGER,
    volume REAL,
    density REAL,
    molar_volume REAL
);
```

## Implementation Details

The molecule lookup functionality is implemented using a tiered lookup strategy that starts with fast exact matches and falls back to more expensive operations only when necessary:

1. First, try an exact formula match (fastest)
2. Next, try a name search
3. If the query looks like a number, try these searches in order:
   - Molecular weight search
   - Volume search
   - Density search (if the value is within a typical range for molecular density)
   - Molar volume search
4. If the query looks like a SMILES string, try a similarity search
5. As a last resort, try a substructure search

This approach ensures that we get results quickly for common queries while still supporting more complex searches when needed.

### Volume and Related Properties

The database now stores and allows searching by these additional molecular properties:

- **Volume**: The molecular volume in cubic angstroms (Å³), calculated using either RDKit's 3D coordinates or an additive method based on atomic volumes
- **Density**: The molecular density in g/cm³, calculated from the molecular weight and volume
- **Molar Volume**: The molar volume in cm³/mol, calculated as the molecular weight divided by the density

These properties are automatically calculated when adding molecules to the database if they are not explicitly provided. They can be accessed as properties of Molecule objects (e.g., `molecule.volume_value`, `molecule.density_value`, `molecule.molar_volume`).
