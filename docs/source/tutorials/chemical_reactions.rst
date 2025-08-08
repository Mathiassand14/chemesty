Chemical Reactions
==================

This tutorial covers modeling and analyzing chemical reactions using the Chemesty library. You'll learn how to represent reactions, balance equations, calculate yields, and analyze reaction mechanisms.

Learning Objectives
------------------

After completing this tutorial, you will be able to:

- Model chemical reactions with reactants and products
- Balance chemical equations
- Calculate theoretical and percent yields
- Analyze reaction stoichiometry
- Work with reaction mechanisms and pathways

Prerequisites
------------

- Completion of the :doc:`getting_started` and :doc:`molecular_calculations` tutorials
- Understanding of chemical reaction principles
- Knowledge of stoichiometry and reaction balancing

Step 1: Representing Chemical Reactions
--------------------------------------

Chemesty provides multiple ways to represent chemical reactions, from traditional explicit methods to intuitive operator syntax.

Intuitive Operator Syntax (NEW)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most natural way to create reactions uses the ``&`` and ``>>`` operators:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create molecules
   methane = Molecule("CH4")
   oxygen = Molecule("O2")
   co2 = Molecule("CO2")
   water = Molecule("H2O")
   
   # Create reaction using intuitive operator syntax
   # CH4 + 2O2 → CO2 + 2H2O
   combustion = (methane & (2, oxygen)) >> (co2 & (2, water))
   
   print(f"Reaction: {combustion}")
   print(f"Balanced: {combustion.is_balanced()}")
   
   # Simple reactions
   water_formation = Molecule("H2") >> Molecule("H2O")
   print(f"Simple reaction: {water_formation}")

**Key Syntax Rules:**

- Use ``&`` to combine reactants or products: ``CH4 & O2``
- Use ``>>`` to create reactions: ``reactants >> products``
- Use ``(coefficient, molecule)`` tuples for stoichiometry: ``(2, O2)``
- Use parentheses for complex expressions: ``(A & B) >> (C & D)``

**For complex cases, use the helper function:**

.. code-block:: python

   from chemesty.molecules.molecule import create_reaction_side
   
   # Photosynthesis: 6CO2 + 6H2O → C6H12O6 + 6O2
   reactants = create_reaction_side((6, Molecule("CO2")), (6, Molecule("H2O")))
   products = create_reaction_side(Molecule("C6H12O6"), (6, Molecule("O2")))
   photosynthesis = reactants >> products
   
   print(f"Photosynthesis: {photosynthesis}")

Traditional Reaction Representation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The traditional explicit approach is still fully supported:

.. code-block:: python

   from chemesty.reactions.reaction import Reaction
   from chemesty.molecules.molecule import Molecule
   
   # Create molecules
   methane = Molecule(formula="CH4")
   oxygen = Molecule(formula="O2")
   carbon_dioxide = Molecule(formula="CO2")
   water = Molecule(formula="H2O")
   
   # Create reaction using traditional method
   combustion = Reaction(name="Methane Combustion")
   combustion.add_reactant(methane, 1)
   combustion.add_reactant(oxygen, 2)
   combustion.add_product(carbon_dioxide, 1)
   combustion.add_product(water, 2)
   
   print(f"Reaction: {combustion}")
   print(f"Balanced: {combustion.is_balanced()}")
   
   # Calculate total reactant and product masses
   reactant_mass = sum(comp.molecule.molecular_weight() * comp.coefficient 
                      for comp in combustion.get_reactants())
   product_mass = sum(comp.molecule.molecular_weight() * comp.coefficient 
                     for comp in combustion.get_products())
   
   print(f"Total reactant mass: {reactant_mass:.2f} g/mol")
   print(f"Total product mass: {product_mass:.2f} g/mol")
   print(f"Mass difference: {abs(reactant_mass - product_mass):.6f} g/mol")

**Expected Output:**

.. code-block:: text

   Reaction: Methane Combustion
   Equation: CH4 + 2O2 → CO2 + 2H2O
   Total reactant mass: 80.04 g/mol
   Total product mass: 80.04 g/mol
   Mass difference: 0.000000 g/mol

