"""
Standalone script to generate element classes from element data.
This script creates a Python file for each element in the element_data.py file.
It handles element symbols that are Python keywords by adding an underscore suffix.
"""

import os
import sys
import keyword
import re

def extract_element_data(element_data_path):
    """
    Extract element data from the element_data.py file.
    
    Args:
        element_data_path: Path to the element_data.py file
        
    Returns:
        Dictionary mapping element symbols to their data
    """
    with open(element_data_path, 'r') as f:
        content = f.read()
    
    # Extract the ELEMENT_DATA dictionary
    element_data = {}
    
    # Find all element entries in the file
    pattern = r'"([^"]+)":\s*{([^}]+)}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for symbol, data_str in matches:
        element_data[symbol] = {}
        
        # Extract properties for this element
        prop_pattern = r'"([^"]+)":\s*([^,\n]+)'
        prop_matches = re.findall(prop_pattern, data_str)
        
        for prop, value_str in prop_matches:
            # Convert value string to appropriate Python value
            value_str = value_str.strip()
            if value_str == "None":
                value = None
            elif value_str.startswith('"') and value_str.endswith('"'):
                value = value_str[1:-1]  # Remove quotes
            elif value_str.startswith('[') and value_str.endswith(']'):
                # Parse list
                value = eval(value_str)
            elif value_str.startswith('{') and value_str.endswith('}'):
                # Parse dictionary
                value = eval(value_str)
            elif '.' in value_str:
                # Float
                value = float(value_str)
            else:
                # Integer
                try:
                    value = int(value_str)
                except ValueError:
                    value = value_str
            
            element_data[symbol][prop] = value
    
    return element_data

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
    {data.get('name', 'Unknown')} element ({symbol}, Z={data.get('atomic_number', 0)}).
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

def generate_all_elements(element_data_path, output_dir):
    """
    Generate Python files for all elements in element_data.py.
    
    Args:
        element_data_path: Path to the element_data.py file
        output_dir: Directory to save the files to
    """
    # Extract element data
    element_data = extract_element_data(element_data_path)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Keep track of filename mappings for import statements
    filename_map = {}
    
    # Generate a file for each element
    for symbol, data in element_data.items():
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
        f.write("# This file is auto-generated by generate_elements_standalone.py\n\n")
        
        # Import all element classes
        for symbol in element_data:
            class_name = symbol.capitalize()
            safe_filename = filename_map[symbol]
            f.write(f"from chemesty.elements.{safe_filename} import {class_name}\n")
        
        # Export all element classes
        f.write("\n__all__ = [\n")
        for symbol in element_data:
            class_name = symbol.capitalize()
            f.write(f"    '{class_name}',\n")
        f.write("]\n")
    
    print(f"Updated {init_path}")

if __name__ == "__main__":
    # Get the path to the element_data.py file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    elements_dir = os.path.join(script_dir, "chemesty", "elements")
    element_data_path = os.path.join(elements_dir, "element_data.py")
    
    # Generate all elements
    generate_all_elements(element_data_path, elements_dir)