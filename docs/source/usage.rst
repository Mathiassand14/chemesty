Usage
=====

This guide provides basic usage examples for Chemesty.

Working with Elements
-------------------

Importing Elements
~~~~~~~~~~~~~~~~

You can import specific elements:

.. code-block:: python

   from chemesty.elements import H, C, O, N

Or import all elements:

.. code-block:: python

   from chemesty.elements import *

Accessing Element Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~

Each element has properties that you can access:

.. code-block:: python

   from chemesty.elements import Fe
   
   iron = Fe()
   print(f"Symbol: {iron.symbol}")
   print(f"Name: {iron.name}")
   print(f"Atomic number: {iron.atomic_number}")
   print(f"Atomic mass: {iron.atomic_mass}")
   print(f"Electron configuration: {iron.electron_configuration}")

Working with Molecules
--------------------

Creating Molecules
~~~~~~~~~~~~~~~~

There are several ways to create molecules:

1. From elements:

.. code-block:: python

   from chemesty.elements import H, O
   from chemesty.molecules.molecule import Molecule
   
   # Create a water molecule
   water = Molecule()
   water.add_element(H, 2)
   water.add_element(O, 1)

2. From a chemical formula:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create a glucose molecule
   glucose = Molecule(formula="C6H12O6")

3. From a SMILES string:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create an ethanol molecule
   ethanol = Molecule(smiles="CCO")

Calculating Molecular Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can calculate various properties of molecules:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   water = Molecule(formula="H2O")
   
   print(f"Molecular formula: {water.molecular_formula()}")
   print(f"Molecular weight: {water.molecular_weight()}")
   print(f"Volume: {water.volume()}")
   print(f"Density: {water.density()}")
   print(f"Molar volume: {water.molar_volume()}")

Combining Molecules
~~~~~~~~~~~~~~~~

You can combine molecules using the + operator:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   water = Molecule(formula="H2O")
   methane = Molecule(formula="CH4")
   
   # Combine water and methane
   mixture = water + methane
   print(f"Mixture formula: {mixture.molecular_formula()}")

Multiplying Molecules
~~~~~~~~~~~~~~~~~~

You can create multiple instances of a molecule using the * operator:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   water = Molecule(formula="H2O")
   
   # Create a water dimer
   water_dimer = water * 2
   print(f"Water dimer formula: {water_dimer.molecular_formula()}")

Working with Databases
--------------------

Creating a Database
~~~~~~~~~~~~~~~~

You can create a database to store molecules:

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   # Create a database
   db = MoleculeDatabase("molecules.db")
   db.initialize()

Storing Molecules
~~~~~~~~~~~~~~

You can store molecules in the database:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   from chemesty.data.database import MoleculeDatabase
   
   # Create a database
   db = MoleculeDatabase("molecules.db")
   db.initialize()
   
   # Create some molecules
   water = Molecule(formula="H2O")
   methane = Molecule(formula="CH4")
   
   # Store molecules
   db.store_molecule("water", water)
   db.store_molecule("methane", methane)

Retrieving Molecules
~~~~~~~~~~~~~~~~~

You can retrieve molecules from the database:

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   # Open the database
   db = MoleculeDatabase("molecules.db")
   
   # Retrieve a molecule
   water = db.get_molecule("water")
   print(f"Water formula: {water.molecular_formula()}")

Searching for Molecules
~~~~~~~~~~~~~~~~~~~~

You can search for molecules by various properties:

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   # Open the database
   db = MoleculeDatabase("molecules.db")
   
   # Search by molecular weight
   small_molecules = db.search_by_molecular_weight(max_weight=50)
   for name, molecule in small_molecules:
       print(f"{name}: {molecule.molecular_formula()}")

Closing the Database
~~~~~~~~~~~~~~~~~

Always close the database when you're done:

.. code-block:: python

   db.close()