Creating a Reaction Class
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   class ChemicalReaction:
       """A class to represent and analyze chemical reactions."""
       
       def __init__(self, name, reactants, products):
           """
           Initialize a chemical reaction.
           
           Args:
               name: Name of the reaction
               reactants: Dictionary of {molecule: coefficient}
               products: Dictionary of {molecule: coefficient}
           """
           self.name = name
           self.reactants = reactants
           self.products = products
       
       def is_balanced(self):
           """Check if the reaction is mass balanced."""
           reactant_mass = sum(mol.molecular_weight() * coeff 
                              for mol, coeff in self.reactants.items())
           product_mass = sum(mol.molecular_weight() * coeff 
                             for mol, coeff in self.products.items())
           return abs(reactant_mass - product_mass) < 1e-6
       
       def get_equation(self):
           """Get the reaction equation as a string."""
           reactant_str = " + ".join(
               f"{coeff if coeff > 1 else ''}{mol.molecular_formula()}"
               for mol, coeff in self.reactants.items()
           )
           product_str = " + ".join(
               f"{coeff if coeff > 1 else ''}{mol.molecular_formula()}"
               for mol, coeff in self.products.items()
           )
           return f"{reactant_str} → {product_str}"
       
       def calculate_yield(self, limiting_reagent_moles):
           """Calculate theoretical yield based on limiting reagent."""
           # Find the limiting reagent coefficient
           limiting_coeff = None
           for mol, coeff in self.reactants.items():
               if limiting_reagent_moles <= 0:
                   continue
               limiting_coeff = coeff
               break
           
           if limiting_coeff is None:
               return {}
           
           # Calculate moles of products formed
           reaction_extent = limiting_reagent_moles / limiting_coeff
           yields = {}
           
           for product, coeff in self.products.items():
               product_moles = reaction_extent * coeff
               product_mass = product_moles * product.molecular_weight()
               yields[product] = {
                   "moles": product_moles,
                   "mass": product_mass
               }
           
           return yields
   
   # Example: Create the methane combustion reaction
   methane = Molecule(formula="CH4")
   oxygen = Molecule(formula="O2")
   carbon_dioxide = Molecule(formula="CO2")
   water = Molecule(formula="H2O")
   
   combustion = ChemicalReaction(
       name="Methane Combustion",
       reactants={methane: 1, oxygen: 2},
       products={carbon_dioxide: 1, water: 2}
   )
   
   print(f"Reaction: {combustion.name}")
   print(f"Equation: {combustion.get_equation()}")
   print(f"Is balanced: {combustion.is_balanced()}")

Step 2: Reaction Stoichiometry
-----------------------------

Learn how to perform stoichiometric calculations for reactions.

Limiting Reagent Analysis
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Synthesis of ammonia: N2 + 3H2 → 2NH3
   nitrogen = Molecule(formula="N2")
   hydrogen = Molecule(formula="H2")
   ammonia = Molecule(formula="NH3")
   
   haber_process = ChemicalReaction(
       name="Haber Process",
       reactants={nitrogen: 1, hydrogen: 3},
       products={ammonia: 2}
   )
   
   # Available reactants (in grams)
   available_reactants = {
       nitrogen: 280.0,  # 280g of N2
       hydrogen: 60.0    # 60g of H2
   }
   
   print("Haber Process Limiting Reagent Analysis")
   print("=" * 45)
   print(f"Equation: {haber_process.get_equation()}")
   
   # Convert masses to moles
   available_moles = {}
   for molecule, mass in available_reactants.items():
       moles = mass / molecule.molecular_weight()
       available_moles[molecule] = moles
       print(f"Available {molecule.molecular_formula()}: {mass}g = {moles:.2f} mol")
   
   # Determine limiting reagent
   limiting_reagent = None
   min_reaction_extent = float('inf')
   
   for molecule, available in available_moles.items():
       required_coeff = haber_process.reactants[molecule]
       reaction_extent = available / required_coeff
       
       print(f"{molecule.molecular_formula()} can support {reaction_extent:.2f} reaction cycles")
       
       if reaction_extent < min_reaction_extent:
           min_reaction_extent = reaction_extent
           limiting_reagent = molecule
   
   print(f"\nLimiting reagent: {limiting_reagent.molecular_formula()}")
   print(f"Maximum reaction extent: {min_reaction_extent:.2f}")
   
   # Calculate theoretical yields
   yields = haber_process.calculate_yield(available_moles[limiting_reagent])
   
   print("\nTheoretical yields:")
   for product, yield_data in yields.items():
       print(f"{product.molecular_formula()}: {yield_data['moles']:.2f} mol = {yield_data['mass']:.2f} g")

