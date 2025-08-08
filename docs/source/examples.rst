Examples
========

This section provides detailed examples of using Chemesty for various chemistry tasks.

Basic Molecule Creation
---------------------

Creating Water Molecule
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import H, O
   from chemesty.molecules.molecule import Molecule
   
   # Create a water molecule
   water = Molecule()
   water.add_element(H, 2)
   water.add_element(O, 1)
   
   print(f"Water formula: {water.molecular_formula()}")
   print(f"Water weight: {water.molecular_weight()}")
   print(f"Water volume: {water.volume()}")
   print(f"Water density: {water.density()}")

Creating Molecules from Formulas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create molecules from formulas
   water = Molecule(formula="H2O")
   methane = Molecule(formula="CH4")
   glucose = Molecule(formula="C6H12O6")
   sulfuric_acid = Molecule(formula="H2SO4")
   
   # Print their properties
   for name, molecule in [("Water", water), ("Methane", methane), 
                         ("Glucose", glucose), ("Sulfuric Acid", sulfuric_acid)]:
       print(f"{name}:")
       print(f"  Formula: {molecule.molecular_formula()}")
       print(f"  Weight: {molecule.molecular_weight()}")
       print(f"  Volume: {molecule.volume()}")

Chemical Reactions
----------------

Combustion of Methane
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import C, H, O
   from chemesty.molecules.molecule import Molecule
   
   # Create methane (CH4)
   methane = Molecule()
   methane.add_element(C, 1)
   methane.add_element(H, 4)
   
   # Create oxygen (O2)
   oxygen = Molecule()
   oxygen.add_element(O, 2)
   
   # Combustion reaction: CH4 + 2O2 -> CO2 + 2H2O
   
   # Create carbon dioxide (CO2)
   carbon_dioxide = Molecule()
   carbon_dioxide.add_element(C, 1)
   carbon_dioxide.add_element(O, 2)
   
   # Create water (H2O)
   water = Molecule()
   water.add_element(H, 2)
   water.add_element(O, 1)
   
   # Verify conservation of mass
   reactants_mass = methane.molecular_weight() + 2 * oxygen.molecular_weight()
   products_mass = carbon_dioxide.molecular_weight() + 2 * water.molecular_weight()
   
   print(f"Reactants mass: {reactants_mass}")
   print(f"Products mass: {products_mass}")
   print(f"Difference: {abs(reactants_mass - products_mass)}")
   
   # Should be very close to zero if mass is conserved

Acid-Base Reaction
~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.molecules.molecule import Molecule
   
   # Create hydrochloric acid (HCl)
   hcl = Molecule(formula="HCl")
   
   # Create sodium hydroxide (NaOH)
   naoh = Molecule(formula="NaOH")
   
   # Reaction: HCl + NaOH -> NaCl + H2O
   
   # Create sodium chloride (NaCl)
   nacl = Molecule(formula="NaCl")
   
   # Create water (H2O)
   water = Molecule(formula="H2O")
   
   # Verify conservation of mass
   reactants_mass = hcl.molecular_weight() + naoh.molecular_weight()
   products_mass = nacl.molecular_weight() + water.molecular_weight()
   
   print(f"Reactants mass: {reactants_mass}")
   print(f"Products mass: {products_mass}")
   print(f"Difference: {abs(reactants_mass - products_mass)}")

Working with Databases
--------------------

Creating and Populating a Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from chemesty.molecules.molecule import Molecule
   from chemesty.data.database import MoleculeDatabase
   
   # Create a database
   db_path = "example_molecules.db"
   db = MoleculeDatabase(db_path)
   db.initialize()
   
   # Create common molecules
   molecules = {
       "water": Molecule(formula="H2O"),
       "methane": Molecule(formula="CH4"),
       "carbon_dioxide": Molecule(formula="CO2"),
       "ammonia": Molecule(formula="NH3"),
       "glucose": Molecule(formula="C6H12O6"),
       "ethanol": Molecule(formula="C2H5OH"),
       "acetic_acid": Molecule(formula="CH3COOH"),
       "benzene": Molecule(formula="C6H6"),
       "acetone": Molecule(formula="C3H6O"),
       "aspirin": Molecule(formula="C9H8O4")
   }
   
   # Store molecules in the database
   for name, molecule in molecules.items():
       db.store_molecule(name, molecule)
       print(f"Stored {name}: {molecule.molecular_formula()}")
   
   # Close the database
   db.close()

Searching and Analyzing Molecules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.data.database import MoleculeDatabase
   
   # Open the database
   db_path = "example_molecules.db"
   db = MoleculeDatabase(db_path)
   
   # Search for small molecules (molecular weight < 50)
   print("Small molecules:")
   small_molecules = db.search_by_molecular_weight(max_weight=50)
   for name, molecule in small_molecules:
       print(f"  {name}: {molecule.molecular_formula()} (MW: {molecule.molecular_weight()})")
   
   # Search for molecules containing carbon and oxygen
   print("\nMolecules containing carbon and oxygen:")
   co_molecules = db.search_by_elements(["C", "O"])
   for name, molecule in co_molecules:
       print(f"  {name}: {molecule.molecular_formula()}")
   
   # Calculate average molecular weight
   all_molecules = db.get_all_molecules()
   total_weight = sum(molecule.molecular_weight() for _, molecule in all_molecules)
   avg_weight = total_weight / len(all_molecules)
   print(f"\nAverage molecular weight: {avg_weight}")
   
   # Close the database
   db.close()
   
   # Clean up
   import os
   if os.path.exists(db_path):
       os.remove(db_path)