from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class S(AtomicElement):
    """
    Sulfur element (S, Z=16).
    """
    
    @property
    def name(self) -> str:
        return "Sulfur"
    
    @property
    def atomic_number(self) -> int:
        return 16
    
    @property
    def atomic_mass(self) -> float:
        return 32.06
    
    @property
    def electron_configuration(self) -> str:
        return "[Ne] 3s2 3p4"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 6]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.58
    
    @property
    def atomic_radius(self) -> float:
        return 88.0
    
    @property
    def ionization_energy(self) -> float:
        return 10.36
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 2.077
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2, 3, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 16
    
    @property
    def period(self) -> int:
        return 3
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "nonmetal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {32: 0.9499, 33: 0.0075, 34: 0.0425, 36: 0.0001}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 388.36
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 717.87
    
    @property
    def density_value(self) -> Optional[float]:
        return 2.067
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "S"