Percent Yield Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Continue with the Haber process example
   
   # Actual experimental yield (typically lower than theoretical)
   actual_nh3_mass = 200.0  # grams (actual yield from experiment)
   
   theoretical_nh3_mass = yields[ammonia]["mass"]
   percent_yield = (actual_nh3_mass / theoretical_nh3_mass) * 100
   
   print(f"\nYield Analysis:")
   print(f"Theoretical NH3 yield: {theoretical_nh3_mass:.2f} g")
   print(f"Actual NH3 yield: {actual_nh3_mass:.2f} g")
   print(f"Percent yield: {percent_yield:.1f}%")
   
   # Calculate efficiency
   if percent_yield < 50:
       efficiency = "Poor"
   elif percent_yield < 75:
       efficiency = "Fair"
   elif percent_yield < 90:
       efficiency = "Good"
   else:
       efficiency = "Excellent"
   
   print(f"Reaction efficiency: {efficiency}")

Step 3: Complex Reaction Analysis
--------------------------------

Analyze more complex reactions and reaction networks.

Multi-step Reactions
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Two-step synthesis: A → B → C
   # Step 1: 2A → B + D
   # Step 2: B + E → C + F
   
   # Define molecules
   A = Molecule(formula="C2H4")    # Ethylene
   B = Molecule(formula="C2H5OH")  # Ethanol
   C = Molecule(formula="C2H4O")   # Acetaldehyde
   D = Molecule(formula="H2O")     # Water
   E = Molecule(formula="O2")      # Oxygen
   F = Molecule(formula="H2O")     # Water
   
   # Step 1: Hydration of ethylene
   step1 = ChemicalReaction(
       name="Ethylene Hydration",
       reactants={A: 1, D: 1},  # C2H4 + H2O
       products={B: 1}          # → C2H5OH
   )
   
   # Step 2: Oxidation of ethanol
   step2 = ChemicalReaction(
       name="Ethanol Oxidation",
       reactants={B: 1, E: 0.5},  # C2H5OH + 0.5O2
       products={C: 1, F: 1}      # → C2H4O + H2O
   )
   
   print("Multi-step Synthesis Analysis")
   print("=" * 35)
   print(f"Step 1: {step1.get_equation()}")
   print(f"Step 2: {step2.get_equation()}")
   
   # Calculate overall reaction
   print(f"\nOverall reaction: {A.molecular_formula()} + 0.5{E.molecular_formula()} → {C.molecular_formula()} + {F.molecular_formula()}")
   
   # Starting with 100g of A, calculate final yield of C
   starting_mass_A = 100.0  # grams
   starting_moles_A = starting_mass_A / A.molecular_weight()
   
   print(f"\nStarting material: {starting_mass_A}g of {A.molecular_formula()} = {starting_moles_A:.2f} mol")
   
   # Assume 80% yield for each step
   step1_yield = 0.80
   step2_yield = 0.75
   
   # Calculate step-by-step
   moles_B_theoretical = starting_moles_A  # 1:1 stoichiometry
   moles_B_actual = moles_B_theoretical * step1_yield
   mass_B_actual = moles_B_actual * B.molecular_weight()
   
   moles_C_theoretical = moles_B_actual  # 1:1 stoichiometry
   moles_C_actual = moles_C_theoretical * step2_yield
   mass_C_actual = moles_C_actual * C.molecular_weight()
   
   overall_yield = (moles_C_actual / starting_moles_A) * 100
   
   print(f"\nStep 1 Results:")
   print(f"  Theoretical {B.molecular_formula()}: {moles_B_theoretical:.2f} mol")
   print(f"  Actual {B.molecular_formula()}: {moles_B_actual:.2f} mol ({mass_B_actual:.2f}g)")
   print(f"  Step 1 yield: {step1_yield*100}%")
   
   print(f"\nStep 2 Results:")
   print(f"  Theoretical {C.molecular_formula()}: {moles_C_theoretical:.2f} mol")
   print(f"  Actual {C.molecular_formula()}: {moles_C_actual:.2f} mol ({mass_C_actual:.2f}g)")
   print(f"  Step 2 yield: {step2_yield*100}%")
   
   print(f"\nOverall Results:")
   print(f"  Overall yield: {overall_yield:.1f}%")
   print(f"  Final product: {mass_C_actual:.2f}g of {C.molecular_formula()}")

