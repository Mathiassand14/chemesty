from abc import ABC, ABCMeta, abstractmethod
from typing import Optional, List, Dict, Union
import math
import numbers
from sympy.physics.units import meter, kilogram, gram, centimeter, angstrom
from sympy import pi


class ElementMeta(ABCMeta):
    """Make the *class object* act like a neutral atom."""
    def __pos__(cls):
        return +cls()          # neutral instance → +1
    
    def __neg__(cls):
        return -cls()          # neutral instance → –1
    
    # Optional: forward other operations to instance methods
    def __mul__(cls, other):
        return cls() * other
    
    def __add__(cls, other):
        return cls() + other
    
    def __radd__(cls, other):
        """Handle cases where the class is on the right side of addition (e.g., molecule + Fe)"""
        # Create an instance and delegate to its __radd__ method
        return other + cls()
    
    def __rmul__(cls, other):
        """Handle cases where the class is on the right side of multiplication (e.g., 2 * Fe)"""
        # Create an instance and delegate to its __rmul__ method
        return other * cls()
    
    # Special case for charge property to ensure it's always 0 at the class level
    def __getattribute__(cls, name):
        if name == 'charge':
            return 0
        return super().__getattribute__(name)

# Define functions that are not available in the installed version of sympy
def cubic(unit):
    """Return the cube of a unit."""
    return unit**3

def density(mass_unit, volume_unit):
    """Return a density unit (mass/volume)."""
    return mass_unit / volume_unit

def volume(unit):
    """Return a volume unit."""
    return cubic(unit)

class ClassInstanceProperty:
    """
    A descriptor that works as both a class property and an instance property.
    This allows properties to be accessed both from the class (Element.name) and
    from instances (Element().name).
    """
    def __init__(self, fget):
        self.fget = fget
        self.__doc__ = fget.__doc__
        self._cache = {}  # Cache for class property values

    def __get__(self, instance, owner):
        if instance is None:
            # Access from class, use cached value if available
            if owner not in self._cache:
                # Create a temporary instance to get the property value
                temp_instance = owner()
                self._cache[owner] = self.fget(temp_instance)
            return self._cache[owner]
        return self.fget(instance)

def class_property(func):
    """Decorator to create a ClassInstanceProperty."""
    return ClassInstanceProperty(func)

def abstract_class_property(func):
    """Decorator that combines abstractmethod and ClassInstanceProperty."""
    return abstractmethod(ClassInstanceProperty(func))


