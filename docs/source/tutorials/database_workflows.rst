Database Workflows
==================

This tutorial covers working with chemical databases in Chemesty. You'll learn how to store, retrieve, search, and manage chemical data efficiently using the database functionality.

Learning Objectives
------------------

After completing this tutorial, you will be able to:

- Create and manage chemical databases
- Store molecules with metadata
- Perform complex searches and queries
- Implement batch operations for efficiency
- Handle database transactions and backups

Prerequisites
------------

- Completion of the :doc:`getting_started` tutorial
- Basic understanding of databases and SQL concepts
- Familiarity with Python file operations

Step 1: Setting Up Your First Database
-------------------------------------

Let's start by creating a chemical database and understanding its structure.

Creating and Initializing a Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   from chemesty.molecules.molecule import Molecule
   
   # Create a new database file
   db = MoleculeDatabase("my_chemicals.db")
   
   # Initialize the database schema
   db.initialize()
   
   print("Database created and initialized successfully!")
   
   # Check if the database is empty
   molecule_count = len(db.get_all_molecules())
   print(f"Current molecule count: {molecule_count}")

**Expected Output:**

.. code-block:: text

   Database created and initialized successfully!
   Current molecule count: 0

Adding Your First Molecules
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   from chemesty.molecules.molecule import Molecule
   
   # Connect to the database
   db = MoleculeDatabase("my_chemicals.db")
   
   # Create some common molecules
   molecules_to_add = [
       ("water", "H2O"),
       ("methane", "CH4"),
       ("carbon_dioxide", "CO2"),
       ("ammonia", "NH3"),
       ("oxygen", "O2")
   ]
   
   # Add molecules to the database
   for name, formula in molecules_to_add:
       molecule = Molecule(formula=formula)
       db.store_molecule(name, molecule)
       print(f"Added {name} ({formula}) to database")
   
   # Verify the molecules were added
   all_molecules = db.get_all_molecules()
   print(f"\nDatabase now contains {len(all_molecules)} molecules:")
   for name, molecule in all_molecules:
       print(f"  {name}: {molecule.molecular_formula()}")
   
   # Don't forget to close the database
   db.close()

Step 2: Working with Metadata
-----------------------------

Enhance your molecules with additional chemical and physical properties.

Storing Molecules with Rich Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   from chemesty.molecules.molecule import Molecule
   
   db = MoleculeDatabase("chemical_properties.db")
   db.initialize()
   
   # Define molecules with comprehensive metadata
   molecules_with_data = [
       {
           "name": "water",
           "formula": "H2O",
           "metadata": {
               "state": "liquid",
               "boiling_point": 100.0,  # Celsius
               "melting_point": 0.0,    # Celsius
               "density": 1.0,          # g/cm³
               "solubility": "miscible",
               "hazard_class": "none",
               "common_name": "Water",
               "uses": ["solvent", "drinking", "industrial"]
           }
       },
       {
           "name": "ethanol",
           "formula": "C2H5OH",
           "metadata": {
               "state": "liquid",
               "boiling_point": 78.4,
               "melting_point": -114.1,
               "density": 0.789,
               "solubility": "miscible",
               "hazard_class": "flammable",
               "common_name": "Ethyl Alcohol",
               "uses": ["solvent", "fuel", "beverage"]
           }
       },
       {
           "name": "sodium_chloride",
           "formula": "NaCl",
           "metadata": {
               "state": "solid",
               "boiling_point": 1465.0,
               "melting_point": 801.0,
               "density": 2.16,
               "solubility": "36g/100mL water",
               "hazard_class": "irritant",
               "common_name": "Table Salt",
               "uses": ["food", "de-icing", "industrial"]
           }
       }
   ]
   
   # Store molecules with metadata
   for mol_data in molecules_with_data:
       molecule = Molecule(formula=mol_data["formula"])
       db.store_molecule(mol_data["name"], molecule, mol_data["metadata"])
       print(f"Stored {mol_data['name']} with metadata")
   
   db.close()

