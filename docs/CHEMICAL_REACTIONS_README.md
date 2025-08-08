# Chemical Reactions Database

This document describes the implementation of a database containing common chemical reactions including combustion, acid-base, redox, and other types of reactions that are commonly studied in chemistry.

## Overview

The chemical reactions database is implemented using SQLite and the `ReactionDatabase` class from the Chemesty library. The database stores information about reactions including:

- Name and type of reaction
- Reactants with coefficients and phases
- Products with coefficients and phases
- Reaction conditions (temperature, pressure, catalysts)
- Balance status

## Scripts

Two scripts have been created to manage and interact with the database:

1. `common_reactions.py`: Adds common chemical reactions to the database
2. `display_reactions.py`: Displays and searches for reactions in the database

### Adding Reactions to the Database

The `common_reactions.py` script adds a list of common chemical reactions to the database. The script:

1. Initializes a `ReactionDatabase` with a database file named "common_reactions.db"
2. Creates `Reaction` objects from a list of reaction data
3. Adds the reactions to the database
4. Prints statistics about the database

The list of reactions includes:

- **Combustion Reactions**: Methane, ethane, propane, butane
- **Acid-Base Reactions**: HCl + NaOH, H2SO4 + NaOH, etc.
- **Redox Reactions**: H2 + O2, H2 + F2, Fe + O2, etc.
- **Precipitation Reactions**: AgNO3 + NaCl, etc.
- **Synthesis Reactions**: N2 + H2 → NH3, etc.
- **Decomposition Reactions**: H2O2 → H2O + O2, etc.
- **Double Replacement Reactions**: Na2CO3 + CaCl2 → CaCO3 + 2NaCl, etc.
- **Hydrolysis Reactions**: CH3COOC2H5 + H2O → CH3COOH + C2H5OH, etc.

### Displaying and Searching for Reactions

The `display_reactions.py` script provides functions to:

1. Display all reactions in the database with their properties
2. Display detailed information about a specific reaction
3. Search for reactions based on various criteria (reaction type, reactant, product, name, etc.)

## Usage Examples

### Adding Reactions to the Database

```bash
python common_reactions.py
```

Output:
```
Added 25 reactions to the database.
Database contains 25 reactions.
Reaction types: combustion, acid_base, neutralization, redox, single_replacement, precipitation, synthesis, decomposition, double_replacement, hydrolysis
```

### Displaying All Reactions

```bash
python display_reactions.py
```

Output:
```
Database: common_reactions.db
Total reactions: 25
Total reactants: 58
Total products: 47
Database size: 0.05 MB

Reaction Types:
  combustion: 4
  acid_base: 3
  neutralization: 1
  redox: 3
  single_replacement: 1
  precipitation: 3
  synthesis: 3
  decomposition: 3
  double_replacement: 2
  hydrolysis: 2

--------------------------------------------------------------------------------
ID    Name                           Type                 Equation                                           
-------------------------------------------------------------------------------------------------
1     Methane Combustion             combustion           CH4 + 2 O2 → CO2 + 2 H2O
2     Ethane Combustion              combustion           C2H6 + 3.5 O2 → 2 CO2 + 3 H2O
3     Propane Combustion             combustion           C3H8 + 5 O2 → 3 CO2 + 4 H2O
...
```

### Displaying Reaction Details

```bash
python display_reactions.py --reaction-id 1
```

Output:
```
================================================================================
Reaction ID: 1
Name: Methane Combustion
Type: combustion
Balanced: Yes
Equation: CH4 + 2 O2 → CO2 + 2 H2O

Reactants:
  1 CH4
  2 O2

Products:
  1 CO2
  2 H2O

Element Balance:
  C: 0.000000 (Balanced)
  H: 0.000000 (Balanced)
  O: 0.000000 (Balanced)
================================================================================
```

### Searching for Reactions

#### Search by Reaction Type

```bash
python display_reactions.py --type combustion
```

Output:
```
Found 4 reactions matching the search criteria:
--------------------------------------------------------------------------------
1. Methane Combustion (combustion)
   CH4 + 2 O2 → CO2 + 2 H2O

2. Ethane Combustion (combustion)
   C2H6 + 3.5 O2 → 2 CO2 + 3 H2O

3. Propane Combustion (combustion)
   C3H8 + 5 O2 → 3 CO2 + 4 H2O

4. Butane Combustion (combustion)
   C4H10 + 6.5 O2 → 4 CO2 + 5 H2O
```

#### Search by Reactant

```bash
python display_reactions.py --reactant H2O
```

Output:
```
Found 2 reactions matching the search criteria:
--------------------------------------------------------------------------------
1. Ethyl Acetate Hydrolysis (hydrolysis)
   CH3COOC2H5 + H2O → CH3COOH + C2H5OH [catalyst: H+]

2. Sucrose Hydrolysis (hydrolysis)
   C12H22O11 + H2O → C6H12O6 + C6H12O6 [catalyst: H+]
```

#### Search by Product

```bash
python display_reactions.py --product H2O
```

