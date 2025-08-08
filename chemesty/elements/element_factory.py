from typing import Dict
from chemesty.elements.atomic_element import AtomicElement
from chemesty.elements.data_driven_element import DataDrivenElement
from chemesty.elements.element_data import ELEMENT_DATA
from chemesty.utils.cache import get_cache_manager

class ElementFactory:
    """Factory class for creating element instances using data-driven approach."""
    
    _elements: Dict[str, AtomicElement] = {}  # Cache for singleton instances
    
    @classmethod
    def get_element(cls, symbol: str) -> AtomicElement:
        """
        Get an element instance by its symbol using the data-driven approach with caching.
        
        Args:
            symbol: Chemical symbol of the element (e.g., 'H', 'He')
            
        Returns:
            An instance of the corresponding element class
            
        Raises:
            ValueError: If the symbol is not a valid element symbol
        """
        symbol = symbol.capitalize()
        
        # Try to get from global cache first
        cache_manager = get_cache_manager()
        cached_element = cache_manager.get_element(symbol)
        
        if cached_element is not None:
            return cached_element
        
        # Check local cache for backward compatibility
        if symbol in cls._elements:
            element = cls._elements[symbol]
            cache_manager.cache_element(symbol, element)
            return element
        
        # Create new element using data-driven approach
        if symbol not in ELEMENT_DATA:
            raise ValueError(f"Unknown element symbol: {symbol}")
        
        element = DataDrivenElement(symbol)
        
        # Cache in both local and global cache
        cls._elements[symbol] = element
        cache_manager.cache_element(symbol, element)
        
        return element
    
    @classmethod
    def get_element_by_number(cls, atomic_number: int) -> AtomicElement:
        """
        Get an element instance by its atomic number.
        
        Args:
            atomic_number: Atomic number of the element
            
        Returns:
            An instance of the corresponding element class
            
        Raises:
            ValueError: If the atomic number is not valid
        """
        # Mapping of atomic numbers to symbols
        number_to_symbol = {
            1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 10: "Ne",
            11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar",
            19: "K", 20: "Ca", 21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn",
            31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr",
            37: "Rb", 38: "Sr", 39: "Y", 40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd",
            49: "In", 50: "Sn", 51: "Sb", 52: "Te", 53: "I", 54: "Xe",
            55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr", 60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb", 71: "Lu",
            72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg",
            81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn",
            87: "Fr", 88: "Ra", 89: "Ac", 90: "Th", 91: "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es", 100: "Fm", 101: "Md", 102: "No", 103: "Lr",
            104: "Rf", 105: "Db", 106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt", 110: "Ds", 111: "Rg", 112: "Cn",
            113: "Nh", 114: "Fl", 115: "Mc", 116: "Lv", 117: "Ts", 118: "Og"
        }
        
        if atomic_number not in number_to_symbol:
            raise ValueError(f"Invalid atomic number: {atomic_number}")
            
        return cls.get_element(number_to_symbol[atomic_number])