Retrieving and Using Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   db = MoleculeDatabase("chemical_properties.db")
   
   # Retrieve a molecule with its metadata
   water, water_metadata = db.get_molecule_with_metadata("water")
   
   print("Water Properties:")
   print(f"  Formula: {water.molecular_formula()}")
   print(f"  Molecular Weight: {water.molecular_weight():.2f} g/mol")
   print(f"  Boiling Point: {water_metadata.get('boiling_point')}°C")
   print(f"  Density: {water_metadata.get('density')} g/cm³")
   print(f"  Uses: {', '.join(water_metadata.get('uses', []))}")
   
   # Compare properties of different molecules
   molecules_to_compare = ["water", "ethanol", "sodium_chloride"]
   
   print("\nComparison of Physical Properties:")
   print(f"{'Molecule':<15} {'BP (°C)':<10} {'MP (°C)':<10} {'Density':<10}")
   print("-" * 50)
   
   for name in molecules_to_compare:
       molecule, metadata = db.get_molecule_with_metadata(name)
       bp = metadata.get('boiling_point', 'N/A')
       mp = metadata.get('melting_point', 'N/A')
       density = metadata.get('density', 'N/A')
       print(f"{name:<15} {bp:<10} {mp:<10} {density:<10}")
   
   db.close()

Step 3: Advanced Search Operations
---------------------------------

Learn how to find molecules based on various criteria.

Searching by Molecular Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   from chemesty.molecules.molecule import Molecule
   
   # First, let's populate a database with more molecules
   db = MoleculeDatabase("search_demo.db")
   db.initialize()
   
   # Add a variety of molecules
   molecules_data = [
       ("methane", "CH4", {"molecular_weight": 16.04, "category": "alkane"}),
       ("ethane", "C2H6", {"molecular_weight": 30.07, "category": "alkane"}),
       ("propane", "C3H8", {"molecular_weight": 44.10, "category": "alkane"}),
       ("water", "H2O", {"molecular_weight": 18.02, "category": "inorganic"}),
       ("ammonia", "NH3", {"molecular_weight": 17.03, "category": "inorganic"}),
       ("methanol", "CH3OH", {"molecular_weight": 32.04, "category": "alcohol"}),
       ("ethanol", "C2H5OH", {"molecular_weight": 46.07, "category": "alcohol"}),
       ("glucose", "C6H12O6", {"molecular_weight": 180.16, "category": "sugar"})
   ]
   
   for name, formula, metadata in molecules_data:
       molecule = Molecule(formula=formula)
       db.store_molecule(name, molecule, metadata)
   
   # Search by molecular weight range
   print("Molecules with molecular weight between 15 and 50 g/mol:")
   light_molecules = db.search_by_molecular_weight(min_weight=15, max_weight=50)
   for name, molecule in light_molecules:
       print(f"  {name}: {molecule.molecular_formula()} ({molecule.molecular_weight():.2f} g/mol)")
   
   # Search by elements present
   print("\nMolecules containing carbon:")
   carbon_molecules = db.search_by_elements(["C"])
   for name, molecule in carbon_molecules:
       print(f"  {name}: {molecule.molecular_formula()}")
   
   # Search by metadata
   print("\nAlkane molecules:")
   alkanes = db.search_by_metadata({"category": "alkane"})
   for name, molecule in alkanes:
       print(f"  {name}: {molecule.molecular_formula()}")
   
   db.close()

Complex Query Examples
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   db = MoleculeDatabase("search_demo.db")
   
   def find_molecules_by_criteria(db, min_weight=None, max_weight=None, 
                                  required_elements=None, excluded_elements=None,
                                  metadata_filters=None):
       """Find molecules matching multiple criteria."""
       # Start with all molecules
       all_molecules = db.get_all_molecules()
       results = []
       
       for name, molecule in all_molecules:
           # Check molecular weight
           if min_weight and molecule.molecular_weight() < min_weight:
               continue
           if max_weight and molecule.molecular_weight() > max_weight:
               continue
           
           # Check required elements
           if required_elements:
               composition = molecule.composition()
               molecule_elements = [elem.symbol for elem in composition.keys()]
               if not all(elem in molecule_elements for elem in required_elements):
                   continue
           
           # Check excluded elements
           if excluded_elements:
               composition = molecule.composition()
               molecule_elements = [elem.symbol for elem in composition.keys()]
               if any(elem in molecule_elements for elem in excluded_elements):
                   continue
           
           # Check metadata filters
           if metadata_filters:
               try:
                   _, metadata = db.get_molecule_with_metadata(name)
                   for key, value in metadata_filters.items():
                       if metadata.get(key) != value:
                           break
                   else:
                       results.append((name, molecule))
               except:
                   continue
           else:
               results.append((name, molecule))
       
       return results
   
   # Example: Find organic molecules (containing C and H) under 100 g/mol
   print("Organic molecules under 100 g/mol:")
   organic_light = find_molecules_by_criteria(
       db, 
       max_weight=100, 
       required_elements=["C", "H"]
   )
   for name, molecule in organic_light:
       print(f"  {name}: {molecule.molecular_formula()} ({molecule.molecular_weight():.2f} g/mol)")
   
   # Example: Find alcohols
   print("\nAlcohol molecules:")
   alcohols = find_molecules_by_criteria(
       db,
       metadata_filters={"category": "alcohol"}
   )
   for name, molecule in alcohols:
       print(f"  {name}: {molecule.molecular_formula()}")
   
   db.close()

