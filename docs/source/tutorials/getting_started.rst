Getting Started with Chemesty
=============================

This tutorial will guide you through the basics of using the Chemesty library. By the end of this tutorial, you'll be able to create elements, build molecules, and perform basic chemical calculations.

Learning Objectives
------------------

After completing this tutorial, you will be able to:

- Import and use chemical elements
- Create simple and complex molecules
- Calculate molecular properties
- Understand the basic structure of the Chemesty library

Prerequisites
------------

- Python 3.13+ installed
- Chemesty library installed (``pip install chemesty`` or ``poetry install``)
- Basic understanding of Python programming
- Basic knowledge of chemistry concepts

Step 1: Working with Elements
----------------------------

Let's start by exploring chemical elements, which are the building blocks of all molecules.

Importing Elements
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Import specific elements
   from chemesty.elements import H, O, C, N, Na, Cl
   
   # Create element instances
   hydrogen = H()
   oxygen = O()
   carbon = C()
   
   print(f"Hydrogen symbol: {hydrogen.symbol}")
   print(f"Oxygen atomic number: {oxygen.atomic_number}")
   print(f"Carbon atomic mass: {carbon.atomic_mass}")

**Expected Output:**

.. code-block:: text

   Hydrogen symbol: H
   Oxygen atomic number: 8
   Carbon atomic mass: 12.011

Exploring Element Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import Fe, Au, He
   
   # Create elements
   iron = Fe()
   gold = Au()
   helium = He()
   
   # Check element categories
   print(f"Iron is a metal: {iron.is_metal()}")
   print(f"Gold is a metal: {gold.is_metal()}")
   print(f"Helium is a noble gas: {helium.is_noble_gas()}")
   
   # Compare elements
   print(f"Iron atomic number < Gold atomic number: {iron.atomic_number < gold.atomic_number}")

**Expected Output:**

.. code-block:: text

   Iron is a metal: True
   Gold is a metal: True
   Helium is a noble gas: True
   Iron atomic number < Gold atomic number: True

Step 2: Creating Molecules
-------------------------

Now let's learn how to create molecules from elements.

Simple Molecules
~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import H, O, C
   from chemesty.molecules.molecule import Molecule
   
   # Create water (H2O)
   water = Molecule(formula="H2O")
   print(f"Water formula: {water.molecular_formula()}")
   print(f"Water molecular weight: {water.molecular_weight():.2f} g/mol")
   
   # Create methane (CH4)
   methane = Molecule(formula="CH4")
   print(f"Methane formula: {methane.molecular_formula()}")
   print(f"Methane molecular weight: {methane.molecular_weight():.2f} g/mol")

**Expected Output:**

.. code-block:: text

   Water formula: H2O
   Water molecular weight: 18.02 g/mol
   Methane formula: CH4
   Methane molecular weight: 16.04 g/mol

Building Molecules Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import C, H, O
   from chemesty.molecules.molecule import Molecule
   
   # Create ethanol (C2H5OH) step by step
   ethanol = Molecule()
   ethanol.add_element(C, 2)  # 2 carbon atoms
   ethanol.add_element(H, 6)  # 6 hydrogen atoms
   ethanol.add_element(O, 1)  # 1 oxygen atom
   
   print(f"Ethanol formula: {ethanol.molecular_formula()}")
   print(f"Ethanol composition: {ethanol.composition()}")
   print(f"Ethanol atom count: {ethanol.atom_count()}")

**Expected Output:**

.. code-block:: text

   Ethanol formula: C2H6O
   Ethanol composition: {C: 2, H: 6, O: 1}
   Ethanol atom count: 9

Step 3: Molecular Calculations
-----------------------------

Let's perform some basic calculations with our molecules.

Molecular Weight Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create several molecules
   molecules = {
       "Water": Molecule(formula="H2O"),
       "Carbon Dioxide": Molecule(formula="CO2"),
       "Glucose": Molecule(formula="C6H12O6"),
       "Caffeine": Molecule(formula="C8H10N4O2")
   }
   
   # Calculate and display molecular weights
   print("Molecular Weights:")
   print("-" * 30)
   for name, molecule in molecules.items():
       weight = molecule.molecular_weight()
       print(f"{name:15}: {weight:7.2f} g/mol")

**Expected Output:**

