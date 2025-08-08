# Chemesty Deployment Guide

This guide covers deploying Chemesty to various platforms and websites to increase discoverability and accessibility.

## Table of Contents

- [PyPI Publication](#pypi-publication)
- [Conda-forge Submission](#conda-forge-submission)
- [Web Interface Deployment](#web-interface-deployment)
- [Documentation Hosting](#documentation-hosting)
- [Platform Submissions](#platform-submissions)
- [GitHub Configuration](#github-configuration)

## PyPI Publication

### Prerequisites

1. Create accounts on [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)
2. Install required tools:
   ```bash
   pip install twine build
   ```

### Publishing Steps

1. **Build the package:**
   ```bash
   poetry build
   ```

2. **Test on TestPyPI first:**
   ```bash
   twine upload --repository testpypi dist/*
   ```

3. **Test installation from TestPyPI:**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ chemesty
   ```

4. **Upload to PyPI:**
   ```bash
   twine upload dist/*
   ```

### Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
    - name: Install Poetry
      uses: snok/install-poetry@v1
    - name: Build package
      run: poetry build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

## Conda-forge Submission

### Creating a Conda Recipe

1. **Fork the conda-forge/staged-recipes repository**

2. **Create recipe in `recipes/chemesty/meta.yaml`:**

```yaml
{% set name = "chemesty" %}
{% set version = "0.1.0" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.io/packages/source/{{ name[0] }}/{{ name }}/chemesty-{{ version }}.tar.gz
  sha256: # Add SHA256 hash from PyPI

build:
  noarch: python
  script: {{ PYTHON }} -m pip install . -vv
  number: 0

requirements:
  host:
    - python >=3.13
    - pip
    - poetry-core
  run:
    - python >=3.13
    - openmm >=8.3.0
    - chempy >=0.9.0
    - rdkit >=2025.3.3
    - pyscf >=2.9.0
    - jupytext >=1.17.2
    - pubchempy >=1.0.4
    - sympy >=1.12
    - tqdm >=4.67.1
    - requests >=2.31.0
    - flask >=3.1.1
    - plotly >=5.17.0

test:
  imports:
    - chemesty
  commands:
    - chemesty --help

about:
  home: https://github.com/Mathiassand14/chemesty
  license: MIT
  license_family: MIT
  license_file: LICENSE
  summary: A comprehensive chemistry package for working with elements, molecules, and chemical datasets
  description: |
    Chemesty is a Python library that provides tools for working with chemical elements,
    molecules, and datasets. It includes features for molecular modeling, quantum chemistry
    calculations, reaction analysis, and database integration.
  doc_url: https://chemesty.readthedocs.io
  dev_url: https://github.com/Mathiassand14/chemesty

extra:
  recipe-maintainers:
    - Mathiassand14
```

3. **Submit pull request to conda-forge/staged-recipes**

## Web Interface Deployment

### Local Development

```bash
# Start the web interface
python -m chemesty.web.app

# Or using Flask directly
export FLASK_APP=chemesty.web.app
export FLASK_ENV=development
flask run
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up web

# Or build manually
docker build -t chemesty .
docker run -p 8000:8000 chemesty python -m chemesty.web.app
```

### Cloud Deployment Options

#### Heroku

1. **Create `Procfile`:**
   ```
   web: python -m chemesty.web.app
   ```

2. **Create `runtime.txt`:**
   ```
   python-3.13.0
   ```

3. **Deploy:**
   ```bash
   heroku create chemesty-demo
   git push heroku main
   ```

#### Railway

1. **Create `railway.toml`:**
   ```toml
   [build]
   builder = "NIXPACKS"
   
   [deploy]
   startCommand = "python -m chemesty.web.app"
   ```

#### Render

1. **Create `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: chemesty
       env: python
       buildCommand: "pip install ."
       startCommand: "python -m chemesty.web.app"
   ```

## Documentation Hosting

### Read the Docs

1. **Connect GitHub repository to Read the Docs**
2. **Create `.readthedocs.yaml`:**

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.13"

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - dev

sphinx:
  configuration: docs/source/conf.py
```

### GitHub Pages

```bash
# Build documentation
cd docs
make html

# Deploy to gh-pages branch
git subtree push --prefix docs/build/html origin gh-pages
```

## Platform Submissions

### Scientific Software Directories

1. **SciPy.org Ecosystem**
   - Submit to scipy.org/topical-software.html
   - Add to PyData ecosystem

2. **NumFOCUS**
   - Apply for affiliated project status
   - Submit to numfocus.org

3. **Research Software Directory**
   - Submit to research-software-directory.org
   - Provide comprehensive metadata

### Chemistry-Specific Platforms

1. **ChemSpider Integration**
   - Register as data provider
   - Submit molecular data

2. **PubChem Integration**
   - Use PubChem API for data exchange
   - Submit computed properties

### Academic Platforms

1. **Journal of Open Source Software (JOSS)**
   - Prepare JOSS paper
   - Submit for peer review

2. **Zenodo**
   - Create DOI for releases
   - Archive software versions

## GitHub Configuration

### Repository Settings

1. **Topics/Tags:**
   ```
   chemistry, python, molecules, quantum-chemistry, cheminformatics,
   molecular-modeling, reactions, periodic-table, scientific-computing
   ```

2. **Description:**
   ```
   A comprehensive chemistry package for working with elements, molecules, and chemical datasets
   ```

3. **Website:** `https://chemesty.readthedocs.io`

### GitHub Actions

Create comprehensive CI/CD pipeline:

```yaml
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.13]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install poetry
        poetry install
    - name: Run tests
      run: poetry run pytest
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Monitoring and Analytics

### Package Statistics

- Monitor PyPI download statistics
- Track GitHub stars and forks
- Monitor documentation views

### User Feedback

- Set up GitHub Discussions
- Monitor issue reports
- Collect user testimonials

## Maintenance

### Regular Updates

1. **Keep dependencies updated**
2. **Monitor security advisories**
3. **Update documentation**
4. **Respond to user issues**

### Version Management

1. **Follow semantic versioning**
2. **Maintain CHANGELOG.md**
3. **Create GitHub releases**
4. **Update platform listings**

## Success Metrics

- PyPI download counts
- GitHub stars and forks
- Documentation page views
- User engagement (issues, discussions)
- Academic citations
- Platform adoption rates