Output:
```
Found 12 reactions matching the search criteria:
--------------------------------------------------------------------------------
1. Methane Combustion (combustion)
   CH4 + 2 O2 → CO2 + 2 H2O

2. Ethane Combustion (combustion)
   C2H6 + 3.5 O2 → 2 CO2 + 3 H2O

...
```

#### Search by Name

```bash
python display_reactions.py --name "Acid"
```

Output:
```
Found 4 reactions matching the search criteria:
--------------------------------------------------------------------------------
1. Hydrochloric Acid and Sodium Hydroxide (acid_base)
   HCl + NaOH → NaCl + H2O

2. Sulfuric Acid and Sodium Hydroxide (neutralization)
   H2SO4 + 2 NaOH → Na2SO4 + 2 H2O

3. Nitric Acid and Potassium Hydroxide (acid_base)
   HNO3 + KOH → KNO3 + H2O

4. Acetic Acid and Sodium Hydroxide (acid_base)
   CH3COOH + NaOH → CH3COONa + H2O
```

#### Search for Balanced Reactions Only

```bash
python display_reactions.py --balanced-only
```

## Programmatic Usage

### Using the ReactionDatabase Class

You can use the `ReactionDatabase` class directly in your code:

```python
from chemesty.data.reaction_database import ReactionDatabase
from chemesty.reactions.reaction import Reaction

# Initialize the database
db = ReactionDatabase("common_reactions.db")

# Search for reactions by type
combustion_reactions = db.search_reactions(reaction_type="combustion")
for reaction in combustion_reactions:
    print(f"Found: {reaction.name} - {reaction}")

# Search for reactions by reactant
water_reactant_reactions = db.search_reactions(reactant_formula="H2O")
for reaction in water_reactant_reactions:
    print(f"Found: {reaction.name} - {reaction}")

# Get a specific reaction by ID
reaction = db.get_reaction_by_id(1)
print(f"Reaction: {reaction.name}")
print(f"Equation: {reaction}")
print(f"Balanced: {reaction.is_balanced()}")

# Close the database connection
db.close()
```

### Creating and Adding Reactions

You can create and add your own reactions to the database:

```python
from chemesty.data.reaction_database import ReactionDatabase
from chemesty.reactions.reaction import Reaction

# Initialize the database
db = ReactionDatabase("my_reactions.db")

# Create a new reaction
reaction = Reaction(name="Glucose Combustion")

# Add reactants
reaction.add_reactant("C6H12O6", 1.0)
reaction.add_reactant("O2", 6.0)

# Add products
reaction.add_product("CO2", 6.0)
reaction.add_product("H2O", 6.0)

# Balance the reaction (optional)
reaction.balance()

# Add the reaction to the database
reaction_id = db.add_reaction(reaction)
print(f"Added reaction with ID {reaction_id}")

# Close the database connection
db.close()
```

### Creating Reactions with Operator Syntax

The Chemesty library provides an intuitive operator syntax for creating chemical reactions:

```python
from chemesty.elements import *
from chemesty.reactions.reaction import Reaction
from chemesty.data.reaction_database import ReactionDatabase

# Create a reaction using operator syntax
# CH4 + 2O2 → CO2 + 2H2O
reaction = C+H*4 & O*2*2 >> C+O*2 & H*2+O*1

# Balance the reaction (optional)
reaction.balance()

# Print the reaction
print(reaction)  # Output: CH4 + 2 O2 → CO2 + 2 H2O

# Add the reaction to the database
db = ReactionDatabase("my_reactions.db")
reaction_id = db.add_reaction(reaction)
db.close()
```

## Extending the Database

### Adding More Reactions

To add more reactions to the database, you can modify the `COMMON_REACTIONS` list in the `common_reactions.py` script and run it again. The script will add all the reactions to the database.

### Creating Custom Reaction Types

You can create your own reaction types by setting the `type` property of the `Reaction` object:

```python
reaction = Reaction(name="My Custom Reaction")
reaction.add_reactant("A", 1.0)
reaction.add_reactant("B", 1.0)
reaction.add_product("C", 1.0)
reaction.type = "my_custom_type"
```

## Integration with Molecule Database

The reaction database can be integrated with the molecule database to provide a comprehensive chemistry database:

```python
from chemesty.data.database import MoleculeDatabase
from chemesty.data.reaction_database import ReactionDatabase

# Initialize the databases
molecule_db = MoleculeDatabase("common_molecules.db")
reaction_db = ReactionDatabase("common_reactions.db")

# Search for molecules
molecules = molecule_db.search_by_formula("H2O")
for molecule in molecules:
    print(f"Found molecule: {molecule['name']} ({molecule['formula']})")

# Search for reactions involving the molecule
reactions = reaction_db.search_reactions(product_formula="H2O")
for reaction in reactions:
    print(f"Found reaction: {reaction.name} - {reaction}")

# Close the database connections
molecule_db.close()
reaction_db.close()
```

This integration allows you to search for molecules and then find reactions involving those molecules, providing a powerful tool for chemistry education and research.