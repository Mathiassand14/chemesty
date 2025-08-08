Data Module User Guide
===================

This guide provides detailed information on working with the data module in the Chemesty library.

Introduction to the Data Module
-----------------------------

The data module provides functionality for storing, retrieving, and manipulating chemical data. It includes database operations, molecule lookups, and data downloading capabilities.

Working with Databases
--------------------

The database functionality allows you to store and retrieve molecules in a persistent database.

Creating a Database
~~~~~~~~~~~~~~~~

To create a new database or connect to an existing one:

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   # Create a new database
   db = MoleculeDatabase("molecules.db")
   
   # Initialize the database schema
   db.initialize()

Storing Molecules
~~~~~~~~~~~~~~

You can store molecules in the database with associated metadata:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   from chemesty.data.database import MoleculeDatabase
   
   # Create a database
   db = MoleculeDatabase("molecules.db")
   db.initialize()
   
   # Create some molecules
   water = Molecule(formula="H2O")
   methane = Molecule(formula="CH4")
   glucose = Molecule(formula="C6H12O6")
   
   # Store molecules with names
   db.store_molecule("water", water)
   db.store_molecule("methane", methane)
   db.store_molecule("glucose", glucose)
   
   # Store molecules with additional metadata
   db.store_molecule("water", water, {
       "state": "liquid",
       "boiling_point": 100,
       "melting_point": 0,
       "density": 1.0
   })

Retrieving Molecules
~~~~~~~~~~~~~~~~~

You can retrieve molecules from the database:

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   # Connect to the database
   db = MoleculeDatabase("molecules.db")
   
   # Retrieve a molecule by name
   water = db.get_molecule("water")
   print(f"Retrieved water: {water.molecular_formula()}")
   
   # Retrieve a molecule with its metadata
   water, metadata = db.get_molecule_with_metadata("water")
   print(f"Water boiling point: {metadata.get('boiling_point')} °C")
   
   # Get all molecules
   all_molecules = db.get_all_molecules()
   print(f"Number of molecules in database: {len(all_molecules)}")
   for name, molecule in all_molecules:
       print(f"  {name}: {molecule.molecular_formula()}")

Searching for Molecules
~~~~~~~~~~~~~~~~~~~~

You can search for molecules based on various criteria:

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   # Connect to the database
   db = MoleculeDatabase("molecules.db")
   
   # Search by molecular weight
   small_molecules = db.search_by_molecular_weight(max_weight=50)
   print("Small molecules:")
   for name, molecule in small_molecules:
       print(f"  {name}: {molecule.molecular_formula()}")
   
   # Search by elements
   carbon_molecules = db.search_by_elements(["C"])
   print("Molecules containing carbon:")
   for name, molecule in carbon_molecules:
       print(f"  {name}: {molecule.molecular_formula()}")
   
   # Search by formula pattern
   h2_molecules = db.search_by_formula_pattern("H2*")
   print("Molecules with H2 in formula:")
   for name, molecule in h2_molecules:
       print(f"  {name}: {molecule.molecular_formula()}")
   
   # Search by metadata
   liquids = db.search_by_metadata({"state": "liquid"})
   print("Liquid molecules:")
   for name, molecule in liquids:
       print(f"  {name}: {molecule.molecular_formula()}")

Updating and Deleting Molecules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can update or delete molecules in the database:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   from chemesty.data.database import MoleculeDatabase
   
   # Connect to the database
   db = MoleculeDatabase("molecules.db")
   
   # Update a molecule
   heavy_water = Molecule(formula="D2O")  # Deuterium oxide
   db.update_molecule("water", heavy_water)
   
   # Update metadata
   db.update_metadata("water", {"isotope": "deuterium"})
   
   # Delete a molecule
   db.delete_molecule("methane")
   
   # Check if a molecule exists
   if db.has_molecule("glucose"):
       print("Glucose is in the database")
   
   if not db.has_molecule("methane"):
       print("Methane is not in the database")

Closing the Database
~~~~~~~~~~~~~~~~~

Always close the database when you're done:

.. code-block:: python

   # Close the database connection
   db.close()

Batch Operations
~~~~~~~~~~~~~

For efficiency, you can perform batch operations:

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   from chemesty.data.database import MoleculeDatabase
   
   # Connect to the database
   db = MoleculeDatabase("molecules.db")
   
   # Create multiple molecules
   molecules = {
       "ethanol": Molecule(formula="C2H5OH"),
       "acetone": Molecule(formula="C3H6O"),
       "benzene": Molecule(formula="C6H6"),
       "toluene": Molecule(formula="C7H8")
   }
   
   # Store multiple molecules in a batch
   with db.transaction():
       for name, molecule in molecules.items():
           db.store_molecule(name, molecule)
   
   # Retrieve multiple molecules in a batch
   names = ["ethanol", "acetone", "benzene"]
   batch_molecules = db.get_molecules_batch(names)
   
   # Delete multiple molecules in a batch
   with db.transaction():
       for name in ["benzene", "toluene"]:
           db.delete_molecule(name)