Step 4: Batch Operations and Performance
---------------------------------------

Learn how to efficiently handle large amounts of chemical data.

Batch Insertion
~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   from chemesty.molecules.molecule import Molecule
   import time
   
   # Create a database for performance testing
   db = MoleculeDatabase("batch_demo.db")
   db.initialize()
   
   # Generate a large dataset of molecules
   def generate_alkane_series(max_carbons=20):
       """Generate a series of alkanes from methane to larger molecules."""
       alkanes = []
       for n in range(1, max_carbons + 1):
           formula = f"C{n}H{2*n + 2}"
           name = f"alkane_C{n}"
           metadata = {
               "carbon_count": n,
               "hydrogen_count": 2*n + 2,
               "category": "alkane",
               "series": "normal_alkane"
           }
           alkanes.append((name, formula, metadata))
       return alkanes
   
   alkanes = generate_alkane_series(50)  # Generate 50 alkanes
   
   # Method 1: Individual insertions (slower)
   start_time = time.time()
   for name, formula, metadata in alkanes[:10]:  # Just first 10 for demo
       molecule = Molecule(formula=formula)
       db.store_molecule(name, molecule, metadata)
   individual_time = time.time() - start_time
   
   # Method 2: Batch insertion with transaction (faster)
   start_time = time.time()
   with db.transaction():
       for name, formula, metadata in alkanes[10:20]:  # Next 10
           molecule = Molecule(formula=formula)
           db.store_molecule(name, molecule, metadata)
   batch_time = time.time() - start_time
   
   print(f"Individual insertions (10 molecules): {individual_time:.4f} seconds")
   print(f"Batch insertion (10 molecules): {batch_time:.4f} seconds")
   print(f"Speed improvement: {individual_time/batch_time:.1f}x faster")
   
   # Verify the data
   total_molecules = len(db.get_all_molecules())
   print(f"Total molecules in database: {total_molecules}")
   
   db.close()

Batch Retrieval and Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   db = MoleculeDatabase("batch_demo.db")
   
   # Retrieve multiple molecules at once
   alkane_names = [f"alkane_C{i}" for i in range(1, 11)]
   molecules = db.get_molecules_batch(alkane_names)
   
   print("Alkane Series Analysis:")
   print(f"{'Name':<12} {'Formula':<8} {'MW (g/mol)':<12} {'C Count':<8}")
   print("-" * 45)
   
   for name, molecule in molecules:
       if molecule:  # Check if molecule exists
           mw = molecule.molecular_weight()
           # Get carbon count from composition
           composition = molecule.composition()
           carbon_count = sum(count for elem, count in composition.items() 
                            if elem.symbol == 'C')
           formula = molecule.molecular_formula()
           print(f"{name:<12} {formula:<8} {mw:<12.2f} {carbon_count:<8}")
   
   # Analyze trends in the data
   molecular_weights = []
   carbon_counts = []
   
   for name, molecule in molecules:
       if molecule:
           molecular_weights.append(molecule.molecular_weight())
           composition = molecule.composition()
           carbon_count = sum(count for elem, count in composition.items() 
                            if elem.symbol == 'C')
           carbon_counts.append(carbon_count)
   
   if molecular_weights:
       print(f"\nTrends in alkane series:")
       print(f"Molecular weight range: {min(molecular_weights):.2f} - {max(molecular_weights):.2f} g/mol")
       print(f"Average MW per carbon: {sum(molecular_weights)/sum(carbon_counts):.2f} g/mol per C")
   
   db.close()

