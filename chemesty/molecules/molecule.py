from collections import OrderedDict
from typing import Dict, List, Optional, Union, Any
import math
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
from sympy.physics.units import centimeter, gram, angstrom
from chemesty.utils.logging_config import get_logger, log_operation

# Define functions that are not available in the installed version of sympy
def cubic(unit):
    """Return the cube of a unit."""
    return unit**3

from chemesty.elements.atomic_element import AtomicElement, ElementMeta


def create_reaction_side(*components) -> 'ReactionSide':
    """
    Helper function to create a ReactionSide from various component types.
    
    This function handles the creation of ReactionSide objects from different
    input formats, making the reaction syntax more flexible.
    
    Args:
        *components: Variable number of components (molecules, tuples, etc.)
        
    Returns:
        ReactionSide object
        
    Examples:
        >>> create_reaction_side((2, H2), O2)  # 2*H2 & O2
        >>> create_reaction_side(CH4, (2, O2))  # CH4 & 2*O2
    """
    processed_components = []
    
    for comp in components:
        if isinstance(comp, tuple) and len(comp) == 2:
            coeff, mol = comp
            if isinstance(mol, Molecule):
                processed_components.append((coeff, mol))
            else:
                raise TypeError(f"Tuple must contain (coefficient, Molecule), got {type(mol)}")
        elif isinstance(comp, Molecule):
            processed_components.append((1.0, comp))
        else:
            raise TypeError(f"Invalid component type: {type(comp)}")
    
    return ReactionSide(processed_components)


class ReactionSide:
    """
    Represents one side of a chemical equation (reactants or products).
    
    This class handles multiple molecules with their coefficients for use
    in chemical reaction operator overloading.
    """
    
    def __init__(self, components: Optional[List[Union['Molecule', tuple]]] = None):
        """
        Initialize a reaction side.
        
        Args:
            components: List of molecules or (molecule, coefficient) tuples
        """
        self.components = []
        if components:
            for comp in components:
                if isinstance(comp, tuple) and len(comp) == 2:
                    # Check if the first element is a molecule and the second is a number
                    if isinstance(comp[0], Molecule) and isinstance(comp[1], (int, float)):
                        mol, coeff = comp
                    # Check if the first element is a number and the second is a molecule
                    elif isinstance(comp[0], (int, float)) and isinstance(comp[1], Molecule):
                        coeff, mol = comp
                    else:
                        raise TypeError(f"Tuple must contain (molecule, coefficient) or (coefficient, molecule), got {type(comp[0])}, {type(comp[1])}")
                    
                    # Create a deep copy of the molecule to prevent unintended modifications
                    import copy
                    mol_copy = copy.deepcopy(mol)
                    
                    # Try to handle ReactionComponent (import here to avoid circular imports)
                    try:
                        from chemesty.reactions.reaction import ReactionComponent
                        # If this is from a ReactionComponent with a phase, preserve the phase
                        if isinstance(comp, ReactionComponent) and hasattr(comp, 'phase') and comp.phase is not None:
                            mol_copy.phase = comp.phase
                    except ImportError:
                        pass
                    
                    self.components.append((mol_copy, coeff))
                elif isinstance(comp, Molecule):
                    # Create a deep copy of the molecule to prevent unintended modifications
                    import copy
                    comp_copy = copy.deepcopy(comp)
                    self.components.append((comp_copy, 1.0))
                else:
                    # Try to handle ReactionComponent (import here to avoid circular imports)
                    try:
                        from chemesty.reactions.reaction import ReactionComponent
                        if isinstance(comp, ReactionComponent):
                            # Create a deep copy of the reaction component
                            import copy
                            comp_copy = copy.deepcopy(comp)
                            # Store the phase in the molecule to preserve it
                            if hasattr(comp_copy, 'phase') and comp_copy.phase is not None:
                                comp_copy.molecule.phase = comp_copy.phase
                            self.components.append((comp_copy.molecule, comp_copy.coefficient))
                        else:
                            raise TypeError(f"Invalid component type: {type(comp)}")
                    except (ImportError, TypeError):
                        raise TypeError(f"Invalid component type: {type(comp)}")
    
    def __and__(self, other: Union['Molecule', tuple, 'ReactionSide', 'Reaction']) -> Union['ReactionSide', 'Reaction']:
        """
        Combine this reaction side with another molecule, reaction component, reaction side, or reaction.
        
        Args:
            other: Molecule, (coefficient, molecule) tuple, ReactionSide, ReactionComponent, or Reaction
            
        Returns:
            New ReactionSide with combined components or a Reaction if other is a Reaction
        """
        import copy
        
        # Handle Reaction objects by delegating to the Reaction's __rand__ method
        try:
            from chemesty.reactions.reaction import Reaction
            if isinstance(other, Reaction):
                # Use the Reaction's __rand__ method to handle this case
                return other.__rand__(self)
        except ImportError:
            pass
            
        # Create deep copies of all components
        new_components = []
        for mol, coeff in self.components:
            mol_copy = copy.deepcopy(mol)
            new_components.append((mol_copy, coeff))
        
        if isinstance(other, tuple) and len(other) == 2:
            coeff, mol = other
            mol_copy = copy.deepcopy(mol)
            new_components.append((mol_copy, coeff))
        elif isinstance(other, Molecule):
            other_copy = copy.deepcopy(other)
            new_components.append((other_copy, 1.0))
        elif isinstance(other, ReactionSide):
            for mol, coeff in other.components:
                mol_copy = copy.deepcopy(mol)
                new_components.append((mol_copy, coeff))
        else:
            # Try to handle ReactionComponent (import here to avoid circular imports)
            try:
                from chemesty.reactions.reaction import ReactionComponent
                if isinstance(other, ReactionComponent):
                    # Create a deep copy of the reaction component
                    other_copy = copy.deepcopy(other)
                    # Store the phase in the molecule to preserve it
                    if hasattr(other_copy, 'phase') and other_copy.phase is not None:
                        other_copy.molecule.phase = other_copy.phase
                    new_components.append((other_copy.molecule, other_copy.coefficient))
                else:
                    raise TypeError(f"Cannot combine ReactionSide with {type(other)}")
            except (ImportError, TypeError):
                raise TypeError(f"Cannot combine ReactionSide with {type(other)}")
        
        return ReactionSide([comp for comp in new_components])
        
    def __add__(self, other: Union['Molecule', tuple, 'ReactionSide']) -> 'ReactionSide':
        """
        Add another molecule, reaction component, or reaction side to this reaction side.
        
        This method is an alias for __and__ to support the + operator.
        
        Args:
            other: Molecule, (coefficient, molecule) tuple, ReactionSide, or ReactionComponent
            
        Returns:
            New ReactionSide with combined components
        """
        return self.__and__(other)
    
    def __rshift__(self, other: Union['Molecule', tuple, 'ReactionSide']) -> 'Reaction':
        """
        Create a reaction from this side to products.
        
        Args:
            other: Products side (Molecule, tuple, ReactionSide, or ReactionComponent)
            
        Returns:
            Reaction object
        """
        # Import here to avoid circular imports
        from chemesty.reactions.reaction import Reaction, ReactionComponent
        
        # Handle products
        if isinstance(other, ReactionSide):
            products = other
        elif isinstance(other, tuple) and len(other) == 2:
            coeff, mol = other
            products = ReactionSide([(coeff, mol)])
        elif isinstance(other, Molecule):
            products = ReactionSide([other])
        elif isinstance(other, ReactionComponent):
            # Create a deep copy of the reaction component
            import copy
            other_copy = copy.deepcopy(other)
            # Store the phase in the molecule to preserve it
            if hasattr(other_copy, 'phase') and other_copy.phase is not None:
                other_copy.molecule.phase = other_copy.phase
            # Create a ReactionSide with the ReactionComponent
            products = ReactionSide([(other_copy.molecule, other_copy.coefficient)])
        else:
            raise TypeError(f"Cannot create reaction with products of type {type(other)}")
        
        # Create reaction
        reaction = Reaction()
        
        # Add reactants
        for mol, coeff in self.components:
            # Pass the molecule's phase to the add_reactant method
            reaction.add_reactant(mol, coeff, phase=mol.phase if hasattr(mol, 'phase') else None)
        
        # Add products
        for mol, coeff in products.components:
            # Pass the molecule's phase to the add_product method
            reaction.add_product(mol, coeff, phase=mol.phase if hasattr(mol, 'phase') else None)
        
        return reaction
    
    def __str__(self) -> str:
        """String representation of the reaction side."""
        parts = []
        for mol, coeff in self.components:
            if coeff == 1.0:
                parts.append(str(mol))
            else:
                parts.append(f"{coeff} {mol}")
        return " & ".join(parts)
    
    def __repr__(self) -> str:
        """Detailed representation of the reaction side."""
        return f"ReactionSide({self.components})"

