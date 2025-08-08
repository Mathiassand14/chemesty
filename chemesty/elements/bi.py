from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Bi(AtomicElement):
    """
    Bismuth element (Bi, Z=83).
    """
    
    @property
    def name(self) -> str:
        return "Bismuth"
    
    @property
    def atomic_number(self) -> int:
        return 83
    
    @property
    def atomic_mass(self) -> float:
        return 208.98
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d10 6s2 6p3"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 5]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.02
    
    @property
    def atomic_radius(self) -> float:
        return 160.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.289
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.942
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -2, -1, 1, 2, 3, 4, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 15
    
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
        return {209: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 544.7
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1837.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 9.78
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "Bi"
