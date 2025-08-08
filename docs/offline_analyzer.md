# Offline Reaction Analyzer

## Overview

The `OfflineReactionAnalyzer` is a powerful tool for analyzing chemical reactions without relying on external resources or online connectivity. It extends the base `ReactionAnalyzer` class with advanced algorithms for reaction type detection, oxidation state analysis, functional group analysis, and other chemical reaction properties.

## Features

- **Completely Offline Operation**: All analysis is performed using built-in algorithms and data, with no need for internet connectivity or external APIs.
- **Enhanced Reaction Type Detection**: Comprehensive analysis of reaction types with confidence scores.
- **Oxidation State Analysis**: Calculates and tracks oxidation states of elements to identify redox reactions.
- **Functional Group Analysis**: Identifies functional groups and their transformations to classify organic reaction mechanisms.
- **Rule-Based Expert System**: Uses a set of chemical rules to classify reactions with confidence scores.
- **Reaction Fingerprinting**: Generates detailed fingerprints of reactions for pattern recognition.

## Installation

The `OfflineReactionAnalyzer` is included in the Chemesty package. No additional installation is required beyond the main package installation:

```bash
# Install with Poetry (includes all dependencies)
poetry install
```

## Usage

### Basic Usage

```python
from chemesty.reactions.reaction import Reaction
from chemesty.reactions.offline_analyzer import OfflineReactionAnalyzer

# Create a reaction
reaction = Reaction()
reaction.add_reactant("CH4")
reaction.add_reactant("O2", coefficient=2)
reaction.add_product("CO2")
reaction.add_product("H2O", coefficient=2)

# Create an analyzer
analyzer = OfflineReactionAnalyzer()

# Analyze the reaction
analysis = analyzer.enhanced_analyze_reaction_type(reaction)

# Access the results
print(f"Primary reaction type: {analysis['primary_type']}")
print(f"Is redox reaction: {analysis['electron_transfer']['is_redox']}")
print(f"Confidence scores: {analysis['confidence_scores']}")
```

### Analysis Results

The `enhanced_analyze_reaction_type` method returns a dictionary with the following keys:

- `primary_type`: The reaction type with the highest confidence score (e.g., "combustion", "acid_base", "redox").
- `reaction_type_from_property`: The reaction type from the reaction's own type property.
- `reaction_types`: A list of possible reaction types.
- `confidence_scores`: A dictionary mapping reaction types to confidence scores.
- `electron_transfer`: Analysis of electron transfer in the reaction.
- `functional_groups`: Analysis of functional groups and their transformations.
- `rule_matches`: Results from the rule-based expert system.
- `fingerprint`: A detailed fingerprint of the reaction.

The primary reaction type is determined based on the highest confidence score from all the analyses, which ensures that the most likely reaction type is reported even if it differs from the reaction's own type property. This is particularly important for reactions that may be classified differently by different methods, such as redox reactions that might also be classified as synthesis or decomposition reactions.

### Electron Transfer Analysis

The `electron_transfer` key in the analysis results contains:

- `oxidation_changes`: A dictionary mapping elements to their changes in oxidation state.
- `is_redox`: A boolean indicating whether the reaction is a redox reaction.
- `oxidizing_agent`: The formula of the oxidizing agent (if identified).
- `reducing_agent`: The formula of the reducing agent (if identified).

### Functional Group Analysis

The `functional_groups` key in the analysis results contains:

- `reactant_groups`: A dictionary mapping functional group names to their counts in reactants.
- `product_groups`: A dictionary mapping functional group names to their counts in products.
- `transformations`: A list of tuples representing functional group transformations.
- `reaction_mechanism`: The identified reaction mechanism (e.g., "oxidation", "reduction").

### Reaction Fingerprint

The `fingerprint` key in the analysis results contains:

- `reactant_elements`: A dictionary mapping elements to their total counts in reactants.
- `product_elements`: A dictionary mapping elements to their total counts in products.
- `element_balance`: A dictionary mapping elements to their balance (product count - reactant count).
- `phase_changes`: Analysis of phase changes in the reaction.
- `charge_changes`: Analysis of charge changes in the reaction.

## Examples

See the [offline_reaction_analysis_example.py](../examples/offline_reaction_analysis_example.py) file for complete examples of using the `OfflineReactionAnalyzer` with different types of reactions.

## Supported Reaction Types

The `OfflineReactionAnalyzer` can identify the following types of reactions:

- **Combustion**: A hydrocarbon reacts with oxygen to produce carbon dioxide and water.
- **Redox (Reduction-Oxidation)**: Involves the transfer of electrons between species.
- **Acid-Base**: An acid reacts with a base.
- **Neutralization**: An acid reacts with a base to form a salt and water.
- **Precipitation**: A reaction that forms an insoluble solid.
- **Single Replacement/Displacement**: One element replaces another in a compound.
- **Double Replacement/Displacement**: Two compounds exchange ions.
- **Synthesis/Combination**: Multiple reactants combine to form a single product.
- **Decomposition**: A single reactant breaks down into multiple products.
- **Isomerization**: Rearrangement of atoms within a molecule.

## Comparison with Online Analysis

The `OfflineReactionAnalyzer` offers several advantages over online reaction analysis tools:

- **Privacy**: All analysis is performed locally, with no data sent to external servers.
- **Reliability**: Works without internet connectivity, making it suitable for offline environments.
- **Speed**: No network latency, resulting in faster analysis.
- **Customizability**: Can be extended or modified to suit specific needs.

## Testing

The `OfflineReactionAnalyzer` includes a comprehensive test suite in the `tests/unit/test_offline_analyzer.py` file. Run the tests with:

```bash
pytest tests/unit/test_offline_analyzer.py
```

## Implementation Details

The `OfflineReactionAnalyzer` uses several algorithms and data structures to perform its analysis:

- **Oxidation State Assignment**: Uses electronegativity values and common oxidation states to assign oxidation states to elements in molecules.
- **Functional Group Detection**: Uses pattern matching to identify common functional groups in molecular formulas.
- **Rule-Based Classification**: Uses a set of rules with conditions and confidence scores to classify reactions.
- **Reaction Fingerprinting**: Generates a detailed fingerprint of the reaction for pattern recognition.

## Limitations

- The functional group analysis is based on simple pattern matching and may not be accurate for complex molecules.
- The oxidation state assignment uses heuristics and may not be accurate for all compounds.
- The analyzer does not have access to structural information beyond what is provided in the molecular formula.

## Future Improvements

- Improved functional group detection using structural information.
- More sophisticated oxidation state assignment algorithms.
- Support for more reaction types and mechanisms.
- Machine learning-based classification using offline models.

## Contributing

Contributions to the `OfflineReactionAnalyzer` are welcome! Please see the [CONTRIBUTING.md](../CONTRIBUTING.md) file for guidelines.

## License

The `OfflineReactionAnalyzer` is part of the Chemesty package and is licensed under the same license as the main package. See the [LICENSE](../LICENSE) file for details.