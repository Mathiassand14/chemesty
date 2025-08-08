"""
Utility module for common physical states/phases in chemical reactions.

This module provides constants for common physical states (solid, liquid, gas, aqueous)
and functions to apply these states to molecules.

Examples:
    >>> from chemesty.elements import H, O, Na, Cl
    >>> from chemesty.states import SOLID, LIQUID, GAS, AQUEOUS
    >>> 
    >>> # Create water in liquid state
    >>> water = H*2 + O
    >>> water.phase = LIQUID
    >>> print(water)
    H2O(l)
    >>> 
    >>> # Create sodium chloride in aqueous solution
    >>> nacl = Na + Cl
    >>> nacl.phase = AQUEOUS
    >>> print(nacl)
    NaCl(aq)
    >>> 
    >>> # Use in reactions
    >>> from chemesty.reactions.reaction import Reaction
    >>> reaction = Reaction()
    >>> reaction.add_reactant(Na, phase=SOLID)
    >>> reaction.add_reactant(H*2 + O, phase=LIQUID)
    >>> reaction.add_product(Na + O + H, phase=AQUEOUS)
    >>> reaction.add_product(H, phase=GAS)
    >>> print(reaction)
    Na(s) + H2O(l) -> NaOH(aq) + H(g)
"""

# Constants for common physical states
SOLID = s = 's'
LIQUID = l = 'l'
GAS = g = 'g'
AQUEOUS = aq = 'aq'



def apply_state(molecule, state):
    """
    Apply a physical state to a molecule.
    
    Args:
        molecule: The molecule to apply the state to
        state: The state to apply ('s', 'l', 'g', 'aq')
        
    Returns:
        The molecule with the state applied
        
    Examples:
        >>> from chemesty.elements import H, O
        >>> from chemesty.states import apply_state, LIQUID
        >>> 
        >>> # Create water molecule
        >>> water = H*2 + O
        >>> 
        >>> # Apply liquid state
        >>> water = apply_state(water, LIQUID)
        >>> print(water)
        H2O(l)
    """
    molecule.phase = state
    return molecule

# Convenience functions for each state
def as_solid(molecule):
    """Apply solid state to a molecule."""
    return apply_state(molecule, SOLID)

def as_liquid(molecule):
    """Apply liquid state to a molecule."""
    return apply_state(molecule, LIQUID)

def as_gas(molecule):
    """Apply gas state to a molecule."""
    return apply_state(molecule, GAS)

def as_aqueous(molecule):
    """Apply aqueous state to a molecule."""
    return apply_state(molecule, AQUEOUS)