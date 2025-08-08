from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class I(AtomicElement):
    """
    Iodine element (I, Z=53).
    """
    
    @property
    def name(self) -> str:
        return "Iodine"
    
    @property
    def atomic_number(self) -> int:
        return 53
    
    @property
    def atomic_mass(self) -> float:
        return 126.9
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10 5s2 5p5"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 7]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.66
    
    @property
    def atomic_radius(self) -> float:
        return 115.0
    
    @property
    def ionization_energy(self) -> float:
        return 10.451
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 3.059
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1, 3, 4, 5, 6, 7]
    
    @property
    def group(self) -> Optional[int]:
        return 17
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "halogen"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {127: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 386.85
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 457.4
    
    @property
    def density_value(self) -> Optional[float]:
        return 4.93
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1811
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Bernard Courtois"
    
    @property
    def symbol(self) -> str:
        return "I"
