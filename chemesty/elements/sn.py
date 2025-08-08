from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Sn(AtomicElement):
    """
    Tin element (Sn, Z=50).
    """
    
    @property
    def name(self) -> str:
        return "Tin"
    
    @property
    def atomic_number(self) -> int:
        return 50
    
    @property
    def atomic_mass(self) -> float:
        return 118.71
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10 5s2 5p2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 4]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.96
    
    @property
    def atomic_radius(self) -> float:
        return 145.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.344
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.2
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -3, -2, -1, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 14
    
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
        return {112: 0.0097, 114: 0.0066, 115: 0.0034, 116: 0.1454, 117: 0.0768, 118: 0.2422, 119: 0.0859, 120: 0.3258, 122: 0.0463, 124: 0.0579}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 505.08
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2875.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.287
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "Sn"
