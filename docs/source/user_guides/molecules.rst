Molecules User Guide
=================

This guide provides detailed information on working with molecules in the Chemesty library.

Introduction to Molecules
-----------------------

The molecules module allows you to create, manipulate, and analyze chemical compounds. The core of this module is the ``Molecule`` class, which represents a collection of elements with specific quantities.

Creating Molecules
----------------

There are several ways to create molecules in Chemesty:

From Individual Elements
~~~~~~~~~~~~~~~~~~~~~

You can build molecules by adding elements one by one:

.. code-block:: python

   from chemesty.elements import H, O, C, N
   from chemesty.molecules.molecule import Molecule
   
   # Create a water molecule
   water = Molecule()
   water.add_element(H, 2)
   water.add_element(O, 1)
   
   # Create an ammonia molecule
   ammonia = Molecule()
   ammonia.add_element(N, 1)
   ammonia.add_element(H, 3)
   
   # Create a methane molecule
   methane = Molecule()
   methane.add_element(C, 1)
   methane.add_element(H, 4)

From Chemical Formulas
~~~~~~~~~~~~~~~~~~~

You can create molecules directly from chemical formulas:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Simple molecules
   water = Molecule(formula="H2O")
   ammonia = Molecule(formula="NH3")
   methane = Molecule(formula="CH4")
   
   # More complex molecules
   glucose = Molecule(formula="C6H12O6")
   aspirin = Molecule(formula="C9H8O4")
   caffeine = Molecule(formula="C8H10N4O2")
   
   # Molecules with parentheses
   calcium_carbonate = Molecule(formula="Ca(CO3)")
   ammonium_nitrate = Molecule(formula="NH4(NO3)")

From SMILES Strings
~~~~~~~~~~~~~~~~

You can create molecules from SMILES (Simplified Molecular Input Line Entry System) strings:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create molecules from SMILES
   ethanol = Molecule(smiles="CCO")
   benzene = Molecule(smiles="c1ccccc1")
   aspirin = Molecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O")

Molecule Properties
----------------

Once you have created a molecule, you can access various properties:

Basic Properties
~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   water = Molecule(formula="H2O")
   
   # Get the molecular formula
   print(f"Molecular formula: {water.molecular_formula()}")
   
   # Get the empirical formula (simplest ratio)
   print(f"Empirical formula: {water.empirical_formula()}")
   
   # Get the molecular weight
   print(f"Molecular weight: {water.molecular_weight()} g/mol")
   
   # Get the number of atoms
   print(f"Number of atoms: {water.atom_count()}")
   
   # Get the element composition
   print(f"Element composition: {water.composition()}")

Physical Properties
~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   water = Molecule(formula="H2O")
   
   # Calculate volume
   print(f"Volume: {water.volume()} cm³")
   
   # Calculate density
   print(f"Density: {water.density()} g/cm³")
   
   # Calculate molar volume
   print(f"Molar volume: {water.molar_volume()} cm³/mol")

Manipulating Molecules
-------------------

Chemesty provides several ways to manipulate molecules:

Adding and Removing Elements
~~~~~~~~~~~~~~~~~~~~~~~~~

You can add or remove elements from existing molecules:

.. code-block:: python

   from chemesty.elements import H, O, C
   from chemesty.molecules.molecule import Molecule
   
   # Start with water
   water = Molecule(formula="H2O")
   print(f"Water: {water.molecular_formula()}")
   
   # Add a hydrogen to make H3O+
   water.add_element(H, 1)
   print(f"Hydronium ion: {water.molecular_formula()}")
   
   # Remove a hydrogen to get back to water
   water.remove_element(H, 1)
   print(f"Water again: {water.molecular_formula()}")
   
   # Remove another hydrogen to make OH-
   water.remove_element(H, 1)
   print(f"Hydroxide ion: {water.molecular_formula()}")

Combining Molecules
~~~~~~~~~~~~~~~~

You can combine molecules using the addition operator:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create molecules
   water = Molecule(formula="H2O")
   oxygen = Molecule(formula="O2")
   
   # Combine to form hydrogen peroxide
   hydrogen_peroxide = water + oxygen
   print(f"H2O + O2 = {hydrogen_peroxide.molecular_formula()}")
   
   # Another example: combining methane and oxygen
   methane = Molecule(formula="CH4")
   oxygen = Molecule(formula="O2")
   
   # This would be the reactants in combustion
   combustion_reactants = methane + (oxygen * 2)
   print(f"CH4 + 2O2 = {combustion_reactants.molecular_formula()}")

Scaling Molecules
~~~~~~~~~~~~~~

You can create multiple copies of a molecule using the multiplication operator:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create a water molecule
   water = Molecule(formula="H2O")
   
   # Create a water dimer (H2O)2
   water_dimer = water * 2
   print(f"Water dimer: {water_dimer.molecular_formula()}")
   
   # Create a water hexamer (H2O)6
   water_hexamer = water * 6
   print(f"Water hexamer: {water_hexamer.molecular_formula()}")

Comparing Molecules
----------------

You can compare molecules for equality:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create molecules in different ways
   water1 = Molecule(formula="H2O")
   water2 = Molecule()
   water2.add_element("H", 2)
   water2.add_element("O", 1)
   
   # Check if they're equal
   print(f"water1 == water2: {water1 == water2}")
   
   # Compare with a different molecule
   methane = Molecule(formula="CH4")
   print(f"water1 == methane: {water1 == methane}")
   
   # Check if a molecule is in a list
   molecules = [water1, methane]
   print(f"water2 in molecules: {water2 in molecules}")

Advanced Usage
------------

Working with Complex Molecules
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can work with more complex molecules:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create a complex molecule (glucose)
   glucose = Molecule(formula="C6H12O6")
   
   # Analyze its composition
   composition = glucose.composition()
   for element, count in composition.items():
       print(f"{element}: {count}")
   
   # Calculate the percentage composition
   total_weight = glucose.molecular_weight()
   for element, count in composition.items():
       element_weight = element.atomic_weight * count
       percentage = (element_weight / total_weight) * 100
       print(f"{element.symbol}: {percentage:.2f}%")

Chemical Reactions
~~~~~~~~~~~~~~~

You can model simple chemical reactions:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Combustion of methane: CH4 + 2O2 -> CO2 + 2H2O
   
   # Reactants
   methane = Molecule(formula="CH4")
   oxygen = Molecule(formula="O2")
   
   # Products
   carbon_dioxide = Molecule(formula="CO2")
   water = Molecule(formula="H2O")
   
   # Check mass conservation
   reactants_mass = methane.molecular_weight() + 2 * oxygen.molecular_weight()
   products_mass = carbon_dioxide.molecular_weight() + 2 * water.molecular_weight()
   
   print(f"Reactants mass: {reactants_mass} g/mol")
   print(f"Products mass: {products_mass} g/mol")
   print(f"Difference: {abs(reactants_mass - products_mass)} g/mol")

Best Practices
------------

When working with molecules, follow these best practices:

1. Use the formula constructor for simple molecules
2. Use the element-by-element approach for more control
3. Always check the molecular formula after creation to ensure correctness
4. Use the composition method to analyze the elements in a molecule
5. Remember that molecule operations (addition, multiplication) create new molecules
6. Store important molecules in variables rather than recreating them
7. Use meaningful names for molecule variables
8. Check molecule equality with the == operator, not by comparing formulas as strings