class Molecule:
    """
    A class representing a chemical molecule composed of multiple atomic elements.
    Only the elements composition is settable; all other properties are calculated.
    """

    def __init__(self, formula: Optional[str] = None, smiles: Optional[str] = None, phase: Optional[str] = None):
        """
        Initialize a Molecule instance.

        Args:
            formula: Optional string representation of the compound (e.g., "H2O", "C6H12O6")
            smiles: Optional SMILES string representation of the molecule
            phase: Optional physical state/phase of the molecule ('s', 'l', 'g', 'aq')
        """
        self._logger = get_logger(f"{__name__}.Molecule")
        self._elements = OrderedDict()  # Use OrderedDict to remember the order
        self._sub_molecules = []  # List of (molecule, multiplier) tuples for sub-molecules
        self._rdkit_mol = None
        self._phase = None
        self._charge = 0  # Initialize charge to 0 (neutral)
        
        # Set phase if provided
        if phase:
            self.phase = phase

        if formula:
            self._logger.debug(f"Creating molecule from formula: {formula}")
            self.set_from_formula(formula)
        elif smiles:
            self._logger.debug(f"Creating molecule from SMILES: {smiles}")
            self.set_from_smiles(smiles)
        else:
            self._logger.debug("Creating empty molecule")

    @property
    def elements(self) -> Dict[AtomicElement, int]:
        """Get the elements composition of the molecule."""
        return self._elements.copy()
        
    @property
    def phase(self) -> Optional[str]:
        """
        Get the physical state/phase of the molecule.
        
        Returns:
            The phase as a string ('s', 'l', 'g', 'aq') or None if not set
            
        Examples:
            >>> from chemesty.molecules.molecule import Molecule
            >>> from chemesty.elements import H, O
            >>> 
            >>> # Create water molecule with liquid phase
            >>> water = Molecule(phase='l')
            >>> water.add_element(H(), 2)
            >>> water.add_element(O(), 1)
            >>> print(water.phase)
            l
            >>> 
            >>> # Change phase to gas
            >>> water.phase = 'g'
            >>> print(water.phase)
            g
        """
        return self._phase
        
    @phase.setter
    def phase(self, value: Optional[str]) -> None:
        """
        Set the physical state/phase of the molecule.
        
        Args:
            value: The phase as a string ('s', 'l', 'g', 'aq') or None
            
        Raises:
            ValueError: If value is not one of the valid phases
        """
        if value is not None and value not in ['s', 'l', 'g', 'aq']:
            self._logger.error(f"Invalid phase: {value}")
            raise ValueError(f"Phase must be one of: 's', 'l', 'g', 'aq', got {value}")
        self._logger.debug(f"Setting phase to {value}")
        self._phase = value
        
    @property
    def charge(self) -> int:
        """
        Get the ionic charge of the molecule.
        
        Returns:
            The charge value (positive for cations, negative for anions)
            
        Examples:
            >>> from chemesty.molecules.molecule import Molecule
            >>> from chemesty.elements import H, O
            >>> 
            >>> # Create hydroxide ion (OH⁻)
            >>> oh = O + H
            >>> oh.charge = -1
            >>> print(oh.charge)
            -1
        """
        return self._charge
        
    @charge.setter
    def charge(self, value: int) -> None:
        """
        Set the ionic charge of the molecule.
        
        Args:
            value: The charge value (positive for cations, negative for anions)
            
        Raises:
            TypeError: If value is not an integer
        """
        if not isinstance(value, int):
            raise TypeError(f"Charge must be an integer, got {type(value)}")
        self._charge = value

    def add_element(self, element: AtomicElement, quantity: int = 1) -> None:
        """Add an element to the molecule or increase its quantity if already present.

        Args:
            element: The AtomicElement instance to add to the molecule.
            quantity: The number of atoms of this element to add (default: 1).

        Raises:
            TypeError: If element is not an AtomicElement instance.
            ValueError: If quantity is not a positive integer.

        Examples:
            >>> from chemesty.elements import H, O, C
            >>> from chemesty.molecules.molecule import Molecule
            >>> 
            >>> # Create an empty molecule
            >>> mol = Molecule()
            >>> 
            >>> # Add hydrogen atoms
            >>> mol.add_element(H, 2)
            >>> 
            >>> # Add oxygen atom
            >>> mol.add_element(O, 1)
            >>> 
            >>> # Now we have water (H2O)
            >>> print(mol.molecular_formula)
            H2O
            >>> 
            >>> # Add more hydrogen (will increase existing count)
            >>> mol.add_element(H, 1)
            >>> print(mol.molecular_formula)
            H3O
            >>> 
            >>> # Add carbon atoms to make a more complex molecule
            >>> mol.add_element(C, 2)
            >>> print(mol.molecular_formula)
            C2H3O
            >>> 
            >>> # Add charged elements
            >>> from chemesty.elements import Fe
            >>> import copy
            >>> fe_plus2 = copy.deepcopy(Fe)
            >>> fe_plus2.charge = 2
            >>> mol = Molecule()
            >>> mol.add_element(fe_plus2, 1)
            >>> print(mol.molecular_formula)
            Fe²⁺
        """
        if not isinstance(element, AtomicElement):
            self._logger.error(f"Invalid element type: {type(element)}")
            raise TypeError(f"Expected AtomicElement instance, got {type(element)}")
        if not isinstance(quantity, int) or quantity <= 0:
            self._logger.error(f"Invalid quantity: {quantity}")
            raise ValueError(f"Element quantity must be a positive integer, got {quantity}")

        self._logger.debug(f"Adding {quantity} {element.symbol} atoms to molecule")
        
        # Check if we already have this element with the same charge
        element_found = False
        for existing_element in list(self._elements.keys()):
            if (existing_element.symbol == element.symbol and 
                getattr(existing_element, 'charge', 0) == getattr(element, 'charge', 0)):
                old_quantity = self._elements[existing_element]
                self._elements[existing_element] += quantity
                self._logger.debug(f"Updated {element.symbol} from {old_quantity} to {self._elements[existing_element]} atoms")
                element_found = True
                break
        
        # If we didn't find a matching element, add it as a new element
        if not element_found:
            import copy
            element_copy = copy.deepcopy(element)
            self._elements[element_copy] = quantity
            self._logger.debug(f"Added new element {element_copy.symbol} with {quantity} atoms")

        self._rdkit_mol = None  # Reset cached RDKit molecule

    def remove_element(self, element: AtomicElement, quantity: Optional[int] = None) -> None:
        """
        Remove an element from the molecule or decrease its quantity.

        Args:
            element: The AtomicElement to remove
            quantity: The quantity to remove (default: None, which removes all)

        Raises:
            ValueError: If the element is not in the molecule or if quantity is invalid
        """
        if element not in self._elements:
            raise ValueError(f"Element {element.symbol} is not in the molecule")

        if quantity is None:
            # Remove the element completely
            del self._elements[element]
        else:
            if not isinstance(quantity, int) or quantity <= 0:
                raise ValueError(f"Quantity must be a positive integer, got {quantity}")

            if self._elements[element] <= quantity:
                # Remove the element completely if quantity is greater than or equal to current
                del self._elements[element]
            else:
                # Decrease the quantity
                self._elements[element] -= quantity

        self._rdkit_mol = None  # Reset cached RDKit molecule

    def set_from_formula(self, formula: str) -> None:
        """Set the elements composition from a chemical formula string.
        
        Args:
            formula: Chemical formula string (e.g., "H2O", "C6H12O6")
            
        Raises:
            TypeError: If formula is not a string
            ValueError: If formula is empty or contains invalid elements
        """
        import re
        from chemesty.exceptions import InvalidFormulaError, ValidationError

        # Input validation
        if not isinstance(formula, str):
            raise TypeError(f"Formula must be a string, got {type(formula)}")
        
        if not formula or not formula.strip():
            raise ValidationError("Formula cannot be empty", parameter="formula", value=formula)

        # Clear current elements
        self._elements = OrderedDict()

        # Regular expression to match element symbols and their quantities
        pattern = r'([A-Z][a-z]*)(\d*)'
        matches = re.findall(pattern, formula)
        
        if not matches:
            raise InvalidFormulaError(formula, "No valid element symbols found")

        from chemesty.elements.element_factory import ElementFactory
        factory = ElementFactory()

        for symbol, quantity_str in matches:
            try:
                quantity = int(quantity_str) if quantity_str else 1
                if quantity <= 0:
                    raise InvalidFormulaError(formula, f"Invalid quantity {quantity} for element {symbol}")
            except ValueError as e:
                raise InvalidFormulaError(formula, f"Invalid quantity '{quantity_str}' for element {symbol}")
            
            try:
                element = factory.get_element(symbol)
                self.add_element(element, quantity)
            except ValueError:
                raise InvalidFormulaError(formula, f"Unknown element symbol: {symbol}")

        self._rdkit_mol = None  # Reset cached RDKit molecule

    def set_from_smiles(self, smiles: str) -> None:
        """Set the molecule from a SMILES string.
        
        Args:
            smiles: SMILES string representation of the molecule
            
        Raises:
            TypeError: If smiles is not a string
            InvalidSMILESError: If the SMILES string is invalid or empty
        """
        from chemesty.exceptions import InvalidSMILESError, ValidationError
        
        # Input validation
        if not isinstance(smiles, str):
            raise TypeError(f"SMILES must be a string, got {type(smiles)}")
        
        if not smiles or not smiles.strip():
            raise ValidationError("SMILES string cannot be empty", parameter="smiles", value=smiles)
        
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise InvalidSMILESError(smiles, "Failed to parse SMILES string")

        self._rdkit_mol = mol

        # Extract elements from the molecule
        self._elements = OrderedDict()

        from chemesty.elements.element_factory import ElementFactory
        factory = ElementFactory()

        for atom in mol.GetAtoms():
            symbol = atom.GetSymbol()
            try:
                element = factory.get_element(symbol)
                if element in self._elements:
                    self._elements[element] += 1
                else:
                    self._elements[element] = 1
            except ValueError:
                raise InvalidSMILESError(smiles, f"Unknown element symbol: {symbol}")

    @property
    def molecular_weight(self) -> float:
        """Calculate the molecular weight of the molecule in g/mol.

        Returns:
            The molecular weight as a float in grams per mole.

        Examples:
            >>> from chemesty.molecules.molecule import Molecule
            >>> 
            >>> # Water (H2O)
            >>> water = Molecule(formula="H2O")
            >>> print(f"Water MW: {water.molecular_weight:.2f} g/mol")
            Water MW: 18.02 g/mol
            >>> 
            >>> # Glucose (C6H12O6)
            >>> glucose = Molecule(formula="C6H12O6")
            >>> print(f"Glucose MW: {glucose.molecular_weight:.2f} g/mol")
            Glucose MW: 180.16 g/mol
            >>> 
            >>> # Caffeine (C8H10N4O2)
            >>> caffeine = Molecule(formula="C8H10N4O2")
            >>> print(f"Caffeine MW: {caffeine.molecular_weight:.2f} g/mol")
            Caffeine MW: 194.19 g/mol
        """
        if self._rdkit_mol is not None:
            return Descriptors.ExactMolWt(self._rdkit_mol)

        return sum(element.atomic_mass * quantity for element, quantity in self._elements.items())

    @property
    def molecular_formula(self) -> str:
        """
        Get the molecular formula of the compound, including charges if present.
        Numbers are displayed as subscripts. Sub-molecules are displayed with parentheses.
        
        Examples:
            >>> from chemesty.elements import H, O, Fe, Ba, N
            >>> from chemesty.molecules.molecule import Molecule
            >>> 
            >>> # Water (H₂O)
            >>> water = Molecule()
            >>> water.add_element(H(), 2)
            >>> water.add_element(O(), 1)
            >>> print(water.molecular_formula)
            H₂O
            >>> 
            >>> # Carbon dioxide (CO₂)
            >>> co2 = Molecule()
            >>> co2.add_element(C(), 1)
            >>> co2.add_element(O(), 2)
            >>> print(co2.molecular_formula)
            CO₂
            >>> 
            >>> # Iron(II) ion (Fe²⁺)
            >>> fe_plus2 = ++Fe()  # Fe²⁺
            >>> fe_mol = fe_plus2 * 1
            >>> print(fe_mol.molecular_formula)
            Fe²⁺
            >>> 
            >>> # Iron(III) ion (Fe³⁺)
            >>> fe_plus3 = +++Fe()  # Fe³⁺
            >>> fe_mol = fe_plus3 * 1
            >>> print(fe_mol.molecular_formula)
            Fe³⁺
            >>>
            >>> # Barium hydroxide (Ba(OH)₂)
            >>> oh = O + H
            >>> ba_oh_2 = Molecule()
            >>> ba_oh_2 = ba_oh_2 + Ba
            >>> ba_oh_2 = ba_oh_2.add_sub_molecule(oh, 2)
            >>> print(ba_oh_2.molecular_formula)
            Ba(OH)₂
            >>>
            >>> # Iron(III) nitrate (Fe(NO₃)₃)
            >>> no3 = N + O*3
            >>> fe_no3_3 = Molecule()
            >>> fe_no3_3 = fe_no3_3 + Fe
            >>> fe_no3_3 = fe_no3_3.add_sub_molecule(no3, 3)
            >>> print(fe_no3_3.molecular_formula)
            Fe(NO₃)₃
        """
        # Subscript digits mapping
        subscript_digits = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
        }
        
        # Superscript digits mapping
        superscript_digits = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
        }
        
        # If there are no sub-molecules, use the original formula generation
        if not self._sub_molecules:
            if not self._elements:
                return ""

            # Sort elements by Hill system (C, H, then alphabetically)
            sorted_elements = sorted(
                self._elements.items(),
                key=lambda x: (
                    x[0].symbol != "C",  # C first
                    x[0].symbol != "H" if x[0].symbol != "C" else False,  # H second
                    x[0].symbol  # Rest alphabetically
                )
            )

            # Build the molecular formula
            formula = ""
            
            for element, quantity in sorted_elements:
                # Create a copy of the element with charge set to 0 to avoid duplicate charge display
                import copy
                element_copy = copy.deepcopy(element)
                if hasattr(element_copy, 'charge'):
                    element_copy.charge = 0
                
                # Use the element symbol without any charge
                formula += element_copy.symbol
                if quantity > 1:
                    # Convert quantity to subscript
                    quantity_str = str(quantity)
                    subscript_quantity = ''.join(subscript_digits[digit] for digit in quantity_str)
                    formula += subscript_quantity
        else:
            # Handle molecules with sub-molecules
            import copy
            
            # Special case: if there's only one submolecule and it contains all elements
            # This handles cases like Fe + (N + O * 3) * 3 which should be displayed as Fe(NO₃)₃
            if len(self._sub_molecules) == 1:
                sub_mol, multiplier = self._sub_molecules[0]
                total_sub_elements = sum(count * multiplier for element, count in sub_mol._elements.items())
                
                # Check if this submolecule contains all elements except one (the main element)
                # This is a common pattern for compounds like Fe(NO₃)₃
                if len(self._elements) - total_sub_elements <= 1:
                    # Find the main element (the one not in the submolecule)
                    main_elements = []
                    for element, count in self._elements.items():
                        found = False
                        for sub_element, sub_count in sub_mol._elements.items():
                            if element.symbol == sub_element.symbol:
                                found = True
                                break
                        if not found:
                            main_elements.append((element, count))
                    
                    # Build the formula with the main element first, then the submolecule
                    formula = ""
                    for element, quantity in main_elements:
                        element_copy = copy.deepcopy(element)
                        if hasattr(element_copy, 'charge'):
                            element_copy.charge = 0
                        formula += element_copy.symbol
                        if quantity > 1:
                            quantity_str = str(quantity)
                            subscript_quantity = ''.join(subscript_digits[digit] for digit in quantity_str)
                            formula += subscript_quantity
                    
                    # Add the submolecule with parentheses
                    formula += "(" + sub_mol.molecular_formula + ")"
                    
                    # Add the multiplier as a subscript if it's greater than 1
                    if multiplier > 1:
                        multiplier_str = str(multiplier)
                        subscript_multiplier = ''.join(subscript_digits[digit] for digit in multiplier_str)
                        formula += subscript_multiplier
                    
                    # Return early since we've handled this special case
                    return formula
            
            # Standard case: calculate remaining elements
            remaining_elements = copy.deepcopy(self._elements)
            
            for sub_mol, multiplier in self._sub_molecules:
                for element, count in sub_mol._elements.items():
                    # Find the element in remaining_elements
                    for rem_element in list(remaining_elements.keys()):
                        if rem_element.symbol == element.symbol:
                            # Subtract the count from remaining_elements
                            remaining_elements[rem_element] -= count * multiplier
                            # If the count is 0 or negative, remove the element
                            if remaining_elements[rem_element] <= 0:
                                del remaining_elements[rem_element]
                            break
            
            # Sort remaining elements by Hill system
            sorted_elements = sorted(
                remaining_elements.items(),
                key=lambda x: (
                    x[0].symbol != "C",  # C first
                    x[0].symbol != "H" if x[0].symbol != "C" else False,  # H second
                    x[0].symbol  # Rest alphabetically
                )
            )
            
            # Build the formula with remaining elements first
            formula = ""
            for element, quantity in sorted_elements:
                # Create a copy of the element with charge set to 0 to avoid duplicate charge display
                element_copy = copy.deepcopy(element)
                if hasattr(element_copy, 'charge'):
                    element_copy.charge = 0
                
                # Use the element symbol without any charge
                formula += element_copy.symbol
                if quantity > 1:
                    # Convert quantity to subscript
                    quantity_str = str(quantity)
                    subscript_quantity = ''.join(subscript_digits[digit] for digit in quantity_str)
                    formula += subscript_quantity
            
            # Then add sub-molecules with parentheses
            for sub_mol, multiplier in self._sub_molecules:
                # Add the sub-molecule formula in parentheses
                formula += "(" + sub_mol.molecular_formula + ")"
                
                # Add the multiplier as a subscript if it's greater than 1
                if multiplier > 1:
                    multiplier_str = str(multiplier)
                    subscript_multiplier = ''.join(subscript_digits[digit] for digit in multiplier_str)
                    formula += subscript_multiplier
        
        # Add charge to the formula if there is one
        if self._charge != 0:
            # Convert charge to superscript
            charge_str = ""
            if abs(self._charge) > 1:
                # Use superscript numbers for magnitude
                magnitude = str(abs(self._charge))
                charge_str = ''.join(superscript_digits[digit] for digit in magnitude)
            
            # Add superscript plus or minus
            if self._charge > 0:
                charge_str += '⁺'
            else:
                charge_str += '⁻'
            
            formula += charge_str
        
        return formula

    @property
    def formula(self) -> str:
        """
        Get the molecular formula of the compound.
        
        This is an alias for molecular_formula for backward compatibility
        and convenience in web applications.
        """
        return self.molecular_formula

    @property
    def empirical_formula(self) -> str:
        """
        Get the empirical formula of the compound.
        """
        if not self._elements:
            return ""

        # Find the greatest common divisor of all quantities
        from math import gcd
        from functools import reduce

        quantities = list(self._elements.values())
        if len(quantities) == 1:
            divisor = quantities[0]
        else:
            divisor = reduce(gcd, quantities)

        # Sort elements by Hill system (C, H, then alphabetically)
        sorted_elements = sorted(
            self._elements.items(),
            key=lambda x: (
                x[0].symbol != "C",  # C first
                x[0].symbol != "H" if x[0].symbol != "C" else False,  # H second
                x[0].symbol  # Rest alphabetically
            )
        )

        # Build the empirical formula
        formula = ""
        for element, quantity in sorted_elements:
            formula += element.symbol
            reduced_quantity = quantity // divisor
            if reduced_quantity > 1:
                formula += str(reduced_quantity)

        return formula

    @property
    def volume_value(self) -> Optional[float]:
        """Estimate the raw molecular volume value in cubic angstroms (Å³)."""
        if self._rdkit_mol is not None:
            # Use RDKit to calculate 3D coordinates and volume
            try:
                mol = Chem.AddHs(self._rdkit_mol)
                AllChem.EmbedMolecule(mol)
                AllChem.MMFFOptimizeMolecule(mol)

                # Calculate volume from 3D coordinates
                conformer = mol.GetConformer()
                positions = [conformer.GetAtomPosition(i) for i in range(mol.GetNumAtoms())]

                # Calculate bounding box volume as a rough estimate
                x_coords = [pos.x for pos in positions]
                y_coords = [pos.y for pos in positions]
                z_coords = [pos.z for pos in positions]

                volume = (max(x_coords) - min(x_coords)) * \
                         (max(y_coords) - min(y_coords)) * \
                         (max(z_coords) - min(z_coords))

                return volume
            except Exception:
                # Fall back to additive method if 3D embedding fails
                pass

        # Fallback to additive method
        packing_factor = 0.74
        total_volume = 0.0

        for element, quantity in self._elements.items():
            element_volume = element.volume_value
            if element_volume is None:
                return None

            total_volume += element_volume * quantity

        return total_volume * packing_factor

    @property
    def volume(self):
        """Molecular volume with units (Å³)."""
        if self.volume_value is None:
            return None
        return self.volume_value * cubic(angstrom)

    @property
    def density_value(self) -> Optional[float]:
        """Calculate the raw density value of the compound in g/cm³."""
        volume = self.volume_value
        if volume is None:
            return None

        # Convert molecular weight from amu to grams
        mass_in_g = self.molecular_weight * 1.66053886e-24

        # Convert volume from Å³ to cm³
        volume_in_cm3 = volume * 1e-24

        # Calculate density
        return mass_in_g / volume_in_cm3

    @property
    def density(self):
        """Density with units (g/cm³)."""
        if self.density_value is None:
            return None
        return self.density_value * gram / cubic(centimeter)

    @property
    def molar_volume(self) -> Optional[float]:
        """
        Calculate the molar volume in cm³/mol.

        Returns:
            The molar volume, or None if density is None
        """
        if self.density_value is None:
            return None

        # Molar volume = Molar mass / Density
        return self.molecular_weight / self.density_value

    @property
    def element_count(self) -> int:
        """
        Get the number of unique elements in the compound.

        Returns:
            The number of unique elements
        """
        return len(self._elements)

    @property
    def atom_count(self) -> int:
        """
        Get the total number of atoms in the compound.

        Returns:
            The total number of atoms
        """
        return sum(self._elements.values())

    def __mul__(self, other: int) -> 'Molecule':
        """
        Multiply a molecule by a number.

        Example: (H + O) * 2 creates a molecule with 2 hydrogen and 2 oxygen atoms
        Example: (N + O*3) * 3 creates a molecule with a submolecule (NO₃) repeated 3 times
        """
        if not isinstance(other, int) or other <= 0:
            raise ValueError("Can only multiply molecules by positive integers")

        result = Molecule()
        
        # Copy elements with multiplied counts
        for element, count in self._elements.items():
            result.add_element(element, count * other)
            
        # Copy submolecules with multiplied counts if this molecule has submolecules
        import copy
        if self._sub_molecules:
            # If the original molecule has submolecules, preserve them in the result
            for sub_mol, multiplier in self._sub_molecules:
                result._sub_molecules.append((copy.deepcopy(sub_mol), multiplier * other))
        else:
            # If the original molecule doesn't have submolecules, add itself as a submolecule
            # This preserves the grouping information when multiplying a molecule
            result._sub_molecules.append((copy.deepcopy(self), other))
        
        # Copy the phase from this molecule
        if hasattr(self, '_phase') and self._phase is not None:
            result.phase = self._phase
            
        return result

    def __rmul__(self, other: int) -> 'ReactionComponent':
        """
        Support for multiplication from the left (e.g., 2 * (H + O)).
        
        When multiplying a molecule from the left (e.g., 2 * molecule),
        this creates a ReactionComponent with the specified coefficient,
        rather than a Molecule with multiplied elements.
        
        Args:
            other: The coefficient (must be a positive integer)
            
        Returns:
            A ReactionComponent with this molecule and the specified coefficient
            
        Examples:
            >>> from chemesty.elements import H, O
            >>> water = H*2 + O
            >>> # Create a reaction component with coefficient 2
            >>> water_component = 2 * water  # 2 H₂O
        """
        if not isinstance(other, int) or other <= 0:
            raise ValueError("Can only multiply molecules by positive integers")
            
        # Import here to avoid circular imports
        from chemesty.reactions.reaction import ReactionComponent
        
        # Create a deep copy of this molecule to prevent unintended modifications
        import copy
        molecule_copy = copy.deepcopy(self)
        
        # Create a ReactionComponent with the specified coefficient and phase
        phase = self.phase if hasattr(self, 'phase') else None
        return ReactionComponent(molecule=molecule_copy, coefficient=other, phase=phase)

    def add_sub_molecule(self, molecule: 'Molecule', multiplier: int = 1) -> 'Molecule':
        """
        Add a sub-molecule to this molecule.
        
        Args:
            molecule: The molecule to add as a sub-molecule
            multiplier: The number of times to repeat the sub-molecule
            
        Returns:
            Self for method chaining
            
        Examples:
            >>> from chemesty.elements import Ba, O, H
            >>> oh = O + H
            >>> ba_oh_2 = Molecule()
            >>> ba_oh_2 = ba_oh_2 + Ba
            >>> ba_oh_2 = ba_oh_2.add_sub_molecule(oh, 2)
            >>> print(ba_oh_2)
            Ba(OH)₂
        """
        import copy
        self._sub_molecules.append((copy.deepcopy(molecule), multiplier))
        
        # Also add the elements for compatibility with existing code
        for element, count in molecule._elements.items():
            element_copy = copy.deepcopy(element)
            self.add_element(element_copy, count * multiplier)
        
        return self
        
    def add_sub_molecule_preserve(self, molecule: 'Molecule', multiplier: int = 1) -> 'Molecule':
        """
        Add a sub-molecule to this molecule without adding its elements to the main molecule's elements.
        This preserves the submolecule structure for display purposes.
        
        Args:
            molecule: The molecule to add as a sub-molecule
            multiplier: The number of times to repeat the sub-molecule
            
        Returns:
            Self for method chaining
            
        Examples:
            >>> from chemesty.elements import Fe, N, O
            >>> no3 = N + O * 3
            >>> fe_no3_3 = Molecule()
            >>> fe_no3_3 = fe_no3_3 + Fe
            >>> fe_no3_3 = fe_no3_3.add_sub_molecule_preserve(no3, 3)
            >>> print(fe_no3_3)
            Fe(NO₃)₃
        """
        import copy
        self._sub_molecules.append((copy.deepcopy(molecule), multiplier))
        
        # Don't add the elements to the main molecule's elements
        # This preserves the submolecule structure for display purposes
        
        return self
    
    def group(self, multiplier: int) -> tuple:
        """
        Group a molecule for use in complex formulas.
        
        Example: (N + O*3).group(3) creates (NO₃)₃
        
        Args:
            multiplier: The number of times to repeat the group
            
        Returns:
            A tuple (self, multiplier) for use with __add__
            
        Examples:
            >>> from chemesty.elements import N, O, Fe
            >>> nitrate = N + O*3
            >>> iron_nitrate = Fe + nitrate.group(3)
            >>> print(iron_nitrate)
            Fe(NO₃)₃
        """
        # Create a deep copy of this molecule to prevent unintended modifications
        import copy
        molecule_copy = copy.deepcopy(self)
        
        return (molecule_copy, multiplier)
        
    def __add__(self, other: Union[AtomicElement, 'Molecule', tuple]) -> 'Molecule':
        """
        Add elements or molecules to create a new molecule.

        Example: (H * 2) + O creates a molecule with 2 hydrogen and 1 oxygen atom
        Example: Fe + (N + O*3).group(3) creates Fe(NO₃)₃
        
        Args:
            other: An AtomicElement, Molecule, or a tuple (molecule, multiplier)
            
        Returns:
            A new Molecule instance
        """
        result = Molecule()

        # Add all elements from this molecule
        for element, count in self._elements.items():
            import copy
            element_copy = copy.deepcopy(element)
            result.add_element(element_copy, count)
            
        # Copy the sub-molecules from this molecule
        import copy
        result._sub_molecules = copy.deepcopy(self._sub_molecules)
            
        # Copy the charge from this molecule
        result.charge = self.charge
        
        # Copy the phase from this molecule
        if hasattr(self, '_phase') and self._phase is not None:
            result.phase = self._phase

        # Handle different types of additions
        if isinstance(other, AtomicElement):
            import copy
            other_copy = copy.deepcopy(other)
            result.add_element(other_copy, 1)
        elif isinstance(other, type) and isinstance(other, ElementMeta):
            # Handle element class (e.g., Fe, O) by instantiating it
            import copy
            instance = other()  # Create an instance of the element class
            other_copy = copy.deepcopy(instance)
            result.add_element(other_copy, 1)
        elif isinstance(other, Molecule):
            # Check if the other molecule has submolecules or is the result of a multiplication
            if other._sub_molecules:
                # If the other molecule has submolecules, add them directly to the result
                # This handles cases like Fe + (N + O * 3) * 3
                import copy
                
                # Add the submolecules from the other molecule to the result
                # This preserves the submolecule structure without adding an extra layer of parentheses
                for sub_mol, multiplier in other._sub_molecules:
                    result._sub_molecules.append((copy.deepcopy(sub_mol), multiplier))
                
                # Add the charge from the other molecule
                result.charge += other.charge
            else:
                # Otherwise, add elements and charge as before
                for element, count in other._elements.items():
                    import copy
                    element_copy = copy.deepcopy(element)
                    result.add_element(element_copy, count)
                
                # Add the charge from the other molecule
                result.charge += other.charge
        elif isinstance(other, tuple) and len(other) == 2:
            # Handle (molecule, multiplier) format for complex formulas
            mol, multiplier = other
            if isinstance(mol, Molecule) and isinstance(multiplier, int):
                # Create a deep copy of the molecule to prevent unintended modifications
                import copy
                mol_copy = copy.deepcopy(mol)
                
                # Use add_sub_molecule_preserve to properly handle sub-molecules
                # This preserves the submolecule structure for display purposes
                result = result.add_sub_molecule_preserve(mol_copy, multiplier)
                
                # Add the charge from the other molecule, multiplied by the multiplier
                result.charge += mol.charge * multiplier
            else:
                raise TypeError(f"Tuple must be (Molecule, int), got ({type(mol)}, {type(multiplier)})")
        else:
            raise TypeError(f"Cannot add {type(other)} to a molecule")

        return result

    def __and__(self, other: Union['Molecule', tuple, ReactionSide, 'Reaction']) -> Union[ReactionSide, 'Reaction']:
        """
        Combine molecules for chemical reactions using & operator.
        
        This operator is used to combine reactants or products on one side
        of a chemical equation. Unlike +, which combines atoms into a single
        molecule, & keeps molecules separate for stoichiometric purposes.
        
        If the other operand is a Reaction, this molecule is added to the reactants.
        
        Args:
            other: Another molecule, (coefficient, molecule) tuple, ReactionSide, or Reaction
            
        Returns:
            ReactionSide containing this molecule and the other component(s),
            or Reaction with this molecule added to reactants
            
        Example:
            >>> methane = Molecule("CH4")
            >>> oxygen = Molecule("O2")
            >>> reactants = methane & (2, oxygen)  # CH4 & 2O2
        """
        # Import here to avoid circular imports
        from chemesty.reactions.reaction import Reaction
        import copy
        
        # If other is a Reaction, add this molecule to its reactants
        if isinstance(other, Reaction):
            result = other
            # Create a deep copy of this molecule
            self_copy = copy.deepcopy(self)
            result.add_reactant(self_copy, 1.0)
            return result
            
        # Start with this molecule - pass as (coeff, mol) tuple to ReactionSide
        # Create a deep copy of this molecule
        self_copy = copy.deepcopy(self)
        components = [(1.0, self_copy)]
        
        if isinstance(other, tuple) and len(other) == 2:
            coeff, mol = other
            if isinstance(mol, Molecule):
                # Create a deep copy of the other molecule
                mol_copy = copy.deepcopy(mol)
                components.append((coeff, mol_copy))
            else:
                raise TypeError(f"Tuple must contain (coefficient, Molecule), got {type(mol)}")
        elif isinstance(other, Molecule):
            # Create a deep copy of the other molecule
            other_copy = copy.deepcopy(other)
            components.append((1.0, other_copy))
        elif isinstance(other, ReactionSide):
            # ReactionSide stores components as (mol, coeff), so we need to convert
            for mol, coeff in other.components:
                # Create a deep copy of each molecule
                mol_copy = copy.deepcopy(mol)
                components.append((coeff, mol_copy))
        else:
            raise TypeError(f"Cannot combine Molecule with {type(other)} using &")
        
        return ReactionSide(components)

    def __rshift__(self, other: Union['Molecule', tuple, ReactionSide]) -> 'Reaction':
        """
        Create a chemical reaction using >> operator.
        
        This operator creates a reaction with this molecule as a reactant
        and the other component(s) as product(s).
        
        Args:
            other: Products (Molecule, tuple, or ReactionSide)
            
        Returns:
            Reaction object
            
        Example:
            >>> methane = Molecule("CH4")
            >>> co2 = Molecule("CO2")
            >>> water = Molecule("H2O")
            >>> reaction = methane >> (co2 & (2, water))  # CH4 >> CO2 & 2H2O
        """
        # Import here to avoid circular imports
        from chemesty.reactions.reaction import Reaction
        import copy
        
        # Create a deep copy of this molecule for the reactant side
        self_copy = copy.deepcopy(self)
        reactants = ReactionSide([self_copy])
        
        # Handle products
        if isinstance(other, ReactionSide):
            # Create deep copies of all molecules in the ReactionSide
            products_components = []
            for mol, coeff in other.components:
                mol_copy = copy.deepcopy(mol)
                products_components.append((mol_copy, coeff))
            products = ReactionSide(products_components)
        elif isinstance(other, tuple) and len(other) == 2:
            coeff, mol = other
            mol_copy = copy.deepcopy(mol)
            products = ReactionSide([(coeff, mol_copy)])
        elif isinstance(other, Molecule):
            other_copy = copy.deepcopy(other)
            products = ReactionSide([other_copy])
        else:
            raise TypeError(f"Cannot create reaction with products of type {type(other)}")
        
        # Create reaction
        reaction = Reaction()
        
        # Add reactants
        for mol, coeff in reactants.components:
            # Pass the molecule's phase to the add_reactant method
            reaction.add_reactant(mol, coeff, phase=mol.phase if hasattr(mol, 'phase') else None)
        
        # Add products
        for mol, coeff in products.components:
            # Pass the molecule's phase to the add_product method
            reaction.add_product(mol, coeff, phase=mol.phase if hasattr(mol, 'phase') else None)
        
        return reaction

    def __matmul__(self, state):
        """
        Set the physical state using the @ operator.
        
        Example: H2O @ 'l' creates H2O(l)
        
        Args:
            state: The state to apply ('s', 'l', 'g', 'aq')
            
        Returns:
            The molecule with the state applied
            
        Examples:
            >>> from chemesty.elements import H, O
            >>> water = H*2 + O
            >>> water_liquid = water @ 'l'
            >>> print(water_liquid)
            H₂O(l)
        """
        import copy
        if not isinstance(state, str) or state not in ['s', 'l', 'g', 'aq']:
            raise ValueError(f"Invalid state: {state}. Must be one of: 's', 'l', 'g', 'aq'")
        
        result = copy.deepcopy(self)
        result.phase = state
        return result
        
    def __pos__(self):
        """
        Increment charge by 1 (e.g., +molecule means molecule¹⁺, ++molecule means molecule²⁺).
        
        Returns:
            A copy of this molecule with charge increased by 1
            
        Examples:
            >>> from chemesty.elements import H, O
            >>> 
            >>> # Create hydroxide
            >>> oh = O + H
            >>> 
            >>> # Create hydroxide with +1 charge (OH⁺)
            >>> oh_plus = +oh
            >>> print(oh_plus.charge)
            1
        """
        import copy
        result = copy.deepcopy(self)
        result.charge += 1
        return result
        
    def __neg__(self):
        """
        Decrement charge by 1 (e.g., -molecule means molecule¹⁻, --molecule means molecule²⁻).
        
        Returns:
            A copy of this molecule with charge decreased by 1
            
        Examples:
            >>> from chemesty.elements import H, O
            >>> 
            >>> # Create hydroxide
            >>> oh = O + H
            >>> 
            >>> # Create hydroxide with -1 charge (OH⁻)
            >>> oh_minus = -oh
            >>> print(oh_minus.charge)
            -1
        """
        import copy
        result = copy.deepcopy(self)
        result.charge -= 1
        return result
        
    def apply(self, charge: int):
        """
        Apply a specific charge to the molecule, creating a new copy.
        
        This method provides a way to create charged molecular ions like OH⁻.
        For complex molecules, the charge distribution among atoms depends on
        the specific chemical structure and would require more sophisticated
        modeling. This method simply sets the overall charge on the molecule.
        
        Args:
            charge: The charge value to apply (positive for cations, negative for anions)
            
        Returns:
            A copy of this molecule with the specified charge
            
        Examples:
            >>> from chemesty.elements import H, O
            >>> 
            >>> # Create hydroxide ion (OH⁻)
            >>> oh = O + H
            >>> oh_minus = oh.apply(-1)
            >>> 
            >>> # Create hydronium ion (H₃O⁺)
            >>> h3o = O + H*3
            >>> h3o_plus = h3o.apply(1)
        """
        import copy
        result = copy.deepcopy(self)
        result.charge = charge
        return result
        
    def __str__(self) -> str:
        """
        String representation of the molecule with charge and phase if present.
        
        Examples:
            >>> from chemesty.molecules.molecule import Molecule
            >>> from chemesty.elements import H, O, Na, Cl
            >>> 
            >>> # Water in liquid phase
            >>> water = Molecule(phase='l')
            >>> water.add_element(H(), 2)
            >>> water.add_element(O(), 1)
            >>> print(water)
            H₂O(l)
            >>> 
            >>> # Sodium chloride in aqueous solution
            >>> nacl = Molecule(phase='aq')
            >>> nacl.add_element(Na(), 1)
            >>> nacl.add_element(Cl(), 1)
            >>> print(nacl)
            NaCl(aq)
            >>> 
            >>> # Hydroxide ion in aqueous solution
            >>> oh = (O + H).apply(-1)
            >>> oh_aq = oh @ 'aq'
            >>> print(oh_aq)
            OH⁻(aq)
        """
        formula = self.molecular_formula
        
        # Add phase if present
        if self._phase:
            return f"{formula}({self._phase})"
        
        return formula

    def __repr__(self) -> str:
        """Detailed representation of the molecule."""
        return f"Molecule({self.molecular_formula})"

    # Advanced molecular analysis methods for complex molecules
    
    def get_stereochemistry_info(self) -> Optional[Dict[str, Any]]:
        """
        Get stereochemistry information for the molecule.
        
        Returns:
            Dictionary containing stereochemistry information or None if not available
        """
        if self._rdkit_mol is None:
            return None
            
        try:
            stereo_info = {
                'chiral_centers': [],
                'double_bond_stereo': [],
                'has_stereochemistry': False
            }
            
            # Find chiral centers
            chiral_centers = Chem.FindMolChiralCenters(self._rdkit_mol, includeUnassigned=True)
            for center in chiral_centers:
                stereo_info['chiral_centers'].append({
                    'atom_idx': center[0],
                    'chirality': center[1]
                })
            
            # Check for double bond stereochemistry
            for bond in self._rdkit_mol.GetBonds():
                if bond.GetBondType() == Chem.BondType.DOUBLE:
                    stereo = bond.GetStereo()
                    if stereo != Chem.BondStereo.STEREONONE:
                        stereo_info['double_bond_stereo'].append({
                            'bond_idx': bond.GetIdx(),
                            'stereo': str(stereo)
                        })
            
            stereo_info['has_stereochemistry'] = (
                len(stereo_info['chiral_centers']) > 0 or 
                len(stereo_info['double_bond_stereo']) > 0
            )
            
            return stereo_info
            
        except Exception as e:
            self._logger.warning(f"Could not determine stereochemistry: {e}")
            return None
    
    def generate_conformers(self, num_conformers: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        Generate multiple conformers for the molecule.
        
        Args:
            num_conformers: Number of conformers to generate
            
        Returns:
            List of conformer information dictionaries or None if not available
        """
        if self._rdkit_mol is None:
            return None
            
        try:
            mol = Chem.AddHs(self._rdkit_mol)
            
            # Generate conformers
            conformer_ids = AllChem.EmbedMultipleConfs(
                mol, 
                numConfs=num_conformers,
                randomSeed=42
            )
            
            # Optimize conformers
            for conf_id in conformer_ids:
                AllChem.MMFFOptimizeMolecule(mol, confId=conf_id)
            
            conformers = []
            for conf_id in conformer_ids:
                conformer = mol.GetConformer(conf_id)
                
                # Calculate energy (if possible)
                try:
                    energy = AllChem.MMFFGetMoleculeForceField(mol, confId=conf_id).CalcEnergy()
                except:
                    energy = None
                
                # Get coordinates
                positions = []
                for i in range(mol.GetNumAtoms()):
                    pos = conformer.GetAtomPosition(i)
                    positions.append([pos.x, pos.y, pos.z])
                
                conformers.append({
                    'id': conf_id,
                    'energy': energy,
                    'positions': positions
                })
            
            # Sort by energy if available
            if all(conf['energy'] is not None for conf in conformers):
                conformers.sort(key=lambda x: x['energy'])
            
            return conformers
            
        except Exception as e:
            self._logger.warning(f"Could not generate conformers: {e}")
            return None
    
    def get_molecular_descriptors(self) -> Dict[str, Any]:
        """
        Calculate various molecular descriptors for complex analysis.
        
        Returns:
            Dictionary containing molecular descriptors
        """
        descriptors = {
            'basic': {
                'molecular_weight': self.molecular_weight,
                'atom_count': self.atom_count(),
                'element_count': self.element_count(),
                'molecular_formula': self.molecular_formula(),
                'empirical_formula': self.empirical_formula()
            }
        }
        
        if self._rdkit_mol is not None:
            try:
                from rdkit.Chem import Descriptors, Crippen, Lipinski
                
                # Physicochemical descriptors
                descriptors['physicochemical'] = {
                    'logp': Crippen.MolLogP(self._rdkit_mol),
                    'tpsa': Descriptors.TPSA(self._rdkit_mol),
                    'hbd': Descriptors.NumHDonors(self._rdkit_mol),
                    'hba': Descriptors.NumHAcceptors(self._rdkit_mol),
                    'rotatable_bonds': Descriptors.NumRotatableBonds(self._rdkit_mol),
                    'aromatic_rings': Descriptors.NumAromaticRings(self._rdkit_mol),
                    'saturated_rings': Descriptors.NumSaturatedRings(self._rdkit_mol)
                }
                
                # Lipinski's Rule of Five
                descriptors['drug_likeness'] = {
                    'lipinski_violations': Lipinski.NumLipinskiViolations(self._rdkit_mol),
                    'mw_ok': descriptors['basic']['molecular_weight'] <= 500,
                    'logp_ok': abs(descriptors['physicochemical']['logp']) <= 5,
                    'hbd_ok': descriptors['physicochemical']['hbd'] <= 5,
                    'hba_ok': descriptors['physicochemical']['hba'] <= 10
                }
                
                # Structural descriptors
                descriptors['structural'] = {
                    'rings': Descriptors.RingCount(self._rdkit_mol),
                    'heavy_atoms': Descriptors.HeavyAtomCount(self._rdkit_mol),
                    'formal_charge': Chem.GetFormalCharge(self._rdkit_mol),
                    'radical_electrons': Descriptors.NumRadicalElectrons(self._rdkit_mol)
                }
                
            except Exception as e:
                self._logger.warning(f"Could not calculate RDKit descriptors: {e}")
        
        return descriptors
