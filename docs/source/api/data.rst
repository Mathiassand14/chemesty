Data Module
==========

This module provides classes and functions for working with chemical data and databases. It enables storage, retrieval, and manipulation of molecular information, as well as integration with external data sources.

Key Features
-----------

* Store and retrieve molecules in a structured database
* Search for molecules based on various properties and criteria
* Download chemical data from external sources
* Efficient lookup of molecular properties
* Data validation and normalization

Database
--------

The database module provides functionality for persistent storage and retrieval of molecular data. It centers around the MoleculeDatabase class which offers a comprehensive API for database operations.

.. automodule:: chemesty.data.database
   :members:
   :undoc-members:
   :show-inheritance:

Key Capabilities
~~~~~~~~~~~~~~

- Create and initialize molecule databases with appropriate schema
- Store molecules with associated metadata and properties
- Retrieve molecules by name, formula, or other identifiers
- Search for molecules based on property ranges or specific criteria
- Update existing molecule information
- Delete molecules from the database
- Perform batch operations for efficiency
- Handle database connections and transactions safely

Molecule Lookup
--------------

The molecule_lookup module provides efficient mechanisms for looking up molecular properties and information without requiring a full database. It's optimized for performance when dealing with frequently accessed data.

.. automodule:: chemesty.data.molecule_lookup
   :members:
   :undoc-members:
   :show-inheritance:

Key Capabilities
~~~~~~~~~~~~~~

- Fast lookup of molecular properties by formula or identifier
- Caching of frequently accessed molecular data
- Memory-efficient storage of molecular information
- Support for custom lookup strategies
- Integration with external data sources

Usage Example
~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.molecule_lookup import MoleculeLookup
   
   # Initialize the lookup system
   lookup = MoleculeLookup()
   
   # Look up properties for common molecules
   water_props = lookup.get_properties("H2O")
   methane_props = lookup.get_properties("CH4")
   
   # Print some properties
   print(f"Water boiling point: {water_props.get('boiling_point')} K")
   print(f"Methane density: {methane_props.get('density')} g/cm³")
   
   # Check if a molecule exists in the lookup
   print(f"Is ethanol in lookup? {lookup.has_molecule('C2H5OH')}")
   
   # Get all available properties for a molecule
   all_water_props = lookup.get_all_properties("H2O")
   print(f"Available properties for water: {list(all_water_props.keys())}")

Download
-------

The download module provides functionality for retrieving chemical data from external sources and integrating it into the Chemesty system. It handles network requests, data parsing, and error handling.

.. automodule:: chemesty.data.download
   :members:
   :undoc-members:
   :show-inheritance:

Key Capabilities
~~~~~~~~~~~~~~

- Download chemical data from various online databases
- Parse and normalize data from different formats
- Handle network errors and retry mechanisms
- Validate downloaded data for integrity
- Convert external data formats to Chemesty's internal representation

Usage Example
~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.download import ChemicalDataDownloader
   
   # Initialize the downloader
   downloader = ChemicalDataDownloader()
   
   # Download data for a specific element
   hydrogen_data = downloader.download_element_data("H")
   print(f"Downloaded hydrogen data: {hydrogen_data}")
   
   # Download data for a specific molecule
   water_data = downloader.download_molecule_data("H2O")
   print(f"Downloaded water data: {water_data}")
   
   # Download a batch of elements
   elements = ["C", "N", "O", "F", "P", "S"]
   batch_data = downloader.download_elements_batch(elements)
   print(f"Downloaded data for {len(batch_data)} elements")
   
   # Save downloaded data to a local file
   downloader.save_data_to_file(batch_data, "elements_data.json")

Example Usage
~~~~~~~~~~~~

.. code-block:: python

   import os
   from chemesty.molecules.molecule import Molecule
   from chemesty.data.database import MoleculeDatabase

   # Create a database
   db_path = "molecules.db"
   db = MoleculeDatabase(db_path)
   db.initialize()

   # Create some molecules
   water = Molecule(formula="H2O")
   methane = Molecule(formula="CH4")
   glucose = Molecule(formula="C6H12O6")

   # Store molecules in the database
   db.store_molecule("water", water)
   db.store_molecule("methane", methane)
   db.store_molecule("glucose", glucose)

   # Retrieve a molecule
   retrieved_water = db.get_molecule("water")
   print(f"Retrieved water formula: {retrieved_water.molecular_formula()}")

   # Search for molecules by property
   small_molecules = db.search_by_molecular_weight(max_weight=50)
   for name, molecule in small_molecules:
       print(f"{name}: {molecule.molecular_formula()}")

   # Clean up
   db.close()
   if os.path.exists(db_path):
       os.remove(db_path)