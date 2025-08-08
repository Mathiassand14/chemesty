from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ge(AtomicElement):
    """
    Germanium element (Ge, Z=32).
    """
    
    @property
    def name(self) -> str:
        return "Germanium"
    
    @property
    def atomic_number(self) -> int:
        return 32
    
    @property
    def atomic_mass(self) -> float:
        return 72.63
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d10 4s2 4p2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 4]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.01
    
    @property
    def atomic_radius(self) -> float:
        return 125.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.9
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.35
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -3, -2, -1, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 14
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "metalloid"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {70: 0.2057, 72: 0.2745, 73: 0.0775, 74: 0.365, 76: 0.0773}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1211.4
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3106.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 5.323
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1886
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Clemens Winkler"
    
    @property
    def symbol(self) -> str:
        return "Ge"
