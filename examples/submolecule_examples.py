"""
Examples of using sub-molecules in the Chemesty package.

This script demonstrates how to create and work with molecules that contain
sub-molecules, such as Ba(OH)2, Fe(NO3)3, and more complex structures.
"""

from chemesty.elements import *
from chemesty.molecules.molecule import Molecule

# Example 1: Creating Barium Hydroxide - Ba(OH)2
print("Example 1: Creating Barium Hydroxide - Ba(OH)2")
# First, create the hydroxide (OH) group
oh = O + H
print(f"Hydroxide group: {oh}")

# Method 1: Using the add_sub_molecule method (recommended)
ba_oh_2 = Molecule()
ba_oh_2 = ba_oh_2 + Ba
ba_oh_2 = ba_oh_2.add_sub_molecule(oh, 2)
print(f"Barium Hydroxide using add_sub_molecule: {ba_oh_2}")

# Method 2: Using the traditional approach (for comparison)
ba_oh_2_flat = Ba + O*2 + H*2
print(f"Barium Hydroxide using flat approach: {ba_oh_2_flat}")
print()

# Example 2: Creating Iron(III) Nitrate - Fe(NO3)3
print("Example 2: Creating Iron(III) Nitrate - Fe(NO3)3")
# First, create the nitrate (NO3) group
no3 = N + O*3
print(f"Nitrate group: {no3}")

# Create Iron(III) Nitrate using the add_sub_molecule method
fe_no3_3 = Molecule()
fe_no3_3 = fe_no3_3 + Fe
fe_no3_3 = fe_no3_3.add_sub_molecule(no3, 3)
print(f"Iron(III) Nitrate: {fe_no3_3}")
print()

# Example 3: Creating Ammonium Carbonate - (NH4)2CO3
print("Example 3: Creating Ammonium Carbonate - (NH4)2CO3")
# Create the ammonium (NH4) group
nh4 = N + H*4
print(f"Ammonium group: {nh4}")

# Create the carbonate (CO3) group
co3 = C + O*3
print(f"Carbonate group: {co3}")

# Create Ammonium Carbonate using the add_sub_molecule method
ammonium_carbonate = Molecule()
ammonium_carbonate = ammonium_carbonate.add_sub_molecule(nh4, 2)
ammonium_carbonate = ammonium_carbonate.add_sub_molecule(co3, 1)
print(f"Ammonium Carbonate: {ammonium_carbonate}")
print()

# Example 4: Creating a complex molecule with nested groups - Ba((CO2)2H2O)3
print("Example 4: Creating a complex molecule with nested groups - Ba((CO2)2H2O)3")
# Create the carbon dioxide (CO2) group
co2 = C + O*2
print(f"Carbon Dioxide group: {co2}")

# Create a complex group (CO2)2H2O
complex_group = Molecule()
complex_group = complex_group.add_sub_molecule(co2, 2)
complex_group = complex_group + H*2 + O
print(f"Complex group (CO2)2H2O: {complex_group}")

# Create the final nested molecule Ba((CO2)2H2O)3
nested_molecule = Molecule()
nested_molecule = nested_molecule + Ba
nested_molecule = nested_molecule.add_sub_molecule(complex_group, 3)
print(f"Nested molecule Ba((CO2)2H2O)3: {nested_molecule}")
print()

# Example 5: Creating molecules with both sub-molecules and charges
print("Example 5: Creating molecules with both sub-molecules and charges")
# Create the carbonate ion (CO3^2-)
carbonate = Molecule()
carbonate = carbonate + C + O*3
carbonate.charge = -2
print(f"Carbonate ion: {carbonate}")

# Create calcium carbonate (CaCO3)
calcium_carbonate = Molecule()
calcium_carbonate = calcium_carbonate + Ca
calcium_carbonate = calcium_carbonate.add_sub_molecule(carbonate, 1)
print(f"Calcium Carbonate: {calcium_carbonate}")
print()

# Example 6: Creating molecules with both sub-molecules and phases
print("Example 6: Creating molecules with both sub-molecules and phases")
# Create calcium hydroxide in solid phase - Ca(OH)2(s)
calcium_hydroxide = Molecule(phase='s')
calcium_hydroxide = calcium_hydroxide + Ca
calcium_hydroxide = calcium_hydroxide.add_sub_molecule(oh, 2)
print(f"Calcium Hydroxide (solid): {calcium_hydroxide}")
print()

# Example 7: Creating a complex salt with multiple sub-molecules
print("Example 7: Creating a complex salt with multiple sub-molecules")
# Create the sulfate ion (SO4^2-)
sulfate = Molecule()
sulfate = sulfate + S + O*4
sulfate.charge = -2
print(f"Sulfate ion: {sulfate}")

# Create the ammonium iron(II) sulfate - (NH4)2Fe(SO4)2·6H2O (Mohr's salt)
mohr_salt = Molecule()
mohr_salt = mohr_salt.add_sub_molecule(nh4, 2)
mohr_salt = mohr_salt + Fe
mohr_salt = mohr_salt.add_sub_molecule(sulfate, 2)
# Add water of crystallization
water = H*2 + O
mohr_salt = mohr_salt.add_sub_molecule(water, 6)
print(f"Ammonium Iron(II) Sulfate Hexahydrate (Mohr's salt): {mohr_salt}")
print()

print("These examples demonstrate how to create and work with molecules that contain sub-molecules.")
print("The add_sub_molecule method allows for creating complex molecular structures with proper")
print("parentheses notation, making the formulas more readable and chemically accurate.")