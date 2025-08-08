from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Cu(AtomicElement):
    """
    Copper element (Cu, Z=29).
    """
    
    @property
    def name(self) -> str:
        return "Copper"
    
    @property
    def atomic_number(self) -> int:
        return 29
    
    @property
    def atomic_mass(self) -> float:
        return 63.546
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d10 4s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.9
    
    @property
    def atomic_radius(self) -> float:
        return 145.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.726
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.228
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 11
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {63: 0.6915, 65: 0.3085}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1357.77
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2835.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.96
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "Cu"
