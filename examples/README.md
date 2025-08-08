# Chemesty Examples

This directory contains comprehensive examples demonstrating all major features of the Chemesty library. Each example file focuses on a specific aspect of chemical computation and analysis.

## Available Examples

### 1. Basic Usage (`usage_example.py`)
**What it covers:**
- Element creation and properties
- Basic molecule operations
- Database interactions
- Getting started with Chemesty

**Run with:**
```bash
python examples/usage_example.py
```

### 2. Quantum Chemistry (`quantum_chemistry_examples.py`)
**What it covers:**
- Molecular orbital calculations
- Basis set management
- Quantum property calculations (dipole moment, polarizability, etc.)
- Energy calculations with different methods
- Advanced quantum chemistry concepts

**Run with:**
```bash
python examples/quantum_chemistry_examples.py
```

**Prerequisites:**
- PySCF: `pip install pyscf`
- OpenMM: `pip install openmm`

### 3. Reaction Modeling (`reaction_examples.py`)
**What it covers:**
- Creating and balancing chemical reactions
- Reaction analysis and classification
- Reaction mechanisms and pathways
- Kinetics calculations
- Thermodynamic properties

**Run with:**
```bash
python examples/reaction_examples.py
```

## Running All Examples

To run all examples individually:

```bash
# Run basic usage examples
python examples/usage_example.py

# Run quantum chemistry examples
python examples/quantum_chemistry_examples.py

# Run reaction modeling examples
python examples/reaction_examples.py
```

## Interactive Examples

For interactive exploration, check out the Jupyter notebook tutorial:

- `tutorials/01_getting_started.ipynb` - Interactive introduction to Chemesty

## Prerequisites

### Basic Requirements
All examples require the core Chemesty installation. From the project directory:

```bash
# Install with Poetry (recommended)
poetry install

# Or install with pip in development mode
pip install -e .
```

### Optional Dependencies
For full functionality, install optional dependencies:

```bash
# Quantum chemistry
pip install pyscf openmm

# Visualization
pip install matplotlib rdkit plotly

# Machine learning
pip install scikit-learn pandas numpy

# File formats
pip install openbabel

# Install all optional dependencies individually as needed
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the project root directory or have Chemesty properly installed.

2. **Missing Dependencies**: Some examples require optional dependencies. Install them as needed or run examples that don't require them.

3. **Database Not Found**: Some examples require the chemical database. Download it first:
   ```bash
   python -m chemesty.data.download
   ```

4. **Performance Issues**: Some quantum chemistry calculations can be slow. Start with smaller molecules or reduce the number of iterations.

### Getting Help

- Check the main documentation: `docs/`
- Review the API reference: `docs/source/api/`
- Check the project README.md for general information
- Review the CONTRIBUTING.md for development guidelines

## Contributing Examples

We welcome contributions of new examples! Please:

1. Follow the existing code style and structure
2. Include comprehensive docstrings and comments
3. Add error handling and progress reporting where appropriate
4. Test your examples with different inputs
5. Update this README with your new example

## Example Template

When creating new examples, use this template:

```python
"""
[Feature Name] Examples for Chemesty.

This module demonstrates how to use Chemesty's [feature] capabilities
including [list key features covered].
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def example_function():
    """Example function demonstrating feature usage."""
    print("=== [Example Section] ===")
    
    # Your example code here
    pass

def main():
    """Run all examples."""
    print("Chemesty [Feature] Examples")
    print("=" * 40)
    
    try:
        example_function()
        print("\n✅ Examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
```

## License

These examples are part of the Chemesty project and are subject to the same license terms.