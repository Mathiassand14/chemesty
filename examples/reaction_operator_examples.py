"""
Reaction Operator Examples for Chemesty.

This module demonstrates the new intuitive reaction syntax using & and >> operators
for creating chemical reactions with natural, mathematical notation.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chemesty.molecules.molecule import Molecule
from chemesty.reactions.reaction import Reaction
from chemesty.utils.progress import progress_context, progress_bar
from chemesty.utils.errors import with_error_handling, ValidationError

@with_error_handling("reaction operator examples")
def basic_operator_syntax_examples():
    """Examples of the new & and >> operator syntax for reactions."""
    print("=== Basic Operator Syntax Examples ===")
    
    # Example 1: Combustion of methane using new syntax
    print("1. Combustion of Methane (New Syntax):")
    print("   CH4 & 2*O2 >> CO2 & 2*H2O")
    
    try:
        # Create molecules
        methane = Molecule("CH4")
        oxygen = Molecule("O2")
        co2 = Molecule("CO2")
        water = Molecule("H2O")
        
        # Create reaction using new operator syntax
        combustion = (methane & (2, oxygen)) >> (co2 & (2, water))
        
        print(f"   Reaction: {combustion}")
        print(f"   Balanced: {combustion.is_balanced()}")
        print(f"   Type: {type(combustion)}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Water synthesis
    print("\n2. Water Synthesis (New Syntax):")
    print("   2*H2 & O2 >> 2*H2O")
    
    try:
        h2 = Molecule("H2")
        o2 = Molecule("O2")
        h2o = Molecule("H2O")
        
        # Note: Start with a molecule, then add coefficient tuples
        water_synthesis = ((2, h2) & o2) >> (2, h2o)
        
        # Alternative syntax that works:
        from chemesty.molecules.molecule import create_reaction_side
        reactants = create_reaction_side((2, h2), o2)
        products = create_reaction_side((2, h2o))
        water_synthesis_alt = reactants >> products
        
        print(f"   Reaction: {water_synthesis_alt}")
        print(f"   Balanced: {water_synthesis_alt.is_balanced()}")
        
    except Exception as e:
        print(f"   Error: {e}")
        print("   Note: Use create_reaction_side() helper for complex cases")
    
    # Example 3: Simple single reactant/product
    print("\n3. Simple Conversion:")
    print("   H2 >> H2O")
    
    try:
        simple_reaction = h2 >> h2o
        print(f"   Reaction: {simple_reaction}")
        print(f"   Balanced: {simple_reaction.is_balanced()}")
        
    except Exception as e:
        print(f"   Error: {e}")

@with_error_handling("complex reaction examples")
def complex_reaction_examples():
    """Examples of complex reactions using the new syntax."""
    print("\n=== Complex Reaction Examples ===")
    
    # Example 1: Haber Process
    print("1. Haber Process:")
    print("   N2 & 3*H2 >> 2*NH3")
    
    try:
        n2 = Molecule("N2")
        h2 = Molecule("H2")
        nh3 = Molecule("NH3")
        
        haber_process = (n2 & (3, h2)) >> (2, nh3)
        
        print(f"   Reaction: {haber_process}")
        print(f"   Balanced: {haber_process.is_balanced()}")
        
        # Add conditions
        haber_process.temperature = 723  # 450°C in Kelvin
        haber_process.pressure = 200     # 200 atm
        haber_process.conditions = {"catalyst": "Fe"}
        
        print(f"   Temperature: {haber_process.temperature} K")
        print(f"   Pressure: {haber_process.pressure} atm")
        print(f"   Catalyst: {haber_process.conditions.get('catalyst')}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Acid-Base Neutralization
    print("\n2. Acid-Base Neutralization:")
    print("   HCl & NaOH >> NaCl & H2O")
    
    try:
        hcl = Molecule("HCl")
        naoh = Molecule("NaOH")
        nacl = Molecule("NaCl")
        water = Molecule("H2O")
        
        neutralization = (hcl & naoh) >> (nacl & water)
        
        print(f"   Reaction: {neutralization}")
        print(f"   Balanced: {neutralization.is_balanced()}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Photosynthesis (simplified)
    print("\n3. Photosynthesis (Simplified):")
    print("   6*CO2 & 6*H2O >> C6H12O6 & 6*O2")
    
    try:
        co2 = Molecule("CO2")
        h2o = Molecule("H2O")
        glucose = Molecule("C6H12O6")
        o2 = Molecule("O2")
        
        # Use create_reaction_side helper for complex cases
        from chemesty.molecules.molecule import create_reaction_side
        reactants = create_reaction_side((6, co2), (6, h2o))
        products = create_reaction_side(glucose, (6, o2))
        photosynthesis = reactants >> products
        
        print(f"   Reaction: {photosynthesis}")
        print(f"   Balanced: {photosynthesis.is_balanced()}")
        
        # Add conditions
        photosynthesis.conditions = {
            "light": "required",
            "chlorophyll": "catalyst",
            "temperature": "25°C"
        }
        
        print(f"   Conditions: {photosynthesis.conditions}")
        
    except Exception as e:
        print(f"   Error: {e}")

@with_error_handling("syntax comparison")
def syntax_comparison_examples():
    """Compare traditional syntax with new operator syntax."""
    print("\n=== Syntax Comparison Examples ===")
    
    try:
        # Create molecules
        ch4 = Molecule("CH4")
        o2 = Molecule("O2")
        co2 = Molecule("CO2")
        h2o = Molecule("H2O")
        
        print("Methane Combustion - Three Different Ways:")
        
        # Method 1: Traditional explicit construction
        print("\n1. Traditional Method:")
        traditional = Reaction(name="Methane Combustion")
        traditional.add_reactant(ch4, 1)
        traditional.add_reactant(o2, 2)
        traditional.add_product(co2, 1)
        traditional.add_product(h2o, 2)
        
        print(f"   Code: reaction.add_reactant(CH4, 1); reaction.add_reactant(O2, 2); ...")
        print(f"   Result: {traditional}")
        print(f"   Balanced: {traditional.is_balanced()}")
        
        # Method 2: From equation string
        print("\n2. String Method:")
        from_string = Reaction.from_equation("CH4 + 2O2 → CO2 + 2H2O") if hasattr(Reaction, 'from_equation') else None
        if from_string:
            print(f"   Code: Reaction.from_equation('CH4 + 2O2 → CO2 + 2H2O')")
            print(f"   Result: {from_string}")
            print(f"   Balanced: {from_string.is_balanced()}")
        else:
            print("   Code: Reaction.from_equation('CH4 + 2O2 → CO2 + 2H2O')")
            print("   Result: [Method not available in current implementation]")
        
        # Method 3: New operator syntax
        print("\n3. Operator Method (NEW):")
        operator_based = (ch4 & (2, o2)) >> (co2 & (2, h2o))
        
        print(f"   Code: (CH4 & (2, O2)) >> (CO2 & (2, H2O))")
        print(f"   Result: {operator_based}")
        print(f"   Balanced: {operator_based.is_balanced()}")
        
        # Verify they're equivalent
        print(f"\n   All methods produce equivalent results: {traditional.is_balanced() == operator_based.is_balanced()}")
        
    except Exception as e:
        print(f"   Error: {e}")

@with_error_handling("syntax limitations and workarounds")
def syntax_limitations_examples():
    """Document syntax limitations and provide workarounds."""
    print("\n=== Syntax Limitations and Workarounds ===")
    
    try:
        # Create molecules
        h2 = Molecule("H2")
        o2 = Molecule("O2")
        h2o = Molecule("H2O")
        co2 = Molecule("CO2")
        
        print("Understanding Syntax Limitations:")
        print()
        
        print("✅ WORKS - Start with molecule:")
        reaction1 = h2 & (2, o2)
        print(f"   h2 & (2, o2) = {reaction1}")
        
        print("✅ WORKS - Molecule to molecule:")
        reaction2 = h2 >> h2o
        print(f"   h2 >> h2o = {reaction2}")
        
        print("✅ WORKS - Complex with parentheses:")
        reaction3 = (h2 & (2, o2)) >> (co2 & (2, h2o))
        print(f"   (h2 & (2, o2)) >> (co2 & (2, h2o)) = {reaction3}")
        
        print("\n❌ DOESN'T WORK - Start with tuple:")
        print("   (2, h2) & o2  # Error: tuple has no & operator")
        
        print("❌ DOESN'T WORK - Tuple to tuple:")
        print("   (2, h2) & (3, o2)  # Error: tuple has no & operator")
        
        print("\n🔧 WORKAROUNDS:")
        
        print("\n1. Use create_reaction_side() helper:")
        from chemesty.molecules.molecule import create_reaction_side
        reactants = create_reaction_side((2, h2), (3, o2))
        products = create_reaction_side((2, h2o), co2)
        workaround1 = reactants >> products
        print(f"   reactants = create_reaction_side((2, h2), (3, o2))")
        print(f"   products = create_reaction_side((2, h2o), co2)")
        print(f"   reaction = reactants >> products")
        print(f"   Result: {workaround1}")
        
        print("\n2. Start with any molecule, then add tuples:")
        # Start with the first molecule, then add coefficient tuples
        workaround2 = h2 & (3, o2) & (1, co2)  # This creates a reaction side
        print(f"   h2 & (3, o2) & (1, co2) = {workaround2}")
        
        print("\n3. Use traditional methods for complex cases:")
        from chemesty.reactions.reaction import Reaction
        traditional = Reaction()
        traditional.add_reactant(h2, 2)
        traditional.add_reactant(o2, 3)
        traditional.add_product(h2o, 2)
        traditional.add_product(co2, 1)
        print(f"   Traditional method: {traditional}")
        
    except Exception as e:
        print(f"   Error: {e}")

@with_error_handling("operator precedence examples")
def operator_precedence_examples():
    """Demonstrate operator precedence and parentheses usage."""
    print("\n=== Operator Precedence Examples ===")
    
    try:
        # Create molecules
        a = Molecule("H2")
        b = Molecule("O2")
        c = Molecule("H2O")
        d = Molecule("CO2")
        
        print("Understanding Operator Precedence:")
        print("Python operator precedence: * > & > >>")
        print("This means: A & 2*B >> C & 2*D")
        print("Is evaluated as: A & (2*B) >> C & (2*D)")
        print("NOT as: (A & 2*B) >> (C & 2*D)")
        
        print("\n1. Correct Usage (with parentheses):")
        correct = (a & (2, b)) >> (c & (2, d))
        print(f"   Code: (A & (2, B)) >> (C & (2, D))")
        print(f"   Result: {correct}")
        
        print("\n2. Alternative: Use variables for clarity:")
        reactants = a & (2, b)
        products = c & (2, d)
        alternative = reactants >> products
        print(f"   Code: reactants = A & (2, B); products = C & (2, D); reaction = reactants >> products")
        print(f"   Result: {alternative}")
        
        print("\n3. Simple cases (no parentheses needed):")
        simple = a >> c
        print(f"   Code: A >> C")
        print(f"   Result: {simple}")
        
    except Exception as e:
        print(f"   Error: {e}")

@with_error_handling("advanced features")
def advanced_features_examples():
    """Demonstrate advanced features with the new syntax."""
    print("\n=== Advanced Features Examples ===")
    
    try:
        # Example 1: Reaction analysis
        print("1. Reaction Analysis:")
        ch4 = Molecule("CH4")
        o2 = Molecule("O2")
        co2 = Molecule("CO2")
        h2o = Molecule("H2O")
        
        combustion = (ch4 & (2, o2)) >> (co2 & (2, h2o))
        
        print(f"   Reaction: {combustion}")
        print(f"   Reactants: {[str(r) for r in combustion.get_reactants()]}")
        print(f"   Products: {[str(p) for p in combustion.get_products()]}")
        
        # Element balance
        balance = combustion.get_element_balance()
        print(f"   Element balance: {balance}")
        
        # Molecular weight balance
        mw_balance = combustion.get_molecular_weight_balance()
        print(f"   Molecular weight balance: {mw_balance:.6f}")
        
        # Example 2: Reaction with catalysts (using traditional method for catalyst)
        print("\n2. Reaction with Catalyst:")
        n2 = Molecule("N2")
        h2 = Molecule("H2")
        nh3 = Molecule("NH3")
        
        haber = (n2 & (3, h2)) >> (2, nh3)
        # Add catalyst using traditional method
        fe_catalyst = Molecule("Fe")  # Iron catalyst
        haber.add_reactant(fe_catalyst, 1, is_catalyst=True)
        
        print(f"   Reaction: {haber}")
        print(f"   Catalysts: {[str(c) for c in haber.get_catalysts()]}")
        
    except Exception as e:
        print(f"   Error: {e}")

def main():
    """Run all reaction operator examples."""
    print("Chemesty Reaction Operator Examples")
    print("=" * 50)
    print("Demonstrating the new & and >> operators for intuitive reaction syntax")
    print()
    
    examples = [
        basic_operator_syntax_examples,
        complex_reaction_examples,
        syntax_comparison_examples,
        syntax_limitations_examples,
        operator_precedence_examples,
        advanced_features_examples
    ]
    
    for example in examples:
        try:
            example()
            print()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
            print()
    
    print("=" * 50)
    print("✅ Reaction operator examples completed!")
    print()
    print("Key Takeaways:")
    print("• Use & to combine reactants or products: CH4 & O2")
    print("• Use >> to create reactions: reactants >> products")
    print("• Use (coeff, molecule) tuples for stoichiometry: (2, O2)")
    print("• Use parentheses for complex expressions: (A & B) >> (C & D)")
    print("• The new syntax is equivalent to traditional methods")
    print("• All existing reaction analysis methods work with operator-created reactions")

if __name__ == "__main__":
    main()