Competitive Reactions
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Competitive reactions: A can react to form either B or C
   # Reaction 1: A → B (desired product)
   # Reaction 2: A → C (side product)
   
   A = Molecule(formula="C6H6")    # Benzene
   B = Molecule(formula="C6H5NO2") # Nitrobenzene (desired)
   C = Molecule(formula="C6H4N2O4") # Dinitrobenzene (side product)
   
   # Reaction rates (relative)
   k1 = 0.8  # Rate constant for desired reaction
   k2 = 0.2  # Rate constant for side reaction
   
   total_rate = k1 + k2
   selectivity_B = k1 / total_rate
   selectivity_C = k2 / total_rate
   
   print("Competitive Reaction Analysis")
   print("=" * 35)
   print(f"Desired: {A.molecular_formula()} → {B.molecular_formula()}")
   print(f"Side:    {A.molecular_formula()} → {C.molecular_formula()}")
   
   print(f"\nSelectivity:")
   print(f"  {B.molecular_formula()}: {selectivity_B*100:.1f}%")
   print(f"  {C.molecular_formula()}: {selectivity_C*100:.1f}%")
   
   # Calculate product distribution for 100g of A
   starting_mass = 100.0
   starting_moles = starting_mass / A.molecular_weight()
   
   moles_B_formed = starting_moles * selectivity_B
   moles_C_formed = starting_moles * selectivity_C
   
   mass_B_formed = moles_B_formed * B.molecular_weight()
   mass_C_formed = moles_C_formed * C.molecular_weight()
   
   print(f"\nProduct Distribution (from {starting_mass}g {A.molecular_formula()}):")
   print(f"  {B.molecular_formula()}: {moles_B_formed:.2f} mol = {mass_B_formed:.2f}g")
   print(f"  {C.molecular_formula()}: {moles_C_formed:.2f} mol = {mass_C_formed:.2f}g")

Step 4: Reaction Mechanisms
--------------------------

Model and analyze reaction mechanisms.

Elementary Steps
~~~~~~~~~~~~~~~

.. code-block:: python

   # SN2 mechanism: R-X + Nu⁻ → R-Nu + X⁻
   # Example: CH3Br + OH⁻ → CH3OH + Br⁻
   
   from chemesty.molecules.molecule import Molecule
   
   # Define species
   methyl_bromide = Molecule(formula="CH3Br")
   hydroxide = Molecule(formula="OH")  # OH⁻ (simplified)
   methanol = Molecule(formula="CH3OH")
   bromide = Molecule(formula="Br")    # Br⁻ (simplified)
   
   class ElementaryStep:
       """Represents an elementary reaction step."""
       
       def __init__(self, name, reactants, products, rate_constant=None):
           self.name = name
           self.reactants = reactants
           self.products = products
           self.rate_constant = rate_constant
       
       def get_equation(self):
           reactant_str = " + ".join(
               f"{coeff if coeff > 1 else ''}{mol.molecular_formula()}"
               for mol, coeff in self.reactants.items()
           )
           product_str = " + ".join(
               f"{coeff if coeff > 1 else ''}{mol.molecular_formula()}"
               for mol, coeff in self.products.items()
           )
           return f"{reactant_str} → {product_str}"
       
       def calculate_rate(self, concentrations):
           """Calculate reaction rate given concentrations."""
           if self.rate_constant is None:
               return None
           
           rate = self.rate_constant
           for molecule, order in self.reactants.items():
               concentration = concentrations.get(molecule, 0)
               rate *= concentration ** order
           
           return rate
   
   # Define the SN2 mechanism
   sn2_step = ElementaryStep(
       name="SN2 Substitution",
       reactants={methyl_bromide: 1, hydroxide: 1},
       products={methanol: 1, bromide: 1},
       rate_constant=0.1  # L/mol·s
   )
   
   print("SN2 Mechanism Analysis")
   print("=" * 25)
   print(f"Elementary step: {sn2_step.get_equation()}")
   
   # Calculate reaction rate at different concentrations
   concentrations = [
       {methyl_bromide: 0.1, hydroxide: 0.1},  # M
       {methyl_bromide: 0.2, hydroxide: 0.1},
       {methyl_bromide: 0.1, hydroxide: 0.2},
       {methyl_bromide: 0.2, hydroxide: 0.2}
   ]
   
   print("\nRate Analysis:")
   print(f"{'[CH3Br]':<10} {'[OH⁻]':<10} {'Rate (M/s)':<12}")
   print("-" * 35)
   
   for conc in concentrations:
       rate = sn2_step.calculate_rate(conc)
       ch3br_conc = conc[methyl_bromide]
       oh_conc = conc[hydroxide]
       print(f"{ch3br_conc:<10.1f} {oh_conc:<10.1f} {rate:<12.3f}")

