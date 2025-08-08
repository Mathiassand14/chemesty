"""
Utility module for working with element charges in a more intuitive way.

This module provides functions to enable and disable charge chaining,
allowing for syntax like ++Fe to create Fe²⁺.
"""

from typing import Callable, Dict, Any
import types
import inspect
import sys
from chemesty.elements.atomic_element import AtomicElement

# Store the original __pos__ methods for each element class
_original_pos_methods = {}

def _chaining_pos(self):
    """
    Enhanced __pos__ method that supports chaining.
    
    This method checks if the element already has a charge and
    increments it accordingly, allowing for syntax like ++Fe to create Fe²⁺.
    
    Returns:
        A copy of this element with charge increased by 1
    """
    import copy
    result = copy.deepcopy(self)
    result.charge += 1
    
    # Store the original class's __pos__ method on this instance
    # This allows us to chain the + operator
    result.__pos__ = types.MethodType(_chaining_pos, result)
    
    return result

def enable_charge_chaining():
    """
    Enable charge chaining for all element classes.
    
    This allows for syntax like ++Fe to create Fe²⁺, +++Fe to create Fe³⁺, etc.
    
    Returns:
        A dictionary of the original __pos__ methods, to be used with disable_charge_chaining
        
    Examples:
        >>> from chemesty.elements import Fe, Ce
        >>> from chemesty.elements.charge import enable_charge_chaining, disable_charge_chaining
        >>> 
        >>> # Save the original methods
        >>> original_methods = enable_charge_chaining()
        >>> 
        >>> # Now you can use operator chaining
        >>> fe_plus2 = ++Fe
        >>> print(fe_plus2.charge)  # Outputs: 2
        >>> 
        >>> ce_plus3 = +++Ce
        >>> print(ce_plus3.charge)  # Outputs: 3
        >>> 
        >>> # Restore the original methods when done
        >>> disable_charge_chaining(original_methods)
    """
    # Get all element classes from the elements module
    import chemesty.elements
    element_classes = []
    
    # Find all AtomicElement subclasses
    for name, obj in inspect.getmembers(sys.modules['chemesty.elements']):
        if inspect.isclass(obj) and issubclass(obj, AtomicElement) and obj != AtomicElement:
            element_classes.append(obj)
    
    # Store the original __pos__ methods and replace them
    for cls in element_classes:
        _original_pos_methods[cls] = cls.__pos__
        cls.__pos__ = _chaining_pos
    
    return _original_pos_methods

def disable_charge_chaining(original_methods=None):
    """
    Disable charge chaining and restore the original __pos__ methods.
    
    Args:
        original_methods: Dictionary of original __pos__ methods, as returned by enable_charge_chaining
        
    Examples:
        >>> from chemesty.elements import Fe, Ce
        >>> from chemesty.elements.charge import enable_charge_chaining, disable_charge_chaining
        >>> 
        >>> # Save the original methods
        >>> original_methods = enable_charge_chaining()
        >>> 
        >>> # Use operator chaining
        >>> fe_plus2 = ++Fe
        >>> 
        >>> # Restore the original methods when done
        >>> disable_charge_chaining(original_methods)
    """
    if original_methods is None:
        original_methods = _original_pos_methods
    
    # Restore the original __pos__ methods
    for cls, method in original_methods.items():
        cls.__pos__ = method

def with_charge(element_or_molecule, charge):
    """
    Create a copy of an element or molecule with a specific charge.
    
    This is an alternative to using operator chaining when you need
    to set a specific charge value directly.
    
    Args:
        element_or_molecule: The element or molecule to copy
        charge: The charge to apply
        
    Returns:
        If element_or_molecule is an element: A molecule containing the element with the specified charge
        If element_or_molecule is a molecule: A copy of the molecule with the specified charge
        
    Examples:
        >>> from chemesty.elements import Fe, Ce, H, O
        >>> from chemesty.elements.charge import with_charge
        >>> from chemesty.molecules.molecule import Molecule
        >>> 
        >>> # With elements
        >>> fe_plus2 = with_charge(Fe, 2)
        >>> print(fe_plus2.charge)  # Outputs: 2
        >>> 
        >>> ce_plus4 = with_charge(Ce, 4)
        >>> print(ce_plus4.charge)  # Outputs: 4
        >>> 
        >>> # With molecules
        >>> water = H*2 + O
        >>> hydronium = with_charge(water, 1)
        >>> print(hydronium.charge)  # Outputs: 1
    """
    import copy
    from chemesty.elements.atomic_element import AtomicElement
    from chemesty.molecules.molecule import Molecule
    
    if isinstance(element_or_molecule, AtomicElement):
        # Create a molecule with this element
        mol = Molecule()
        mol.add_element(element_or_molecule, 1)
        mol.charge = charge
        return mol
    elif isinstance(element_or_molecule, Molecule):
        result = copy.deepcopy(element_or_molecule)
        result.charge = charge
        return result
    elif isinstance(element_or_molecule, type) and issubclass(element_or_molecule, AtomicElement):
        # Handle element class (e.g., Fe, O) by instantiating it
        instance = element_or_molecule()  # Create an instance of the element class
        mol = Molecule()
        mol.add_element(instance, 1)
        mol.charge = charge
        return mol
    else:
        raise TypeError(f"Cannot apply charge to {type(element_or_molecule)}")
