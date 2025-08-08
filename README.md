# Chemesty

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive chemistry package for working with elements, molecules, and chemical datasets.

## Features

- **Element Classes**: Concrete classes for all elements in the periodic table with properties like atomic mass, electron configuration, etc.
- **Molecule Class**: Representation of chemical molecules with support for operations like addition and multiplication.
- **Database Integration**: Tools for downloading and querying chemical datasets.
- **Intuitive API**: Simple and intuitive API for working with chemical elements and molecules.

## Installation

### Development Installation

```bash
# Navigate to the project directory
cd chemesty

# Install with Poetry (includes all dependencies)
poetry install

# For development with additional tools
poetry install --with dev

# Activate the virtual environment
poetry shell
```

### Production Installation

```bash
# Install from local directory
pip install .

# Or install in development mode
pip install -e .
```

## Usage

### Working with Elements

```python
from chemesty.elements.element_factory import ElementFactory

# Get elements by symbol
H = ElementFactory.get_element("H")
O = ElementFactory.get_element("O")
C = ElementFactory.get_element("C")

# Get elements by atomic number
iron = ElementFactory.get_element_by_number(26)
gold = ElementFactory.get_element_by_number(79)

# Access element properties
print(f"Hydrogen: {H}")
print(f"Atomic number: {H.atomic_number}")
print(f"Atomic mass: {H.atomic_mass}")
print(f"Electron configuration: {H.electron_configuration}")
print(f"Is metal: {H.is_metal()}")
```

### Working with Molecules

```python
from chemesty.elements.element_factory import ElementFactory
from chemesty.molecules.molecule import Molecule

# Get elements
H = ElementFactory.get_element("H")
O = ElementFactory.get_element("O")
C = ElementFactory.get_element("C")

# Create water molecule using addition and multiplication
water = 2 * H + O
print(f"Water: {water}")
print(f"Molecular formula: {water.molecular_formula}")
print(f"Molecular weight: {water.molecular_weight:.3f}")

# Create glucose molecule
glucose = 6 * C + 12 * H + 6 * O
print(f"Glucose: {glucose}")
print(f"Molecular formula: {glucose.molecular_formula}")
print(f"Empirical formula: {glucose.empirical_formula}")

# Create molecule from formula
ethanol = Molecule(formula="C2H6O")
print(f"Ethanol: {ethanol}")

# Create molecule from SMILES
aspirin = Molecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O")
print(f"Aspirin: {aspirin}")
```

### Working with Chemical Reactions

Chemesty provides intuitive syntax for creating chemical reactions using `&` and `>>` operators:

```python
from chemesty.molecules.molecule import Molecule

# Create molecules
methane = Molecule("CH4")
oxygen = Molecule("O2")
co2 = Molecule("CO2")
water = Molecule("H2O")

# Create reactions using intuitive operator syntax
combustion = (methane & (2, oxygen)) >> (co2 & (2, water))
print(f"Combustion: {combustion}")
print(f"Balanced: {combustion.is_balanced()}")

# Simple reactions
water_formation = (2, Molecule("H2")) & Molecule("O2") >> (2, Molecule("H2O"))

# Complex reactions with helper function
from chemesty.molecules.molecule import create_reaction_side
reactants = create_reaction_side((6, Molecule("CO2")), (6, Molecule("H2O")))
products = create_reaction_side(Molecule("C6H12O6"), (6, Molecule("O2")))
photosynthesis = reactants >> products
print(f"Photosynthesis: {photosynthesis}")

# Traditional method still available
from chemesty.reactions.reaction import Reaction
traditional = Reaction()
traditional.add_reactant(methane, 1)
traditional.add_reactant(oxygen, 2)
traditional.add_product(co2, 1)
traditional.add_product(water, 2)
print(f"Traditional: {traditional}")
```

### Working with the Database

First, download a dataset:

```bash
# Download the ChEMBL dataset (default)
python -m chemesty.data.download

# Or download a subset of PubChem
python -m chemesty.data.download --source pubchem --limit 10000
```

Then, use the database in your code:

```python
from chemesty.data.database import MoleculeDatabase

# Initialize the database
db = MoleculeDatabase()

# Search by formula
results = db.search_by_formula("C6H12O6")
print(f"Found {len(results)} molecules with formula C6H12O6")

# Search by name
results = db.search_by_name("aspirin")
print(f"Found {len(results)} molecules with 'aspirin' in the name")

# Search by molecular weight
results = db.search_by_molecular_weight(180.16, tolerance=0.1)
print(f"Found {len(results)} molecules with molecular weight around 180.16")

# Search by substructure
results = db.search_by_substructure("c1ccccc1")  # Benzene ring
print(f"Found {len(results)} molecules containing a benzene ring")

# Close the database when done
db.close()
```

## Project Structure

```
chemesty/
├── __init__.py
├── cli/                   # Command-line interface
│   ├── __init__.py
│   └── main.py
├── data/                  # Database and data management
│   ├── __init__.py
│   ├── database.py        # Database access
│   ├── download.py        # Dataset download
│   ├── molecule_lookup.py # Molecule lookup functionality
│   ├── downloads/         # Downloaded datasets
│   └── plugins/           # Data source plugins
├── elements/              # Chemical elements
│   ├── __init__.py
│   ├── atomic_element.py  # Abstract base class
│   ├── element_data.py    # Element property data
│   ├── element_factory.py # Element creation factory
│   ├── element/           # Individual element classes
│   └── utils/             # Element utilities
├── ml/                    # Machine learning integration
├── molecules/             # Molecular modeling
│   ├── __init__.py
│   └── molecule.py        # Molecule class
├── quantum/               # Quantum chemistry calculations
├── reactions/             # Chemical reaction modeling
├── utils/                 # General utilities
└── visualization/         # Molecular visualization
```

## Examples

See the `examples/` directory for more usage examples.

## Dependencies

### Core Dependencies
- Python 3.13+
- OpenMM - Molecular simulation toolkit
- ChemPy - Chemistry in Python
- RDKit - Cheminformatics and machine learning toolkit
- PySCF - Python-based simulations of chemistry framework
- Jupytext - Jupyter notebooks as Markdown documents
- PubChemPy - Python wrapper for the PubChem API
- SymPy - Symbolic mathematics library
- tqdm - Progress bar library
- Requests - HTTP library
- Plotly - Interactive plotting library

### Development Dependencies
- pytest - Testing framework
- pytest-cov - Coverage plugin
- hypothesis - Property-based testing
- sphinx - Documentation generator
- mypy - Static type checker
- flake8 - Code linting
- pre-commit - Git hooks

## License

MIT

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Setting up the development environment
- Code style and testing requirements
- Pull request process
- Documentation standards

For questions or discussions, please review the project documentation and existing issues first.