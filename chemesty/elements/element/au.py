from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Au(AtomicElement):
    """
    Gold element (Au, Z=79).
    """
    
    @property
    def name(self) -> str:
        return "Gold"
    
    @property
    def atomic_number(self) -> int:
        return 79
    
    @property
    def atomic_mass(self) -> float:
        return 196.967
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d10 6s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.54
    
    @property
    def atomic_radius(self) -> float:
        return 144.0
    
    @property
    def ionization_energy(self) -> float:
        return 9.226
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 2.309
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1, 2, 3, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 11
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {197: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1337.33
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3129.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 19.3
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "Au"