Multi-step Mechanisms
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # SN1 mechanism (two steps):
   # Step 1: R-X → R⁺ + X⁻ (slow)
   # Step 2: R⁺ + Nu⁻ → R-Nu (fast)
   
   # Example: (CH3)3CBr → (CH3)3C⁺ + Br⁻
   #          (CH3)3C⁺ + OH⁻ → (CH3)3COH
   
   tert_butyl_bromide = Molecule(formula="C4H9Br")
   tert_butyl_cation = Molecule(formula="C4H9")  # Simplified
   tert_butanol = Molecule(formula="C4H9OH")
   
   # Step 1: Ionization (rate-determining)
   step1 = ElementaryStep(
       name="Ionization",
       reactants={tert_butyl_bromide: 1},
       products={tert_butyl_cation: 1, bromide: 1},
       rate_constant=0.001  # s⁻¹ (slow)
   )
   
   # Step 2: Nucleophilic attack (fast)
   step2 = ElementaryStep(
       name="Nucleophilic Attack",
       reactants={tert_butyl_cation: 1, hydroxide: 1},
       products={tert_butanol: 1},
       rate_constant=1000  # L/mol·s (fast)
   )
   
   class ReactionMechanism:
       """Represents a multi-step reaction mechanism."""
       
       def __init__(self, name, steps):
           self.name = name
           self.steps = steps
       
       def get_overall_equation(self):
           """Get the overall reaction equation."""
           # This is simplified - in practice, you'd need to cancel intermediates
           first_step = self.steps[0]
           last_step = self.steps[-1]
           
           # For this example, manually construct overall equation
           return f"{tert_butyl_bromide.molecular_formula()} + {hydroxide.molecular_formula()} → {tert_butanol.molecular_formula()} + {bromide.molecular_formula()}"
       
       def identify_rate_determining_step(self):
           """Identify the slowest step."""
           slowest_step = min(self.steps, key=lambda s: s.rate_constant or float('inf'))
           return slowest_step
   
   sn1_mechanism = ReactionMechanism(
       name="SN1 Mechanism",
       steps=[step1, step2]
   )
   
   print("\nSN1 Mechanism Analysis")
   print("=" * 25)
   print(f"Overall: {sn1_mechanism.get_overall_equation()}")
   
   print("\nElementary Steps:")
   for i, step in enumerate(sn1_mechanism.steps, 1):
       print(f"  Step {i}: {step.get_equation()} (k = {step.rate_constant})")
   
   rds = sn1_mechanism.identify_rate_determining_step()
   print(f"\nRate-determining step: {rds.name}")
   print("Overall rate depends only on [substrate] (first-order kinetics)")

Step 5: Reaction Databases
-------------------------

Store and manage reaction data systematically.

