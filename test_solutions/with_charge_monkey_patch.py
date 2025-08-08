from chemesty.elements import Fe, Ce
from chemesty.states import aq
import copy
import types

# Save the original __pos__ method
original_pos = Fe.__class__.__pos__

# Define a new __pos__ method that handles chaining
def chainable_pos(self):
    import copy
    result = copy.deepcopy(self)
    result.charge += 1
    return result

# Monkey patch the __pos__ method
Fe.__class__.__pos__ = chainable_pos
Ce.__class__.__pos__ = chainable_pos

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
    print(f"Fe²⁺ charge: {element.charge}")
for element, count in reaction.reactants[1].molecule.elements.items():
    print(f"Ce⁴⁺ charge: {element.charge}")
for element, count in reaction.products[0].molecule.elements.items():
    print(f"Fe³⁺ charge: {element.charge}")
for element, count in reaction.products[1].molecule.elements.items():
    print(f"Ce³⁺ charge: {element.charge}")

# Restore the original __pos__ method
Fe.__class__.__pos__ = original_pos
Ce.__class__.__pos__ = original_pos
