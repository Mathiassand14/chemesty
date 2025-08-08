# Chemesty Requirements

This document outlines all the requirements for the Chemesty project.

## System Requirements

- Python 3.13+
- Poetry 1.8.0+ (for dependency management)

## Core Dependencies

| Dependency | Version | Description |
|------------|---------|-------------|
| openmm | ^8.3.0 | Molecular simulation toolkit |
| chempy | ^0.9.0 | Chemistry in Python |
| rdkit | ^2025.3.3 | Open-source cheminformatics software |
| pyscf | ^2.9.0 | Python module for quantum chemistry |
| jupytext | ^1.17.2 | Jupyter notebooks as Markdown documents |
| pubchempy | ^1.0.4 | Python wrapper for the PubChem API |
| sympy | ^1.12 | Python library for symbolic mathematics |
| tqdm | ^4.67.1 | Fast, extensible progress bar |
| requests | ^2.31.0 | HTTP library for Python |

## Development Dependencies

| Dependency | Version | Description |
|------------|---------|-------------|
| pytest | ^8.0.0 | Testing framework |
| pytest-cov | ^4.1.0 | Coverage plugin for pytest |
| hypothesis | ^6.98.0 | Property-based testing |
| sphinx | ^8.2.0 | Documentation generator |
| sphinx-rtd-theme | ^2.0.0 | Read the Docs theme for Sphinx |
| sphinx-autodoc-typehints | ^2.0.0 | Type hints support for Sphinx |
| myst-parser | ^3.0.0 | MyST parser for Sphinx |

## Environment Setup

The project is configured to create virtual environments in the project directory (see `poetry.toml`).

### Installation

```bash
# Navigate to the project directory
cd chemesty

# Install dependencies with Poetry
poetry install

# For development, include dev dependencies
poetry install --with dev
```

### Activating the Environment

```bash
poetry shell
```

## Hardware Requirements

No specific hardware requirements are defined, but computational chemistry operations may benefit from:
- Multi-core CPU
- Sufficient RAM (8GB+) for larger molecular simulations
- GPU acceleration for certain operations (via OpenMM)