Step 5: Database Management and Maintenance
------------------------------------------

Learn how to maintain and optimize your chemical databases.

Database Backup and Restore
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import shutil
   import os
   from chemesty.data.database import MoleculeDatabase
   
   def backup_database(db_path, backup_path):
       """Create a backup of the database."""
       try:
           shutil.copy2(db_path, backup_path)
           print(f"Database backed up to {backup_path}")
           return True
       except Exception as e:
           print(f"Backup failed: {e}")
           return False
   
   def restore_database(backup_path, db_path):
       """Restore database from backup."""
       try:
           shutil.copy2(backup_path, db_path)
           print(f"Database restored from {backup_path}")
           return True
       except Exception as e:
           print(f"Restore failed: {e}")
           return False
   
   # Example usage
   original_db = "my_chemicals.db"
   backup_file = "my_chemicals_backup.db"
   
   # Create backup
   if os.path.exists(original_db):
       backup_database(original_db, backup_file)
   
   # Verify backup by checking molecule count
   if os.path.exists(backup_file):
       backup_db = MoleculeDatabase(backup_file)
       molecule_count = len(backup_db.get_all_molecules())
       print(f"Backup contains {molecule_count} molecules")
       backup_db.close()

Database Statistics and Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   from collections import Counter
   
   def analyze_database(db_path):
       """Provide comprehensive database statistics."""
       db = MoleculeDatabase(db_path)
       
       # Get all molecules
       all_molecules = db.get_all_molecules()
       total_count = len(all_molecules)
       
       print(f"Database Analysis for {db_path}")
       print("=" * 50)
       print(f"Total molecules: {total_count}")
       
       if total_count == 0:
           print("Database is empty")
           db.close()
           return
       
       # Analyze molecular weights
       weights = [mol.molecular_weight() for name, mol in all_molecules]
       print(f"Molecular weight range: {min(weights):.2f} - {max(weights):.2f} g/mol")
       print(f"Average molecular weight: {sum(weights)/len(weights):.2f} g/mol")
       
       # Analyze elements
       all_elements = []
       for name, molecule in all_molecules:
           composition = molecule.composition()
           all_elements.extend([elem.symbol for elem in composition.keys()])
       
       element_counts = Counter(all_elements)
       print(f"\nMost common elements:")
       for element, count in element_counts.most_common(5):
           print(f"  {element}: {count} molecules ({count/total_count*100:.1f}%)")
       
       # Analyze atom counts
       atom_counts = [mol.atom_count() for name, mol in all_molecules]
       print(f"\nMolecule complexity:")
       print(f"  Atom count range: {min(atom_counts)} - {max(atom_counts)} atoms")
       print(f"  Average atoms per molecule: {sum(atom_counts)/len(atom_counts):.1f}")
       
       # Check for metadata
       molecules_with_metadata = 0
       for name, molecule in all_molecules:
           try:
               _, metadata = db.get_molecule_with_metadata(name)
               if metadata:
                   molecules_with_metadata += 1
           except:
               pass
       
       print(f"\nMetadata coverage: {molecules_with_metadata}/{total_count} molecules ({molecules_with_metadata/total_count*100:.1f}%)")
       
       db.close()
   
   # Analyze our databases
   databases_to_analyze = ["my_chemicals.db", "chemical_properties.db", "batch_demo.db"]
   
   for db_path in databases_to_analyze:
       if os.path.exists(db_path):
           analyze_database(db_path)
           print()

Step 6: Real-World Workflow Example
----------------------------------

Let's put it all together with a practical example.

