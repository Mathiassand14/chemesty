Contributing
============

Thank you for your interest in contributing to Chemesty! This document provides guidelines and instructions for contributing to the project.

Setting Up Development Environment
--------------------------------

1. Navigate to the project directory:

   .. code-block:: bash

      cd chemesty

2. Install development dependencies using Poetry:

   .. code-block:: bash

      poetry install --with dev

3. Activate the virtual environment:

   .. code-block:: bash

      poetry shell

Code Style Guidelines
-------------------

Chemesty follows these coding standards:

- PEP 8 for Python code style
- Type hints for all function parameters and return values
- Comprehensive docstrings in Google style format
- Maximum line length of 88 characters
- Use of f-strings for string formatting

Example of proper function style:

.. code-block:: python

   def calculate_molecular_weight(elements: Dict[AtomicElement, int]) -> float:
       """Calculate the molecular weight of a molecule.

       Args:
           elements: A dictionary mapping elements to their quantities.

       Returns:
           The molecular weight in atomic mass units.

       Raises:
           ValueError: If the elements dictionary is empty.
       """
       if not elements:
           raise ValueError("Elements dictionary cannot be empty")
           
       return sum(element.atomic_mass * quantity for element, quantity in elements.items())

Testing
------

All code contributions should include tests:

1. Run the existing tests to ensure they pass:

   .. code-block:: bash

      pytest

2. Add tests for your new functionality:

   - Unit tests for individual functions and classes
   - Integration tests for end-to-end workflows
   - Property-based tests for mathematical properties

3. Ensure test coverage remains high:

   .. code-block:: bash

      pytest --cov=chemesty

Pull Request Process
------------------

1. Create a new branch for your feature or bugfix:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. Make your changes and commit them with clear, descriptive commit messages.

3. Push your branch to GitHub:

   .. code-block:: bash

      git push origin feature/your-feature-name

4. Create a pull request with a clear description of the changes.

5. Ensure all tests pass and the documentation is updated.

6. Address any feedback from code reviews.

Documentation
------------

When contributing, please update the documentation:

1. Update docstrings for any modified functions or classes.

2. Update the API documentation if you add or modify public interfaces.

3. Add examples for new features.

4. Build the documentation to verify your changes:

   .. code-block:: bash

      cd docs
      make html

Code of Conduct
-------------

Please note that Chemesty has a Code of Conduct. By participating in this project, you agree to abide by its terms.

Getting Help
----------

If you need help with contributing, please:

- Open an issue on GitHub
- Contact the maintainers via email
- Join our community chat