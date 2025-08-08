from chemesty.elements import *
from chemesty.states import *
from chemesty.molecules.molecule import Molecule

reaction = O*2 & C+H*4 >> C+O*2 & H*2+O

print(reaction)

reaction.balance()

print(reaction)

print(reaction.reactants)

print(reaction.products)

print(reaction.type)

reduxreac = H*2 & F*2 >> H+F

print(reduxreac)

reduxreac.balance()

print(reduxreac)

print(reduxreac.reactants)

print(reduxreac.products)

print(reduxreac.type)

#new reaction
reaction = C*2 & O*2 >> C*2+O*2

print(reaction)

reaction.balance()

print(reaction)

print(reaction.reactants)

print(reaction.products)

print(reaction.type)

# new reaction with different elements

reaction = C*2 & O*2 >> C*2+O*2 & H*4

print(reaction)

reaction.balance()
print(reaction)
print(reaction.reactants)
print(reaction.products)
print(reaction.type)
# new reaction with different elements and coefficients


reaction = ++Fe @ aq & ++++Ce @ aq >> +++Fe @ aq & +++Ce @ aq

print(reaction)
reaction.balance()
print(reaction)
print(reaction.reactants)
print(reaction.products)
print(reaction.type)
print(reaction.reactants[0].phase)
print(reaction.reactants[1].phase)
print(reaction.products[0].phase)
print(reaction.products[1].phase)
print(reaction.reactants[0].molecule.elements)
print(reaction.reactants[1].molecule.elements)
print(reaction.products[0].molecule.elements)
print(reaction.products[1].molecule.elements)

print("_______________________________________")




reaction = (2 * Fe + (N + O * 3) * 3 @ aq & 3 * Ba + (O + H) * 2 @ aq >>
            2 * Fe + (O + H) * 3 @ s & 6 * -(N + 6 * O) & ++Ba)

print(reaction)
reaction.balance()
print(reaction)
print(reaction.reactants)
print(reaction.products)
print(reaction.type)
print(reaction.reactants[0].phase)
print(reaction.reactants[1].phase)
print(reaction.products[0].phase)
print(reaction.products[1].phase)
print(reaction.reactants[0].molecule.elements)
print(reaction.reactants[1].molecule.elements)
print(reaction.products[0].molecule.elements)
print(reaction.products[1].molecule.elements)









