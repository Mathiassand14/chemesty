from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ni(AtomicElement):
    """
    Nickel element (Ni, Z=28).
    """
    
    @property
    def name(self) -> str:
        return "Nickel"
    
    @property
    def atomic_number(self) -> int:
        return 28
    
    @property
    def atomic_mass(self) -> float:
        return 58.693
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d8 4s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 16, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.91
    
    @property
    def atomic_radius(self) -> float:
        return 149.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.64
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.156
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 10
    
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
        return {58: 0.68077, 60: 0.26223, 61: 0.0114, 62: 0.03634, 64: 0.00926}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1728.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3186.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.912
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1751
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Axel Fredrik Cronstedt"
    
    @property
    def symbol(self) -> str:
        return "Ni"
