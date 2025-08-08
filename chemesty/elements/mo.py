from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Mo(AtomicElement):
    """
    Molybdenum element (Mo, Z=42).
    """
    
    @property
    def name(self) -> str:
        return "Molybdenum"
    
    @property
    def atomic_number(self) -> int:
        return 42
    
    @property
    def atomic_mass(self) -> float:
        return 95.95
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d5 5s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 13, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.16
    
    @property
    def atomic_radius(self) -> float:
        return 190.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.092
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.746
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 6
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {92: 0.1484, 94: 0.0925, 95: 0.1592, 96: 0.1668, 97: 0.0955, 98: 0.2413, 100: 0.0963}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2896.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4912.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 10.28
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1781
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Carl Wilhelm Scheele"
    
    @property
    def symbol(self) -> str:
        return "Mo"
