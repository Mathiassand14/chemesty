from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Fe(AtomicElement):
    """
    Iron element (Fe, Z=26).
    """
    
    @property
    def name(self) -> str:
        return "Iron"
    
    @property
    def atomic_number(self) -> int:
        return 26
    
    @property
    def atomic_mass(self) -> float:
        return 55.845
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d6 4s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 14, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.83
    
    @property
    def atomic_radius(self) -> float:
        return 126.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.902
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.163
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2, 3, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return None
    
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
        return {54: 0.05845, 56: 0.91754, 57: 0.02119, 58: 0.00282}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1811.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3134.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.874
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "Fe"
