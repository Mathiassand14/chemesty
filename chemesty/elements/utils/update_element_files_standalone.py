import os
import re
import ast

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

    # Find the ELEMENT_DATA dictionary in the file
    start_index = content.find("ELEMENT_DATA = {")
    if start_index == -1:
        raise ValueError("Could not find ELEMENT_DATA dictionary in the file")

    # Extract the dictionary content
    brace_count = 0
    for i in range(start_index, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_index = i + 1
                break

    # Get the dictionary string
    dict_str = content[start_index:end_index]

    # Parse the dictionary using ast.literal_eval
    # First, extract just the dictionary part (remove the variable assignment)
    dict_str = dict_str.replace("ELEMENT_DATA = ", "")

    # Use a simpler approach: extract each element's data separately
    element_data = {}

    # Find all element entries in the dictionary
    pattern = r'"([^"]+)":\s*{([^}]+)}'
    matches = re.findall(pattern, dict_str, re.DOTALL)

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
                try:
                    value = ast.literal_eval(value_str)
                except:
                    value = []  # Default to empty list if parsing fails
            elif value_str.startswith('{') and value_str.endswith('}'):
                # Parse dictionary
                try:
                    value = ast.literal_eval(value_str)
                except:
                    value = {}  # Default to empty dict if parsing fails
            elif '.' in value_str:
                # Float
                try:
                    value = float(value_str)
                except:
                    value = 0.0  # Default to 0.0 if parsing fails
            else:
                # Integer
                try:
                    value = int(value_str)
                except:
                    value = 0  # Default to 0 if parsing fails

            element_data[symbol][prop] = value

    return element_data

def update_element_file(symbol, data, file_path):
    """
    Update an element file with data from element_data.

    Args:
        symbol: Element symbol
        data: Element data dictionary
        file_path: Path to the element file

    Returns:
        True if the file was updated, False otherwise
    """
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

    # Update the file content with data from element_data
    updated_content = content

    # Update atomic_mass
    if "atomic_mass" in data:
        updated_content = re.sub(
            r'def atomic_mass\(self\) -> float:\s+return 0\.0',
            f'def atomic_mass(self) -> float:\n        return {data["atomic_mass"]}',
            updated_content
        )

    # Update electron_configuration
    if "electron_configuration" in data:
        updated_content = re.sub(
            r'def electron_configuration\(self\) -> str:\s+return ""',
            f'def electron_configuration(self) -> str:\n        return "{data["electron_configuration"]}"',
            updated_content
        )

    # Update electron_shells
    if "electron_shells" in data:
        updated_content = re.sub(
            r'def electron_shells\(self\) -> List\[int\]:\s+return \[\]',
            f'def electron_shells(self) -> List[int]:\n        return {data["electron_shells"]}',
            updated_content
        )
        # Also handle the case where it returns 0 instead of a list
        updated_content = re.sub(
            r'def electron_shells\(self\) -> List\[int\]:\s+return 0',
            f'def electron_shells(self) -> List[int]:\n        return {data["electron_shells"]}',
            updated_content
        )

    # Update electronegativity
    if "electronegativity" in data:
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
    if "atomic_radius" in data:
        updated_content = re.sub(
            r'def atomic_radius\(self\) -> float:\s+return 0\.0',
            f'def atomic_radius(self) -> float:\n        return {data["atomic_radius"]}',
            updated_content
        )

    # Update ionization_energy
    if "ionization_energy" in data:
        updated_content = re.sub(
            r'def ionization_energy\(self\) -> float:\s+return 0\.0',
            f'def ionization_energy(self) -> float:\n        return {data["ionization_energy"]}',
            updated_content
        )

    # Update electron_affinity
    if "electron_affinity" in data:
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
    if "oxidation_states" in data:
        updated_content = re.sub(
            r'def oxidation_states\(self\) -> List\[int\]:\s+return \[\]',
            f'def oxidation_states(self) -> List[int]:\n        return {data["oxidation_states"]}',
            updated_content
        )
        # Also handle the case where it returns 0 instead of a list
        updated_content = re.sub(
            r'def oxidation_states\(self\) -> List\[int\]:\s+return 0',
            f'def oxidation_states(self) -> List[int]:\n        return {data["oxidation_states"]}',
            updated_content
        )

    # Update group
    if "group" in data:
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
    if "period" in data:
        updated_content = re.sub(
            r'def period\(self\) -> int:\s+return 0',
            f'def period(self) -> int:\n        return {data["period"]}',
            updated_content
        )

    # Update block
    if "block" in data:
        updated_content = re.sub(
            r'def block\(self\) -> str:\s+return ""',
            f'def block(self) -> str:\n        return "{data["block"]}"',
            updated_content
        )

    # Update category
    if "category" in data:
        updated_content = re.sub(
            r'def category\(self\) -> str:\s+return ""',
            f'def category(self) -> str:\n        return "{data["category"]}"',
            updated_content
        )

    # Update isotopes
    if "isotopes" in data:
        updated_content = re.sub(
            r'def isotopes\(self\) -> Dict\[int, float\]:\s+return \{\}',
            f'def isotopes(self) -> Dict[int, float]:\n        return {data["isotopes"]}',
            updated_content
        )
        # Also handle the case where it returns 0.0 instead of a dictionary
        updated_content = re.sub(
            r'def isotopes\(self\) -> Dict\[int, float\]:\s+return 0\.0',
            f'def isotopes(self) -> Dict[int, float]:\n        return {data["isotopes"]}',
            updated_content
        )

    # Update melting_point
    if "melting_point" in data:
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
    if "boiling_point" in data:
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
    if "density_value" in data:
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
    if "year_discovered" in data:
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
    if "discoverer" in data:
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

    print(f"{symbol}: Updated with data from element_data")
    return True

def main():
    # Get the path to the element_data.py file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    elements_dir = os.path.join(script_dir, "chemesty", "elements")
    element_data_path = os.path.join(elements_dir, "element_data.py")

    # Extract element data
    print(f"Extracting element data from {element_data_path}...")
    element_data = extract_element_data(element_data_path)
    print(f"Found data for {len(element_data)} elements")

    # Keep track of updated files
    updated_files = []

    # Update each element file
    for symbol, data in element_data.items():
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
            was_updated = update_element_file(symbol, data, file_path)
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
