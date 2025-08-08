from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Na(AtomicElement):
    """
    Sodium element (Na, Z=11).
    """
    
    @property
    def name(self) -> str:
        return "Sodium"
    
    @property
    def atomic_number(self) -> int:
        return 11
    
    @property
    def atomic_mass(self) -> float:
        return 22.99
    
    @property
    def electron_configuration(self) -> str:
        return "[Ne] 3s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 0.93
    
    @property
    def atomic_radius(self) -> float:
        return 190.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.139
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.548
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1]
    
    @property
    def group(self) -> Optional[int]:
        return 1
    
    @property
    def period(self) -> int:
        return 3
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkali metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {23: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 370.87
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1156.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.968
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1807
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Humphry Davy"
    
    @property
    def symbol(self) -> str:
        return "Na"
