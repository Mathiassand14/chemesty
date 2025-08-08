from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ag(AtomicElement):
    """
    Silver element (Ag, Z=47).
    """
    
    @property
    def name(self) -> str:
        return "Silver"
    
    @property
    def atomic_number(self) -> int:
        return 47
    
    @property
    def atomic_mass(self) -> float:
        return 107.87
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10 5s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.93
    
    @property
    def atomic_radius(self) -> float:
        return 165.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.576
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.302
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2, 3]
    
    @property
    def group(self) -> Optional[int]:
        return 11
    
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
        return {107: 0.51839, 109: 0.48161}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1234.93
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2435.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 10.49
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "Ag"
