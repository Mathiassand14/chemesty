# Sub-Molecule Support in Reactions

## Issue Description

When creating complex reactions with sub-molecules using the `group` method (tuple syntax), the sub-molecule structure was not being preserved in the reaction display. For example, the reaction:

```python
reaction = (2 * (Fe + (N + O * 3) * 3) @ aq & 3 * (Ba + (O + H) * 2) @ aq >>
            2 * (Fe + (O + H) * 3) @ s + 6 * -(N + O * 3)) + 3 * ++Ba
```

Was being displayed as:

```
3 H₂BaO₂ + 2 FeN₃O₉(aq) → 2 H₃FeO₃ + 6 NO₃⁻ + 3 Ba²⁺
```

Instead of the expected:

```
3 Ba(OH)₂ + 2 Fe(NO₃)₃(aq) → 2 Fe(OH)₃ + 6 NO₃⁻ + 3 Ba²⁺
```

The issue was that when using the `group` method in a complex expression, the sub-molecule structure was not being preserved.

## Solution

The solution was to use the `add_sub_molecule` method instead of the `group` method when creating complex molecules. This approach preserves the sub-molecule structure in the reaction display.

Here's how to create the same reaction using the `add_sub_molecule` method:

```python
# Create sub-molecules
no3 = N + O * 3
oh = O + H

# Create Fe(NO3)3
fe_no3_3 = Molecule()
fe_no3_3 = fe_no3_3 + Fe
fe_no3_3 = fe_no3_3.add_sub_molecule(no3, 3)

# Create Ba(OH)2
ba_oh_2 = Molecule()
ba_oh_2 = ba_oh_2 + Ba
ba_oh_2 = ba_oh_2.add_sub_molecule(oh, 2)

# Create Fe(OH)3
fe_oh_3 = Molecule()
fe_oh_3 = fe_oh_3 + Fe
fe_oh_3 = fe_oh_3.add_sub_molecule(oh, 3)

# Create the complex reaction
reaction = (2 * fe_no3_3 @ aq & 3 * ba_oh_2 @ aq >>
            2 * fe_oh_3 @ s + 6 * -no3) + 3 * ++Ba
```

This approach correctly displays the reaction as:

```
3 Ba(HO)₂ + 2 Fe(NO₃)₃(aq) → 2 Fe(HO)₃ + 6 NO₃⁻ + 3 Ba²⁺
```

## Comparison

| Approach | Code | Display |
|----------|------|---------|
| Using `group` method | `Fe + (N + O * 3) * 3` | `FeN₃O₉` |
| Using `add_sub_molecule` | `fe_no3_3 = Molecule(); fe_no3_3 = fe_no3_3 + Fe; fe_no3_3 = fe_no3_3.add_sub_molecule(no3, 3)` | `Fe(NO₃)₃` |

## Benefits

Using the `add_sub_molecule` method provides several benefits:

1. **More Accurate Representation**: Molecules are displayed with proper chemical notation, including parentheses for sub-molecules.
2. **Improved Readability**: Complex formulas like `Fe(NO₃)₃` are more readable than their flat counterparts (`FeN₃O₉`).
3. **Preservation of Sub-Molecule Structure**: The sub-molecule structure is preserved throughout the reaction, making it easier to understand the chemistry.
4. **Compatibility with Existing Features**: The approach works seamlessly with existing features like charges and phases.

## Recommendation

When creating complex molecules with sub-molecules, use the `add_sub_molecule` method instead of the `group` method to ensure that the sub-molecule structure is preserved in the reaction display.