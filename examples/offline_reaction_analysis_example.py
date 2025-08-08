"""
Offline Reaction Analysis Example

This example demonstrates how to use the OfflineReactionAnalyzer class to analyze
chemical reactions without relying on external resources or online connectivity.
"""

from chemesty.reactions.reaction import Reaction
from chemesty.reactions.offline_analyzer import OfflineReactionAnalyzer


def main():
    """Run the offline reaction analysis examples."""
    print("Chemesty Offline Reaction Analysis Examples")
    print("===========================================\n")
    
    # Create an instance of the offline analyzer
    analyzer = OfflineReactionAnalyzer()
    
    # Example 1: Combustion Reaction
    print("Example 1: Combustion Reaction")
    print("-----------------------------")
    combustion_reaction = create_combustion_reaction()
    analyze_and_print_results(combustion_reaction, analyzer)
    
    # Example 2: Acid-Base Reaction
    print("\nExample 2: Acid-Base Reaction")
    print("---------------------------")
    acid_base_reaction = create_acid_base_reaction()
    analyze_and_print_results(acid_base_reaction, analyzer)
    
    # Example 3: Redox Reaction
    print("\nExample 3: Redox Reaction")
    print("-----------------------")
    redox_reaction = create_redox_reaction()
    analyze_and_print_results(redox_reaction, analyzer)
    
    # Example 4: Complex Reaction with Multiple Features
    print("\nExample 4: Complex Reaction with Multiple Features")
    print("-----------------------------------------------")
    complex_reaction = create_complex_reaction()
    analyze_and_print_results(complex_reaction, analyzer, detailed=True)


def create_combustion_reaction():
    """Create a methane combustion reaction: CH4 + 2O2 → CO2 + 2H2O."""
    reaction = Reaction()
    reaction.add_reactant("CH4")
    reaction.add_reactant("O2", coefficient=2)
    reaction.add_product("CO2")
    reaction.add_product("H2O", coefficient=2)
    return reaction


def create_acid_base_reaction():
    """Create an acid-base reaction: HCl + NaOH → NaCl + H2O."""
    reaction = Reaction()
    reaction.add_reactant("HCl")
    reaction.add_reactant("NaOH")
    reaction.add_product("NaCl")
    reaction.add_product("H2O")
    return reaction


def create_redox_reaction():
    """Create a redox reaction: Zn + CuSO4 → ZnSO4 + Cu."""
    reaction = Reaction()
    reaction.add_reactant("Zn")
    reaction.add_reactant("CuSO4")
    reaction.add_product("ZnSO4")
    reaction.add_product("Cu")
    return reaction


def create_complex_reaction():
    """Create a complex reaction: 4Fe(s) + 3O2(g) → 2Fe2O3(s)."""
    reaction = Reaction()
    reaction.add_reactant("Fe", coefficient=4, phase="s")
    reaction.add_reactant("O2", coefficient=3, phase="g")
    reaction.add_product("Fe2O3", coefficient=2, phase="s")
    return reaction


def analyze_and_print_results(reaction, analyzer, detailed=False):
    """
    Analyze a reaction and print the results.
    
    Args:
        reaction: The reaction to analyze
        analyzer: The OfflineReactionAnalyzer instance
        detailed: Whether to print detailed analysis results
    """
    # Print the reaction
    print(f"Reaction: {reaction}")
    
    # Analyze the reaction
    analysis = analyzer.enhanced_analyze_reaction_type(reaction)
    
    # Print basic results
    print(f"Primary reaction type: {analysis['primary_type']}")
    print("Confidence scores:")
    for reaction_type, confidence in analysis['confidence_scores'].items():
        print(f"  - {reaction_type}: {confidence:.2f}")
    
    # Print electron transfer analysis
    electron_transfer = analysis['electron_transfer']
    print(f"Is redox reaction: {electron_transfer['is_redox']}")
    if electron_transfer['is_redox']:
        print("Oxidation changes:")
        for element, change in electron_transfer['oxidation_changes'].items():
            print(f"  - {element}: {change:.2f}")
        
        if electron_transfer['oxidizing_agent']:
            print(f"Oxidizing agent: {electron_transfer['oxidizing_agent']}")
        if electron_transfer['reducing_agent']:
            print(f"Reducing agent: {electron_transfer['reducing_agent']}")
    
    # Print detailed analysis if requested
    if detailed:
        print("\nDetailed Analysis:")
        
        # Functional group analysis
        print("Functional Groups:")
        functional_groups = analysis['functional_groups']
        if functional_groups['reactant_groups']:
            print("  Reactant functional groups:")
            for group, count in functional_groups['reactant_groups'].items():
                print(f"    - {group}: {count}")
        
        if functional_groups['product_groups']:
            print("  Product functional groups:")
            for group, count in functional_groups['product_groups'].items():
                print(f"    - {group}: {count}")
        
        if functional_groups['transformations']:
            print("  Functional group transformations:")
            for from_group, to_group in functional_groups['transformations']:
                print(f"    - {from_group} → {to_group}")
        
        if functional_groups['reaction_mechanism'] != "unknown":
            print(f"  Reaction mechanism: {functional_groups['reaction_mechanism']}")
        
        # Reaction fingerprint
        print("Reaction Fingerprint:")
        fingerprint = analysis['fingerprint']
        
        print("  Element counts:")
        print("    Reactants:")
        for element, count in fingerprint['reactant_elements'].items():
            print(f"      - {element}: {count}")
        
        print("    Products:")
        for element, count in fingerprint['product_elements'].items():
            print(f"      - {element}: {count}")
        
        print("  Phase changes:")
        if fingerprint['phase_changes']['has_phase_changes']:
            print("    Changes:")
            for formula, (from_phase, to_phase) in fingerprint['phase_changes']['changes'].items():
                print(f"      - {formula}: {from_phase} → {to_phase}")
        else:
            print("    No phase changes detected")


if __name__ == "__main__":
    main()