from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Sb(AtomicElement):
    """
    Antimony element (Sb, Z=51).
    """
    
    @property
    def name(self) -> str:
        return "Antimony"
    
    @property
    def atomic_number(self) -> int:
        return 51
    
    @property
    def atomic_mass(self) -> float:
        return 121.76
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10 5s2 5p3"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 5]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.05
    
    @property
    def atomic_radius(self) -> float:
        return 133.0
    
    @property
    def ionization_energy(self) -> float:
        return 8.64
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.07
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -2, -1, 1, 2, 3, 4, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 15
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "metalloid"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {121: 0.5721, 123: 0.4279}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 903.78
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1860.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 6.685
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Early historic times"
    
    @property
    def symbol(self) -> str:
        return "Sb"
