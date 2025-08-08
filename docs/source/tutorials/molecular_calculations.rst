Advanced Molecular Calculations
===============================

This tutorial covers advanced molecular calculations using the Chemesty library. You'll learn how to perform complex chemical computations, analyze molecular properties, and work with chemical data.

Learning Objectives
------------------

After completing this tutorial, you will be able to:

- Calculate advanced molecular properties
- Perform stoichiometric calculations
- Analyze molecular composition and structure
- Work with empirical and molecular formulas
- Calculate reaction yields and limiting reagents

Prerequisites
------------

- Completion of the :doc:`getting_started` tutorial
- Understanding of basic chemistry concepts (moles, stoichiometry, molecular formulas)
- Familiarity with Python data structures (lists, dictionaries)

Step 1: Advanced Molecular Properties
------------------------------------

Let's explore more sophisticated molecular property calculations.

Molar Mass and Mole Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create molecules for pharmaceutical compounds
   aspirin = Molecule(formula="C9H8O4")
   ibuprofen = Molecule(formula="C13H18O2")
   acetaminophen = Molecule(formula="C8H9NO2")
   
   compounds = {
       "Aspirin": aspirin,
       "Ibuprofen": ibuprofen,
       "Acetaminophen": acetaminophen
   }
   
   print("Pharmaceutical Compound Analysis:")
   print("=" * 50)
   
   for name, compound in compounds.items():
       molar_mass = compound.molecular_weight()
       
       # Calculate number of moles in 1 gram
       moles_per_gram = 1.0 / molar_mass
       
       # Calculate mass of 0.1 moles
       mass_01_moles = 0.1 * molar_mass
       
       print(f"\n{name}:")
       print(f"  Formula: {compound.molecular_formula()}")
       print(f"  Molar mass: {molar_mass:.2f} g/mol")
       print(f"  Moles in 1g: {moles_per_gram:.6f} mol")
       print(f"  Mass of 0.1 mol: {mass_01_moles:.2f} g")

**Expected Output:**

.. code-block:: text

   Pharmaceutical Compound Analysis:
   ==================================================
   
   Aspirin:
     Formula: C9H8O4
     Molar mass: 180.16 g/mol
     Moles in 1g: 0.005551 mol
     Mass of 0.1 mol: 18.02 g
   
   Ibuprofen:
     Formula: C13H18O2
     Molar mass: 206.28 g/mol
     Moles in 1g: 0.004848 mol
     Mass of 0.1 mol: 20.63 g
   
   Acetaminophen:
     Formula: C8H9NO2
     Molar mass: 151.16 g/mol
     Moles in 1g: 0.006615 mol
     Mass of 0.1 mol: 15.12 g

Empirical vs Molecular Formulas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create molecules with different empirical/molecular formulas
   molecules = [
       ("Glucose", "C6H12O6"),
       ("Acetic Acid", "C2H4O2"),
       ("Benzene", "C6H6"),
       ("Acetylene", "C2H2")
   ]
   
   print("Empirical vs Molecular Formula Analysis:")
   print("=" * 55)
   
   for name, formula in molecules:
       molecule = Molecule(formula=formula)
       molecular_formula = molecule.molecular_formula()
       empirical_formula = molecule.empirical_formula()
       
       # Calculate the ratio
       molecular_weight = molecule.molecular_weight()
       
       print(f"\n{name}:")
       print(f"  Molecular formula: {molecular_formula}")
       print(f"  Empirical formula: {empirical_formula}")
       print(f"  Molecular weight: {molecular_weight:.2f} g/mol")
       
       if molecular_formula != empirical_formula:
           print(f"  Different formulas - molecular is a multiple of empirical")
       else:
           print(f"  Same formula - molecular equals empirical")

Step 2: Stoichiometric Calculations
----------------------------------

Learn how to perform stoichiometric calculations for chemical reactions.

