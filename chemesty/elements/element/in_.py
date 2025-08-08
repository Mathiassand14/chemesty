from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class In(AtomicElement):
    """
    Indium element (In, Z=49).
    """

    @property
    def name(self) -> str:
        return "Indium"

    @property
    def atomic_number(self) -> int:
        return 49

    @property
    def symbol(self) -> str:
        return "In"

    # Note: This is a minimal implementation.
    # In a real application, you would need to implement all abstract methods
    # from the AtomicElement base class.

    # Placeholder implementations for required abstract methods
    @property
    def atomic_mass(self) -> float:
        return 114.82

    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10 5s2 5p1"

    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 3]

    @property
    def electronegativity(self) -> Optional[float]:
        return 1.78

    @property
    def atomic_radius(self) -> float:
        return 156.0

    @property
    def ionization_energy(self) -> float:
        return 5.786

    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.3

    @property
    def oxidation_states(self) -> List[int]:
        return [-5, -2, -1, 1, 2, 3]

    @property
    def group(self) -> Optional[int]:
        return 13

    @property
    def period(self) -> int:
        return 5

    @property
    def block(self) -> str:
        return "p"

    @property
    def category(self) -> str:
        return "post-transition metal"

    @property
    def isotopes(self) -> Dict[int, float]:
        return {113: 0.0429, 115: 0.9571}

    @property
    def melting_point(self) -> Optional[float]:
        return 429.75

    @property
    def boiling_point(self) -> Optional[float]:
        return 2345.0

    @property
    def density_value(self) -> Optional[float]:
        return 7.31

    @property
    def year_discovered(self) -> Optional[int]:
        return 1863

    @property
    def discoverer(self) -> Optional[str]:
        return "Ferdinand Reich, Hieronymous Theodor Richter"
