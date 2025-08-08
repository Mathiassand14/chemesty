"""
Offline Reaction Analyzer Module

This module provides tools for analyzing chemical reactions without relying on
external resources or online connectivity. It implements advanced algorithms
for reaction type detection, oxidation state analysis, functional group analysis,
and other chemical reaction properties.
"""

from typing import Dict, List, Optional, Tuple, Union, Any, Set
import math
from collections import defaultdict

from chemesty.reactions.reaction import Reaction, ReactionComponent
from chemesty.reactions.analyzer import ReactionAnalyzer
from chemesty.molecules.molecule import Molecule


class OfflineReactionAnalyzer(ReactionAnalyzer):
    """
    Enhanced offline analyzer for chemical reaction properties and kinetics.
    
    This class extends the base ReactionAnalyzer with advanced offline algorithms
    for reaction type detection, oxidation state analysis, functional group analysis,
    and other chemical reaction properties without relying on external resources.
    """
    
    def __init__(self):
        """Initialize the offline reaction analyzer."""
        super().__init__()
        
        # Common oxidation states for elements
        self.common_oxidation_states = {
            'H': [1, -1],
            'Li': [1],
            'Na': [1],
            'K': [1],
            'Rb': [1],
            'Cs': [1],
            'Be': [2],
            'Mg': [2],
            'Ca': [2],
            'Sr': [2],
            'Ba': [2],
            'B': [3],
            'Al': [3],
            'Ga': [3],
            'In': [3],
            'C': [-4, -3, -2, -1, 0, 1, 2, 3, 4],
            'Si': [-4, 4],
            'Ge': [-4, 2, 4],
            'N': [-3, -2, -1, 0, 1, 2, 3, 4, 5],
            'P': [-3, 3, 5],
            'As': [-3, 3, 5],
            'O': [-2, -1, 0, 1, 2],
            'S': [-2, 0, 2, 4, 6],
            'Se': [-2, 0, 2, 4, 6],
            'F': [-1],
            'Cl': [-1, 0, 1, 3, 5, 7],
            'Br': [-1, 0, 1, 3, 5, 7],
            'I': [-1, 0, 1, 3, 5, 7],
            'Fe': [2, 3],
            'Co': [2, 3],
            'Ni': [2, 3],
            'Cu': [1, 2],
            'Ag': [1],
            'Au': [1, 3],
            'Zn': [2],
            'Cd': [2],
            'Hg': [1, 2],
            'Mn': [2, 3, 4, 6, 7],
            'Cr': [2, 3, 6],
            'Mo': [2, 3, 4, 5, 6],
            'W': [2, 3, 4, 5, 6],
            'V': [2, 3, 4, 5],
            'Ti': [2, 3, 4],
            'Pt': [2, 4],
            'Pd': [2, 4],
        }
        
        # Electronegativity values for elements (Pauling scale)
        self.electronegativity = {
            'H': 2.20, 'Li': 0.98, 'Be': 1.57, 'B': 2.04, 'C': 2.55, 'N': 3.04, 'O': 3.44, 'F': 3.98,
            'Na': 0.93, 'Mg': 1.31, 'Al': 1.61, 'Si': 1.90, 'P': 2.19, 'S': 2.58, 'Cl': 3.16,
            'K': 0.82, 'Ca': 1.00, 'Sc': 1.36, 'Ti': 1.54, 'V': 1.63, 'Cr': 1.66, 'Mn': 1.55,
            'Fe': 1.83, 'Co': 1.88, 'Ni': 1.91, 'Cu': 1.90, 'Zn': 1.65, 'Ga': 1.81, 'Ge': 2.01,
            'As': 2.18, 'Se': 2.55, 'Br': 2.96, 'Rb': 0.82, 'Sr': 0.95, 'Y': 1.22, 'Zr': 1.33,
            'Nb': 1.6, 'Mo': 2.16, 'Tc': 1.9, 'Ru': 2.2, 'Rh': 2.28, 'Pd': 2.20, 'Ag': 1.93,
            'Cd': 1.69, 'In': 1.78, 'Sn': 1.96, 'Sb': 2.05, 'Te': 2.1, 'I': 2.66, 'Cs': 0.79,
            'Ba': 0.89, 'La': 1.1, 'Ce': 1.12, 'Pr': 1.13, 'Nd': 1.14, 'Pm': 1.13, 'Sm': 1.17,
            'Eu': 1.2, 'Gd': 1.2, 'Tb': 1.1, 'Dy': 1.22, 'Ho': 1.23, 'Er': 1.24, 'Tm': 1.25,
            'Yb': 1.1, 'Lu': 1.27, 'Hf': 1.3, 'Ta': 1.5, 'W': 2.36, 'Re': 1.9, 'Os': 2.2,
            'Ir': 2.20, 'Pt': 2.28, 'Au': 2.54, 'Hg': 2.00, 'Tl': 1.62, 'Pb': 2.33, 'Bi': 2.02,
            'Po': 2.0, 'At': 2.2, 'Fr': 0.7, 'Ra': 0.9, 'Ac': 1.1, 'Th': 1.3, 'Pa': 1.5,
            'U': 1.38, 'Np': 1.36, 'Pu': 1.28, 'Am': 1.3, 'Cm': 1.3, 'Bk': 1.3, 'Cf': 1.3,
            'Es': 1.3, 'Fm': 1.3, 'Md': 1.3, 'No': 1.3, 'Lr': 1.3
        }
        
        # Common functional groups
        self.functional_groups = {
            'alcohol': ['OH'],
            'aldehyde': ['CHO'],
            'ketone': ['CO'],
            'carboxylic_acid': ['COOH'],
            'ester': ['COO'],
            'ether': ['O'],
            'amine': ['NH2', 'NH', 'N'],
            'amide': ['CONH2', 'CONH'],
            'nitrile': ['CN'],
            'nitro': ['NO2'],
            'sulfide': ['S'],
            'sulfoxide': ['SO'],
            'sulfone': ['SO2'],
            'thiol': ['SH'],
            'halide': ['F', 'Cl', 'Br', 'I']
        }
        
        # Common acids and bases
        self.acids = {
            'HCl': 'strong', 'H2SO4': 'strong', 'HNO3': 'strong', 
            'HBr': 'strong', 'HI': 'strong', 'HClO4': 'strong',
            'H3PO4': 'weak', 'CH3COOH': 'weak', 'HF': 'weak', 
            'H2CO3': 'weak', 'H2S': 'weak', 'HCN': 'weak'
        }
        
        self.bases = {
            'NaOH': 'strong', 'KOH': 'strong', 'LiOH': 'strong', 
            'Ca(OH)2': 'strong', 'Ba(OH)2': 'strong', 'Sr(OH)2': 'strong',
            'NH3': 'weak', 'CH3NH2': 'weak', 'C5H5N': 'weak'
        }
        
        # Rules for reaction type classification
        self.reaction_rules = self._initialize_reaction_rules()
    
    def _initialize_reaction_rules(self) -> List[Dict[str, Any]]:
        """
        Initialize the rule-based expert system for reaction classification.
        
        Returns:
            List of rules with conditions and confidence scores
        """
        return [
            # Rule for combustion reactions
            {
                'name': 'combustion',
                'condition': lambda r: (
                    any('C' in comp.molecule.elements and 'H' in comp.molecule.elements 
                        for comp in r.reactants) and
                    any(comp.molecule.molecular_formula == 'O2' for comp in r.reactants) and
                    any(comp.molecule.molecular_formula == 'CO2' for comp in r.products) and
                    any(comp.molecule.molecular_formula == 'H2O' for comp in r.products)
                ),
                'confidence': 0.95
            },
            
            # Rule for acid-base reactions
            {
                'name': 'acid_base',
                'condition': lambda r: (
                    self._contains_acid(r.reactants) and
                    self._contains_base(r.reactants) and
                    any(comp.molecule.molecular_formula == 'H2O' for comp in r.products)
                ),
                'confidence': 0.9
            },
            
            # Rule for precipitation reactions
            {
                'name': 'precipitation',
                'condition': lambda r: (
                    any(comp.phase == 'aq' for comp in r.reactants) and
                    any(comp.phase == 's' for comp in r.products) and
                    len(r.reactants) >= 2
                ),
                'confidence': 0.85
            },
            
            # Rule for single replacement reactions
            {
                'name': 'single_replacement',
                'condition': lambda r: (
                    len(r.reactants) == 2 and len(r.products) == 2 and
                    self._is_single_replacement(r.reactants, r.products)
                ),
                'confidence': 0.8
            },
            
            # Rule for double replacement reactions
            {
                'name': 'double_replacement',
                'condition': lambda r: (
                    len(r.reactants) == 2 and len(r.products) == 2 and
                    self._is_double_replacement(r.reactants, r.products)
                ),
                'confidence': 0.8
            },
            
            # Rule for synthesis reactions
            {
                'name': 'synthesis',
                'condition': lambda r: (
                    len(r.reactants) > 1 and len(r.products) == 1
                ),
                'confidence': 0.9
            },
            
            # Rule for decomposition reactions
            {
                'name': 'decomposition',
                'condition': lambda r: (
                    len(r.reactants) == 1 and len(r.products) > 1
                ),
                'confidence': 0.9
            },
            
            # Rule for isomerization reactions
            {
                'name': 'isomerization',
                'condition': lambda r: (
                    len(r.reactants) == 1 and len(r.products) == 1 and
                    r.reactants[0].molecule.molecular_formula == r.products[0].molecule.molecular_formula
                ),
                'confidence': 0.95
            }
        ]
    
    def enhanced_analyze_reaction_type(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Comprehensive offline analysis of reaction type with confidence scores.
        
        This method analyzes a chemical reaction using multiple approaches:
        1. Oxidation state analysis
        2. Charge-based redox detection
        3. Functional group analysis
        4. Rule-based expert system
        5. Reaction fingerprinting
        
        The primary reaction type is determined based on the highest confidence score
        from all the analyses, which ensures that the most likely reaction type is
        reported even if it differs from the reaction's own type property.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary containing detailed reaction type analysis with the following keys:
            - primary_type: The reaction type with the highest confidence score
            - reaction_type_from_property: The reaction type from the reaction's own type property
            - confidence_scores: Dictionary mapping reaction types to confidence scores
            - electron_transfer: Analysis of electron transfer in the reaction
            - functional_groups: Analysis of functional groups and their transformations
            - rule_matches: Results from the rule-based expert system
            - fingerprint: A detailed fingerprint of the reaction
        """
        # Get basic analysis from existing method
        basic_analysis = self.analyze_reaction_type(reaction)
        
        # Get reaction type from the reaction's type property
        reaction_type = reaction.type
        
        # Perform oxidation state analysis
        electron_transfer = self._analyze_electron_transfer(reaction)
        
        # Also check for redox reactions based on ion charges
        charge_based_redox = self._detect_redox_from_charges(reaction)
        
        # If charge-based analysis detects a redox reaction, use that result
        if charge_based_redox["is_redox"]:
            electron_transfer = charge_based_redox
        
        # Perform functional group analysis
        functional_groups = self._analyze_functional_groups(reaction)
        
        # Apply rule-based expert system
        rule_matches = self._apply_expert_rules(reaction)
        
        # Generate reaction fingerprint
        fingerprint = self._generate_reaction_fingerprint(reaction)
        
        # Calculate confidence scores
        confidence_scores = self._calculate_type_confidence(reaction, 
                                                         electron_transfer,
                                                         rule_matches)
        
        # Determine the primary type based on the highest confidence score
        primary_type = max(confidence_scores.items(), key=lambda x: x[1])[0] if confidence_scores else reaction_type
        
        # Combine all analyses
        analysis = {
            **basic_analysis,
            'primary_type': primary_type,
            'reaction_type_from_property': reaction_type,  # Keep the original type for reference
            'electron_transfer': electron_transfer,
            'functional_groups': functional_groups,
            'rule_matches': rule_matches,
            'fingerprint': fingerprint,
            'confidence_scores': confidence_scores
        }
        
        return analysis
    
    def _analyze_electron_transfer(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Analyze electron transfer in the reaction by tracking oxidation states.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with electron transfer analysis
        """
        # Calculate oxidation states for each element in reactants and products
        reactant_states = self._calculate_oxidation_states(reaction.reactants)
        product_states = self._calculate_oxidation_states(reaction.products)
        
        # Track changes in oxidation states
        oxidation_changes = {}
        for element in set(reactant_states.keys()) | set(product_states.keys()):
            if element in reactant_states and element in product_states:
                change = product_states[element] - reactant_states[element]
                if abs(change) > 0.1:  # Use a small threshold to account for numerical errors
                    oxidation_changes[element] = change
        
        # Determine if this is a redox reaction
        is_redox = len(oxidation_changes) >= 2
        
        # Identify oxidizing and reducing agents
        oxidizing_agent = None
        reducing_agent = None
        
        if is_redox:
            # Find elements that are oxidized (lose electrons, increase in oxidation state)
            oxidized_elements = {elem for elem, change in oxidation_changes.items() if change > 0}
            
            # Find elements that are reduced (gain electrons, decrease in oxidation state)
            reduced_elements = {elem for elem, change in oxidation_changes.items() if change < 0}
            
            # Identify compounds containing these elements in the reactants
            for reactant in reaction.reactants:
                reactant_elements = set(reactant.molecule.elements.keys())
                
                if reactant_elements & oxidized_elements:
                    reducing_agent = reactant.molecule.molecular_formula
                
                if reactant_elements & reduced_elements:
                    oxidizing_agent = reactant.molecule.molecular_formula
        
        return {
            'oxidation_changes': oxidation_changes,
            'is_redox': is_redox,
            'oxidizing_agent': oxidizing_agent,
            'reducing_agent': reducing_agent
        }
    

    def _detect_redox_from_charges(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Detect redox reactions by analyzing changes in ion charges.
        
        This method specifically looks for changes in the charges of ions
        between reactants and products, which is a direct indicator of
        electron transfer in redox reactions.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with redox analysis based on charges
        """
        # Map elements to their charges in reactants and products
        reactant_charges = {}
        product_charges = {}
        
        # Process reactants
        for component in reaction.reactants:
            molecule = component.molecule
            if len(molecule.elements) == 1 and hasattr(molecule, "_charge") and molecule._charge != 0:
                element = list(molecule.elements.keys())[0].symbol
                reactant_charges[element] = molecule._charge
        
        # Process products
        for component in reaction.products:
            molecule = component.molecule
            if len(molecule.elements) == 1 and hasattr(molecule, "_charge") and molecule._charge != 0:
                element = list(molecule.elements.keys())[0].symbol
                product_charges[element] = molecule._charge
        
        # Detect charge changes
        charge_changes = {}
        for element in set(reactant_charges.keys()) | set(product_charges.keys()):
            if element in reactant_charges and element in product_charges:
                change = product_charges[element] - reactant_charges[element]
                if change != 0:
                    charge_changes[element] = change
        
        # Determine if this is a redox reaction
        is_redox = len(charge_changes) >= 2
        
        # Identify oxidizing and reducing agents
        oxidizing_agent = None
        reducing_agent = None
        
        if is_redox:
            # Find elements that are oxidized (lose electrons, increase in charge)
            oxidized_elements = {elem for elem, change in charge_changes.items() if change > 0}
            
            # Find elements that are reduced (gain electrons, decrease in charge)
            reduced_elements = {elem for elem, change in charge_changes.items() if change < 0}
            
            # Identify compounds containing these elements in the reactants
            for reactant in reaction.reactants:
                if len(reactant.molecule.elements) == 1:
                    element = list(reactant.molecule.elements.keys())[0].symbol
                    
                    if element in oxidized_elements:
                        reducing_agent = reactant.molecule.molecular_formula
                    
                    if element in reduced_elements:
                        oxidizing_agent = reactant.molecule.molecular_formula
        
        return {
            'charge_changes': charge_changes,
            'is_redox': is_redox,
            'oxidizing_agent': oxidizing_agent,
            'reducing_agent': reducing_agent
        }

    def _calculate_oxidation_states(self, components: List[ReactionComponent]) -> Dict[str, float]:
        """
        Calculate average oxidation states for elements in reaction components.
        
        Args:
            components: List of reaction components (reactants or products)
            
        Returns:
            Dictionary mapping elements to their average oxidation states
        """
        total_elements = defaultdict(float)
        total_oxidation = defaultdict(float)
        
        for component in components:
            molecule = component.molecule
            coefficient = component.coefficient
            
            # Get the molecular formula and parse it
            formula = molecule.molecular_formula
            
            # Calculate oxidation states for this molecule
            element_oxidation = self._assign_oxidation_states(molecule)
            
            # Add to totals, weighted by coefficient
            for element, count in molecule.elements.items():
                total_elements[element] += count * coefficient
                if element in element_oxidation:
                    total_oxidation[element] += element_oxidation[element] * count * coefficient
        
        # Calculate average oxidation state for each element
        average_oxidation = {}
        for element, total_count in total_elements.items():
            if total_count > 0:
                average_oxidation[element] = total_oxidation[element] / total_count
        
        return average_oxidation
    
    def _assign_oxidation_states(self, molecule: Molecule) -> Dict[str, float]:
        """
        Assign oxidation states to elements in a molecule.
        
        This uses a set of rules to estimate oxidation states:
        1. Fluorine is always -1
        2. Oxygen is usually -2 (except in peroxides)
        3. Hydrogen is usually +1 (except in metal hydrides)
        4. In binary compounds, the more electronegative element gets a negative oxidation state
        5. The sum of oxidation states equals the total charge of the molecule
        
        Args:
            molecule: Molecule to analyze
            
        Returns:
            Dictionary mapping elements to their oxidation states
        """
        elements = molecule.elements
        oxidation_states = {}
        
        # Rule 1: Fluorine is always -1
        if 'F' in elements:
            oxidation_states['F'] = -1
        
        # Rule 2: Oxygen is usually -2 (except in peroxides)
        if 'O' in elements:
            # Check for peroxides (O-O bonds)
            if 'O2' in molecule.molecular_formula:
                oxidation_states['O'] = -1
            else:
                oxidation_states['O'] = -2
        
        # Rule 3: Hydrogen is usually +1 (except in metal hydrides)
        if 'H' in elements:
            # Check if this is a metal hydride
            metals = ['Li', 'Na', 'K', 'Rb', 'Cs', 'Be', 'Mg', 'Ca', 'Sr', 'Ba', 
                     'Al', 'Ga', 'In', 'Sn', 'Pb', 'Fe', 'Co', 'Ni', 'Cu', 'Ag', 
                     'Au', 'Zn', 'Cd', 'Hg', 'Pt', 'Mn', 'Cr', 'Mo', 'W', 'V', 'Ti']
            
            if any(metal in elements for metal in metals):
                oxidation_states['H'] = -1
            else:
                oxidation_states['H'] = 1
        
        # Rule 4: In binary compounds, the more electronegative element gets a negative oxidation state
        if len(elements) == 2:
            element_list = list(elements.keys())
            if element_list[0] in self.electronegativity and element_list[1] in self.electronegativity:
                if self.electronegativity[element_list[0]] > self.electronegativity[element_list[1]]:
                    more_electronegative = element_list[0]
                    less_electronegative = element_list[1]
                else:
                    more_electronegative = element_list[1]
                    less_electronegative = element_list[0]
                
                # If not already assigned
                if more_electronegative not in oxidation_states:
                    # Determine the oxidation state based on common values
                    if more_electronegative in self.common_oxidation_states:
                        # Use the most negative common oxidation state
                        oxidation_states[more_electronegative] = min(self.common_oxidation_states[more_electronegative])
        
        # Rule 5: The sum of oxidation states equals the total charge of the molecule
        # Calculate the remaining oxidation states
        total_charge = getattr(molecule, "_charge", 0)  # Use molecule charge if available
        assigned_charge = sum(oxidation_states.get(element, 0) * count 
                             for element, count in elements.items())
        
        remaining_elements = [elem for elem in elements if elem not in oxidation_states]
        
        # Special case for single-element ions (like Fe²⁺, Ce⁴⁺)
        if len(elements) == 1 and hasattr(molecule, "_charge") and molecule._charge != 0:
            element = list(elements.keys())[0]
            oxidation_states[element] = molecule._charge / elements[element]
        elif len(remaining_elements) == 1:
            # If only one element remains, its oxidation state can be calculated
            element = remaining_elements[0]
            oxidation_states[element] = (total_charge - assigned_charge) / elements[element]
        
        return oxidation_states
    
    def _analyze_functional_groups(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Analyze changes in functional groups to identify reaction mechanisms.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with functional group analysis
        """
        # Identify functional groups in reactants and products
        reactant_groups = self._identify_functional_groups(reaction.reactants)
        product_groups = self._identify_functional_groups(reaction.products)
        
        # Identify functional group transformations
        transformations = []
        for group in reactant_groups:
            if group not in product_groups or reactant_groups[group] > product_groups.get(group, 0):
                for new_group in product_groups:
                    if new_group not in reactant_groups or product_groups[new_group] > reactant_groups.get(new_group, 0):
                        transformations.append((group, new_group))
        
        # Classify based on functional group changes
        reaction_mechanism = "unknown"
        
        # Some common organic reaction mechanisms
        if ('alcohol', 'ketone') in transformations or ('alcohol', 'aldehyde') in transformations:
            reaction_mechanism = "oxidation"
        elif ('ketone', 'alcohol') in transformations or ('aldehyde', 'alcohol') in transformations:
            reaction_mechanism = "reduction"
        elif ('halide', 'alcohol') in transformations:
            reaction_mechanism = "nucleophilic_substitution"
        elif ('alcohol', 'ester') in transformations and ('carboxylic_acid', 'ester') in transformations:
            reaction_mechanism = "esterification"
        elif ('ester', 'alcohol') in transformations and ('ester', 'carboxylic_acid') in transformations:
            reaction_mechanism = "hydrolysis"
        
        return {
            'reactant_groups': reactant_groups,
            'product_groups': product_groups,
            'transformations': transformations,
            'reaction_mechanism': reaction_mechanism
        }
    
    def _identify_functional_groups(self, components: List[ReactionComponent]) -> Dict[str, int]:
        """
        Identify functional groups in reaction components.
        
        Args:
            components: List of reaction components
            
        Returns:
            Dictionary mapping functional group names to their counts
        """
        group_counts = defaultdict(int)
        
        for component in components:
            molecule = component.molecule
            formula = molecule.molecular_formula
            coefficient = component.coefficient
            
            # Simple pattern matching for functional groups
            # This is a simplified approach - a more comprehensive implementation
            # would use structural information from the molecule
            
            if 'OH' in formula and not formula.startswith('HO'):
                group_counts['alcohol'] += coefficient
            
            if 'CHO' in formula or (formula.endswith('O') and 'C' in formula):
                group_counts['aldehyde'] += coefficient
            
            if 'CO' in formula and not 'CHO' in formula and not 'COOH' in formula:
                group_counts['ketone'] += coefficient
            
            if 'COOH' in formula:
                group_counts['carboxylic_acid'] += coefficient
            
            if 'COO' in formula and not 'COOH' in formula:
                group_counts['ester'] += coefficient
            
            if 'NH2' in formula:
                group_counts['amine'] += coefficient
            
            if 'CN' in formula:
                group_counts['nitrile'] += coefficient
            
            if 'NO2' in formula:
                group_counts['nitro'] += coefficient
            
            # Check for halides
            for halogen in ['F', 'Cl', 'Br', 'I']:
                if halogen in formula:
                    group_counts['halide'] += coefficient
                    break
        
        return dict(group_counts)
    
    def _apply_expert_rules(self, reaction: Reaction) -> List[Dict[str, Any]]:
        """
        Apply a comprehensive set of expert rules to classify the reaction.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            List of matching rules with confidence scores
        """
        matches = []
        
        for rule in self.reaction_rules:
            try:
                if rule['condition'](reaction):
                    matches.append({
                        'type': rule['name'],
                        'confidence': rule['confidence']
                    })
            except Exception as e:
                # If a rule fails to evaluate, skip it
                continue
        
        return matches
    
    def _generate_reaction_fingerprint(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Generate a comprehensive fingerprint of the reaction for classification.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with reaction fingerprint
        """
        # Count elements in reactants and products
        reactant_elements = self._count_elements(reaction.reactants)
        product_elements = self._count_elements(reaction.products)
        
        # Calculate element balance
        element_balance = {}
        for element in set(reactant_elements.keys()) | set(product_elements.keys()):
            reactant_count = reactant_elements.get(element, 0)
            product_count = product_elements.get(element, 0)
            element_balance[element] = product_count - reactant_count
        
        # Analyze phase changes
        phase_changes = self._analyze_phase_changes(reaction)
        
        # Analyze charge changes
        charge_changes = self._analyze_charge_changes(reaction)
        
        return {
            'reactant_elements': reactant_elements,
            'product_elements': product_elements,
            'element_balance': element_balance,
            'phase_changes': phase_changes,
            'charge_changes': charge_changes,
            'num_reactants': len(reaction.reactants),
            'num_products': len(reaction.products)
        }
    
    def _count_elements(self, components: List[ReactionComponent]) -> Dict[str, float]:
        """
        Count elements in reaction components.
        
        Args:
            components: List of reaction components
            
        Returns:
            Dictionary mapping elements to their total counts
        """
        element_counts = defaultdict(float)
        
        for component in components:
            molecule = component.molecule
            coefficient = component.coefficient
            
            for element, count in molecule.elements.items():
                element_counts[element] += count * coefficient
        
        return dict(element_counts)
    
    def _analyze_phase_changes(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Analyze phase changes in the reaction.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with phase change analysis
        """
        reactant_phases = {}
        product_phases = {}
        
        for component in reaction.reactants:
            if component.phase:
                reactant_phases[component.molecule.molecular_formula] = component.phase
        
        for component in reaction.products:
            if component.phase:
                product_phases[component.molecule.molecular_formula] = component.phase
        
        phase_changes = {}
        for formula in set(reactant_phases.keys()) & set(product_phases.keys()):
            if reactant_phases[formula] != product_phases[formula]:
                phase_changes[formula] = (reactant_phases[formula], product_phases[formula])
        
        return {
            'reactant_phases': reactant_phases,
            'product_phases': product_phases,
            'changes': phase_changes,
            'has_phase_changes': len(phase_changes) > 0
        }
    
    def _analyze_charge_changes(self, reaction: Reaction) -> Dict[str, Any]:
        """
        Analyze charge changes in the reaction.
        
        Args:
            reaction: Reaction to analyze
            
        Returns:
            Dictionary with charge change analysis
        """
        # This is a simplified implementation
        # A more comprehensive implementation would calculate actual charges
        # based on molecular structure
        
        return {
            'has_charge_transfer': self._analyze_electron_transfer(reaction)['is_redox']
        }
    
    def _calculate_type_confidence(self, reaction: Reaction, 
                                 electron_transfer: Dict[str, Any],
                                 rule_matches: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate confidence scores for different reaction types.
        
        Args:
            reaction: Reaction to analyze
            electron_transfer: Electron transfer analysis
            rule_matches: Rule-based analysis results
            
        Returns:
            Dictionary mapping reaction types to confidence scores
        """
        confidence_scores = defaultdict(float)
        
        # Start with rule-based confidence scores
        for match in rule_matches:
            confidence_scores[match['type']] = max(confidence_scores[match['type']], match['confidence'])
        
        # Adjust based on electron transfer analysis
        if electron_transfer['is_redox']:
            confidence_scores['redox'] = max(confidence_scores['redox'], 0.95)  # Increased confidence
            # If we detected a redox reaction, reduce confidence in synthesis/decomposition
            if 'synthesis' in confidence_scores:
                confidence_scores['synthesis'] *= 0.5
            if 'decomposition' in confidence_scores:
                confidence_scores['decomposition'] *= 0.5
        
        # Adjust based on reaction's own type property
        reaction_type = reaction.type
        if reaction_type != "unknown":
            confidence_scores[reaction_type] = max(confidence_scores[reaction_type], 0.8)
        
        # Normalize confidence scores
        return dict(confidence_scores)
    
    def _contains_acid(self, components: List[ReactionComponent]) -> bool:
        """
        Check if reaction components contain an acid.
        
        Args:
            components: List of reaction components
            
        Returns:
            True if components contain an acid
        """
        for component in components:
            formula = component.molecule.molecular_formula
            if formula in self.acids:
                return True
            
            # Check for H+ ions
            if formula == 'H' and component.charge == 1:
                return True
        
        return False
    
    def _contains_base(self, components: List[ReactionComponent]) -> bool:
        """
        Check if reaction components contain a base.
        
        Args:
            components: List of reaction components
            
        Returns:
            True if components contain a base
        """
        for component in components:
            formula = component.molecule.molecular_formula
            if formula in self.bases:
                return True
            
            # Check for OH- ions
            if formula == 'OH' and component.charge == -1:
                return True
        
        return False
    
    def _is_single_replacement(self, reactants: List[ReactionComponent], 
                             products: List[ReactionComponent]) -> bool:
        """
        Check if reaction is a single replacement reaction.
        
        Args:
            reactants: List of reactant components
            products: List of product components
            
        Returns:
            True if reaction is a single replacement
        """
        # Simple heuristic: A + BC → AC + B
        if len(reactants) != 2 or len(products) != 2:
            return False
        
        # Get elements in each component
        reactant_elements = [set(r.molecule.elements.keys()) for r in reactants]
        product_elements = [set(p.molecule.elements.keys()) for p in products]
        
        # Check if one reactant is a single element
        if len(reactant_elements[0]) == 1 or len(reactant_elements[1]) == 1:
            # Identify the single element and the compound
            if len(reactant_elements[0]) == 1:
                single_element = list(reactant_elements[0])[0]
                compound_elements = reactant_elements[1]
            else:
                single_element = list(reactant_elements[1])[0]
                compound_elements = reactant_elements[0]
            
            # Check if the single element appears in one of the products
            # and if the other product contains elements from the compound
            for i, prod_elements in enumerate(product_elements):
                if single_element in prod_elements:
                    other_product = product_elements[1 - i]
                    # Check if other product contains elements from the compound
                    if len(other_product & compound_elements) > 0:
                        return True
        
        return False
    
    def _is_double_replacement(self, reactants: List[ReactionComponent], 
                             products: List[ReactionComponent]) -> bool:
        """
        Check if reaction is a double replacement reaction.
        
        Args:
            reactants: List of reactant components
            products: List of product components
            
        Returns:
            True if reaction is a double replacement
        """
        # Simple heuristic: AB + CD → AD + CB
        if len(reactants) != 2 or len(products) != 2:
            return False
        
        # Get elements in each component
        reactant_elements = [set(r.molecule.elements.keys()) for r in reactants]
        product_elements = [set(p.molecule.elements.keys()) for p in products]
        
        # Check if elements have been exchanged between compounds
        if (len(reactant_elements[0].intersection(product_elements[0])) > 0 and
            len(reactant_elements[0].intersection(product_elements[1])) > 0 and
            len(reactant_elements[1].intersection(product_elements[0])) > 0 and
            len(reactant_elements[1].intersection(product_elements[1])) > 0):
            return True
        
        return False