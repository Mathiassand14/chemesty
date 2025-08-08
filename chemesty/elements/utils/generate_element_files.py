"""
Script to generate element class files for all elements in the periodic table.
This script creates a Python file for each element, handling Python keywords properly.
"""

import os
import keyword

# Dictionary of element symbols and their data
ELEMENTS = [
    # Symbol, Name, Atomic Number
    ("H", "Hydrogen", 1),
    ("He", "Helium", 2),
    ("Li", "Lithium", 3),
    ("Be", "Beryllium", 4),
    ("B", "Boron", 5),
    ("C", "Carbon", 6),
    ("N", "Nitrogen", 7),
    ("O", "Oxygen", 8),
    ("F", "Fluorine", 9),
    ("Ne", "Neon", 10),
    ("Na", "Sodium", 11),
    ("Mg", "Magnesium", 12),
    ("Al", "Aluminum", 13),
    ("Si", "Silicon", 14),
    ("P", "Phosphorus", 15),
    ("S", "Sulfur", 16),
    ("Cl", "Chlorine", 17),
    ("Ar", "Argon", 18),
    ("K", "Potassium", 19),
    ("Ca", "Calcium", 20),
    ("Sc", "Scandium", 21),
    ("Ti", "Titanium", 22),
    ("V", "Vanadium", 23),
    ("Cr", "Chromium", 24),
    ("Mn", "Manganese", 25),
    ("Fe", "Iron", 26),
    ("Co", "Cobalt", 27),
    ("Ni", "Nickel", 28),
    ("Cu", "Copper", 29),
    ("Zn", "Zinc", 30),
    ("Ga", "Gallium", 31),
    ("Ge", "Germanium", 32),
    ("As", "Arsenic", 33),
    ("Se", "Selenium", 34),
    ("Br", "Bromine", 35),
    ("Kr", "Krypton", 36),
    ("Rb", "Rubidium", 37),
    ("Sr", "Strontium", 38),
    ("Y", "Yttrium", 39),
    ("Zr", "Zirconium", 40),
    ("Nb", "Niobium", 41),
    ("Mo", "Molybdenum", 42),
    ("Tc", "Technetium", 43),
    ("Ru", "Ruthenium", 44),
    ("Rh", "Rhodium", 45),
    ("Pd", "Palladium", 46),
    ("Ag", "Silver", 47),
    ("Cd", "Cadmium", 48),
    ("In", "Indium", 49),
    ("Sn", "Tin", 50),
    ("Sb", "Antimony", 51),
    ("Te", "Tellurium", 52),
    ("I", "Iodine", 53),
    ("Xe", "Xenon", 54),
    ("Cs", "Cesium", 55),
    ("Ba", "Barium", 56),
    ("La", "Lanthanum", 57),
    ("Ce", "Cerium", 58),
    ("Pr", "Praseodymium", 59),
    ("Nd", "Neodymium", 60),
    ("Pm", "Promethium", 61),
    ("Sm", "Samarium", 62),
    ("Eu", "Europium", 63),
    ("Gd", "Gadolinium", 64),
    ("Tb", "Terbium", 65),
    ("Dy", "Dysprosium", 66),
    ("Ho", "Holmium", 67),
    ("Er", "Erbium", 68),
    ("Tm", "Thulium", 69),
    ("Yb", "Ytterbium", 70),
    ("Lu", "Lutetium", 71),
    ("Hf", "Hafnium", 72),
    ("Ta", "Tantalum", 73),
    ("W", "Tungsten", 74),
    ("Re", "Rhenium", 75),
    ("Os", "Osmium", 76),
    ("Ir", "Iridium", 77),
    ("Pt", "Platinum", 78),
    ("Au", "Gold", 79),
    ("Hg", "Mercury", 80),
    ("Tl", "Thallium", 81),
    ("Pb", "Lead", 82),
    ("Bi", "Bismuth", 83),
    ("Po", "Polonium", 84),
    ("At", "Astatine", 85),
    ("Rn", "Radon", 86),
    ("Fr", "Francium", 87),
    ("Ra", "Radium", 88),
    ("Ac", "Actinium", 89),
    ("Th", "Thorium", 90),
    ("Pa", "Protactinium", 91),
    ("U", "Uranium", 92),
    ("Np", "Neptunium", 93),
    ("Pu", "Plutonium", 94),
    ("Am", "Americium", 95),
    ("Cm", "Curium", 96),
    ("Bk", "Berkelium", 97),
    ("Cf", "Californium", 98),
    ("Es", "Einsteinium", 99),
    ("Fm", "Fermium", 100),
    ("Md", "Mendelevium", 101),
    ("No", "Nobelium", 102),
    ("Lr", "Lawrencium", 103),
    ("Rf", "Rutherfordium", 104),
    ("Db", "Dubnium", 105),
    ("Sg", "Seaborgium", 106),
    ("Bh", "Bohrium", 107),
    ("Hs", "Hassium", 108),
    ("Mt", "Meitnerium", 109),
    ("Ds", "Darmstadtium", 110),
    ("Rg", "Roentgenium", 111),
    ("Cn", "Copernicium", 112),
    ("Nh", "Nihonium", 113),
    ("Fl", "Flerovium", 114),
    ("Mc", "Moscovium", 115),
    ("Lv", "Livermorium", 116),
    ("Ts", "Tennessine", 117),
    ("Og", "Oganesson", 118),
]

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