Creating a Reaction Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   from datetime import datetime
   
   class ReactionDatabase:
       """A simple database for storing chemical reactions."""
       
       def __init__(self):
           self.reactions = {}
       
       def add_reaction(self, reaction_id, reaction_data):
           """Add a reaction to the database."""
           self.reactions[reaction_id] = {
               **reaction_data,
               "added_date": datetime.now().isoformat()
           }
       
       def get_reaction(self, reaction_id):
           """Retrieve a reaction by ID."""
           return self.reactions.get(reaction_id)
       
       def search_by_reactant(self, reactant_formula):
           """Find reactions containing a specific reactant."""
           results = []
           for rid, reaction in self.reactions.items():
               reactants = reaction.get("reactants", {})
               if any(reactant_formula in r for r in reactants.keys()):
                   results.append((rid, reaction))
           return results
       
       def search_by_product(self, product_formula):
           """Find reactions producing a specific product."""
           results = []
           for rid, reaction in self.reactions.items():
               products = reaction.get("products", {})
               if any(product_formula in p for p in products.keys()):
                   results.append((rid, reaction))
           return results
       
       def save_to_file(self, filename):
           """Save database to JSON file."""
           with open(filename, 'w') as f:
               json.dump(self.reactions, f, indent=2)
       
       def load_from_file(self, filename):
           """Load database from JSON file."""
           try:
               with open(filename, 'r') as f:
                   self.reactions = json.load(f)
           except FileNotFoundError:
               print(f"File {filename} not found. Starting with empty database.")
   
   # Create and populate a reaction database
   db = ReactionDatabase()
   
   # Add some common reactions
   reactions_to_add = [
       {
           "id": "combustion_methane",
           "data": {
               "name": "Methane Combustion",
               "equation": "CH4 + 2O2 → CO2 + 2H2O",
               "reactants": {"CH4": 1, "O2": 2},
               "products": {"CO2": 1, "H2O": 2},
               "reaction_type": "combustion",
               "energy_change": -890.3,  # kJ/mol
               "conditions": {"temperature": 298, "pressure": 1}
           }
       },
       {
           "id": "haber_process",
           "data": {
               "name": "Haber Process",
               "equation": "N2 + 3H2 → 2NH3",
               "reactants": {"N2": 1, "H2": 3},
               "products": {"NH3": 2},
               "reaction_type": "synthesis",
               "energy_change": -92.4,  # kJ/mol
               "conditions": {"temperature": 673, "pressure": 200},
               "catalyst": "Fe"
           }
       },
       {
           "id": "water_electrolysis",
           "data": {
               "name": "Water Electrolysis",
               "equation": "2H2O → 2H2 + O2",
               "reactants": {"H2O": 2},
               "products": {"H2": 2, "O2": 1},
               "reaction_type": "decomposition",
               "energy_change": 571.6,  # kJ/mol
               "conditions": {"temperature": 298, "pressure": 1},
               "requires": "electrical energy"
           }
       }
   ]
   
   for reaction in reactions_to_add:
       db.add_reaction(reaction["id"], reaction["data"])
   
   print("Reaction Database Created")
   print("=" * 25)
   print(f"Total reactions: {len(db.reactions)}")
   
   # Search examples
   print("\nSearch Results:")
   
   # Find reactions involving water
   water_reactions = db.search_by_reactant("H2O")
   print(f"\nReactions with H2O as reactant:")
   for rid, reaction in water_reactions:
       print(f"  {rid}: {reaction['equation']}")
   
   # Find reactions producing hydrogen
   hydrogen_reactions = db.search_by_product("H2")
   print(f"\nReactions producing H2:")
   for rid, reaction in hydrogen_reactions:
       print(f"  {rid}: {reaction['equation']}")
   
   # Save database
   db.save_to_file("reactions.json")
   print(f"\nDatabase saved to reactions.json")

Best Practices for Reaction Modeling
-----------------------------------

1. **Always check mass balance**: Ensure atoms are conserved in reactions
2. **Include reaction conditions**: Temperature, pressure, catalysts affect outcomes
3. **Consider side reactions**: Real reactions often have multiple pathways
4. **Use appropriate units**: Be consistent with concentration and rate units
5. **Validate mechanisms**: Ensure elementary steps are chemically reasonable
6. **Document assumptions**: Clearly state any simplifications made
7. **Include error handling**: Account for invalid inputs and edge cases

Common Reaction Types
-------------------

Here are templates for common reaction types:

.. code-block:: python

   # Combustion: Hydrocarbon + O2 → CO2 + H2O
   # Synthesis: A + B → AB
   # Decomposition: AB → A + B
   # Single displacement: A + BC → AC + B
   # Double displacement: AB + CD → AD + CB
   # Acid-base: Acid + Base → Salt + Water
   # Redox: Oxidation and reduction occur simultaneously

Practice Problems
----------------

1. **Aspirin Synthesis**: Model the synthesis of aspirin from salicylic acid and acetic anhydride
2. **Photosynthesis**: Represent the overall photosynthesis reaction and calculate yields
3. **Polymerization**: Model the formation of polyethylene from ethylene monomers
4. **Enzyme Kinetics**: Create a mechanism for enzyme-catalyzed reactions

Next Steps
----------

You've now mastered chemical reaction modeling in Chemesty! You can:

- Represent and analyze chemical reactions
- Perform stoichiometric calculations
- Model reaction mechanisms
- Create reaction databases
- Calculate yields and selectivities

**Continue Learning:**

- Try the :doc:`advanced_analysis` tutorial for specialized analysis techniques
- Review the :doc:`../user_guides/molecules` for more molecular operations
- Explore real-world reaction databases and mechanisms

**Advanced Topics to Explore:**

- Reaction kinetics and rate laws
- Thermodynamic analysis of reactions
- Catalysis and enzyme mechanisms
- Industrial process optimization