Balanced Chemical Equations
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Combustion of propane: C3H8 + 5O2 → 3CO2 + 4H2O
   print("Propane Combustion Analysis:")
   print("C3H8 + 5O2 → 3CO2 + 4H2O")
   print("=" * 40)
   
   # Reactants
   propane = Molecule(formula="C3H8")
   oxygen = Molecule(formula="O2")
   
   # Products
   carbon_dioxide = Molecule(formula="CO2")
   water = Molecule(formula="H2O")
   
   # Calculate masses for balanced equation
   reactant_masses = {
       "C3H8": 1 * propane.molecular_weight(),
       "O2": 5 * oxygen.molecular_weight()
   }
   
   product_masses = {
       "CO2": 3 * carbon_dioxide.molecular_weight(),
       "H2O": 4 * water.molecular_weight()
   }
   
   total_reactants = sum(reactant_masses.values())
   total_products = sum(product_masses.values())
   
   print("Reactant masses:")
   for compound, mass in reactant_masses.items():
       print(f"  {compound}: {mass:.2f} g")
   print(f"Total reactants: {total_reactants:.2f} g")
   
   print("\nProduct masses:")
   for compound, mass in product_masses.items():
       print(f"  {compound}: {mass:.2f} g")
   print(f"Total products: {total_products:.2f} g")
   
   print(f"\nMass conservation check: {abs(total_reactants - total_products):.6f} g difference")

Limiting Reagent Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Synthesis of ammonia: N2 + 3H2 → 2NH3
   print("Ammonia Synthesis - Limiting Reagent Analysis:")
   print("N2 + 3H2 → 2NH3")
   print("=" * 50)
   
   nitrogen = Molecule(formula="N2")
   hydrogen = Molecule(formula="H2")
   ammonia = Molecule(formula="NH3")
   
   # Available amounts (in grams)
   available_n2 = 100.0  # grams
   available_h2 = 50.0   # grams
   
   # Convert to moles
   moles_n2 = available_n2 / nitrogen.molecular_weight()
   moles_h2 = available_h2 / hydrogen.molecular_weight()
   
   print(f"Available N2: {available_n2} g = {moles_n2:.2f} mol")
   print(f"Available H2: {available_h2} g = {moles_h2:.2f} mol")
   
   # Determine limiting reagent
   # From stoichiometry: 1 mol N2 needs 3 mol H2
   h2_needed_for_n2 = moles_n2 * 3
   n2_needed_for_h2 = moles_h2 / 3
   
   print(f"\nStoichiometric analysis:")
   print(f"H2 needed for available N2: {h2_needed_for_n2:.2f} mol")
   print(f"N2 that can react with available H2: {n2_needed_for_h2:.2f} mol")
   
   if h2_needed_for_n2 > moles_h2:
       limiting_reagent = "H2"
       nh3_produced = (moles_h2 / 3) * 2  # 3 mol H2 → 2 mol NH3
   else:
       limiting_reagent = "N2"
       nh3_produced = moles_n2 * 2  # 1 mol N2 → 2 mol NH3
   
   nh3_mass = nh3_produced * ammonia.molecular_weight()
   
   print(f"\nLimiting reagent: {limiting_reagent}")
   print(f"NH3 produced: {nh3_produced:.2f} mol = {nh3_mass:.2f} g")

Step 3: Composition Analysis
---------------------------

Analyze the composition of complex molecules and mixtures.

Percentage Composition
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   def analyze_composition(name, formula):
       """Analyze the percentage composition of a molecule."""
       molecule = Molecule(formula=formula)
       composition = molecule.composition()
       total_weight = molecule.molecular_weight()
       
       print(f"\n{name} ({formula}):")
       print(f"Molecular weight: {total_weight:.2f} g/mol")
       print("Composition by mass:")
       
       for element, count in composition.items():
           element_mass = element.atomic_mass * count
           percentage = (element_mass / total_weight) * 100
           print(f"  {element.symbol}: {count} atoms, {element_mass:.2f} g, {percentage:.1f}%")
   
   # Analyze various compounds
   compounds = [
       ("Caffeine", "C8H10N4O2"),
       ("Vitamin C", "C6H8O6"),
       ("Aspirin", "C9H8O4"),
       ("Glucose", "C6H12O6")
   ]
   
   print("Molecular Composition Analysis:")
   print("=" * 40)
   
   for name, formula in compounds:
       analyze_composition(name, formula)