Building a Pharmaceutical Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   from chemesty.molecules.molecule import Molecule
   
   # Create a pharmaceutical database
   pharma_db = MoleculeDatabase("pharmaceuticals.db")
   pharma_db.initialize()
   
   # Define pharmaceutical compounds with comprehensive data
   pharmaceuticals = [
       {
           "name": "aspirin",
           "formula": "C9H8O4",
           "metadata": {
               "common_name": "Aspirin",
               "iupac_name": "2-acetoxybenzoic acid",
               "drug_class": "NSAID",
               "indication": "pain relief, anti-inflammatory",
               "dosage_form": "tablet",
               "typical_dose_mg": 325,
               "bioavailability": 0.8,
               "half_life_hours": 0.25,
               "molecular_targets": ["COX-1", "COX-2"],
               "side_effects": ["stomach irritation", "bleeding risk"]
           }
       },
       {
           "name": "ibuprofen",
           "formula": "C13H18O2",
           "metadata": {
               "common_name": "Ibuprofen",
               "iupac_name": "2-(4-isobutylphenyl)propionic acid",
               "drug_class": "NSAID",
               "indication": "pain relief, anti-inflammatory, fever reduction",
               "dosage_form": "tablet",
               "typical_dose_mg": 200,
               "bioavailability": 0.9,
               "half_life_hours": 2.0,
               "molecular_targets": ["COX-1", "COX-2"],
               "side_effects": ["stomach irritation", "kidney effects"]
           }
       },
       {
           "name": "acetaminophen",
           "formula": "C8H9NO2",
           "metadata": {
               "common_name": "Acetaminophen",
               "iupac_name": "N-acetyl-para-aminophenol",
               "drug_class": "analgesic",
               "indication": "pain relief, fever reduction",
               "dosage_form": "tablet",
               "typical_dose_mg": 500,
               "bioavailability": 0.85,
               "half_life_hours": 2.5,
               "molecular_targets": ["COX-3"],
               "side_effects": ["liver toxicity at high doses"]
           }
       }
   ]
   
   # Store pharmaceuticals in database
   with pharma_db.transaction():
       for drug_data in pharmaceuticals:
           molecule = Molecule(formula=drug_data["formula"])
           pharma_db.store_molecule(drug_data["name"], molecule, drug_data["metadata"])
           print(f"Added {drug_data['metadata']['common_name']} to database")
   
   # Query the database for drug information
   print("\nPharmaceutical Database Query Results:")
   print("=" * 60)
   
   # Find all NSAIDs
   all_drugs = pharma_db.get_all_molecules()
   nsaids = []
   
   for name, molecule in all_drugs:
       try:
           _, metadata = pharma_db.get_molecule_with_metadata(name)
           if metadata.get("drug_class") == "NSAID":
               nsaids.append((name, molecule, metadata))
       except:
           continue
   
   print("NSAID Medications:")
   for name, molecule, metadata in nsaids:
       print(f"  {metadata['common_name']} ({molecule.molecular_formula()})")
       print(f"    Typical dose: {metadata['typical_dose_mg']} mg")
       print(f"    Half-life: {metadata['half_life_hours']} hours")
       print(f"    Bioavailability: {metadata['bioavailability']*100}%")
       print()
   
   pharma_db.close()

Best Practices for Database Workflows
------------------------------------

1. **Always close database connections**: Use try/finally blocks or context managers
2. **Use transactions for batch operations**: Improves performance and data integrity
3. **Include meaningful metadata**: Store relevant chemical and physical properties
4. **Regular backups**: Protect your valuable chemical data
5. **Optimize queries**: Use appropriate search methods for your use case
6. **Validate data before storage**: Ensure molecules are valid before adding to database
7. **Use descriptive names**: Make molecule names searchable and meaningful

Common Pitfalls to Avoid
-----------------------

1. **Forgetting to close databases**: Can lead to data corruption
2. **Not using transactions**: Slow performance for batch operations
3. **Inconsistent metadata**: Use standardized keys and formats
4. **No error handling**: Always handle potential database errors
5. **Duplicate entries**: Check if molecules exist before adding
6. **Poor naming conventions**: Use consistent, descriptive names

Next Steps
----------

You've now mastered database workflows in Chemesty! You can:

- Create and manage chemical databases
- Store molecules with rich metadata
- Perform complex searches and queries
- Handle large datasets efficiently
- Maintain and optimize databases

**Continue Learning:**

- Try the :doc:`chemical_reactions` tutorial for reaction databases
- Explore the :doc:`advanced_analysis` tutorial for data analysis
- Review the :doc:`../user_guides/data` for more database features

**Practice Projects:**

1. Create a database of natural products with biological activity data
2. Build a materials database with physical properties
3. Develop a reaction database with mechanism information
4. Create a toxicity database with safety information