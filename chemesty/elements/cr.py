from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Cr(AtomicElement):
    """
    Chromium element (Cr, Z=24).
    """
    
    @property
    def name(self) -> str:
        return "Chromium"
    
    @property
    def atomic_number(self) -> int:
        return 24
    
    @property
    def atomic_mass(self) -> float:
        return 51.996
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d5 4s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 13, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.66
    
    @property
    def atomic_radius(self) -> float:
        return 166.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.767
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.666
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -2, -1, 1, 2, 3, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 6
    
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
        return {50: 0.04345, 52: 0.83789, 53: 0.09501, 54: 0.02365}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2180.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2944.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.15
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1797
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Louis Nicolas Vauquelin"
    
    @property
    def symbol(self) -> str:
        return "Cr"
