"""
Chemical reaction analysis and kinetics.

This module provides tools for analyzing chemical reactions, calculating
reaction rates, equilibrium constants, and other kinetic parameters.
"""

from typing import Dict, List, Optional, Tuple, Union, Any
import math
from chemesty.reactions.reaction import Reaction, ReactionComponent
from chemesty.molecules.molecule import Molecule


class ReactionAnalyzer:
    """
    Analyzer for chemical reaction properties and kinetics.
    
    This class provides methods for analyzing reaction mechanisms,
    calculating rate constants, and determining reaction feasibility.
    """
    
    def __init__(self):
        """Initialize the reaction analyzer."""
        self.gas_constant = 8.314  # J/(mol·K)
        self.avogadro = 6.022e23   # mol⁻¹
        self.boltzmann = 1.381e-23 # J/K
    
    def analyze_reaction_type(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Analyze and classify the type of chemical reaction.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary containing reaction type analysis
        """
        reactants = [r for r in reaction.reactants if not r.is_catalyst]
        products = reaction.products
        
        analysis = {
            'num_reactants': len(reactants),
            'num_products': len(products),
            'num_catalysts': len(reaction.get_catalysts()),
            'reaction_types': [],
            'complexity': 'unknown'
        }
        
        # Basic classification by stoichiometry
        if len(reactants) == 1 and len(products) == 1:
            analysis['reaction_types'].append('isomerization')
            analysis['complexity'] = 'simple'
        elif len(reactants) == 1 and len(products) > 1:
            analysis['reaction_types'].append('decomposition')
            analysis['complexity'] = 'simple'
        elif len(reactants) > 1 and len(products) == 1:
            analysis['reaction_types'].append('combination/synthesis')
            analysis['complexity'] = 'simple'
        elif len(reactants) == 2 and len(products) == 2:
            analysis['reaction_types'].append('double_displacement')
            analysis['complexity'] = 'moderate'
        else:
            analysis['reaction_types'].append('complex')
            analysis['complexity'] = 'complex'
        
        # Check for redox reactions
        if self._is_redox_reaction(reaction):
            analysis['reaction_types'].append('redox')
        
        # Check for acid-base reactions
        if self._is_acid_base_reaction(reaction):
            analysis['reaction_types'].append('acid_base')
        
        # Check for precipitation reactions
        if self._has_phase_changes(reaction):
            analysis['reaction_types'].append('precipitation')
        
        return analysis
    
    def _is_redox_reaction(self, reaction: Reaction) -> bool:
        """
        Check if reaction involves oxidation-reduction.
        
        Args:
            reaction: Reaction to check
            
        Returns:
            True if reaction is redox
        """
        # Simple heuristic: check for common oxidizing/reducing agents
        oxidizing_agents = {'O2', 'H2O2', 'KMnO4', 'K2Cr2O7', 'HNO3'}
        reducing_agents = {'H2', 'C', 'CO', 'Zn', 'Fe', 'Al'}
        
        reactant_formulas = {r.molecule.molecular_formula for r in reaction.reactants}
        
        has_oxidizer = any(formula in oxidizing_agents for formula in reactant_formulas)
        has_reducer = any(formula in reducing_agents for formula in reactant_formulas)
        
        return has_oxidizer and has_reducer
    
    def _is_acid_base_reaction(self, reaction: Reaction) -> bool:
        """
        Check if reaction is acid-base neutralization.
        
        Args:
            reaction: Reaction to check
            
        Returns:
            True if reaction is acid-base
        """
        # Simple heuristic: look for H+ transfer or common acids/bases
        acids = {'HCl', 'H2SO4', 'HNO3', 'CH3COOH', 'H3PO4'}
        bases = {'NaOH', 'KOH', 'Ca(OH)2', 'NH3', 'Mg(OH)2'}
        
        reactant_formulas = {r.molecule.molecular_formula for r in reaction.reactants}
        product_formulas = {p.molecule.molecular_formula for p in reaction.products}
        
        has_acid = any(formula in acids for formula in reactant_formulas)
        has_base = any(formula in bases for formula in reactant_formulas)
        has_water = 'H2O' in product_formulas
        
        return has_acid and has_base and has_water
    
    def _has_phase_changes(self, reaction: Reaction) -> bool:
        """
        Check if reaction involves phase changes.
        
        Args:
            reaction: Reaction to check
            
        Returns:
            True if reaction has phase changes
        """
        phases = set()
        for component in reaction.reactants + reaction.products:
            if component.phase:
                phases.add(component.phase)
        
        return len(phases) > 1
    
    def calculate_atom_economy(self, reaction: Reaction) -> float:
        """
        Calculate the atom economy of a reaction.
        
        Atom economy = (MW of desired product / MW of all products) × 100%
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Atom economy percentage
        """
        if not reaction.products:
            return 0.0
        
        # Assume first product is the desired product
        desired_product = reaction.products[0]
        desired_mw = desired_product.coefficient * desired_product.molecule.molecular_weight
        
        total_product_mw = sum(p.coefficient * p.molecule.molecular_weight 
                              for p in reaction.products)
        
        if total_product_mw == 0:
            return 0.0
        
        return (desired_mw / total_product_mw) * 100.0
    
    def calculate_mass_balance_error(self, reaction: Reaction) -> float:
        """
        Calculate the mass balance error as a percentage.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Mass balance error percentage
        """
        reactant_mass = sum(r.coefficient * r.molecule.molecular_weight 
                          for r in reaction.reactants if not r.is_catalyst)
        product_mass = sum(p.coefficient * p.molecule.molecular_weight 
                         for p in reaction.products)
        
        if reactant_mass == 0:
            return float('inf') if product_mass > 0 else 0.0
        
        return abs(product_mass - reactant_mass) / reactant_mass * 100.0
    
    def estimate_reaction_rate_order(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Estimate the likely reaction order based on mechanism.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with rate order estimates
        """
        reactants = [r for r in reaction.reactants if not r.is_catalyst]
        
        # Simple heuristics for rate order estimation
        if len(reactants) == 1:
            # Unimolecular reactions are typically first order
            overall_order = 1
            individual_orders = {reactants[0].molecule.molecular_formula: 1}
        elif len(reactants) == 2:
            # Bimolecular reactions are typically second order overall
            overall_order = 2
            individual_orders = {r.molecule.molecular_formula: 1 for r in reactants}
        else:
            # Complex reactions - estimate based on stoichiometry
            overall_order = sum(r.coefficient for r in reactants)
            individual_orders = {r.molecule.molecular_formula: r.coefficient 
                               for r in reactants}
        
        return {
            'estimated_overall_order': overall_order,
            'estimated_individual_orders': individual_orders,
            'confidence': 'low',  # These are just estimates
            'notes': 'Estimates based on stoichiometry and mechanism heuristics'
        }
    
    def calculate_theoretical_yield(self, reaction: Reaction, 
                                  limiting_reactant: str,
                                  reactant_amounts: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate theoretical yields for all products.
        
        Args:
            reaction: Balanced reaction
            limiting_reactant: Formula of limiting reactant
            reactant_amounts: Dictionary of reactant amounts (moles)
            
        Returns:
            Dictionary of theoretical yields (moles) for each product
        """
        if not reaction.is_balanced():
            raise ValueError("Reaction must be balanced to calculate theoretical yield")
        
        # Find limiting reactant component
        limiting_component = None
        for r in reaction.reactants:
            if r.molecule.molecular_formula == limiting_reactant and not r.is_catalyst:
                limiting_component = r
                break
        
        if limiting_component is None:
            raise ValueError(f"Limiting reactant {limiting_reactant} not found in reaction")
        
        limiting_amount = reactant_amounts.get(limiting_reactant, 0)
        
        # Calculate yields based on stoichiometry
        yields = {}
        for product in reaction.products:
            # Mole ratio: product coefficient / limiting reactant coefficient
            mole_ratio = product.coefficient / limiting_component.coefficient
            theoretical_yield = limiting_amount * mole_ratio
            yields[product.molecule.molecular_formula] = theoretical_yield
        
        return yields
    
    def analyze_equilibrium_position(self, reaction: Reaction, 
                                   temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Analyze the equilibrium position of a reaction.
        
        Args:
            reaction: Reaction to analyze
            temperature: Temperature in Kelvin
            
        Returns:
            Dictionary with equilibrium analysis
        """
        analysis = {
            'reversible': True,  # Assume all reactions are potentially reversible
            'temperature': temperature or reaction.temperature,
            'factors_favoring_products': [],
            'factors_favoring_reactants': [],
            'le_chatelier_predictions': {}
        }
        
        # Analyze Le Chatelier's principle factors
        reactants = [r for r in reaction.reactants if not r.is_catalyst]
        products = reaction.products
        
        # Count gas molecules
        reactant_gas_count = sum(1 for r in reactants if r.phase == 'g')
        product_gas_count = sum(1 for p in products if p.phase == 'g')
        
        if product_gas_count < reactant_gas_count:
            analysis['factors_favoring_products'].append('decreased gas molecules (high pressure)')
            analysis['le_chatelier_predictions']['pressure_increase'] = 'favors products'
        elif product_gas_count > reactant_gas_count:
            analysis['factors_favoring_reactants'].append('increased gas molecules (low pressure)')
            analysis['le_chatelier_predictions']['pressure_increase'] = 'favors reactants'
        
        # Temperature effects (simplified)
        if temperature:
            if temperature > 298:  # Assume high temperature
                analysis['le_chatelier_predictions']['temperature_increase'] = 'depends on ΔH'
            else:
                analysis['le_chatelier_predictions']['temperature_increase'] = 'depends on ΔH'
        
        return analysis
    
    def suggest_reaction_conditions(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Suggest optimal reaction conditions.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with condition suggestions
        """
        suggestions = {
            'temperature': {},
            'pressure': {},
            'catalysts': {},
            'concentration': {},
            'other': []
        }
        
        reaction_type = self.analyze_reaction_type(reaction)
        
        # Temperature suggestions
        if 'decomposition' in reaction_type['reaction_types']:
            suggestions['temperature']['recommendation'] = 'high'
            suggestions['temperature']['reason'] = 'decomposition reactions typically require heat'
        elif 'combination' in reaction_type['reaction_types']:
            suggestions['temperature']['recommendation'] = 'moderate'
            suggestions['temperature']['reason'] = 'combination reactions may be exothermic'
        
        # Pressure suggestions
        reactants = [r for r in reaction.reactants if not r.is_catalyst]
        products = reaction.products
        
        reactant_gas_count = sum(1 for r in reactants if r.phase == 'g')
        product_gas_count = sum(1 for p in products if p.phase == 'g')
        
        if product_gas_count < reactant_gas_count:
            suggestions['pressure']['recommendation'] = 'high'
            suggestions['pressure']['reason'] = 'high pressure favors fewer gas molecules'
        elif product_gas_count > reactant_gas_count:
            suggestions['pressure']['recommendation'] = 'low'
            suggestions['pressure']['reason'] = 'low pressure favors more gas molecules'
        
        # Catalyst suggestions
        if reaction_type['complexity'] == 'complex':
            suggestions['catalysts']['recommendation'] = 'consider catalyst'
            suggestions['catalysts']['reason'] = 'complex reactions often benefit from catalysis'
        
        # Concentration suggestions
        suggestions['concentration']['recommendation'] = 'optimize reactant concentrations'
        suggestions['concentration']['reason'] = 'proper stoichiometric ratios improve yield'
        
        # Other suggestions
        if any(r.phase == 's' for r in reactants):
            suggestions['other'].append('increase surface area of solid reactants')
        
        if any(p.phase == 'g' for p in products):
            suggestions['other'].append('consider product removal to drive reaction forward')
        
        return suggestions
    
    def calculate_reaction_quotient(self, reaction: Reaction, 
                                  concentrations: Dict[str, float]) -> float:
        """
        Calculate the reaction quotient Q.
        
        Args:
            reaction: Balanced reaction
            concentrations: Dictionary of concentrations (mol/L)
            
        Returns:
            Reaction quotient value
        """
        if not reaction.is_balanced():
            raise ValueError("Reaction must be balanced to calculate reaction quotient")
        
        q_numerator = 1.0
        q_denominator = 1.0
        
        # Products in numerator
        for product in reaction.products:
            formula = product.molecule.molecular_formula
            if formula in concentrations:
                q_numerator *= concentrations[formula] ** product.coefficient
        
        # Reactants in denominator (excluding catalysts)
        for reactant in reaction.reactants:
            if not reactant.is_catalyst:
                formula = reactant.molecule.molecular_formula
                if formula in concentrations:
                    q_denominator *= concentrations[formula] ** reactant.coefficient
        
        return q_numerator / q_denominator if q_denominator != 0 else float('inf')
    
    def analyze_reaction_feasibility(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Analyze the thermodynamic feasibility of a reaction.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with feasibility analysis
        """
        analysis = {
            'mass_balanced': reaction.is_balanced(),
            'charge_balanced': True,  # Simplified assumption
            'thermodynamically_feasible': 'unknown',
            'kinetically_feasible': 'unknown',
            'recommendations': []
        }
        
        if not analysis['mass_balanced']:
            analysis['recommendations'].append('Balance the chemical equation first')
            analysis['thermodynamically_feasible'] = 'cannot_determine'
        
        # Check for obvious impossibilities
        reactant_elements = set()
        for r in reaction.reactants:
            if not r.is_catalyst:
                reactant_elements.update(e.symbol for e in r.molecule.elements.keys())
        
        product_elements = set()
        for p in reaction.products:
            product_elements.update(e.symbol for e in p.molecule.elements.keys())
        
        if not product_elements.issubset(reactant_elements):
            analysis['thermodynamically_feasible'] = 'impossible'
            analysis['recommendations'].append('Products contain elements not present in reactants')
        
        # Add general recommendations
        if analysis['mass_balanced'] and analysis['thermodynamically_feasible'] != 'impossible':
            analysis['recommendations'].extend([
                'Calculate Gibbs free energy change (ΔG) for definitive feasibility',
                'Consider activation energy and reaction kinetics',
                'Optimize reaction conditions (temperature, pressure, catalysts)'
            ])
        
        return analysis