Molecular Complexity Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   def analyze_complexity(molecules_dict):
       """Analyze the complexity of different molecules."""
       print("Molecular Complexity Analysis:")
       print("=" * 50)
       print(f"{'Molecule':<15} {'Formula':<12} {'Atoms':<6} {'Elements':<9} {'MW':<8}")
       print("-" * 50)
       
       for name, formula in molecules_dict.items():
           molecule = Molecule(formula=formula)
           atom_count = molecule.atom_count()
           element_count = len(molecule.composition())
           molecular_weight = molecule.molecular_weight()
           
           print(f"{name:<15} {formula:<12} {atom_count:<6} {element_count:<9} {molecular_weight:<8.1f}")
   
   # Compare molecules of different complexity
   molecules = {
       "Water": "H2O",
       "Methane": "CH4",
       "Ethanol": "C2H6O",
       "Glucose": "C6H12O6",
       "Caffeine": "C8H10N4O2",
       "Penicillin": "C16H18N2O4S",
       "Cholesterol": "C27H46O",
       "DNA Base A": "C5H5N5"
   }
   
   analyze_complexity(molecules)

Step 4: Chemical Formula Manipulation
------------------------------------

Learn advanced techniques for working with chemical formulas.

Formula Parsing and Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   def validate_and_analyze_formula(formula_string):
       """Validate a chemical formula and provide analysis."""
       try:
           molecule = Molecule(formula=formula_string)
           
           print(f"\n✓ Valid formula: {formula_string}")
           print(f"  Molecular formula: {molecule.molecular_formula()}")
           print(f"  Empirical formula: {molecule.empirical_formula()}")
           print(f"  Molecular weight: {molecule.molecular_weight():.2f} g/mol")
           print(f"  Total atoms: {molecule.atom_count()}")
           
           return True
           
       except Exception as e:
           print(f"\n✗ Invalid formula: {formula_string}")
           print(f"  Error: {str(e)}")
           return False
   
   # Test various formulas
   test_formulas = [
       "H2O",           # Simple valid
       "C6H12O6",       # Complex valid
       "Ca(OH)2",       # With parentheses
       "CuSO4·5H2O",    # Hydrated compound (might not work)
       "H2SO4",         # Acid
       "NaCl",          # Salt
       "C2H5OH",        # Alcohol
   ]
   
   print("Formula Validation Test:")
   print("=" * 30)
   
   valid_count = 0
   for formula in test_formulas:
       if validate_and_analyze_formula(formula):
           valid_count += 1
   
   print(f"\nSummary: {valid_count}/{len(test_formulas)} formulas were valid")

Step 5: Advanced Calculations
----------------------------

Perform sophisticated chemical calculations.

Concentration Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   def calculate_molarity(compound_formula, mass_grams, volume_liters):
       """Calculate molarity of a solution."""
       molecule = Molecule(formula=compound_formula)
       molar_mass = molecule.molecular_weight()
       moles = mass_grams / molar_mass
       molarity = moles / volume_liters
       
       return molarity, moles, molar_mass
   
   # Calculate concentrations for various solutions
   solutions = [
       ("NaCl", 58.44, 1.0),      # 58.44g NaCl in 1L
       ("C6H12O6", 180.16, 0.5),  # 180.16g glucose in 0.5L
       ("H2SO4", 98.08, 2.0),     # 98.08g sulfuric acid in 2L
       ("CaCl2", 110.98, 0.25)    # 110.98g calcium chloride in 0.25L
   ]
   
   print("Solution Concentration Analysis:")
   print("=" * 60)
   print(f"{'Compound':<10} {'Mass(g)':<8} {'Volume(L)':<10} {'Molarity(M)':<12} {'Moles':<8}")
   print("-" * 60)
   
   for formula, mass, volume in solutions:
       molarity, moles, molar_mass = calculate_molarity(formula, mass, volume)
       print(f"{formula:<10} {mass:<8.2f} {volume:<10.2f} {molarity:<12.3f} {moles:<8.3f}")

