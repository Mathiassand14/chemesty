from chemesty.elements import Fe, Ce
from chemesty.states import aq
from chemesty.elements.charge import enable_charge_chaining, disable_charge_chaining, with_charge

# Enable charge chaining
original_pos = enable_charge_chaining()

# Now try the operator chaining
fe_plus2 = ++Fe
fe_plus3 = +++Fe
ce_plus4 = ++++Ce
ce_plus3 = +++Ce

print(f"Fe²⁺ charge: {fe_plus2.charge}")
print(f"Fe³⁺ charge: {fe_plus3.charge}")
print(f"Ce⁴⁺ charge: {ce_plus4.charge}")
print(f"Ce³⁺ charge: {ce_plus3.charge}")

# Create molecules with phases
fe2_aq = fe_plus2 @ aq
fe3_aq = fe_plus3 @ aq
ce4_aq = ce_plus4 @ aq
ce3_aq = ce_plus3 @ aq

# Create the reaction
reaction = fe2_aq & ce4_aq >> fe3_aq & ce3_aq

print("Original reaction:")
print(reaction)

print("\nAfter balancing:")
reaction.balance()
print(reaction)

print("\nReactants:")
print(reaction.reactants)

print("\nProducts:")
print(reaction.products)

print("\nReaction type:")
print(reaction.type)

print("\nPhases:")
print(f"Reactant 1 phase: {reaction.reactants[0].phase}")
print(f"Reactant 2 phase: {reaction.reactants[1].phase}")
print(f"Product 1 phase: {reaction.products[0].phase}")
print(f"Product 2 phase: {reaction.products[1].phase}")

print("\nElements in reactants and products:")
print(f"Reactant 1 elements: {reaction.reactants[0].molecule.elements}")
print(f"Reactant 2 elements: {reaction.reactants[1].molecule.elements}")
print(f"Product 1 elements: {reaction.products[0].molecule.elements}")
print(f"Product 2 elements: {reaction.products[1].molecule.elements}")

# Check the charges
print("\nCharges:")
for element, count in reaction.reactants[0].molecule.elements.items():
    print(f"Reactant 1 element charge: {element.charge}")
for element, count in reaction.reactants[1].molecule.elements.items():
    print(f"Reactant 2 element charge: {element.charge}")
for element, count in reaction.products[0].molecule.elements.items():
    print(f"Product 1 element charge: {element.charge}")
for element, count in reaction.products[1].molecule.elements.items():
    print(f"Product 2 element charge: {element.charge}")

# Disable charge chaining
disable_charge_chaining(original_pos)

# Alternative approach using with_charge function
print("\n\nAlternative approach using with_charge function:")
fe_plus2 = with_charge(Fe, 2)
fe_plus3 = with_charge(Fe, 3)
ce_plus4 = with_charge(Ce, 4)
ce_plus3 = with_charge(Ce, 3)

print(f"Fe²⁺ charge: {fe_plus2.charge}")
print(f"Fe³⁺ charge: {fe_plus3.charge}")
print(f"Ce⁴⁺ charge: {ce_plus4.charge}")
print(f"Ce³⁺ charge: {ce_plus3.charge}")

# Create molecules with phases
fe2_aq = fe_plus2 @ aq
fe3_aq = fe_plus3 @ aq
ce4_aq = ce_plus4 @ aq
ce3_aq = ce_plus3 @ aq

# Create the reaction
reaction2 = fe2_aq & ce4_aq >> fe3_aq & ce3_aq

print("Original reaction:")
print(reaction2)

print("\nAfter balancing:")
reaction2.balance()
print(reaction2)

# Check the charges
print("\nCharges:")
for element, count in reaction2.reactants[0].molecule.elements.items():
    print(f"Reactant 1 element charge: {element.charge}")
for element, count in reaction2.reactants[1].molecule.elements.items():
    print(f"Reactant 2 element charge: {element.charge}")
for element, count in reaction2.products[0].molecule.elements.items():
    print(f"Product 1 element charge: {element.charge}")
for element, count in reaction2.products[1].molecule.elements.items():
    print(f"Product 2 element charge: {element.charge}")
