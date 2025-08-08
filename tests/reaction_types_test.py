from chemesty.elements import *
from chemesty.molecules.molecule import Molecule
from chemesty.reactions.reaction import Reaction

# Test function to create a reaction and print its type
def test_reaction_type(name, reaction):
    print(f"\n--- Testing {name} reaction ---")
    print(f"Reaction: {reaction}")
    reaction.balance()
    print(f"Balanced: {reaction}")
    print(f"Type: {reaction.type}")
    return reaction.type

# 1. Combustion reaction (already tested in test.py)
print("\n=== COMBUSTION REACTION ===")
combustion = O*2 & C+H*4 >> C+O*2 & H*2+O
test_reaction_type("Combustion (Methane)", combustion)

# 2. Redox reaction (already tested in test.py)
print("\n=== REDOX REACTION ===")
redox = H*2 & F*2 >> H+F
test_reaction_type("Redox (Hydrogen-Fluorine)", redox)

# 3. Single replacement/displacement reaction
print("\n=== SINGLE REPLACEMENT REACTION ===")
# Zn + CuSO4 → ZnSO4 + Cu
# Create molecules for this reaction
zn = Molecule("Zn")
cuso4 = Molecule("CuSO4")
znso4 = Molecule("ZnSO4")
cu = Molecule("Cu")

# Create the reaction
single_replacement = Reaction()
single_replacement.add_reactant(zn)
single_replacement.add_reactant(cuso4)
single_replacement.add_product(znso4)
single_replacement.add_product(cu)

test_reaction_type("Single Replacement", single_replacement)

# 4. Double replacement/displacement reaction
print("\n=== DOUBLE REPLACEMENT REACTION ===")
# AgNO3 + NaCl → AgCl + NaNO3
agno3 = Molecule("AgNO3")
nacl = Molecule("NaCl")
agcl = Molecule("AgCl")
nano3 = Molecule("NaNO3")

double_replacement = Reaction()
double_replacement.add_reactant(agno3)
double_replacement.add_reactant(nacl)
double_replacement.add_product(agcl)
double_replacement.add_product(nano3)

test_reaction_type("Double Replacement", double_replacement)

# 5. Acid-base reaction
print("\n=== ACID-BASE REACTION ===")
# HCl + NaOH → NaCl + H2O
hcl = Molecule("HCl")
naoh = Molecule("NaOH")
h2o = Molecule("H2O")

acid_base = Reaction()
acid_base.add_reactant(hcl)
acid_base.add_reactant(naoh)
acid_base.add_product(nacl)
acid_base.add_product(h2o)

test_reaction_type("Acid-Base", acid_base)

# 6. Neutralization reaction (specific type of acid-base)
print("\n=== NEUTRALIZATION REACTION ===")
# H2SO4 + 2NaOH → Na2SO4 + 2H2O
h2so4 = Molecule("H2SO4")
na2so4 = Molecule("Na2SO4")

neutralization = Reaction()
neutralization.add_reactant(h2so4)
neutralization.add_reactant(naoh, 2.0)
neutralization.add_product(na2so4)
neutralization.add_product(h2o, 2.0)

test_reaction_type("Neutralization", neutralization)

# 7. Hydrolysis reaction
print("\n=== HYDROLYSIS REACTION ===")
# CH3COOC2H5 + H2O → CH3COOH + C2H5OH
ester = Molecule("CH3COOC2H5")
acetic_acid = Molecule("CH3COOH")
ethanol = Molecule("C2H5OH")

hydrolysis = Reaction()
hydrolysis.add_reactant(ester)
hydrolysis.add_reactant(h2o)
hydrolysis.add_product(acetic_acid)
hydrolysis.add_product(ethanol)

test_reaction_type("Hydrolysis", hydrolysis)

# 8. Precipitation reaction
print("\n=== PRECIPITATION REACTION ===")
# Pb(NO3)2 + 2KI → PbI2 + 2KNO3
pb_nitrate = Molecule("Pb(NO3)2")
ki = Molecule("KI")
pbi2 = Molecule("PbI2")
kno3 = Molecule("KNO3")

precipitation = Reaction()
precipitation.add_reactant(pb_nitrate)
precipitation.add_reactant(ki, 2.0)
precipitation.add_product(pbi2)
precipitation.add_product(kno3, 2.0)

test_reaction_type("Precipitation", precipitation)

# 9. Synthesis reaction
print("\n=== SYNTHESIS REACTION ===")
# N2 + 3H2 → 2NH3
n2 = Molecule("N2")
h2 = Molecule("H2")
nh3 = Molecule("NH3")

synthesis = Reaction()
synthesis.add_reactant(n2)
synthesis.add_reactant(h2, 3.0)
synthesis.add_product(nh3, 2.0)

test_reaction_type("Synthesis", synthesis)

# 10. Decomposition reaction
print("\n=== DECOMPOSITION REACTION ===")
# 2H2O2 → 2H2O + O2
h2o2 = Molecule("H2O2")

decomposition = Reaction()
decomposition.add_reactant(h2o2, 2.0)
decomposition.add_product(h2o, 2.0)
decomposition.add_product(O*2)

test_reaction_type("Decomposition", decomposition)

# 11. Isomerization reaction
print("\n=== ISOMERIZATION REACTION ===")
# C4H8 (cyclobutane) → C4H8 (butene)
cyclobutane = Molecule("C4H8")
butene = Molecule("C4H8")  # Same formula, different structure

isomerization = Reaction()
isomerization.add_reactant(cyclobutane)
isomerization.add_product(butene)

test_reaction_type("Isomerization", isomerization)

print("\n=== TEST SUMMARY ===")
print("All reaction types have been tested.")