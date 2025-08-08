Elements User Guide
=================

This guide provides detailed information on working with chemical elements in the Chemesty library.

Introduction to Elements
-----------------------

The elements module is the foundation of Chemesty, providing representations of all chemical elements in the periodic table. Each element is implemented as a class that inherits from the base ``AtomicElement`` class.

Importing Elements
----------------

There are several ways to import elements:

Individual Elements
~~~~~~~~~~~~~~~~~

You can import specific elements that you need:

.. code-block:: python

   from chemesty.elements import H, O, C, N, Fe, Au

All Elements
~~~~~~~~~~~

You can import all elements at once:

.. code-block:: python

   from chemesty.elements import *

Using the Element Factory
~~~~~~~~~~~~~~~~~~~~~~~

You can use the ElementFactory to create elements dynamically:

.. code-block:: python

   from chemesty.elements.element_factory import ElementFactory
   
   # Create by symbol
   hydrogen = ElementFactory.create_element_by_symbol("H")
   
   # Create by name
   oxygen = ElementFactory.create_element_by_name("Oxygen")
   
   # Create by atomic number
   carbon = ElementFactory.create_element_by_atomic_number(6)

Element Properties
----------------

Each element has a variety of properties that you can access:

Basic Properties
~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import Fe
   
   iron = Fe()
   
   # Basic identification
   print(f"Symbol: {iron.symbol}")
   print(f"Name: {iron.name}")
   print(f"Atomic number: {iron.atomic_number}")
   
   # Physical properties
   print(f"Atomic weight: {iron.atomic_weight}")
   print(f"Density: {iron.density}")
   print(f"Melting point: {iron.melting_point}")
   print(f"Boiling point: {iron.boiling_point}")
   
   # Electronic properties
   print(f"Electron configuration: {iron.electron_configuration}")
   print(f"Valence electrons: {iron.valence_electrons}")
   print(f"Electronegativity: {iron.electronegativity}")

Element Categories
~~~~~~~~~~~~~~~

Elements can be categorized in various ways:

.. code-block:: python

   from chemesty.elements import Na, Cl, Fe, He, C
   
   # Check element categories
   print(f"Sodium is a metal: {Na.is_metal()}")
   print(f"Chlorine is a nonmetal: {Cl.is_nonmetal()}")
   print(f"Iron is a transition metal: {Fe.is_transition_metal()}")
   print(f"Helium is a noble gas: {He.is_noble_gas()}")
   print(f"Carbon is a metalloid: {C.is_metalloid()}")

Comparing Elements
---------------

Elements can be compared based on their atomic numbers:

.. code-block:: python

   from chemesty.elements import H, C, O, Fe, U
   
   # Compare elements
   print(f"H < C: {H < C}")  # True (1 < 6)
   print(f"Fe > O: {Fe > O}")  # True (26 > 8)
   print(f"U >= Fe: {U >= Fe}")  # True (92 >= 26)
   
   # Sort elements
   elements = [Fe, O, H, U, C]
   sorted_elements = sorted(elements)
   print("Elements sorted by atomic number:")
   for element in sorted_elements:
       print(f"  {element.symbol} ({element.atomic_number})")

Element Calculations
-----------------

You can perform various calculations with elements:

Atomic Mass Calculations
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import C, O, H
   
   # Calculate mass of multiple atoms
   carbon_mass = C.atomic_weight
   oxygen_mass = O.atomic_weight
   hydrogen_mass = H.atomic_weight
   
   # Calculate mass of CO2
   co2_mass = carbon_mass + 2 * oxygen_mass
   print(f"CO2 mass: {co2_mass}")
   
   # Calculate mass of CH4
   ch4_mass = carbon_mass + 4 * hydrogen_mass
   print(f"CH4 mass: {ch4_mass}")

Electron Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import Na, Cl, Fe
   
   # Print electron configurations
   print(f"Na electron configuration: {Na.electron_configuration}")
   print(f"Cl electron configuration: {Cl.electron_configuration}")
   print(f"Fe electron configuration: {Fe.electron_configuration}")
   
   # Analyze valence electrons
   print(f"Na valence electrons: {Na.valence_electrons}")
   print(f"Cl valence electrons: {Cl.valence_electrons}")
   print(f"Fe valence electrons: {Fe.valence_electrons}")

Advanced Usage
------------

Working with Element Data
~~~~~~~~~~~~~~~~~~~~~~~

You can access the raw element data:

.. code-block:: python

   from chemesty.elements.element_data import get_element_data, ELEMENT_DATA
   
   # Get data for a specific element
   hydrogen_data = get_element_data("H")
   print(f"Hydrogen data: {hydrogen_data}")
   
   # Get the number of elements in the database
   print(f"Number of elements: {len(ELEMENT_DATA)}")
   
   # Get all element symbols
   all_symbols = list(ELEMENT_DATA.keys())
   print(f"All element symbols: {all_symbols}")

Creating Custom Elements
~~~~~~~~~~~~~~~~~~~~~

For research purposes, you might want to create custom elements:

.. code-block:: python

   from chemesty.elements.atomic_element import AtomicElement
   
   # Create a custom element class
   class CustomElement(AtomicElement):
       def __init__(self):
           super().__init__(
               symbol="Xx",
               name="Custom Element",
               atomic_number=0,
               atomic_weight=100.0,
               electron_configuration="1s2",
               category="custom"
           )
   
   # Create an instance
   custom = CustomElement()
   print(f"Custom element: {custom.name} ({custom.symbol})")
   print(f"Atomic weight: {custom.atomic_weight}")

Best Practices
------------

When working with elements, follow these best practices:

1. Import only the elements you need to avoid namespace pollution
2. Use the ElementFactory when you need to create elements dynamically
3. Compare elements using their atomic numbers, not their symbols
4. Use element properties directly rather than accessing the underlying data
5. Create molecules to work with combinations of elements rather than managing elements individually