Dilution Calculations
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def calculate_dilution(initial_molarity, initial_volume, final_volume):
       """Calculate final molarity after dilution using M1V1 = M2V2."""
       final_molarity = (initial_molarity * initial_volume) / final_volume
       dilution_factor = final_volume / initial_volume
       
       return final_molarity, dilution_factor
   
   print("\nDilution Calculations:")
   print("=" * 40)
   
   # Example dilutions
   dilutions = [
       (1.0, 100, 500),    # 1M, 100mL → 500mL
       (0.5, 50, 250),     # 0.5M, 50mL → 250mL
       (2.0, 25, 100),     # 2M, 25mL → 100mL
   ]
   
   print(f"{'Initial M':<10} {'Initial V':<10} {'Final V':<10} {'Final M':<10} {'Dilution':<10}")
   print("-" * 50)
   
   for m1, v1, v2 in dilutions:
       m2, factor = calculate_dilution(m1, v1, v2)
       print(f"{m1:<10.1f} {v1:<10.0f} {v2:<10.0f} {m2:<10.3f} {factor:<10.1f}x")

Practice Problems
----------------

Try these practice problems to test your understanding:

Problem 1: Pharmaceutical Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Calculate the number of molecules in a 325mg aspirin tablet
   from chemesty.molecules.molecule import Molecule
   
   aspirin = Molecule(formula="C9H8O4")
   mass_mg = 325  # mg
   mass_g = mass_mg / 1000  # convert to grams
   
   # Your code here:
   # 1. Calculate moles of aspirin
   # 2. Calculate number of molecules (use Avogadro's number: 6.022e23)
   # 3. Calculate number of carbon atoms in the tablet

Problem 2: Reaction Yield
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Calculate theoretical and percent yield for this reaction:
   # 2Al + 3CuSO4 → Al2(SO4)3 + 3Cu
   # Given: 10g Al, excess CuSO4, actual yield of Cu = 15g
   
   from chemesty.molecules.molecule import Molecule
   
   aluminum = Molecule(formula="Al")  # Note: This might need adjustment
   copper = Molecule(formula="Cu")
   
   # Your code here:
   # 1. Calculate theoretical yield of Cu
   # 2. Calculate percent yield

Best Practices for Advanced Calculations
---------------------------------------

1. **Always validate inputs**: Check that formulas are valid before calculations
2. **Use appropriate significant figures**: Match the precision of your input data
3. **Include units in your calculations**: Keep track of units throughout
4. **Verify mass conservation**: In reaction calculations, check that mass is conserved
5. **Handle edge cases**: Account for limiting reagents and excess reactants
6. **Document your assumptions**: Clearly state any assumptions in your calculations

Next Steps
----------

You've now mastered advanced molecular calculations! You can:

- Calculate complex molecular properties
- Perform stoichiometric analysis
- Analyze molecular composition
- Work with concentrations and dilutions

**Continue Learning:**

- Try the :doc:`database_workflows` tutorial to learn data management
- Explore the :doc:`chemical_reactions` tutorial for reaction modeling
- Check out the :doc:`advanced_analysis` tutorial for specialized techniques

**Additional Resources:**

- Review the :doc:`../user_guides/molecules` for more molecule methods
- Consult chemistry textbooks for theoretical background
- Practice with real-world chemical problems