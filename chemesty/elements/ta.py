from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ta(AtomicElement):
    """
    Tantalum element (Ta, Z=73).
    """
    
    @property
    def name(self) -> str:
        return "Tantalum"
    
    @property
    def atomic_number(self) -> int:
        return 73
    
    @property
    def atomic_mass(self) -> float:
        return 180.95
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d3 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 11, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.5
    
    @property
    def atomic_radius(self) -> float:
        return 145.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.89
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.322
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -1, 1, 2, 3, 4, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 5
    
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
        return {180: 0.0001201, 181: 0.9998799}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 3290.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 5731.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 16.69
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1802
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Anders Gustaf Ekeberg"
    
    @property
    def symbol(self) -> str:
        return "Ta"
