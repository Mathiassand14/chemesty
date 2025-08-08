from chemesty.elements import Fe, Ce
from chemesty.states import aq
import copy

class ChargedElement:
    """
    A class to create elements with specific charges.
    
    Usage:
        fe_plus2 = ChargedElement(Fe, 2)()
    """
    def __init__(self, element, charge):
        self.element = element
        self.charge = charge
        
    def __call__(self):
        result = copy.deepcopy(self.element)
        result.charge = self.charge
        return result

# Create elements with specific charges
fe_plus2 = ChargedElement(Fe, 2)()
fe_plus3 = ChargedElement(Fe, 3)()
ce_plus4 = ChargedElement(Ce, 4)()
ce_plus3 = ChargedElement(Ce, 3)()

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
