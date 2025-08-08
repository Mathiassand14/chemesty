"""
Data-driven element implementation to eliminate code duplication.

This module provides a generic element class that uses the element data
dictionary instead of hardcoded property methods with lazy loading support.
"""

from typing import Optional, List, Dict, Any
from functools import cached_property
from chemesty.elements.atomic_element import AtomicElement
from chemesty.elements.element_data import ELEMENT_DATA


class DataDrivenElement(AtomicElement):
    """
    A data-driven element class that eliminates code duplication by using
    the ELEMENT_DATA dictionary for all element properties with lazy loading.
    """
    
    def __init__(self, symbol: str):
        """
        Initialize an element using its symbol with lazy loading.
        
        Args:
            symbol: Chemical symbol of the element (e.g., 'H', 'He', 'Li')
            
        Raises:
            ValueError: If the symbol is not found in ELEMENT_DATA
        """
        if symbol not in ELEMENT_DATA:
            raise ValueError(f"Unknown element symbol: {symbol}")
        
        self._symbol = symbol
    
    @property
    def symbol(self) -> str:
        """Get the chemical symbol of the element."""
        return self._symbol
    
    @cached_property
    def name(self) -> str:
        """Get the name of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["name"]
    
    @cached_property
    def atomic_number(self) -> int:
        """Get the atomic number of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["atomic_number"]
    
    @cached_property
    def atomic_mass(self) -> float:
        """Get the atomic mass of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["atomic_mass"]
    
    @cached_property
    def electron_configuration(self) -> str:
        """Get the electron configuration of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["electron_configuration"]
    
    @cached_property
    def electron_shells(self) -> List[int]:
        """Get the electron shells configuration (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["electron_shells"]
    
    @cached_property
    def electronegativity(self) -> Optional[float]:
        """Get the electronegativity of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol].get("electronegativity")
    
    @cached_property
    def atomic_radius(self) -> float:
        """Get the atomic radius of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["atomic_radius"]
    
    @cached_property
    def ionization_energy(self) -> float:
        """Get the ionization energy of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["ionization_energy"]
    
    @cached_property
    def electron_affinity(self) -> Optional[float]:
        """Get the electron affinity of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol].get("electron_affinity")
    
    @cached_property
    def oxidation_states(self) -> List[int]:
        """Get the possible oxidation states of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["oxidation_states"]
    
    @cached_property
    def group(self) -> Optional[int]:
        """Get the group number of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol].get("group")
    
    @cached_property
    def period(self) -> int:
        """Get the period number of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["period"]
    
    @cached_property
    def block(self) -> str:
        """Get the block of the element (s, p, d, f) (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["block"]
    
    @cached_property
    def category(self) -> str:
        """Get the category of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["category"]
    
    @cached_property
    def isotopes(self) -> Dict[int, float]:
        """Get the isotopes and their abundances (lazy loaded)."""
        return ELEMENT_DATA[self._symbol]["isotopes"]
    
    @cached_property
    def melting_point(self) -> Optional[float]:
        """Get the melting point of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol].get("melting_point")
    
    @cached_property
    def boiling_point(self) -> Optional[float]:
        """Get the boiling point of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol].get("boiling_point")
    
    @cached_property
    def density_value(self) -> Optional[float]:
        """Get the density value of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol].get("density_value")
    
    @cached_property
    def year_discovered(self) -> Optional[int]:
        """Get the year the element was discovered (lazy loaded)."""
        return ELEMENT_DATA[self._symbol].get("year_discovered")
    
    @cached_property
    def discoverer(self) -> Optional[str]:
        """Get the discoverer of the element (lazy loaded)."""
        return ELEMENT_DATA[self._symbol].get("discoverer")


def create_element_class(symbol: str) -> type:
    """
    Create a specific element class dynamically.
    
    Args:
        symbol: Chemical symbol of the element
        
    Returns:
        A class for the specific element
    """
    if symbol not in ELEMENT_DATA:
        raise ValueError(f"Unknown element symbol: {symbol}")
    
    element_name = ELEMENT_DATA[symbol]["name"]
    
    class SpecificElement(DataDrivenElement):
        """Dynamically created element class."""
        
        def __init__(self):
            super().__init__(symbol)
    
    # Set the class name and docstring
    SpecificElement.__name__ = symbol
    SpecificElement.__qualname__ = symbol
    SpecificElement.__doc__ = f"{element_name} element ({symbol}, Z={ELEMENT_DATA[symbol]['atomic_number']})."
    
    return SpecificElement