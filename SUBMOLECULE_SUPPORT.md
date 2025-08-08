# Sub-Molecule Support in Chemesty

## Overview

This document describes the implementation of sub-molecule support in the Chemesty package, which allows for the representation of complex molecular formulas with proper parentheses notation, such as Ba(OH)2, Fe(NO3)3, and more complex structures.

## Changes Made

1. **Added `_sub_molecules` List**: Added a list to the Molecule class to store sub-molecules and their multipliers.

2. **Added `add_sub_molecule` Method**: Implemented a method to add a sub-molecule to a molecule with a specified multiplier.

3. **Updated `molecular_formula` Method**: Enhanced the formula generation to properly display sub-molecules with parentheses.

4. **Maintained Compatibility**: Ensured that all existing functionality (charges, phases, etc.) works correctly with sub-molecules.

## Benefits

1. **More Accurate Representation**: Molecules are now displayed with proper chemical notation, including parentheses for sub-molecules.

2. **Improved Readability**: Complex formulas like Ba(OH)2 are more readable than their flat counterparts (H2BaO2).

3. **Support for Nested Structures**: The implementation supports nested sub-molecules, allowing for very complex structures like Ba((CO2)2H2O)3.

4. **Compatibility with Existing Features**: Sub-molecules work seamlessly with existing features like charges and phases.

## Usage Examples

### Basic Example: Barium Hydroxide - Ba(OH)2

```python
from chemesty.elements import *
from chemesty.molecules.molecule import Molecule

# Create the hydroxide (OH) group
oh = O + H

# Create barium hydroxide using the add_sub_molecule method
ba_oh_2 = Molecule()
ba_oh_2 = ba_oh_2 + Ba
ba_oh_2 = ba_oh_2.add_sub_molecule(oh, 2)
print(ba_oh_2)  # Output: Ba(OH)₂
```

### Complex Example: Ammonium Iron(II) Sulfate Hexahydrate - (NH4)2Fe(SO4)2·6H2O

```python
# Create the ammonium (NH4) group
nh4 = N + H*4

# Create the sulfate ion (SO4^2-)
sulfate = Molecule()
sulfate = sulfate + S + O*4
sulfate.charge = -2

# Create water molecule
water = H*2 + O

# Create Mohr's salt
mohr_salt = Molecule()
mohr_salt = mohr_salt.add_sub_molecule(nh4, 2)
mohr_salt = mohr_salt + Fe
mohr_salt = mohr_salt.add_sub_molecule(sulfate, 2)
mohr_salt = mohr_salt.add_sub_molecule(water, 6)
print(mohr_salt)  # Output: Fe(NH₄)₂(SO₄²⁻)₂(H₂O)₆
```

## Comparison with Traditional Approach

| Molecule | With Sub-Molecules | Traditional (Flat) |
|----------|-------------------|-------------------|
| Ba(OH)2  | Ba(OH)₂           | H₂BaO₂            |
| Fe(NO3)3 | Fe(NO₃)₃          | FeN₃O₉            |
| (NH4)2CO3| (NH₄)₂(CO₃)       | C₁H₈N₂O₃          |

## Additional Resources

For more examples and detailed usage, see the `examples/submolecule_examples.py` file in the Chemesty package.