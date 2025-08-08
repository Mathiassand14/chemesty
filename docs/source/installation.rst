Installation
============

This guide will help you install Chemesty and its dependencies.

Requirements
-----------

Chemesty requires:

* Python 3.13 or higher
* Poetry (for dependency management)

Dependencies
-----------

Chemesty depends on several libraries:

* OpenMM: Molecular modeling toolkit
* ChemPy: Chemistry toolkit
* RDKit: Cheminformatics and machine learning toolkit
* PySCF: Python-based simulations of chemistry framework
* SymPy: Symbolic mathematics
* PubChemPy: Python wrapper for the PubChem API

Installation with Poetry
----------------------

The recommended way to install Chemesty is using Poetry:

.. code-block:: bash

   # Navigate to the project directory
   cd chemesty

   # Install with Poetry
   poetry install

   # Activate the virtual environment
   poetry shell

This will create a virtual environment and install all dependencies.

Installation with pip
-------------------

You can also install Chemesty using pip from the local directory:

.. code-block:: bash

   # Install from local directory
   pip install .

   # Or install in development mode
   pip install -e .

Development Installation
----------------------

For development, you should install the development dependencies:

.. code-block:: bash

   # Navigate to the project directory
   cd chemesty

   # Install with Poetry including development dependencies
   poetry install --with dev

   # Activate the virtual environment
   poetry shell

Verifying Installation
--------------------

To verify that Chemesty is installed correctly, you can run:

.. code-block:: python

   import chemesty
   print(chemesty.__version__)

This should print the version number of Chemesty.