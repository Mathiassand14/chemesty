Elements Module
==============

This module provides classes and functions for working with chemical elements in the periodic table. It includes representations for all standard elements with their properties such as atomic number, atomic weight, electron configuration, and more.

Key Features
-----------

* Complete representation of all elements in the periodic table
* Access to physical and chemical properties of elements
* Factory pattern for creating element instances
* Utility functions for element manipulation and conversion

Atomic Element
-------------

The AtomicElement class is the base class for all chemical elements in the library. It defines the common properties and behaviors shared by all elements.

.. automodule:: chemesty.elements.atomic_element
   :members:
   :undoc-members:
   :show-inheritance:

Usage Example
~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements import H, O
   
   # Access element properties
   print(f"Hydrogen atomic number: {H.atomic_number}")
   print(f"Oxygen atomic weight: {O.atomic_weight}")
   
   # Check element categories
   print(f"Is Hydrogen a metal? {H.is_metal()}")
   print(f"Is Oxygen a nonmetal? {O.is_nonmetal()}")
   
   # Compare elements
   print(f"Hydrogen is lighter than Oxygen: {H.atomic_weight < O.atomic_weight}")

Element Factory
--------------

The ElementFactory provides a way to create element instances by symbol, name, or atomic number. It implements the factory pattern to simplify element creation.

.. automodule:: chemesty.elements.element_factory
   :members:
   :undoc-members:
   :show-inheritance:

Usage Example
~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements.element_factory import ElementFactory
   
   # Create elements by symbol
   hydrogen = ElementFactory.create_element_by_symbol("H")
   oxygen = ElementFactory.create_element_by_symbol("O")
   
   # Create elements by name
   carbon = ElementFactory.create_element_by_name("Carbon")
   
   # Create elements by atomic number
   nitrogen = ElementFactory.create_element_by_atomic_number(7)
   
   # Check if they're the same
   from chemesty.elements import H, C, N, O
   print(f"Factory H == imported H: {hydrogen == H}")
   print(f"Factory C == imported C: {carbon == C}")

Element Data
-----------

The element_data module provides access to fundamental data about chemical elements, including physical and chemical properties. This data serves as the foundation for element classes.

.. automodule:: chemesty.elements.element_data
   :members:
   :undoc-members:
   :show-inheritance:

Usage Example
~~~~~~~~~~~~

.. code-block:: python

   from chemesty.elements.element_data import get_element_data, ELEMENT_DATA
   
   # Get data for a specific element
   hydrogen_data = get_element_data("H")
   print(f"Hydrogen data: {hydrogen_data}")
   
   # Access the complete element data dictionary
   print(f"Number of elements in database: {len(ELEMENT_DATA)}")
   
   # Get specific properties for multiple elements
   for symbol in ["H", "C", "O", "Fe", "U"]:
       data = get_element_data(symbol)
       print(f"{symbol}: Atomic number: {data['atomic_number']}, "
             f"Weight: {data['atomic_weight']}, "
             f"Category: {data['category']}")

Individual Elements
------------------

The elements module provides classes for all chemical elements in the periodic table.
Each element is implemented as a separate class that inherits from AtomicElement.

.. note::
   Only a few representative elements are documented here. All elements follow the same pattern.

Hydrogen (H)
~~~~~~~~~~~

.. automodule:: chemesty.elements.element.h
   :members:
   :undoc-members:
   :show-inheritance:

Carbon (C)
~~~~~~~~~

.. automodule:: chemesty.elements.element.c
   :members:
   :undoc-members:
   :show-inheritance:

Oxygen (O)
~~~~~~~~~

.. automodule:: chemesty.elements.element.o
   :members:
   :undoc-members:
   :show-inheritance:

Nitrogen (N)
~~~~~~~~~~~

.. automodule:: chemesty.elements.element.n
   :members:
   :undoc-members:
   :show-inheritance:

Utilities
--------

.. automodule:: chemesty.elements.utils
   :members:
   :undoc-members:
   :show-inheritance: