"""
Thermodynamic calculations for chemical reactions.

This module provides tools for calculating thermodynamic properties
of chemical reactions including enthalpy, entropy, and Gibbs free energy.
"""

from typing import Dict, List, Optional, Tuple, Union, Any
import math
from chemesty.reactions.reaction import Reaction, ReactionComponent
from chemesty.molecules.molecule import Molecule


class ReactionThermodynamics:
    """
    Calculator for thermodynamic properties of chemical reactions.
    
    This class provides methods for calculating reaction enthalpies,
    entropies, Gibbs free energies, and equilibrium constants.
    """
    
    def __init__(self):
        """Initialize the thermodynamics calculator."""
        self.gas_constant = 8.314  # J/(mol·K)
        self.standard_temperature = 298.15  # K (25°C)
        self.standard_pressure = 101325  # Pa (1 atm)
        
        # Standard thermodynamic data (simplified database)
        # In a real implementation, this would come from a comprehensive database
        self.standard_data = {
            'H2O': {
                'delta_h_formation': -285.8,  # kJ/mol
                'delta_g_formation': -237.1,  # kJ/mol
                'entropy': 69.9,  # J/(mol·K)
                'heat_capacity': 75.3  # J/(mol·K)
            },
            'CO2': {
                'delta_h_formation': -393.5,
                'delta_g_formation': -394.4,
                'entropy': 213.8,
                'heat_capacity': 37.1
            },
            'H2': {
                'delta_h_formation': 0.0,
                'delta_g_formation': 0.0,
                'entropy': 130.7,
                'heat_capacity': 28.8
            },
            'O2': {
                'delta_h_formation': 0.0,
                'delta_g_formation': 0.0,
                'entropy': 205.2,
                'heat_capacity': 29.4
            },
            'CH4': {
                'delta_h_formation': -74.6,
                'delta_g_formation': -50.5,
                'entropy': 186.3,
                'heat_capacity': 35.3
            },
            'NH3': {
                'delta_h_formation': -45.9,
                'delta_g_formation': -16.4,
                'entropy': 192.8,
                'heat_capacity': 35.1
            },
            'N2': {
                'delta_h_formation': 0.0,
                'delta_g_formation': 0.0,
                'entropy': 191.6,
                'heat_capacity': 29.1
            },
            'HCl': {
                'delta_h_formation': -92.3,
                'delta_g_formation': -95.3,
                'entropy': 186.9,
                'heat_capacity': 29.1
            },
            'NaCl': {
                'delta_h_formation': -411.2,
                'delta_g_formation': -384.1,
                'entropy': 72.1,
                'heat_capacity': 50.5
            }
        }
    
    def calculate_reaction_enthalpy(self, reaction: Reaction, 
                                  temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate the enthalpy change of a reaction.
        
        Args:
            reaction: Balanced chemical reaction
            temperature: Temperature in Kelvin (default: 298.15 K)
            
        Returns:
            Dictionary containing enthalpy calculations
        """
        if not reaction.is_balanced():
            raise ValueError("Reaction must be balanced for thermodynamic calculations")
        
        temp = temperature or self.standard_temperature
        
        # Calculate standard enthalpy of reaction
        delta_h_products = 0.0
        delta_h_reactants = 0.0
        
        missing_data = []
        
        # Sum enthalpies of formation for products
        for product in reaction.products:
            formula = product.molecule.molecular_formula
            if formula in self.standard_data:
                delta_h_products += (product.coefficient * 
                                   self.standard_data[formula]['delta_h_formation'])
            else:
                missing_data.append(formula)
        
        # Sum enthalpies of formation for reactants (excluding catalysts)
        for reactant in reaction.reactants:
            if not reactant.is_catalyst:
                formula = reactant.molecule.molecular_formula
                if formula in self.standard_data:
                    delta_h_reactants += (reactant.coefficient * 
                                        self.standard_data[formula]['delta_h_formation'])
                else:
                    missing_data.append(formula)
        
        delta_h_reaction = delta_h_products - delta_h_reactants
        
        # Temperature correction (simplified)
        if temp != self.standard_temperature:
            delta_cp = self._calculate_heat_capacity_change(reaction)
            if delta_cp is not None:
                temp_correction = delta_cp * (temp - self.standard_temperature) / 1000.0
                delta_h_reaction += temp_correction
        
        return {
            'delta_h_reaction': delta_h_reaction,  # kJ/mol
            'temperature': temp,
            'exothermic': delta_h_reaction < 0,
            'endothermic': delta_h_reaction > 0,
            'missing_data': missing_data,
            'confidence': 'high' if not missing_data else 'low'
        }
    
    def calculate_reaction_entropy(self, reaction: Reaction, 
                                 temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate the entropy change of a reaction.
        
        Args:
            reaction: Balanced chemical reaction
            temperature: Temperature in Kelvin (default: 298.15 K)
            
        Returns:
            Dictionary containing entropy calculations
        """
        if not reaction.is_balanced():
            raise ValueError("Reaction must be balanced for thermodynamic calculations")
        
        temp = temperature or self.standard_temperature
        
        # Calculate standard entropy of reaction
        entropy_products = 0.0
        entropy_reactants = 0.0
        
        missing_data = []
        
        # Sum entropies for products
        for product in reaction.products:
            formula = product.molecule.molecular_formula
            if formula in self.standard_data:
                entropy_products += (product.coefficient * 
                                   self.standard_data[formula]['entropy'])
            else:
                missing_data.append(formula)
        
        # Sum entropies for reactants (excluding catalysts)
        for reactant in reaction.reactants:
            if not reactant.is_catalyst:
                formula = reactant.molecule.molecular_formula
                if formula in self.standard_data:
                    entropy_reactants += (reactant.coefficient * 
                                        self.standard_data[formula]['entropy'])
                else:
                    missing_data.append(formula)
        
        delta_s_reaction = entropy_products - entropy_reactants
        
        return {
            'delta_s_reaction': delta_s_reaction,  # J/(mol·K)
            'temperature': temp,
            'entropy_increase': delta_s_reaction > 0,
            'entropy_decrease': delta_s_reaction < 0,
            'missing_data': missing_data,
            'confidence': 'high' if not missing_data else 'low'
        }
    
    def calculate_gibbs_free_energy(self, reaction: Reaction, 
                                  temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate the Gibbs free energy change of a reaction.
        
        Args:
            reaction: Balanced chemical reaction
            temperature: Temperature in Kelvin (default: 298.15 K)
            
        Returns:
            Dictionary containing Gibbs free energy calculations
        """
        if not reaction.is_balanced():
            raise ValueError("Reaction must be balanced for thermodynamic calculations")
        
        temp = temperature or self.standard_temperature
        
        # Method 1: Direct calculation from standard Gibbs energies of formation
        delta_g_products = 0.0
        delta_g_reactants = 0.0
        
        missing_data = []
        
        # Sum Gibbs energies of formation for products
        for product in reaction.products:
            formula = product.molecule.molecular_formula
            if formula in self.standard_data:
                delta_g_products += (product.coefficient * 
                                   self.standard_data[formula]['delta_g_formation'])
            else:
                missing_data.append(formula)
        
        # Sum Gibbs energies of formation for reactants (excluding catalysts)
        for reactant in reaction.reactants:
            if not reactant.is_catalyst:
                formula = reactant.molecule.molecular_formula
                if formula in self.standard_data:
                    delta_g_reactants += (reactant.coefficient * 
                                        self.standard_data[formula]['delta_g_formation'])
                else:
                    missing_data.append(formula)
        
        delta_g_reaction = delta_g_products - delta_g_reactants
        
        # Method 2: Calculate from enthalpy and entropy if direct data unavailable
        if missing_data:
            try:
                enthalpy_result = self.calculate_reaction_enthalpy(reaction, temp)
                entropy_result = self.calculate_reaction_entropy(reaction, temp)
                
                if (enthalpy_result['confidence'] == 'high' and 
                    entropy_result['confidence'] == 'high'):
                    # ΔG = ΔH - TΔS
                    delta_g_reaction = (enthalpy_result['delta_h_reaction'] - 
                                      temp * entropy_result['delta_s_reaction'] / 1000.0)
                    missing_data = []  # We can calculate it indirectly
            except:
                pass  # Keep original missing_data
        
        # Calculate equilibrium constant
        equilibrium_constant = None
        if not missing_data:
            # K = exp(-ΔG/RT)
            try:
                equilibrium_constant = math.exp(-delta_g_reaction * 1000.0 / (self.gas_constant * temp))
            except (OverflowError, ValueError):
                equilibrium_constant = float('inf') if delta_g_reaction < 0 else 0.0
        
        return {
            'delta_g_reaction': delta_g_reaction,  # kJ/mol
            'temperature': temp,
            'spontaneous': delta_g_reaction < 0,
            'non_spontaneous': delta_g_reaction > 0,
            'equilibrium_constant': equilibrium_constant,
            'missing_data': missing_data,
            'confidence': 'high' if not missing_data else 'low'
        }
    
    def calculate_equilibrium_constant(self, reaction: Reaction, 
                                     temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate the equilibrium constant for a reaction.
        
        Args:
            reaction: Balanced chemical reaction
            temperature: Temperature in Kelvin (default: 298.15 K)
            
        Returns:
            Dictionary containing equilibrium constant calculations
        """
        gibbs_result = self.calculate_gibbs_free_energy(reaction, temperature)
        
        result = {
            'temperature': gibbs_result['temperature'],
            'equilibrium_constant': gibbs_result['equilibrium_constant'],
            'delta_g_reaction': gibbs_result['delta_g_reaction'],
            'confidence': gibbs_result['confidence']
        }
        
        if result['equilibrium_constant'] is not None:
            K = result['equilibrium_constant']
            if K > 1000:
                result['interpretation'] = 'reaction strongly favors products'
            elif K > 1:
                result['interpretation'] = 'reaction favors products'
            elif K == 1:
                result['interpretation'] = 'reaction is at equilibrium'
            elif K > 0.001:
                result['interpretation'] = 'reaction favors reactants'
            else:
                result['interpretation'] = 'reaction strongly favors reactants'
        else:
            result['interpretation'] = 'cannot determine without complete thermodynamic data'
        
        return result
    
    def _calculate_heat_capacity_change(self, reaction: Reaction) -> Optional[float]:
        """
        Calculate the heat capacity change for a reaction.
        
        Args:
            reaction: Chemical reaction
            
        Returns:
            Heat capacity change in J/(mol·K) or None if data unavailable
        """
        delta_cp = 0.0
        missing_data = False
        
        # Sum heat capacities for products
        for product in reaction.products:
            formula = product.molecule.molecular_formula
            if formula in self.standard_data:
                delta_cp += (product.coefficient * 
                           self.standard_data[formula]['heat_capacity'])
            else:
                missing_data = True
        
        # Subtract heat capacities for reactants (excluding catalysts)
        for reactant in reaction.reactants:
            if not reactant.is_catalyst:
                formula = reactant.molecule.molecular_formula
                if formula in self.standard_data:
                    delta_cp -= (reactant.coefficient * 
                               self.standard_data[formula]['heat_capacity'])
                else:
                    missing_data = True
        
        return None if missing_data else delta_cp
    
    def predict_temperature_dependence(self, reaction: Reaction, 
                                     temperature_range: Tuple[float, float],
                                     num_points: int = 10) -> Dict[str, Any]:
        """
        Predict how thermodynamic properties vary with temperature.
        
        Args:
            reaction: Balanced chemical reaction
            temperature_range: (min_temp, max_temp) in Kelvin
            num_points: Number of temperature points to calculate
            
        Returns:
            Dictionary with temperature-dependent properties
        """
        min_temp, max_temp = temperature_range
        temperatures = [min_temp + i * (max_temp - min_temp) / (num_points - 1) 
                       for i in range(num_points)]
        
        results = {
            'temperatures': temperatures,
            'delta_h_values': [],
            'delta_g_values': [],
            'equilibrium_constants': [],
            'spontaneous_temperatures': []
        }
        
        for temp in temperatures:
            try:
                gibbs_result = self.calculate_gibbs_free_energy(reaction, temp)
                enthalpy_result = self.calculate_reaction_enthalpy(reaction, temp)
                
                results['delta_h_values'].append(enthalpy_result['delta_h_reaction'])
                results['delta_g_values'].append(gibbs_result['delta_g_reaction'])
                results['equilibrium_constants'].append(gibbs_result['equilibrium_constant'])
                
                if gibbs_result['spontaneous']:
                    results['spontaneous_temperatures'].append(temp)
                    
            except Exception:
                results['delta_h_values'].append(None)
                results['delta_g_values'].append(None)
                results['equilibrium_constants'].append(None)
        
        return results
    
    def analyze_reaction_feasibility(self, reaction: Reaction, 
                                   temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Comprehensive thermodynamic feasibility analysis.
        
        Args:
            reaction: Balanced chemical reaction
            temperature: Temperature in Kelvin (default: 298.15 K)
            
        Returns:
            Dictionary with feasibility analysis
        """
        temp = temperature or self.standard_temperature
        
        try:
            enthalpy_result = self.calculate_reaction_enthalpy(reaction, temp)
            entropy_result = self.calculate_reaction_entropy(reaction, temp)
            gibbs_result = self.calculate_gibbs_free_energy(reaction, temp)
            
            analysis = {
                'temperature': temp,
                'thermodynamically_feasible': gibbs_result['spontaneous'],
                'enthalpy_change': enthalpy_result['delta_h_reaction'],
                'entropy_change': entropy_result['delta_s_reaction'],
                'gibbs_change': gibbs_result['delta_g_reaction'],
                'equilibrium_constant': gibbs_result['equilibrium_constant'],
                'reaction_type': '',
                'recommendations': []
            }
            
            # Classify reaction type thermodynamically
            delta_h = enthalpy_result['delta_h_reaction']
            delta_s = entropy_result['delta_s_reaction']
            
            if delta_h < 0 and delta_s > 0:
                analysis['reaction_type'] = 'spontaneous at all temperatures'
                analysis['recommendations'].append('Reaction is thermodynamically favorable')
            elif delta_h > 0 and delta_s < 0:
                analysis['reaction_type'] = 'non-spontaneous at all temperatures'
                analysis['recommendations'].append('Reaction requires external energy input')
            elif delta_h < 0 and delta_s < 0:
                analysis['reaction_type'] = 'spontaneous at low temperatures'
                analysis['recommendations'].append('Lower temperature favors this reaction')
            elif delta_h > 0 and delta_s > 0:
                analysis['reaction_type'] = 'spontaneous at high temperatures'
                analysis['recommendations'].append('Higher temperature favors this reaction')
            
            # Add specific recommendations
            if not analysis['thermodynamically_feasible']:
                analysis['recommendations'].extend([
                    'Consider changing reaction conditions',
                    'Look for alternative reaction pathways',
                    'Consider using a catalyst to lower activation energy'
                ])
            else:
                analysis['recommendations'].extend([
                    'Reaction is thermodynamically favorable',
                    'Focus on optimizing kinetics and reaction conditions'
                ])
            
            return analysis
            
        except Exception as e:
            return {
                'temperature': temp,
                'error': str(e),
                'thermodynamically_feasible': 'unknown',
                'recommendations': ['Insufficient thermodynamic data for analysis']
            }
    
    def estimate_activation_energy(self, reaction: Reaction, 
                                 rate_constants: Dict[float, float]) -> Dict[str, Any]:
        """
        Estimate activation energy from temperature-dependent rate constants.
        
        Args:
            reaction: Chemical reaction
            rate_constants: Dictionary mapping temperature (K) to rate constant
            
        Returns:
            Dictionary with activation energy estimation
        """
        if len(rate_constants) < 2:
            raise ValueError("Need at least 2 temperature-rate constant pairs")
        
        # Use Arrhenius equation: ln(k) = ln(A) - Ea/(RT)
        # Plot ln(k) vs 1/T to get slope = -Ea/R
        
        temperatures = list(rate_constants.keys())
        rate_values = list(rate_constants.values())
        
        # Calculate 1/T and ln(k)
        inv_temps = [1.0 / T for T in temperatures]
        ln_rates = [math.log(k) if k > 0 else None for k in rate_values]
        
        # Remove invalid points
        valid_points = [(inv_t, ln_k) for inv_t, ln_k in zip(inv_temps, ln_rates) 
                       if ln_k is not None]
        
        if len(valid_points) < 2:
            raise ValueError("Need at least 2 valid rate constant values")
        
        # Simple linear regression
        n = len(valid_points)
        sum_x = sum(point[0] for point in valid_points)
        sum_y = sum(point[1] for point in valid_points)
        sum_xy = sum(point[0] * point[1] for point in valid_points)
        sum_x2 = sum(point[0] ** 2 for point in valid_points)
        
        # Calculate slope and intercept
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Activation energy = -slope * R
        activation_energy = -slope * self.gas_constant / 1000.0  # kJ/mol
        pre_exponential_factor = math.exp(intercept)
        
        # Calculate R-squared
        y_mean = sum_y / n
        ss_tot = sum((point[1] - y_mean) ** 2 for point in valid_points)
        ss_res = sum((point[1] - (slope * point[0] + intercept)) ** 2 
                    for point in valid_points)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return {
            'activation_energy': activation_energy,  # kJ/mol
            'pre_exponential_factor': pre_exponential_factor,
            'r_squared': r_squared,
            'temperature_range': (min(temperatures), max(temperatures)),
            'data_points': len(valid_points),
            'confidence': 'high' if r_squared > 0.95 else 'moderate' if r_squared > 0.8 else 'low'
        }