from chemesty.elements import Fe, Ce
from chemesty.states import aq
import copy
from functools import wraps

def with_charge(charge):
    """
    Decorator to apply a specific charge to an element.
    
    Usage:
        @with_charge(2)
        def get_fe_plus2():
            return copy.deepcopy(Fe)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            element = func(*args, **kwargs)
            element.charge = charge
            return element
        return wrapper
    return decorator

# Create functions that return elements with specific charges
@with_charge(2)
def fe_plus2():
    return copy.deepcopy(Fe)

@with_charge(3)
def fe_plus3():
    return copy.deepcopy(Fe)

@with_charge(4)
def ce_plus4():
    return copy.deepcopy(Ce)

@with_charge(3)
def ce_plus3():
    return copy.deepcopy(Ce)

# Create molecules with phases
fe2_aq = fe_plus2() @ aq
fe3_aq = fe_plus3() @ aq
ce4_aq = ce_plus4() @ aq
ce3_aq = ce_plus3() @ aq

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
