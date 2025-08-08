import os
import re
from chemesty.elements.element_data import ELEMENT_DATA

def update_element_file(symbol, file_path):
    """
    Update an element file with data from ELEMENT_DATA.
    
    Args:
        symbol: Element symbol
        file_path: Path to the element file
        
    Returns:
        True if the file was updated, False otherwise
    """
    # Get the data for this element
    data = ELEMENT_DATA.get(symbol)
    if not data:
        print(f"Warning: No data found for {symbol}")
        return False
    
    # Read the current file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the file already has proper values
    has_placeholders = False
    
    # Check for placeholder values in the content
    if 'return 0.0' in content:
        has_placeholders = True
    if 'return ""' in content:
        has_placeholders = True
    if 'return []' in content:
        has_placeholders = True
    if 'return {}' in content:
        has_placeholders = True
    if 'return 0' in content and 'return 0.' not in content:
        has_placeholders = True
    
    if not has_placeholders:
        print(f"{symbol}: No placeholders found, skipping")
        return False
    
    # Update the file content with data from ELEMENT_DATA
    updated_content = content
    
    # Update atomic_mass
    updated_content = re.sub(
        r'def atomic_mass\(self\) -> float:\s+return 0\.0',
        f'def atomic_mass(self) -> float:\n        return {data["atomic_mass"]}',
        updated_content
    )
    
    # Update electron_configuration
    updated_content = re.sub(
        r'def electron_configuration\(self\) -> str:\s+return ""',
        f'def electron_configuration(self) -> str:\n        return "{data["electron_configuration"]}"',
        updated_content
    )
    
    # Update electron_shells
    updated_content = re.sub(
        r'def electron_shells\(self\) -> List\[int\]:\s+return \[\]',
        f'def electron_shells(self) -> List[int]:\n        return {data["electron_shells"]}',
        updated_content
    )
    
    # Update electronegativity
    if data["electronegativity"] is None:
        updated_content = re.sub(
            r'def electronegativity\(self\) -> Optional\[float\]:\s+return None',
            f'def electronegativity(self) -> Optional[float]:\n        return None',
            updated_content
        )
    else:
        updated_content = re.sub(
            r'def electronegativity\(self\) -> Optional\[float\]:\s+return None',
            f'def electronegativity(self) -> Optional[float]:\n        return {data["electronegativity"]}',
            updated_content
        )
    
    # Update atomic_radius
    updated_content = re.sub(
        r'def atomic_radius\(self\) -> float:\s+return 0\.0',
        f'def atomic_radius(self) -> float:\n        return {data["atomic_radius"]}',
        updated_content
    )
    
    # Update ionization_energy
    updated_content = re.sub(
        r'def ionization_energy\(self\) -> float:\s+return 0\.0',
        f'def ionization_energy(self) -> float:\n        return {data["ionization_energy"]}',
        updated_content
    )
    
    # Update electron_affinity
    if data["electron_affinity"] is None:
        updated_content = re.sub(
            r'def electron_affinity\(self\) -> Optional\[float\]:\s+return None',
            f'def electron_affinity(self) -> Optional[float]:\n        return None',
            updated_content
        )
    else:
        updated_content = re.sub(
            r'def electron_affinity\(self\) -> Optional\[float\]:\s+return None',
            f'def electron_affinity(self) -> Optional[float]:\n        return {data["electron_affinity"]}',
            updated_content
        )
    
    # Update oxidation_states
    updated_content = re.sub(
        r'def oxidation_states\(self\) -> List\[int\]:\s+return \[\]',
        f'def oxidation_states(self) -> List[int]:\n        return {data["oxidation_states"]}',
        updated_content
    )
    
    # Update group
    if data["group"] is None:
        updated_content = re.sub(
            r'def group\(self\) -> Optional\[int\]:\s+return None',
            f'def group(self) -> Optional[int]:\n        return None',
            updated_content
        )
    else:
        updated_content = re.sub(
            r'def group\(self\) -> Optional\[int\]:\s+return None',
            f'def group(self) -> Optional[int]:\n        return {data["group"]}',
            updated_content
        )
    
    # Update period
    updated_content = re.sub(
        r'def period\(self\) -> int:\s+return 0',
        f'def period(self) -> int:\n        return {data["period"]}',
        updated_content
    )
    
    # Update block
    updated_content = re.sub(
        r'def block\(self\) -> str:\s+return ""',
        f'def block(self) -> str:\n        return "{data["block"]}"',
        updated_content
    )
    
    # Update category
    updated_content = re.sub(
        r'def category\(self\) -> str:\s+return ""',
        f'def category(self) -> str:\n        return "{data["category"]}"',
        updated_content
    )
    
    # Update isotopes
    updated_content = re.sub(
        r'def isotopes\(self\) -> Dict\[int, float\]:\s+return \{\}',
        f'def isotopes(self) -> Dict[int, float]:\n        return {data["isotopes"]}',
        updated_content
    )
    
    # Update melting_point
    if data["melting_point"] is None:
        updated_content = re.sub(
            r'def melting_point\(self\) -> Optional\[float\]:\s+return None',
            f'def melting_point(self) -> Optional[float]:\n        return None',
            updated_content
        )
    else:
        updated_content = re.sub(
            r'def melting_point\(self\) -> Optional\[float\]:\s+return None',
            f'def melting_point(self) -> Optional[float]:\n        return {data["melting_point"]}',
            updated_content
        )
    
    # Update boiling_point
    if data["boiling_point"] is None:
        updated_content = re.sub(
            r'def boiling_point\(self\) -> Optional\[float\]:\s+return None',
            f'def boiling_point(self) -> Optional[float]:\n        return None',
            updated_content
        )
    else:
        updated_content = re.sub(
            r'def boiling_point\(self\) -> Optional\[float\]:\s+return None',
            f'def boiling_point(self) -> Optional[float]:\n        return {data["boiling_point"]}',
            updated_content
        )
    
    # Update density_value
    if data["density_value"] is None:
        updated_content = re.sub(
            r'def density_value\(self\) -> Optional\[float\]:\s+return None',
            f'def density_value(self) -> Optional[float]:\n        return None',
            updated_content
        )
    else:
        updated_content = re.sub(
            r'def density_value\(self\) -> Optional\[float\]:\s+return None',
            f'def density_value(self) -> Optional[float]:\n        return {data["density_value"]}',
            updated_content
        )
    
    # Update year_discovered
    if data["year_discovered"] is None:
        updated_content = re.sub(
            r'def year_discovered\(self\) -> Optional\[int\]:\s+return None',
            f'def year_discovered(self) -> Optional[int]:\n        return None',
            updated_content
        )
    else:
        updated_content = re.sub(
            r'def year_discovered\(self\) -> Optional\[int\]:\s+return None',
            f'def year_discovered(self) -> Optional[int]:\n        return {data["year_discovered"]}',
            updated_content
        )
    
    # Update discoverer
    if data["discoverer"] is None:
        updated_content = re.sub(
            r'def discoverer\(self\) -> Optional\[str\]:\s+return None',
            f'def discoverer(self) -> Optional[str]:\n        return None',
            updated_content
        )
    else:
        updated_content = re.sub(
            r'def discoverer\(self\) -> Optional\[str\]:\s+return None',
            f'def discoverer(self) -> Optional[str]:\n        return "{data["discoverer"]}"',
            updated_content
        )
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print(f"{symbol}: Updated with data from ELEMENT_DATA")
    return True

def main():
    # Get the path to the elements directory
    elements_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chemesty", "elements")
    
    # Keep track of updated files
    updated_files = []
    
    # Update each element file
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
            was_updated = update_element_file(symbol, file_path)
            if was_updated:
                updated_files.append((symbol, file_path))
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
    
    # Print summary
    print("\nSummary:")
    print(f"Updated {len(updated_files)} files:")
    for symbol, file_path in updated_files:
        print(f"- {symbol}: {file_path}")

if __name__ == "__main__":
    main()