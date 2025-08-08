Molecules Module
===============

This module provides classes and functions for working with molecules, allowing for the creation, manipulation, and analysis of chemical compounds. It builds upon the elements module to represent complex molecular structures.

Key Features
-----------

* Create molecules from chemical formulas or by adding individual elements
* Calculate molecular properties (weight, volume, density, etc.)
* Combine and manipulate molecules through chemical operations
* Convert between different molecular representations
* Analyze molecular composition and structure

Molecule
--------

The Molecule class is the core of the molecules module. It provides a comprehensive representation of chemical compounds with methods for creation, manipulation, and analysis.

.. automodule:: chemesty.molecules.molecule
   :members:
   :undoc-members:
   :show-inheritance:

Key Capabilities
~~~~~~~~~~~~~~

- Create molecules from chemical formulas or SMILES strings
- Add and remove elements with specific quantities
- Calculate molecular properties (weight, volume, density, etc.)
- Combine molecules through addition operations
- Scale molecules through multiplication operations
- Convert between different molecular representations
- Analyze molecular composition and structure
- Compare molecules for equality and similarity

Example Usage
~~~~~~~~~~~~

Basic Molecule Creation and Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from chemesty.elements import H, O, C, N
   from chemesty.molecules.molecule import Molecule

   # Method 1: Create a molecule by adding elements
   water = Molecule()
   water.add_element(H, 2)
   water.add_element(O, 1)
   
   # Method 2: Create a molecule from a chemical formula
   methane = Molecule(formula="CH4")
   
   # Method 3: Create a molecule using element objects
   ammonia = Molecule()
   ammonia.add_element(N, 1)
   ammonia.add_element(H, 3)
   
   # Calculate basic properties
   print(f"Water molecular formula: {water.molecular_formula()}")
   print(f"Water molecular weight: {water.molecular_weight()} g/mol")
   print(f"Methane empirical formula: {methane.empirical_formula()}")
   print(f"Ammonia density: {ammonia.density()} g/cm³")

Molecule Operations
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from chemesty.elements import H, O, C
   from chemesty.molecules.molecule import Molecule

   # Create molecules
   water = Molecule(formula="H2O")
   oxygen = Molecule(formula="O2")
   
   # Combine molecules (addition)
   hydrogen_peroxide = water + oxygen
   print(f"H2O + O2 = {hydrogen_peroxide.molecular_formula()}")
   
   # Scale molecules (multiplication)
   water_dimer = water * 2
   print(f"H2O × 2 = {water_dimer.molecular_formula()}")
   
   # Remove elements
   water.remove_element(H, 1)
   print(f"H2O - H = {water.molecular_formula()}")
   
   # Compare molecules
   water1 = Molecule(formula="H2O")
   water2 = Molecule(formula="H2O")
   h2o2 = Molecule(formula="H2O2")
   
   print(f"water1 == water2: {water1 == water2}")
   print(f"water1 == h2o2: {water1 == h2o2}")
   print(f"water1 in [water2, h2o2]: {water1 in [water2, h2o2]}")