def generate_element_class(symbol, name, atomic_number):
    """
    Generate a minimal Python class for an element.
    
    Args:
        symbol: Element symbol
        name: Element name
        atomic_number: Atomic number
    
    Returns:
        String containing the Python code for the element class
    """
    class_name = symbol.capitalize()
    
    # Start with imports and class definition
    code = f"""from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class {class_name}(AtomicElement):
    \"""
    {name} element ({symbol}, Z={atomic_number}).
    \"""
    
    @property
    def name(self) -> str:
        return "{name}"
    
    @property
    def atomic_number(self) -> int:
        return {atomic_number}
    
    @property
    def symbol(self) -> str:
        return "{symbol}"
    
    # Note: This is a minimal implementation.
    # In a real application, you would need to implement all abstract methods
    # from the AtomicElement base class.
    
    # Placeholder implementations for required abstract methods
    @property
    def atomic_mass(self) -> float:
        return 0.0
    
    @property
    def electron_configuration(self) -> str:
        return ""
    
    @property
    def electron_shells(self) -> List[int]:
        return []
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 0.0
    
    @property
    def ionization_energy(self) -> float:
        return 0.0
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return None
    
    @property
    def oxidation_states(self) -> List[int]:
        return []
    
    @property
    def group(self) -> Optional[int]:
        return None
    
    @property
    def period(self) -> int:
        return 0
    
    @property
    def block(self) -> str:
        return ""
    
    @property
    def category(self) -> str:
        return ""
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {{}}
    
    @property
    def melting_point(self) -> Optional[float]:
        return None
    
    @property
    def boiling_point(self) -> Optional[float]:
        return None
    
    @property
    def density_value(self) -> Optional[float]:
        return None
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return None
"""
    
    return code

def generate_all_elements(output_dir):
    """
    Generate Python files for all elements.
    
    Args:
        output_dir: Directory to save the files to
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Keep track of filename mappings for import statements
    filename_map = {}
    
    # Generate a file for each element
    for symbol, name, atomic_number in ELEMENTS:
        safe_filename = get_safe_filename(symbol)
        filename_map[symbol] = safe_filename
        
        file_path = os.path.join(output_dir, f"{safe_filename}.py")
        
        # Skip if file already exists
        if os.path.exists(file_path):
            print(f"Skipping {file_path} (already exists)")
            continue
            
        code = generate_element_class(symbol, name, atomic_number)
        
        with open(file_path, 'w') as f:
            f.write(code)
        
        print(f"Generated {file_path}")
    
    # Update the __init__.py file to import all elements
    init_path = os.path.join(output_dir, "__init__.py")
    with open(init_path, 'w') as f:
        f.write("# This file is auto-generated by generate_element_files.py\n\n")
        
        # Import all element classes
        for symbol, name, atomic_number in ELEMENTS:
            class_name = symbol.capitalize()
            safe_filename = filename_map[symbol]
            f.write(f"from chemesty.elements.{safe_filename} import {class_name}\n")
        
        # Export all element classes
        f.write("\n__all__ = [\n")
        for symbol, name, atomic_number in ELEMENTS:
            class_name = symbol.capitalize()
            f.write(f"    '{class_name}',\n")
        f.write("]\n")
    
    print(f"Updated {init_path}")

if __name__ == "__main__":
    # Get the path to the elements directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    elements_dir = os.path.join(script_dir, "chemesty", "elements")
    
    # Generate all elements
    generate_all_elements(elements_dir)