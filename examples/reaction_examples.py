"""
Reaction Modeling Examples for Chemesty.

This module demonstrates how to use Chemesty's reaction modeling capabilities
including reaction balancing, energy calculations, and pathway analysis.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chemesty.molecules.molecule import Molecule
from chemesty.utils.progress import progress_context, progress_bar
from chemesty.utils.errors import with_error_handling, ValidationError

try:
    from chemesty.reactions.reaction import Reaction
    from chemesty.reactions.balancer import ReactionBalancer
    REACTIONS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Reaction modules not available: {e}")
    print("Some examples will be skipped.")
    REACTIONS_AVAILABLE = False


@with_error_handling("reaction creation")
def basic_reaction_examples():
    """Examples of creating and working with basic reactions."""
    print("=== Basic Reaction Examples ===")
    
    if not REACTIONS_AVAILABLE:
        print("Reaction modules not available. Skipping basic reaction examples.")
        return
    
    # Example 1: Combustion of methane - Traditional vs New Syntax
    print("1. Combustion of Methane - Two Approaches:")
    print("   CH4 + 2O2 → CO2 + 2H2O")
    
    try:
        # Create molecules
        methane = Molecule(formula="CH4")
        oxygen = Molecule(formula="O2")
        carbon_dioxide = Molecule(formula="CO2")
        water = Molecule(formula="H2O")
        
        # Method A: Traditional approach
        print("\n   A. Traditional Method:")
        traditional = Reaction(name="Methane Combustion")
        traditional.add_reactant(methane, 1)
        traditional.add_reactant(oxygen, 2)
        traditional.add_product(carbon_dioxide, 1)
        traditional.add_product(water, 2)
        
        print(f"      Code: reaction.add_reactant(CH4, 1); reaction.add_reactant(O2, 2); ...")
        print(f"      Result: {traditional}")
        print(f"      Balanced: {traditional.is_balanced()}")
        
        # Method B: New operator syntax
        print("\n   B. Operator Method (NEW):")
        operator_based = (methane & (2, oxygen)) >> (carbon_dioxide & (2, water))
        
        print(f"      Code: (CH4 & (2, O2)) >> (CO2 & (2, H2O))")
        print(f"      Result: {operator_based}")
        print(f"      Balanced: {operator_based.is_balanced()}")
        
        print(f"\n      Both methods produce equivalent results: {traditional.is_balanced() == operator_based.is_balanced()}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Synthesis of water
    print("\n2. Synthesis of Water:")
    print("   H2 + O2 → H2O")
    
    try:
        hydrogen = Molecule(formula="H2")
        oxygen = Molecule(formula="O2")
        water = Molecule(formula="H2O")
        
        water_synthesis = Reaction(
            reactants=[hydrogen, oxygen],
            products=[water],
            name="Water Synthesis"
        )
        
        print(f"   Reaction: {water_synthesis}")
        print(f"   Balanced: {water_synthesis.is_balanced()}")
        
        if not water_synthesis.is_balanced():
            balanced = water_synthesis.balance()
            print(f"   Balanced: {balanced}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Acid-base neutralization
    print("\n3. Acid-Base Neutralization:")
    print("   HCl + NaOH → NaCl + H2O")
    
    try:
        hcl = Molecule(formula="HCl")
        naoh = Molecule(formula="NaOH")
        nacl = Molecule(formula="NaCl")
        water = Molecule(formula="H2O")
        
        neutralization = Reaction(
            reactants=[hcl, naoh],
            products=[nacl, water],
            name="Acid-Base Neutralization"
        )
        
        print(f"   Reaction: {neutralization}")
        print(f"   Balanced: {neutralization.is_balanced()}")
        
        # Calculate reaction properties
        if hasattr(neutralization, 'calculate_enthalpy_change'):
            try:
                delta_h = neutralization.calculate_enthalpy_change()
                print(f"   Enthalpy change: {delta_h:.2f} kJ/mol")
            except Exception as e:
                print(f"   Enthalpy calculation failed: {e}")
        
    except Exception as e:
        print(f"   Error: {e}")


@with_error_handling("reaction balancing")
def reaction_balancing_examples():
    """Examples of reaction balancing algorithms."""
    print("\n=== Reaction Balancing Examples ===")
    
    if not REACTIONS_AVAILABLE:
        print("Reaction modules not available. Skipping balancing examples.")
        return
    
    # Create reaction balancer
    balancer = ReactionBalancer()
    
    # Example reactions to balance
    reactions_to_balance = [
        {
            "name": "Combustion of Propane",
            "equation": "C3H8 + O2 → CO2 + H2O",
            "reactants": ["C3H8", "O2"],
            "products": ["CO2", "H2O"]
        },
        {
            "name": "Photosynthesis",
            "equation": "CO2 + H2O → C6H12O6 + O2",
            "reactants": ["CO2", "H2O"],
            "products": ["C6H12O6", "O2"]
        },
        {
            "name": "Decomposition of Hydrogen Peroxide",
            "equation": "H2O2 → H2O + O2",
            "reactants": ["H2O2"],
            "products": ["H2O", "O2"]
        },
        {
            "name": "Combustion of Ethanol",
            "equation": "C2H5OH + O2 → CO2 + H2O",
            "reactants": ["C2H5OH", "O2"],
            "products": ["CO2", "H2O"]
        }
    ]
    
    print("Balancing various chemical reactions...")
    
    with progress_context(total=len(reactions_to_balance), desc="Balancing reactions", unit="reactions") as progress:
        for reaction_data in reactions_to_balance:
            try:
                print(f"\n{reaction_data['name']}:")
                print(f"  Unbalanced: {reaction_data['equation']}")
                
                # Create molecules
                reactant_molecules = []
                for formula in reaction_data['reactants']:
                    reactant_molecules.append(Molecule(formula=formula))
                
                product_molecules = []
                for formula in reaction_data['products']:
                    product_molecules.append(Molecule(formula=formula))
                
                # Balance the reaction
                balanced_coefficients = balancer.balance_reaction(
                    reactant_molecules, product_molecules
                )
                
                if balanced_coefficients:
                    reactant_coeffs, product_coeffs = balanced_coefficients
                    
                    # Format balanced equation
                    balanced_eq = ""
                    
                    # Add reactants
                    reactant_parts = []
                    for i, (mol, coeff) in enumerate(zip(reactant_molecules, reactant_coeffs)):
                        if coeff == 1:
                            reactant_parts.append(mol.molecular_formula)
                        else:
                            reactant_parts.append(f"{coeff}{mol.molecular_formula}")
                    
                    # Add products
                    product_parts = []
                    for i, (mol, coeff) in enumerate(zip(product_molecules, product_coeffs)):
                        if coeff == 1:
                            product_parts.append(mol.molecular_formula)
                        else:
                            product_parts.append(f"{coeff}{mol.molecular_formula}")
                    
                    balanced_eq = " + ".join(reactant_parts) + " → " + " + ".join(product_parts)
                    print(f"  Balanced:   {balanced_eq}")
                    
                    # Verify mass balance
                    if balancer.verify_balance(reactant_molecules, product_molecules, 
                                             reactant_coeffs, product_coeffs):
                        print("  ✅ Mass balance verified")
                    else:
                        print("  ❌ Mass balance failed")
                
                else:
                    print("  ❌ Could not balance reaction")
                
            except Exception as e:
                print(f"  Error balancing {reaction_data['name']}: {e}")
            
            progress.update(1)


@with_error_handling("reaction analysis")
def reaction_analysis_examples():
    """Examples of analyzing reaction properties."""
    print("\n=== Reaction Analysis Examples ===")
    
    if not REACTIONS_AVAILABLE:
        print("Reaction modules not available. Skipping analysis examples.")
        return
    
    # Analyze different types of reactions
    reactions_to_analyze = [
        {
            "name": "Exothermic Combustion",
            "reactants": ["CH4", "O2"],
            "products": ["CO2", "H2O"],
            "coefficients": ([1, 2], [1, 2])
        },
        {
            "name": "Endothermic Decomposition",
            "reactants": ["CaCO3"],
            "products": ["CaO", "CO2"],
            "coefficients": ([1], [1, 1])
        }
    ]
    
    print("Analyzing reaction properties...")
    
    for reaction_data in reactions_to_analyze:
        try:
            print(f"\n{reaction_data['name']}:")
            
            # Create molecules
            reactants = [Molecule(formula=f) for f in reaction_data['reactants']]
            products = [Molecule(formula=f) for f in reaction_data['products']]
            
            # Create reaction
            reaction = Reaction(
                reactants=reactants,
                products=products,
                name=reaction_data['name']
            )
            
            # Set coefficients if provided
            if 'coefficients' in reaction_data:
                reaction.set_coefficients(*reaction_data['coefficients'])
            
            print(f"  Reaction: {reaction}")
            
            # Calculate molecular weight changes
            reactant_mass = sum(mol.molecular_weight * coeff 
                              for mol, coeff in zip(reactants, reaction_data['coefficients'][0]))
            product_mass = sum(mol.molecular_weight * coeff 
                             for mol, coeff in zip(products, reaction_data['coefficients'][1]))
            
            print(f"  Reactant mass: {reactant_mass:.3f} g/mol")
            print(f"  Product mass: {product_mass:.3f} g/mol")
            print(f"  Mass difference: {abs(product_mass - reactant_mass):.6f} g/mol")
            
            # Analyze reaction type
            reaction_type = analyze_reaction_type(reactants, products)
            print(f"  Reaction type: {reaction_type}")
            
            # Calculate atom economy (theoretical)
            if len(products) == 1:
                atom_economy = (products[0].molecular_weight / reactant_mass) * 100
                print(f"  Atom economy: {atom_economy:.1f}%")
            
        except Exception as e:
            print(f"  Error analyzing {reaction_data['name']}: {e}")


def analyze_reaction_type(reactants, products):
    """Analyze the type of chemical reaction."""
    num_reactants = len(reactants)
    num_products = len(products)
    
    if num_reactants == 1 and num_products > 1:
        return "Decomposition"
    elif num_reactants > 1 and num_products == 1:
        return "Synthesis/Combination"
    elif num_reactants == 2 and num_products == 2:
        # Check for single displacement vs double displacement
        return "Single or Double Displacement"
    elif any("O2" in str(mol.molecular_formula) for mol in reactants):
        if any("CO2" in str(mol.molecular_formula) for mol in products):
            return "Combustion"
    
    return "Unknown/Complex"


@with_error_handling("reaction mechanisms")
def reaction_mechanism_examples():
    """Examples of reaction mechanisms and pathways."""
    print("\n=== Reaction Mechanism Examples ===")
    
    if not REACTIONS_AVAILABLE:
        print("Reaction modules not available. Skipping mechanism examples.")
        return
    
    print("Reaction mechanism concepts (educational examples):")
    
    # Example 1: SN2 mechanism
    print("\n1. SN2 Mechanism (Nucleophilic Substitution):")
    print("   Step 1: Nu⁻ + R-X → [Nu---R---X]⁻ (transition state)")
    print("   Step 2: [Nu---R---X]⁻ → Nu-R + X⁻")
    print("   Characteristics:")
    print("   - Single step (concerted)")
    print("   - Inversion of stereochemistry")
    print("   - Rate depends on both nucleophile and substrate")
    
    # Example 2: SN1 mechanism
    print("\n2. SN1 Mechanism (Nucleophilic Substitution):")
    print("   Step 1: R-X → R⁺ + X⁻ (slow, rate-determining)")
    print("   Step 2: R⁺ + Nu⁻ → R-Nu (fast)")
    print("   Characteristics:")
    print("   - Two steps")
    print("   - Carbocation intermediate")
    print("   - Rate depends only on substrate concentration")
    
    # Example 3: Radical chain reaction
    print("\n3. Radical Chain Reaction (Chlorination of Methane):")
    print("   Initiation: Cl₂ → 2Cl• (light/heat)")
    print("   Propagation:")
    print("     CH₄ + Cl• → CH₃• + HCl")
    print("     CH₃• + Cl₂ → CH₃Cl + Cl•")
    print("   Termination:")
    print("     Cl• + Cl• → Cl₂")
    print("     CH₃• + CH₃• → C₂H₆")
    print("     CH₃• + Cl• → CH₃Cl")
    
    # Example 4: Enzyme catalysis
    print("\n4. Enzyme Catalysis (Michaelis-Menten):")
    print("   E + S ⇌ ES → E + P")
    print("   Where:")
    print("   - E = Enzyme")
    print("   - S = Substrate")
    print("   - ES = Enzyme-Substrate complex")
    print("   - P = Product")
    print("   Key concepts:")
    print("   - Lowers activation energy")
    print("   - Increases reaction rate")
    print("   - Enzyme is regenerated")


@with_error_handling("reaction kinetics")
def reaction_kinetics_examples():
    """Examples of reaction kinetics calculations."""
    print("\n=== Reaction Kinetics Examples ===")
    
    print("Reaction kinetics concepts and calculations:")
    
    # Rate law examples
    print("\n1. Rate Laws:")
    print("   For reaction: A + B → C")
    print("   Rate = k[A]ᵐ[B]ⁿ")
    print("   Where:")
    print("   - k = rate constant")
    print("   - m, n = reaction orders")
    print("   - [A], [B] = concentrations")
    
    # Half-life calculations
    print("\n2. Half-Life Calculations:")
    print("   First-order: t₁/₂ = ln(2)/k = 0.693/k")
    print("   Second-order: t₁/₂ = 1/(k[A]₀)")
    print("   Zero-order: t₁/₂ = [A]₀/(2k)")
    
    # Arrhenius equation
    print("\n3. Arrhenius Equation:")
    print("   k = A·e^(-Ea/RT)")
    print("   Where:")
    print("   - A = pre-exponential factor")
    print("   - Ea = activation energy")
    print("   - R = gas constant")
    print("   - T = temperature")
    
    # Example calculation
    print("\n4. Example Calculation:")
    print("   Given: k₁ = 1.0×10⁻³ s⁻¹ at T₁ = 298 K")
    print("          k₂ = 2.0×10⁻³ s⁻¹ at T₂ = 308 K")
    print("   Find: Activation energy (Ea)")
    print("   Solution:")
    print("   ln(k₂/k₁) = -Ea/R × (1/T₂ - 1/T₁)")
    print("   Ea = -R × ln(k₂/k₁) / (1/T₂ - 1/T₁)")
    
    # Calculate example
    import math
    k1, k2 = 1.0e-3, 2.0e-3
    T1, T2 = 298, 308
    R = 8.314  # J/(mol·K)
    
    Ea = -R * math.log(k2/k1) / (1/T2 - 1/T1)
    print(f"   Ea = {Ea:.0f} J/mol = {Ea/1000:.1f} kJ/mol")


def main():
    """Run all reaction examples."""
    print("Chemesty Reaction Modeling Examples")
    print("==================================")
    
    if not REACTIONS_AVAILABLE:
        print("\n⚠️  Note: Reaction modules are not fully available.")
        print("Some examples will show conceptual information only.")
        print()
    
    try:
        basic_reaction_examples()
        reaction_balancing_examples()
        reaction_analysis_examples()
        reaction_mechanism_examples()
        reaction_kinetics_examples()
        
        print("\n✅ Reaction modeling examples completed!")
        
        print("\n" + "=" * 50)
        print("🆕 NEW: Intuitive Reaction Operator Syntax!")
        print("=" * 50)
        print()
        print("Chemesty now supports intuitive reaction syntax using & and >> operators:")
        print()
        print("✨ Basic Syntax:")
        print("   • Use & to combine reactants or products: CH4 & O2")
        print("   • Use >> to create reactions: reactants >> products")
        print("   • Use (coeff, molecule) for stoichiometry: (2, O2)")
        print()
        print("✨ Examples:")
        print("   • Simple: H2 >> H2O")
        print("   • Complex: (CH4 & (2, O2)) >> (CO2 & (2, H2O))")
        print("   • Helper: create_reaction_side((2, H2), O2) >> (2, H2O)")
        print()
        print("✨ Benefits:")
        print("   • More intuitive and readable")
        print("   • Matches mathematical notation")
        print("   • Fully compatible with existing methods")
        print("   • All analysis tools work the same way")
        print()
        print("📚 For comprehensive examples and documentation:")
        print("   python examples/reaction_operator_examples.py")
        print()
        print("🔗 Both traditional and operator methods are fully supported!")
        
    except Exception as e:
        print(f"\n❌ Error running reaction examples: {e}")
        print("This may be due to missing dependencies or configuration issues.")


if __name__ == "__main__":
    main()