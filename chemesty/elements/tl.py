from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Tl(AtomicElement):
    """
    Thallium element (Tl, Z=81).
    """
    
    @property
    def name(self) -> str:
        return "Thallium"
    
    @property
    def atomic_number(self) -> int:
        return 81
    
    @property
    def atomic_mass(self) -> float:
        return 204.38
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d10 6s2 6p1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 3]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.62
    
    @property
    def atomic_radius(self) -> float:
        return 190.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.108
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.2
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-5, -2, -1, 1, 2, 3]
    
    @property
    def group(self) -> Optional[int]:
        return 13
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "post-transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {203: 0.2952, 205: 0.7048}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 577.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1746.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 11.85
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1861
    
    @property
    def discoverer(self) -> Optional[str]:
        return "William Crookes"
    
    @property
    def symbol(self) -> str:
        return "Tl"