Working with Molecule Lookups
---------------------------

The molecule lookup functionality provides fast access to molecular properties without requiring a full database.

Basic Lookups
~~~~~~~~~~

.. code-block:: python

   from chemesty.data.molecule_lookup import MoleculeLookup
   
   # Create a lookup instance
   lookup = MoleculeLookup()
   
   # Look up properties for common molecules
   water_props = lookup.get_properties("H2O")
   methane_props = lookup.get_properties("CH4")
   
   # Print properties
   print(f"Water boiling point: {water_props.get('boiling_point')} K")
   print(f"Methane density: {methane_props.get('density')} g/cm³")
   
   # Check if a molecule exists in the lookup
   if lookup.has_molecule("C2H5OH"):
       print("Ethanol is in the lookup")

Custom Lookups
~~~~~~~~~~~

You can create custom lookup tables:

.. code-block:: python

   from chemesty.data.molecule_lookup import MoleculeLookup
   
   # Create a custom lookup with your own data
   custom_data = {
       "H2O": {
           "name": "Water",
           "density": 1.0,
           "boiling_point": 373.15,
           "melting_point": 273.15
       },
       "D2O": {
           "name": "Heavy Water",
           "density": 1.11,
           "boiling_point": 374.55,
           "melting_point": 277.0
       }
   }
   
   lookup = MoleculeLookup(custom_data)
   
   # Use the custom lookup
   water = lookup.get_properties("H2O")
   heavy_water = lookup.get_properties("D2O")
   
   print(f"Water density: {water.get('density')} g/cm³")
   print(f"Heavy water density: {heavy_water.get('density')} g/cm³")
   print(f"Density difference: {heavy_water.get('density') - water.get('density')} g/cm³")

Downloading Chemical Data
-----------------------

The download functionality allows you to retrieve chemical data from external sources.

Downloading Element Data
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.download import ChemicalDataDownloader
   
   # Create a downloader
   downloader = ChemicalDataDownloader()
   
   # Download data for a specific element
   hydrogen_data = downloader.download_element_data("H")
   print(f"Downloaded hydrogen data: {hydrogen_data}")
   
   # Download data for multiple elements
   elements = ["C", "N", "O", "F", "P", "S"]
   elements_data = downloader.download_elements_batch(elements)
   
   # Print some properties
   for symbol, data in elements_data.items():
       print(f"{symbol}: Atomic number: {data.get('atomic_number')}, "
             f"Weight: {data.get('atomic_weight')}")

Downloading Molecule Data
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.download import ChemicalDataDownloader
   
   # Create a downloader
   downloader = ChemicalDataDownloader()
   
   # Download data for a specific molecule
   water_data = downloader.download_molecule_data("H2O")
   print(f"Downloaded water data: {water_data}")
   
   # Download data for multiple molecules
   molecules = ["CH4", "CO2", "C2H5OH"]
   molecules_data = downloader.download_molecules_batch(molecules)
   
   # Print some properties
   for formula, data in molecules_data.items():
       print(f"{formula}: Name: {data.get('name')}, "
             f"Molecular weight: {data.get('molecular_weight')}")

Saving Downloaded Data
~~~~~~~~~~~~~~~~~~~

You can save downloaded data for later use:

.. code-block:: python

   import json
   from chemesty.data.download import ChemicalDataDownloader
   
   # Create a downloader
   downloader = ChemicalDataDownloader()
   
   # Download data
   elements_data = downloader.download_elements_batch(["H", "C", "N", "O"])
   
   # Save to a file
   with open("elements_data.json", "w") as f:
       json.dump(elements_data, f, indent=2)
   
   # Load from a file
   with open("elements_data.json", "r") as f:
       loaded_data = json.load(f)
   
   print(f"Loaded data for {len(loaded_data)} elements")

Best Practices
------------

When working with the data module, follow these best practices:

1. Always close database connections when you're done
2. Use transactions for batch operations to improve performance
3. Handle exceptions when downloading data from external sources
4. Cache frequently accessed data using the lookup functionality
5. Use meaningful names for molecules in the database
6. Include relevant metadata when storing molecules
7. Regularly back up your database files
8. Use search functions rather than retrieving all molecules and filtering in code