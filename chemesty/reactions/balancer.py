"""
Chemical equation balancing algorithms.

This module provides algorithms for automatically balancing chemical equations
using matrix algebra and optimization techniques.
"""

import numpy as np
from typing import List, Dict, Optional, Tuple, Union
from fractions import Fraction
from chemesty.reactions.reaction import Reaction, ReactionComponent
from chemesty.molecules.molecule import Molecule


class ReactionBalancer:
    """
    Automatic chemical equation balancer using matrix algebra.
    
    This class implements algorithms to find stoichiometric coefficients
    that balance chemical equations by solving systems of linear equations.
    """
    
    def __init__(self, tolerance: float = 1e-10):
        """
        Initialize the reaction balancer.
        
        Args:
            tolerance: Numerical tolerance for balance checking
        """
        self.tolerance = tolerance
    
    def balance_reaction(self, reaction: Reaction) -> Reaction:
        """
        Balance a chemical reaction automatically.
        
        Args:
            reaction: Unbalanced reaction to balance
            
        Returns:
            New balanced reaction with updated coefficients
            
        Raises:
            ValueError: If the reaction cannot be balanced
        """
        if reaction.is_balanced(self.tolerance):
            return reaction  # Already balanced
        
        # Get all molecules (excluding catalysts)
        reactants = [r for r in reaction.reactants if not r.is_catalyst]
        products = reaction.products
        catalysts = [r for r in reaction.reactants if r.is_catalyst]
        
        if not reactants or not products:
            raise ValueError("Reaction must have both reactants and products to balance")
        
        all_molecules = reactants + products
        
        # Build element matrix
        element_matrix, elements = self._build_element_matrix(all_molecules)
        
        # Solve for coefficients
        coefficients = self._solve_balance_equation(element_matrix)
        
        if coefficients is None:
            raise ValueError("Unable to balance this reaction - may be impossible to balance")
        
        # Create new balanced reaction
        balanced_reaction = Reaction(
            name=reaction.name,
            temperature=reaction.temperature,
            pressure=reaction.pressure,
            conditions=reaction.conditions.copy()
        )
        
        # Add balanced reactants
        for i, reactant in enumerate(reactants):
            balanced_reaction.add_reactant(
                reactant.molecule,
                coefficients[i],
                reactant.phase,
                reactant.is_catalyst
            )
        
        # Add catalysts (unchanged)
        for catalyst in catalysts:
            balanced_reaction.add_reactant(
                catalyst.molecule,
                catalyst.coefficient,
                catalyst.phase,
                catalyst.is_catalyst
            )
        
        # Add balanced products
        for i, product in enumerate(products):
            balanced_reaction.add_product(
                product.molecule,
                coefficients[len(reactants) + i],
                product.phase
            )
        
        return balanced_reaction
    
    def _build_element_matrix(self, molecules: List[ReactionComponent]) -> Tuple[np.ndarray, List[str]]:
        """
        Build the element composition matrix for balancing.
        
        Args:
            molecules: List of reaction components
            
        Returns:
            Tuple of (element_matrix, element_list)
        """
        # Get all unique elements
        all_elements = set()
        for component in molecules:
            for element in component.molecule.elements.keys():
                all_elements.add(element.symbol)
        
        elements = sorted(list(all_elements))
        
        # Build matrix: rows = elements, columns = molecules
        # For balancing: reactants have negative coefficients, products positive
        matrix = np.zeros((len(elements), len(molecules)))
        
        for j, component in enumerate(molecules):
            for element, count in component.molecule.elements.items():
                i = elements.index(element.symbol)
                # Note: we'll handle the sign in the balance equation solving
                matrix[i, j] = count
        
        return matrix, elements
    
    def _solve_balance_equation(self, element_matrix: np.ndarray) -> Optional[List[float]]:
        """
        Solve the balance equation using null space method.
        
        Args:
            element_matrix: Element composition matrix
            
        Returns:
            List of coefficients or None if no solution exists
        """
        try:
            # For balancing, we need to find the null space of the element matrix
            # The equation is: element_matrix @ coefficients = 0
            
            # Use SVD to find null space
            U, s, Vt = np.linalg.svd(element_matrix)
            
            # Find the null space (columns of V corresponding to zero singular values)
            # Use a more lenient tolerance for finding null space
            null_space_tolerance = max(self.tolerance, 1e-8)
            null_space_dim = np.sum(s < null_space_tolerance)
            
            if null_space_dim == 0:
                # Try with the smallest singular value if no clear null space
                coefficients = Vt[-1, :]
            else:
                # Take the last column of Vt (corresponding to smallest singular value)
                coefficients = Vt[-1, :]
            
            # Make all coefficients positive
            if np.any(coefficients < 0):
                coefficients = -coefficients
            
            # Ensure no coefficient is zero (set minimum value)
            coefficients = np.maximum(coefficients, 1e-10)
            
            # Convert to positive integers
            coefficients = self._rationalize_coefficients(coefficients)
            
            # Verify the solution works
            if self._verify_solution(element_matrix, coefficients):
                return coefficients.tolist()
            else:
                return None
            
        except (np.linalg.LinAlgError, ValueError):
            return None
    
    def _verify_solution(self, element_matrix: np.ndarray, coefficients: np.ndarray) -> bool:
        """
        Verify that the coefficients balance the equation.
        
        Args:
            element_matrix: Element composition matrix
            coefficients: Proposed coefficients
            
        Returns:
            True if solution is valid
        """
        try:
            # Check if element_matrix @ coefficients ≈ 0
            result = element_matrix @ coefficients
            return np.allclose(result, 0, atol=1e-6)
        except:
            return False
    
    def _rationalize_coefficients(self, coefficients: np.ndarray) -> np.ndarray:
        """
        Convert floating point coefficients to rational numbers.
        
        Args:
            coefficients: Array of floating point coefficients
            
        Returns:
            Array of rational coefficients as floats
        """
        # Convert to fractions to handle rational numbers exactly
        fractions = [Fraction(float(c)).limit_denominator(10000) for c in coefficients]
        
        # Find common denominator
        denominators = [f.denominator for f in fractions]
        common_denom = 1
        for d in denominators:
            common_denom = common_denom * d // np.gcd(common_denom, d)
        
        # Convert to integers
        int_coeffs = [int(f * common_denom) for f in fractions]
        
        # Find GCD to reduce to smallest integers
        from math import gcd
        from functools import reduce
        
        coeff_gcd = reduce(gcd, int_coeffs)
        if coeff_gcd > 0:
            int_coeffs = [c // coeff_gcd for c in int_coeffs]
        
        return np.array(int_coeffs, dtype=float)
    
    def balance_equation_string(self, equation: str) -> str:
        """
        Balance a chemical equation from string representation.
        
        Args:
            equation: Chemical equation string (e.g., "H2 + O2 -> H2O")
            
        Returns:
            Balanced equation string
            
        Raises:
            ValueError: If equation format is invalid or cannot be balanced
        """
        reaction = self._parse_equation_string(equation)
        balanced_reaction = self.balance_reaction(reaction)
        return str(balanced_reaction)
    
    def _parse_equation_string(self, equation: str) -> Reaction:
        """
        Parse a chemical equation string into a Reaction object.
        
        Args:
            equation: Chemical equation string
            
        Returns:
            Reaction object
            
        Raises:
            ValueError: If equation format is invalid
        """
        # Remove spaces and split by arrow
        equation = equation.replace(" ", "")
        
        # Handle different arrow types
        if "->" in equation:
            reactant_str, product_str = equation.split("->", 1)
        elif "→" in equation:
            reactant_str, product_str = equation.split("→", 1)
        elif "=" in equation:
            reactant_str, product_str = equation.split("=", 1)
        else:
            raise ValueError("Invalid equation format: no arrow or equals sign found")
        
        reaction = Reaction()
        
        # Parse reactants
        if reactant_str.strip():
            reactants = reactant_str.split("+")
            for reactant in reactants:
                reactant = reactant.strip()
                if reactant:
                    # Extract coefficient if present
                    coeff, formula = self._extract_coefficient(reactant)
                    reaction.add_reactant(formula, coeff)
        
        # Parse products
        if product_str.strip():
            products = product_str.split("+")
            for product in products:
                product = product.strip()
                if product:
                    # Extract coefficient if present
                    coeff, formula = self._extract_coefficient(product)
                    reaction.add_product(formula, coeff)
        
        return reaction
    
    def _extract_coefficient(self, term: str) -> Tuple[float, str]:
        """
        Extract coefficient and formula from a term.
        
        Args:
            term: Chemical term (e.g., "2H2O", "H2O")
            
        Returns:
            Tuple of (coefficient, formula)
        """
        import re
        
        # Match coefficient at the beginning
        match = re.match(r'^(\d*\.?\d*)(.*)', term)
        if match:
            coeff_str, formula = match.groups()
            if coeff_str:
                coefficient = float(coeff_str)
            else:
                coefficient = 1.0
            return coefficient, formula
        else:
            return 1.0, term
    
    def suggest_balancing_steps(self, reaction: Reaction) -> List[str]:
        """
        Provide step-by-step suggestions for manually balancing a reaction.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            List of balancing suggestions
        """
        suggestions = []
        
        if reaction.is_balanced():
            suggestions.append("Reaction is already balanced!")
            return suggestions
        
        # Analyze unbalanced elements
        unbalanced = reaction.get_unbalanced_elements()
        
        suggestions.append("Unbalanced elements found:")
        for element, imbalance in unbalanced.items():
            if imbalance > 0:
                suggestions.append(f"  - {element}: excess in products (+{imbalance:.3f})")
            else:
                suggestions.append(f"  - {element}: excess in reactants ({imbalance:.3f})")
        
        # Suggest starting with most complex molecule
        all_molecules = []
        for r in reaction.reactants:
            if not r.is_catalyst:
                all_molecules.append((r.molecule, "reactant"))
        for p in reaction.products:
            all_molecules.append((p.molecule, "product"))
        
        if all_molecules:
            # Find most complex molecule (most elements)
            most_complex = max(all_molecules, key=lambda x: len(x[0].elements))
            suggestions.append(f"\nSuggestion: Start by balancing the most complex molecule:")
            suggestions.append(f"  - {most_complex[0].molecular_formula} ({most_complex[1]})")
        
        # Suggest balancing order
        element_complexity = {}
        for element in unbalanced.keys():
            count = 0
            for mol, _ in all_molecules:
                if any(e.symbol == element for e in mol.elements.keys()):
                    count += 1
            element_complexity[element] = count
        
        if element_complexity:
            sorted_elements = sorted(element_complexity.items(), key=lambda x: x[1])
            suggestions.append(f"\nSuggested balancing order (least to most complex):")
            for element, complexity in sorted_elements:
                suggestions.append(f"  - {element} (appears in {complexity} molecules)")
        
        return suggestions
    
    def verify_balance(self, reaction: Reaction) -> Dict[str, any]:
        """
        Verify and analyze the balance of a reaction.
        
        Args:
            reaction: Reaction to verify
            
        Returns:
            Dictionary with balance analysis results
        """
        element_balance = reaction.get_element_balance()
        mass_balance = reaction.get_molecular_weight_balance()
        
        balanced_elements = {k: v for k, v in element_balance.items() 
                           if abs(v) < self.tolerance}
        unbalanced_elements = {k: v for k, v in element_balance.items() 
                             if abs(v) >= self.tolerance}
        
        return {
            'is_balanced': reaction.is_balanced(self.tolerance),
            'element_balance': element_balance,
            'balanced_elements': balanced_elements,
            'unbalanced_elements': unbalanced_elements,
            'mass_balance': mass_balance,
            'mass_balanced': abs(mass_balance) < self.tolerance,
            'total_reactant_mass': sum(r.coefficient * r.molecule.molecular_weight 
                                     for r in reaction.reactants if not r.is_catalyst),
            'total_product_mass': sum(p.coefficient * p.molecule.molecular_weight 
                                    for p in reaction.products),
            'num_reactants': len([r for r in reaction.reactants if not r.is_catalyst]),
            'num_products': len(reaction.products),
            'num_catalysts': len([r for r in reaction.reactants if r.is_catalyst])
        }