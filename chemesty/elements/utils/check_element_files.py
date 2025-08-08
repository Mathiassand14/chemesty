import os
import importlib.util
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Import the element data
from chemesty.elements.element_data import ELEMENT_DATA

def check_element_file(symbol, file_path):
    """
    Check if an element file has placeholder values.
    
    Args:
        symbol: Element symbol
        file_path: Path to the element file
        
    Returns:
        True if the file has placeholder values, False otherwise
    """
    # Load the module
    spec = importlib.util.spec_from_file_location(f"chemesty.elements.{symbol.lower()}", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get the element class
    class_name = symbol.capitalize()
    element_class = getattr(module, class_name)
    
    # Create an instance of the element
    element = element_class()
    
    # Check for placeholder values
    has_placeholders = False
    
    # Check atomic_mass
    if element.atomic_mass == 0.0:
        print(f"{symbol}: atomic_mass is 0.0")
        has_placeholders = True
    
    # Check electron_configuration
    if element.electron_configuration == "":
        print(f"{symbol}: electron_configuration is empty")
        has_placeholders = True
    
    # Check electron_shells
    if element.electron_shells == []:
        print(f"{symbol}: electron_shells is empty")
        has_placeholders = True
    
    # Check atomic_radius
    if element.atomic_radius == 0.0:
        print(f"{symbol}: atomic_radius is 0.0")
        has_placeholders = True
    
    # Check ionization_energy
    if element.ionization_energy == 0.0:
        print(f"{symbol}: ionization_energy is 0.0")
        has_placeholders = True
    
    # Check oxidation_states
    if element.oxidation_states == []:
        print(f"{symbol}: oxidation_states is empty")
        has_placeholders = True
    
    # Check period
    if element.period == 0:
        print(f"{symbol}: period is 0")
        has_placeholders = True
    
    # Check block
    if element.block == "":
        print(f"{symbol}: block is empty")
        has_placeholders = True
    
    # Check category
    if element.category == "":
        print(f"{symbol}: category is empty")
        has_placeholders = True
    
    return has_placeholders

def main():
    # Get the path to the elements directory
    elements_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chemesty", "elements")
    
    # Keep track of files with placeholder values
    files_with_placeholders = []
    
    # Check each element file
    for symbol in ELEMENT_DATA:
        # Handle Python keywords
        file_name = symbol.lower()
        if file_name == "in":
            file_name = "in_"
        elif file_name == "as":
            file_name = "as_"
        
        file_path = os.path.join(elements_dir, f"{file_name}.py")
        
        # Skip if file doesn't exist
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} does not exist")
            continue
        
        print(f"Checking {file_path}...")
        try:
            has_placeholders = check_element_file(symbol, file_path)
            if has_placeholders:
                files_with_placeholders.append((symbol, file_path))
        except Exception as e:
            print(f"Error checking {file_path}: {e}")
    
    # Print summary
    print("\nSummary:")
    print(f"Found {len(files_with_placeholders)} files with placeholder values:")
    for symbol, file_path in files_with_placeholders:
        print(f"- {symbol}: {file_path}")

if __name__ == "__main__":
    main()