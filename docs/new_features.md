# New Features in Chemesty

This document describes the new features added to the Chemesty library to enhance the representation and manipulation of chemical formulas and reactions.

## Table of Contents
- [States with @ Operator](#states-with--operator)
- [Subscripted Numbers in Formulas](#subscripted-numbers-in-formulas)
- [Complex Formulas with Parentheses](#complex-formulas-with-parentheses)
- [Combined Features](#combined-features)

## States with @ Operator

The `@` operator has been added to set the physical state/phase of a molecule. This provides a more intuitive syntax compared to setting the `phase` property directly.

### Basic Usage

```python
from chemesty.elements import H, O, Na, Cl
from chemesty.molecules.molecule import Molecule

# Create water molecule
water = H*2 + O

# Set state to liquid using @ operator
water_liquid = water @ 'l'
print(water_liquid)  # Output: H₂O(l)

# Set state to gas
water_gas = water @ 'g'
print(water_gas)  # Output: H₂O(g)

# Set state to solid
water_solid = water @ 's'
print(water_solid)  # Output: H₂O(s)

# Set state to aqueous
water_aqueous = water @ 'aq'
print(water_aqueous)  # Output: H₂O(aq)
```

### Available States

The following states are supported:
- `'s'` - Solid
- `'l'` - Liquid
- `'g'` - Gas
- `'aq'` - Aqueous solution

### Chaining Operations

The `@` operator can be chained with other operations:

```python
# Create a complex molecule and set its state
glucose = C*6 + H*12 + O*6
glucose_aqueous = glucose @ 'aq'
print(glucose_aqueous)  # Output: C₆H₁₂O₆(aq)
```

## Subscripted Numbers in Formulas

Numbers in molecular formulas are now displayed as subscripts, making the formulas more visually accurate.

### Examples

```python
from chemesty.elements import H, O, C, N

# Water (H₂O)
water = H*2 + O
print(water.molecular_formula)  # Output: H₂O

# Carbon dioxide (CO₂)
carbon_dioxide = C + O*2
print(carbon_dioxide.molecular_formula)  # Output: CO₂

# Glucose (C₆H₁₂O₆)
glucose = C*6 + H*12 + O*6
print(glucose.molecular_formula)  # Output: C₆H₁₂O₆

# Ethanol (C₂H₆O)
ethanol = C*2 + H*6 + O
print(ethanol.molecular_formula)  # Output: C₂H₆O
```

## Complex Formulas with Parentheses

The `group` method has been added to support complex formulas with parentheses, such as Fe(NO₃)₃.

### Basic Usage

```python
from chemesty.elements import Fe, N, O

# Create nitrate group (NO₃)
nitrate = N + O*3

# Create iron(III) nitrate - Fe(NO₃)₃
iron_nitrate = Fe + nitrate.group(3)

# Check the elements in the molecule
print(f"Iron atoms: {iron_nitrate.elements[Fe]}")  # Output: Iron atoms: 1
print(f"Nitrogen atoms: {iron_nitrate.elements[N]}")  # Output: Nitrogen atoms: 3
print(f"Oxygen atoms: {iron_nitrate.elements[O]}")  # Output: Oxygen atoms: 9
```

### Nested Groups

You can create complex formulas with nested groups by combining molecules:

```python
from chemesty.elements import N, H, S, O

# Create ammonium group (NH₄)
ammonium = N + H*4

# Create sulfate group (SO₄)
sulfate = S + O*4

# Create ammonium sulfate - (NH₄)₂SO₄
# First create a molecule with the correct elements
ammonium_sulfate = Molecule()
ammonium_sulfate.add_element(N, 2)  # 2 N atoms
ammonium_sulfate.add_element(H, 8)  # 8 H atoms
ammonium_sulfate.add_element(S, 1)  # 1 S atom
ammonium_sulfate.add_element(O, 4)  # 4 O atoms
```

## Combined Features

You can combine all these features to create complex chemical formulas with states:

```python
from chemesty.elements import Fe, N, O

# Create nitrate group (NO₃)
nitrate = N + O*3

# Create iron(III) nitrate - Fe(NO₃)₃
iron_nitrate = Fe + nitrate.group(3)

# Set state to aqueous
iron_nitrate_aqueous = iron_nitrate @ 'aq'
print(iron_nitrate_aqueous)  # Output includes (aq) at the end
```

## Future Enhancements

Future enhancements may include:
- Better support for charges in elements and molecules
- Improved display of complex formulas with parentheses
- Additional operators for other chemical properties

## Conclusion

These new features make the Chemesty library more intuitive and visually accurate for representing chemical formulas and reactions. The `@` operator for states, subscripted numbers in formulas, and support for complex formulas with parentheses all contribute to a more natural and readable syntax for chemical computations.