.. code-block:: text

   Molecular Weights:
   ------------------------------
   Water          :   18.02 g/mol
   Carbon Dioxide :   44.01 g/mol
   Glucose        :  180.16 g/mol
   Caffeine       :  194.19 g/mol

Composition Analysis
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Analyze glucose composition
   glucose = Molecule(formula="C6H12O6")
   composition = glucose.composition()
   total_weight = glucose.molecular_weight()
   
   print("Glucose Composition Analysis:")
   print("-" * 35)
   for element, count in composition.items():
       element_weight = element.atomic_mass * count
       percentage = (element_weight / total_weight) * 100
       print(f"{element.symbol}: {count} atoms, {percentage:.1f}% by mass")

**Expected Output:**

.. code-block:: text

   Glucose Composition Analysis:
   -----------------------------------
   C: 6 atoms, 40.0% by mass
   H: 12 atoms, 6.7% by mass
   O: 6 atoms, 53.3% by mass

Step 4: Combining Molecules
--------------------------

Learn how to combine molecules to model chemical reactions.

Molecule Arithmetic
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create reactants for combustion of methane
   methane = Molecule(formula="CH4")
   oxygen = Molecule(formula="O2")
   
   # Combine reactants (CH4 + 2O2)
   reactants = methane + (oxygen * 2)
   print(f"Reactants: {reactants.molecular_formula()}")
   print(f"Reactants weight: {reactants.molecular_weight():.2f} g/mol")
   
   # Create products (CO2 + 2H2O)
   carbon_dioxide = Molecule(formula="CO2")
   water = Molecule(formula="H2O")
   products = carbon_dioxide + (water * 2)
   print(f"Products: {products.molecular_formula()}")
   print(f"Products weight: {products.molecular_weight():.2f} g/mol")
   
   # Check mass conservation
   mass_difference = abs(reactants.molecular_weight() - products.molecular_weight())
   print(f"Mass difference: {mass_difference:.6f} g/mol")

**Expected Output:**

.. code-block:: text

   Reactants: CH4O4
   Reactants weight: 80.04 g/mol
   Products: CO2H4O2
   Products weight: 80.04 g/mol
   Mass difference: 0.000000 g/mol

Step 5: Error Handling and Best Practices
----------------------------------------

Learn how to handle common errors and follow best practices.

Handling Invalid Formulas
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   try:
       # This will work
       valid_molecule = Molecule(formula="H2O")
       print(f"Valid molecule: {valid_molecule.molecular_formula()}")
       
       # This might cause an error with invalid elements
       # invalid_molecule = Molecule(formula="XyZ2")
       
   except ValueError as e:
       print(f"Error creating molecule: {e}")

Best Practices Summary
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import H, O, C, N
   from chemesty.molecules.molecule import Molecule
   
   # 1. Use meaningful variable names
   water_molecule = Molecule(formula="H2O")
   
   # 2. Check molecule properties after creation
   print(f"Created: {water_molecule.molecular_formula()}")
   
   # 3. Store frequently used molecules
   common_molecules = {
       "water": Molecule(formula="H2O"),
       "methane": Molecule(formula="CH4"),
       "oxygen": Molecule(formula="O2")
   }
   
   # 4. Use composition analysis for complex molecules
   complex_molecule = Molecule(formula="C6H12O6")
   if complex_molecule.atom_count() > 10:
       print("This is a complex molecule")
       print(f"Composition: {complex_molecule.composition()}")

Next Steps
----------

Congratulations! You've completed the getting started tutorial. You now know how to:

- Work with chemical elements
- Create and manipulate molecules
- Perform basic molecular calculations
- Handle errors and follow best practices

**What's Next?**

- Try the :doc:`molecular_calculations` tutorial for more advanced calculations
- Explore the :doc:`database_workflows` tutorial to learn about data storage
- Check out the :doc:`chemical_reactions` tutorial for reaction modeling

**Practice Exercises**

1. Create a molecule for table salt (NaCl) and calculate its molecular weight
2. Build aspirin (C9H8O4) step by step and analyze its composition
3. Model the formation of water from hydrogen and oxygen gases
4. Calculate the molecular weight difference between regular water (H2O) and heavy water (D2O)

**Troubleshooting**

If you encounter issues:

- Make sure you have the latest version of Chemesty installed
- Check that your Python version is 3.13 or higher
- Verify that element symbols are correct (case-sensitive)
- Ensure formulas follow standard chemical notation

For more help, consult the :doc:`../user_guides/index` or the API documentation.