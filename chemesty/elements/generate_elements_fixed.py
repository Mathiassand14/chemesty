"""
Script to generate element classes from element data.
This script creates a Python file for each element in the element_data.py file.
It handles element symbols that are Python keywords by adding an underscore suffix.
"""

import os
import sys
from pathlib import Path
import keyword

# Import element data directly from the file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from chemesty.elements.element_data import ELEMENT_DATA

def generate_element_class(symbol, data):
    """
    Generate a Python class for an element.
    
    Args:
        symbol: Element symbol
        data: Element data dictionary
    
    Returns:
        String containing the Python code for the element class
    """
    class_name = symbol.capitalize()
    
    # Start with imports and class definition
    code = f"""from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class {class_name}(AtomicElement):
    \"""
    {data['name']} element ({symbol}, Z={data['atomic_number']}).
    \"""
    
"""
    
    # Add properties
    for prop, value in data.items():
        if prop == "name":
            code += f"""    @property
    def name(self) -> str:
        return "{value}"
    
"""
        elif prop == "symbol":
            continue  # Symbol is handled separately
        elif prop == "atomic_number":
            code += f"""    @property
    def atomic_number(self) -> int:
        return {value}
    
"""
        elif prop == "atomic_mass":
            code += f"""    @property
    def atomic_mass(self) -> float:
        return {value}
    
"""
        elif prop == "electron_configuration":
            code += f"""    @property
    def electron_configuration(self) -> str:
        return "{value}"
    
"""
        elif prop == "electron_shells":
            shells_str = str(value)
            code += f"""    @property
    def electron_shells(self) -> List[int]:
        return {shells_str}
    
"""
        elif prop == "electronegativity":
            if value is None:
                code += f"""    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
"""
            else:
                code += f"""    @property
    def electronegativity(self) -> Optional[float]:
        return {value}
    
"""
        elif prop == "atomic_radius":
            code += f"""    @property
    def atomic_radius(self) -> float:
        return {value}
    
"""
        elif prop == "ionization_energy":
            code += f"""    @property
    def ionization_energy(self) -> float:
        return {value}
    
"""
        elif prop == "electron_affinity":
            if value is None:
                code += f"""    @property
    def electron_affinity(self) -> Optional[float]:
        return None
    
"""
            else:
                code += f"""    @property
    def electron_affinity(self) -> Optional[float]:
        return {value}
    
"""
        elif prop == "oxidation_states":
            states_str = str(value)
            code += f"""    @property
    def oxidation_states(self) -> List[int]:
        return {states_str}
    
"""
        elif prop == "group":
            if value is None:
                code += f"""    @property
    def group(self) -> Optional[int]:
        return None
    
"""
            else:
                code += f"""    @property
    def group(self) -> Optional[int]:
        return {value}
    
"""
        elif prop == "period":
            code += f"""    @property
    def period(self) -> int:
        return {value}
    
"""
        elif prop == "block":
            code += f"""    @property
    def block(self) -> str:
        return "{value}"
    
"""
        elif prop == "category":
            code += f"""    @property
    def category(self) -> str:
        return "{value}"
    
"""
        elif prop == "isotopes":
            isotopes_str = str(value)
            code += f"""    @property
    def isotopes(self) -> Dict[int, float]:
        return {isotopes_str}
    
"""
        elif prop == "melting_point":
            if value is None:
                code += f"""    @property
    def melting_point(self) -> Optional[float]:
        return None
    
"""
            else:
                code += f"""    @property
    def melting_point(self) -> Optional[float]:
        return {value}
    
"""
        elif prop == "boiling_point":
            if value is None:
                code += f"""    @property
    def boiling_point(self) -> Optional[float]:
        return None
    
"""
            else:
                code += f"""    @property
    def boiling_point(self) -> Optional[float]:
        return {value}
    
"""
        elif prop == "density_value":
            if value is None:
                code += f"""    @property
    def density_value(self) -> Optional[float]:
        return None
    
"""
            else:
                code += f"""    @property
    def density_value(self) -> Optional[float]:
        return {value}
    
"""
        elif prop == "year_discovered":
            if value is None:
                code += f"""    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
"""
            else:
                code += f"""    @property
    def year_discovered(self) -> Optional[int]:
        return {value}
    
"""
        elif prop == "discoverer":
            if value is None:
                code += f"""    @property
    def discoverer(self) -> Optional[str]:
        return None
    
"""
            else:
                code += f"""    @property
    def discoverer(self) -> Optional[str]:
        return "{value}"
    
"""
    
    # Add symbol property
    code += f"""    @property
    def symbol(self) -> str:
        return "{symbol}"
"""
    
    return code

def get_safe_filename(symbol):
    """
    Get a safe filename for the element symbol.
    If the symbol is a Python keyword, add an underscore suffix.
    
    Args:
        symbol: Element symbol
        
    Returns:
        Safe filename
    """
    if keyword.iskeyword(symbol.lower()):
        return f"{symbol.lower()}_"
    return symbol.lower()

def generate_all_elements(output_dir=None):
    """
    Generate Python files for all elements in ELEMENT_DATA.
    
    Args:
        output_dir: Directory to save the files to. If None, uses the current directory.
    """
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Keep track of filename mappings for import statements
    filename_map = {}
    
    # Generate a file for each element
    for symbol, data in ELEMENT_DATA.items():
        safe_filename = get_safe_filename(symbol)
        filename_map[symbol] = safe_filename
        
        file_path = os.path.join(output_dir, f"{safe_filename}.py")
        code = generate_element_class(symbol, data)
        
        with open(file_path, 'w') as f:
            f.write(code)
        
        print(f"Generated {file_path}")
    
    # Update the __init__.py file to import all elements
    init_path = os.path.join(output_dir, "__init__.py")
    with open(init_path, 'w') as f:
        f.write("# This file is auto-generated by generate_elements_fixed.py\n\n")
        
        # Import all element classes
        for symbol in ELEMENT_DATA:
            class_name = symbol.capitalize()
            safe_filename = filename_map[symbol]
            f.write(f"from chemesty.elements.{safe_filename} import {class_name}\n")
        
        # Export all element classes
        f.write("\n__all__ = [\n")
        for symbol in ELEMENT_DATA:
            class_name = symbol.capitalize()
            f.write(f"    '{class_name}',\n")
        f.write("]\n")
    
    print(f"Updated {init_path}")

if __name__ == "__main__":
    generate_all_elements()