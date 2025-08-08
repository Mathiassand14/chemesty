# Contributing to Chemesty

Thank you for your interest in contributing to Chemesty! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.13+
- Poetry 1.8.0+
- Git

### Development Setup

1. **Set Up the Development Environment**
   ```bash
   # Navigate to the project directory
   cd chemesty
   ```

2. **Install Dependencies**
   ```bash
   # Install Poetry if you haven't already
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install project dependencies
   poetry install --with dev
   
   # Activate the virtual environment
   poetry shell
   ```

3. **Verify Installation**
   ```bash
   # Run tests to ensure everything is working
   pytest
   
   # Try the CLI
   python -m chemesty.cli.main --help
   ```

4. **Set up Pre-commit Hooks** (Optional but recommended)
   ```bash
   pre-commit install
   ```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Implement new features or fix bugs
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Examples**: Create tutorials or example usage

### Before You Start

1. **Check Existing Issues**: Look through existing issues to see if your contribution is already being discussed
2. **Create an Issue**: For significant changes, create an issue first to discuss the approach
3. **Small Changes**: For small bug fixes or improvements, you can directly create a pull request

## Code Style

We follow strict code style guidelines to maintain consistency:

### Python Code Style

- **PEP 8**: Follow Python's official style guide
- **Line Length**: Maximum 88 characters (Black formatter standard)
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Use Google-style docstrings for all public functions and classes

### Example Function

```python
def calculate_molecular_weight(elements: Dict[str, int]) -> float:
    """Calculate the molecular weight of a molecule.

    Args:
        elements: A dictionary mapping element symbols to their quantities.

    Returns:
        The molecular weight in atomic mass units.

    Raises:
        ValueError: If the elements dictionary is empty.
        
    Example:
        >>> elements = {"H": 2, "O": 1}
        >>> calculate_molecular_weight(elements)
        18.015
    """
    if not elements:
        raise ValueError("Elements dictionary cannot be empty")
        
    return sum(element.atomic_mass * quantity for element, quantity in elements.items())
```

### Code Formatting Tools

We use several tools to maintain code quality:

- **Black**: Code formatter
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run these tools before submitting:

```bash
# Format code
black chemesty tests

# Sort imports
isort chemesty tests

# Check linting
flake8 chemesty tests

# Type checking
mypy chemesty
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chemesty

# Run specific test file
pytest tests/test_elements.py

# Run specific test
pytest tests/test_elements.py::TestElement::test_hydrogen_properties
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Include both positive and negative test cases
- Use pytest fixtures for common setup
- Aim for high test coverage (>90%)

### Test Structure

```python
import pytest
from chemesty.elements import H, O

class TestElementProperties:
    """Test class for element property calculations."""
    
    def test_hydrogen_basic_properties(self):
        """Test basic properties of hydrogen element."""
        hydrogen = H()
        assert hydrogen.symbol == "H"
        assert hydrogen.atomic_number == 1
        assert hydrogen.atomic_mass > 1.0
        assert hydrogen.atomic_mass < 1.1
        
    def test_invalid_element_raises_error(self):
        """Test that invalid element symbols raise appropriate errors."""
        with pytest.raises(ValueError, match="Unknown element"):
            ElementFactory.get_element("Xx")
```

## Documentation

### API Documentation

- All public functions and classes must have comprehensive docstrings
- Use Google-style docstrings
- Include examples in docstrings when helpful
- Document all parameters, return values, and exceptions

### Building Documentation

```bash
cd docs
make html
```

### Documentation Guidelines

- Keep documentation up-to-date with code changes
- Use clear, concise language
- Include practical examples
- Link to related functions and classes

## Pull Request Process

### Before Submitting

1. **Update Documentation**: Ensure all documentation is updated
2. **Add Tests**: Include tests for new functionality
3. **Run Quality Checks**: Ensure all linting and type checking passes
4. **Update CHANGELOG**: Add entry describing your changes

### Pull Request Checklist

- [ ] Code follows the style guidelines
- [ ] Self-review of the code has been performed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Corresponding changes to documentation have been made
- [ ] Tests have been added that prove the fix is effective or feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged and published

### Pull Request Template

When creating a pull request, please include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review performed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

- **Clear Title**: Descriptive title summarizing the issue
- **Environment**: Python version, OS, Chemesty version
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Code Sample**: Minimal code example demonstrating the issue
- **Error Messages**: Full error messages and stack traces

### Feature Requests

For feature requests, please include:

- **Clear Description**: What feature you'd like to see
- **Use Case**: Why this feature would be useful
- **Proposed Implementation**: If you have ideas on how to implement it
- **Alternatives**: Any alternative solutions you've considered

## Development Workflow

### Branch Naming

Use descriptive branch names:

- `feature/add-ml-predictions`
- `bugfix/fix-element-lookup`
- `docs/update-api-documentation`
- `refactor/improve-molecule-class`

### Commit Messages

Write clear, descriptive commit messages:

```
Add ML property prediction functionality

- Implement PropertyPredictor class
- Add support for multiple ML algorithms
- Include feature engineering pipeline
- Add comprehensive tests and documentation

Fixes #123
```

### Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release after merge
5. Automated CI/CD handles publishing

## Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check the documentation first

### Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- Release notes
- Documentation acknowledgments

## Development Tips

### Useful Commands

```bash
# Run full test suite with coverage
make test

# Build documentation
make docs

# Run all quality checks
make lint

# Clean build artifacts
make clean

# Run benchmarks
make benchmark
```

### IDE Setup

#### VS Code

Recommended extensions:
- Python
- Pylance
- Black Formatter
- isort
- GitLens

#### PyCharm

Configure:
- Code style: Black
- Import optimizer: isort
- Type checker: mypy

### Performance Considerations

- Profile code for performance-critical sections
- Use appropriate data structures
- Consider memory usage for large datasets
- Document performance characteristics

### Security

- Never commit sensitive information
- Use secure coding practices
- Report security issues privately
- Follow dependency security updates

## Questions?

If you have questions about contributing, please:

1. Check this document first
2. Search existing issues and discussions
3. Create a new discussion or issue
4. Reach out to maintainers

Thank you for contributing to Chemesty! 🧪