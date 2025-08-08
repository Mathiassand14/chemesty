from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Cl(AtomicElement):
    """
    Chlorine element (Cl, Z=17).
    """
    
    @property
    def name(self) -> str:
        return "Chlorine"
    
    @property
    def atomic_number(self) -> int:
        return 17
    
    @property
    def atomic_mass(self) -> float:
        return 35.453
    
    @property
    def electron_configuration(self) -> str:
        return "[Ne] 3s2 3p5"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 7]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 3.16
    
    @property
    def atomic_radius(self) -> float:
        return 100.0
    
    @property
    def ionization_energy(self) -> float:
        return 12.968
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 3.617
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1, 2, 3, 4, 5, 6, 7]
    
    @property
    def group(self) -> Optional[int]:
        return 17
    
    @property
    def period(self) -> int:
        return 3
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "halogen"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {35: 0.7576, 37: 0.2424}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 171.6
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 239.11
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.003214
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1774
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Carl Wilhelm Scheele"
    
    @property
    def symbol(self) -> str:
        return "Cl"