class AtomicElement(ABC, metaclass=ElementMeta):
    """
    Abstract base class representing a chemical element from the periodic table.
    All properties are read-only except for charge.
    """
    
    def __init__(self):
        """Initialize the element with a default charge of 0 (neutral)."""
        self._charge = 0
        
    @property
    def charge(self) -> int:
        """Get the ionic charge of the element."""
        return self._charge
        
    @charge.setter
    def charge(self, value: int) -> None:
        """
        Set the ionic charge of the element.
        
        Args:
            value: The charge value (positive for cations, negative for anions)
            
        Raises:
            TypeError: If value is not an integer
        """
        if not isinstance(value, int):
            raise TypeError(f"Charge must be an integer, got {type(value)}")
        self._charge = value
        
    def __pos__(self):
        """
        Increment charge by 1 (e.g., +O means O¹⁺, ++O means O²⁺).
        
        Returns:
            A molecule containing this element with charge increased by 1
        """
        from chemesty.molecules.molecule import Molecule
        
        # Create a molecule with this element
        mol = Molecule()
        mol.add_element(self, 1)
        
        # Increment the charge on the molecule
        mol.charge += 1
        
        return mol
        
    def __neg__(self):
        """
        Decrement charge by 1 (e.g., -O means O¹⁻, --O means O²⁻).
        
        Returns:
            A molecule containing this element with charge decreased by 1
        """
        from chemesty.molecules.molecule import Molecule
        
        # Create a molecule with this element
        mol = Molecule()
        mol.add_element(self, 1)
        
        # Decrement the charge on the molecule
        mol.charge -= 1
        
        return mol
        
    def apply(self, charge: int):
        """
        Apply a specific charge to create a molecule containing this element.
        
        This method provides a more explicit and reliable way to set charges
        compared to using operator chaining (++Fe) which doesn't work as expected
        due to how Python evaluates unary operators.
        
        Args:
            charge: The charge value to apply (positive for cations, negative for anions)
            
        Returns:
            A molecule containing this element with the specified charge
            
        Examples:
            >>> from chemesty.elements import Fe, Ce
            >>> 
            >>> # Create iron with +2 charge
            >>> fe_plus2 = Fe.apply(2)
            >>> print(fe_plus2)
            Fe²⁺
            >>> 
            >>> # Create cerium with +4 charge
            >>> ce_plus4 = Ce.apply(4)
            >>> print(ce_plus4)
            Ce⁴⁺
            >>> 
            >>> # Create iron with -3 charge (unusual but possible)
            >>> fe_minus3 = Fe.apply(-3)
            >>> print(fe_minus3)
            Fe³⁻
        """
        from chemesty.molecules.molecule import Molecule
        
        # Create a molecule with this element
        mol = Molecule()
        mol.add_element(self, 1)
        
        # Set the charge on the molecule
        mol.charge = charge
        
        return mol

    @abstract_class_property
    def atomic_number(self) -> int:
        """The atomic number (Z) of the element."""
        pass

    @abstract_class_property
    def symbol(self) -> str:
        """The chemical symbol of the element (e.g., 'H', 'He', 'Li')."""
        pass

    @abstract_class_property
    def name(self) -> str:
        """The full name of the element (e.g., 'Hydrogen', 'Helium')."""
        pass

    @abstract_class_property
    def atomic_mass(self) -> float:
        """The standard atomic weight in atomic mass units (amu)."""
        pass

    @abstract_class_property
    def electron_configuration(self) -> str:
        """The electron configuration (e.g., '1s1' for Hydrogen)."""
        pass

    @abstract_class_property
    def electron_shells(self) -> List[int]:
        """
        The number of electrons in each shell.
        For example, [1] for Hydrogen, [2] for Helium, [2, 1] for Lithium.
        """
        pass

    @abstract_class_property
    def electronegativity(self) -> Optional[float]:
        """Pauling electronegativity value (None if not applicable)."""
        pass

    @abstract_class_property
    def atomic_radius(self) -> float:
        """Atomic radius in picometers (pm)."""
        pass

    @abstract_class_property
    def ionization_energy(self) -> float:
        """First ionization energy in electron volts (eV)."""
        pass

    @abstract_class_property
    def electron_affinity(self) -> Optional[float]:
        """Electron affinity in electron volts (eV) (None if not applicable)."""
        pass

    @abstract_class_property
    def oxidation_states(self) -> List[int]:
        """Common oxidation states of the element."""
        pass

    @abstract_class_property
    def group(self) -> Optional[int]:
        """Group number in the periodic table (None for f-block elements)."""
        pass

    @abstract_class_property
    def period(self) -> int:
        """Period number in the periodic table."""
        pass

    @abstract_class_property
    def block(self) -> str:
        """Block in the periodic table ('s', 'p', 'd', or 'f')."""
        pass

    @abstract_class_property
    def category(self) -> str:
        """
        Chemical category (e.g., 'alkali metal', 'noble gas', 'transition metal').
        """
        pass

    @abstract_class_property
    def isotopes(self) -> Dict[int, float]:
        """
        Dictionary mapping mass numbers to natural abundance (as a fraction).
        For example, {1: 0.999885, 2: 0.000115} for hydrogen.
        """
        pass

    @abstract_class_property
    def melting_point(self) -> Optional[float]:
        """Melting point in Kelvin (None if not applicable)."""
        pass

    @abstract_class_property
    def boiling_point(self) -> Optional[float]:
        """Boiling point in Kelvin (None if not applicable)."""
        pass

    @abstract_class_property
    def density_value(self) -> Optional[float]:
        """Raw density value in g/cm³ at STP (None if not applicable)."""
        pass

    @abstract_class_property
    def year_discovered(self) -> Optional[int]:
        """Year of discovery (None if prehistoric)."""
        pass

    @abstract_class_property
    def discoverer(self) -> Optional[str]:
        """Name of discoverer(s) (None if prehistoric)."""
        pass

    @class_property
    def volume_value(self) -> Optional[float]:
        """
        Calculate the raw atomic volume value in cubic angstroms (Å³).
        """
        if self.atomic_radius is None:
            return None

        # Convert atomic radius from picometers to angstroms (1 pm = 0.01 Å)
        radius_in_angstroms = self.atomic_radius * 0.01

        # Calculate volume of a sphere: V = (4/3) * π * r³
        return (4/3) * math.pi * (radius_in_angstroms ** 3)

    @class_property
    def volume(self):
        """
        Atomic volume with units (Å³).
        """
        if self.volume_value is None:
            return None
        return self.volume_value * cubic(angstrom)

    @class_property
    def density(self):
        """
        Density with units (g/cm³).
        """
        if self.density_value is None:
            return None
        return self.density_value * gram / cubic(centimeter)

    @class_property
    def molar_volume(self) -> Optional[float]:
        """
        Calculate the molar volume in cm³/mol.

        Returns:
            The molar volume, or None if density is None

        Examples:
            >>> from chemesty.elements import Fe, Au, Al, H
            >>> 
            >>> # Calculate molar volume for metals
            >>> iron = Fe()
            >>> if iron.molar_volume is not None:
            ...     print(f"Iron molar volume: {iron.molar_volume:.2f} cm³/mol")
            Iron molar volume: 7.09 cm³/mol
            >>> 
            >>> gold = Au()
            >>> if gold.molar_volume is not None:
            ...     print(f"Gold molar volume: {gold.molar_volume:.2f} cm³/mol")
            Gold molar volume: 10.21 cm³/mol
            >>> 
            >>> aluminum = Al()
            >>> if aluminum.molar_volume is not None:
            ...     print(f"Aluminum molar volume: {aluminum.molar_volume:.2f} cm³/mol")
            Aluminum molar volume: 9.99 cm³/mol
            >>> 
            >>> # Some elements may not have density data
            >>> hydrogen = H()
            >>> if hydrogen.molar_volume is None:
            ...     print("Hydrogen molar volume: Not available (gas at STP)")
            Hydrogen molar volume: Not available (gas at STP)
            >>> 
            >>> # Compare molar volumes
            >>> elements = [Fe(), Au(), Al()]
            >>> volumes = [(elem.symbol, elem.molar_volume) for elem in elements if elem.molar_volume]
            >>> volumes.sort(key=lambda x: x[1])  # Sort by molar volume
            >>> print("Elements by molar volume (ascending):")
            >>> for symbol, volume in volumes:
            ...     print(f"  {symbol}: {volume:.2f} cm³/mol")
            Elements by molar volume (ascending):
              Fe: 7.09 cm³/mol
              Au: 10.21 cm³/mol
              Al: 9.99 cm³/mol
        """
        if self.density_value is None:
            return None

        # Molar volume = Molar mass / Density
        return self.atomic_mass / self.density_value

    def get_neutron_count(self, isotope: int) -> int:
        """
        Calculate the number of neutrons for a specific isotope.

        Args:
            isotope: Mass number of the isotope

        Returns:
            Number of neutrons
        """
        return isotope - self.atomic_number

    def is_metal(self) -> bool:
        """
        Determine if the element is a metal.

        Returns:
            True if the element is a metal, False otherwise

        Examples:
            >>> from chemesty.elements import Fe, Au, Na, He, Cl, C
            >>> 
            >>> # Metals return True
            >>> iron = Fe()
            >>> print(f"Iron is a metal: {iron.is_metal()}")
            Iron is a metal: True
            >>> 
            >>> gold = Au()
            >>> print(f"Gold is a metal: {gold.is_metal()}")
            Gold is a metal: True
            >>> 
            >>> sodium = Na()
            >>> print(f"Sodium is a metal: {sodium.is_metal()}")
            Sodium is a metal: True
            >>> 
            >>> # Non-metals return False
            >>> helium = He()
            >>> print(f"Helium is a metal: {helium.is_metal()}")
            Helium is a metal: False
            >>> 
            >>> chlorine = Cl()
            >>> print(f"Chlorine is a metal: {chlorine.is_metal()}")
            Chlorine is a metal: False
            >>> 
            >>> carbon = C()
            >>> print(f"Carbon is a metal: {carbon.is_metal()}")
            Carbon is a metal: False
            >>> 
            >>> # Use in filtering
            >>> from chemesty.elements import H, O, C, N, Fe, Cu, Zn
            >>> elements = [H(), O(), C(), N(), Fe(), Cu(), Zn()]
            >>> metals = [elem for elem in elements if elem.is_metal()]
            >>> print(f"Metals found: {[elem.symbol for elem in metals]}")
            Metals found: ['Fe', 'Cu', 'Zn']
        """
        non_metal_categories = ['noble gas', 'nonmetal', 'halogen']
        return self.category not in non_metal_categories

    def __mul__(self, other):
        """
        Multiply an element by a number to create a molecule.

        Example: H * 2 creates a molecule with 2 hydrogen atoms
        Example: ++Fe * 3 creates a molecule with 3 Fe²⁺ ions

        Args:
            other: A numeric value to multiply the element by

        Returns:
            A Molecule instance with the specified number of this element

        Raises:
            TypeError: If other is not a numeric type
            ValueError: If other is not a positive number
        """
        if not isinstance(other, numbers.Number):
            raise TypeError(f"Can only multiply elements by numeric types, got {type(other)}")

        if other <= 0:
            raise ValueError("Can only multiply elements by positive numbers")

        # Convert to integer if it's not already one
        count = int(other)
        if count != other:
            raise ValueError("Can only multiply elements by whole numbers")

        from chemesty.molecules.molecule import Molecule
        molecule = Molecule()
        
        # Create a deep copy of the element to preserve all attributes
        import copy
        element_copy = copy.deepcopy(self)
        
        # Add the element to the molecule
        molecule.add_element(element_copy, count)
        
        return molecule

    def __rmul__(self, other):
        """
        Support for multiplication from the left (e.g., 2 * H).
        
        When multiplying an element from the left (e.g., 2 * element),
        this creates a ReactionComponent with the specified coefficient,
        rather than a Molecule with multiplied elements.
        
        Args:
            other: The coefficient (must be a positive integer)
            
        Returns:
            A ReactionComponent with this element as a molecule and the specified coefficient
            
        Examples:
            >>> from chemesty.elements import H
            >>> # Create a reaction component with coefficient 2
            >>> hydrogen_component = 2 * H  # 2 H
        """
        if not isinstance(other, int) or other <= 0:
            raise ValueError("Can only multiply elements by positive integers")
            
        # First create a molecule with this element
        from chemesty.molecules.molecule import Molecule
        molecule = Molecule()
        
        # Create a deep copy of the element to preserve all attributes
        import copy
        element_copy = copy.deepcopy(self)
        
        # Add the element to the molecule
        molecule.add_element(element_copy, 1)
        
        # Import here to avoid circular imports
        from chemesty.reactions.reaction import ReactionComponent
        
        # Create a ReactionComponent with the specified coefficient
        return ReactionComponent(molecule=molecule, coefficient=other)
        
    def __matmul__(self, state):
        """
        Set the physical state using the @ operator.
        
        Example: Fe @ 'aq' creates Fe(aq)
        
        Args:
            state: The state to apply ('s', 'l', 'g', 'aq')
            
        Returns:
            A molecule with this element and the state applied
            
        Examples:
            >>> from chemesty.elements import Fe
            >>> iron_aqueous = Fe @ 'aq'
            >>> print(iron_aqueous)
            Fe(aq)
        """
        if not isinstance(state, str) or state not in ['s', 'l', 'g', 'aq']:
            raise ValueError(f"Invalid state: {state}. Must be one of: 's', 'l', 'g', 'aq'")
        
        # Create a molecule with this element
        from chemesty.molecules.molecule import Molecule
        molecule = Molecule()
        
        # Create a deep copy of the element to preserve all attributes
        import copy
        element_copy = copy.deepcopy(self)
        
        # Add the element to the molecule
        molecule.add_element(element_copy, 1)
        
        # Set the phase
        molecule.phase = state
        
        return molecule

    def __add__(self, other):
        """
        Add elements or molecules to create a new molecule.

        Example: H + O creates a molecule with 1 hydrogen and 1 oxygen atom
        Example: Fe + (N + O*3).group(3) creates Fe(NO₃)₃

        Args:
            other: An AtomicElement, Molecule, or tuple (molecule, multiplier) to add to this element

        Returns:
            A new Molecule instance containing this element and the other element/molecule

        Raises:
            TypeError: If other is not an AtomicElement, Molecule, or valid tuple
        """
        from chemesty.molecules.molecule import Molecule
        import copy

        if isinstance(other, AtomicElement):
            molecule = Molecule()
            # Create deep copies of the elements to preserve all attributes
            self_copy = copy.deepcopy(self)
            other_copy = copy.deepcopy(other)
            molecule.add_element(self_copy, 1)
            molecule.add_element(other_copy, 1)
            return molecule
        elif isinstance(other, type) and isinstance(other, ElementMeta):
            # Handle element class (e.g., Fe, O) by instantiating it
            molecule = Molecule()
            # Create deep copies of the elements to preserve all attributes
            self_copy = copy.deepcopy(self)
            instance = other()  # Create an instance of the element class
            other_copy = copy.deepcopy(instance)
            molecule.add_element(self_copy, 1)
            molecule.add_element(other_copy, 1)
            return molecule
        elif isinstance(other, Molecule):
            molecule = Molecule()
            # Create a deep copy of this element
            self_copy = copy.deepcopy(self)
            molecule.add_element(self_copy, 1)
            # Create deep copies of all elements in the other molecule
            for element, count in other.elements.items():
                element_copy = copy.deepcopy(element)
                molecule.add_element(element_copy, count)
            return molecule
        elif isinstance(other, tuple) and len(other) == 2:
            # Handle (molecule, multiplier) format for complex formulas
            mol, multiplier = other
            if isinstance(mol, Molecule) and isinstance(multiplier, int):
                molecule = Molecule()
                # Create a deep copy of this element
                self_copy = copy.deepcopy(self)
                molecule.add_element(self_copy, 1)
                # Create deep copies of all elements in the other molecule
                for element, count in mol.elements.items():
                    element_copy = copy.deepcopy(element)
                    molecule.add_element(element_copy, count * multiplier)
                return molecule
            else:
                raise TypeError(f"Tuple must be (Molecule, int), got ({type(mol)}, {type(multiplier)})")
        else:
            # Check if it's a ReactionComponent in the context of a reaction
            try:
                from chemesty.reactions.reaction import ReactionComponent
                if isinstance(other, ReactionComponent) and hasattr(other, 'molecule'):
                    # Extract the molecule from the ReactionComponent
                    molecule = Molecule()
                    # Create a deep copy of this element
                    self_copy = copy.deepcopy(self)
                    molecule.add_element(self_copy, 1)
                    # Create deep copies of all elements in the other molecule
                    other_molecule = other.molecule
                    for element, count in other_molecule.elements.items():
                        element_copy = copy.deepcopy(element)
                        molecule.add_element(element_copy, count)
                    # Preserve the charge from the ReactionComponent's molecule if it has one
                    if hasattr(other_molecule, 'charge'):
                        molecule.charge = other_molecule.charge
                    return molecule
            except (ImportError, AttributeError):
                pass
                
            raise TypeError(f"Cannot add {type(other)} to an element. Only AtomicElement, Molecule, or (Molecule, int) tuple types are supported.")

    def __str__(self) -> str:
        """
        String representation of the element with charge if present.
        
        Examples:
            >>> from chemesty.elements import Fe, O
            >>> import copy
            >>> 
            >>> # Neutral elements
            >>> print(Fe)
            Iron (Fe)
            >>> 
            >>> # Charged elements
            >>> fe_plus = copy.deepcopy(Fe)
            >>> fe_plus.charge = 1
            >>> print(fe_plus)
            Iron (Fe¹⁺)
            >>> 
            >>> fe_plus2 = copy.deepcopy(Fe)
            >>> fe_plus2.charge = 2
            >>> print(fe_plus2)
            Iron (Fe²⁺)
            >>> 
            >>> o_minus2 = copy.deepcopy(O)
            >>> o_minus2.charge = -2
            >>> print(o_minus2)
            Oxygen (O²⁻)
        """
        if self.charge == 0:
            return f"{self.name} ({self.symbol})"
        
        # Convert charge to superscript
        charge_str = ""
        if abs(self.charge) > 1:
            # Use superscript numbers for magnitude
            magnitude = str(abs(self.charge))
            superscript_digits = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
            }
            charge_str = ''.join(superscript_digits[digit] for digit in magnitude)
        
        # Add superscript plus or minus
        if self.charge > 0:
            charge_str += '⁺'
        else:
            charge_str += '⁻'
        
        return f"{self.name} ({self.symbol}{charge_str})"

    def __repr__(self) -> str:
        """Detailed representation of the element."""
        return f"{self.__class__.__name__}(Z={self.atomic_number}, symbol='{self.symbol}', name='{self.name}')"
