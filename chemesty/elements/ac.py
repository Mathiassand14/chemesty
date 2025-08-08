from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ac(AtomicElement):
    """
    Actinium element (Ac, Z=89).
    """
    
    @property
    def name(self) -> str:
        return "Actinium"
    
    @property
    def atomic_number(self) -> int:
        return 89
    
    @property
    def atomic_mass(self) -> float:
        return 227.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 6d1 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.1
    
    @property
    def atomic_radius(self) -> float:
        return 195.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.17
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.35
    
    @property
    def oxidation_states(self) -> List[int]:
        return [3]
    
    @property
    def group(self) -> Optional[int]:
        return 3
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "f"
    
    @property
    def category(self) -> str:
        return "actinide"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {227: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1323.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3471.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 10.07
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1899
    
    @property
    def discoverer(self) -> Optional[str]:
        return "André-Louis Debierne, Friedrich Oskar Giesel"
    
    @property
    def symbol(self) -> str:
        return "Ac"
