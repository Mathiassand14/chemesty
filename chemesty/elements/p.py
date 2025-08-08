from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class P(AtomicElement):
    """
    Phosphorus element (P, Z=15).
    """
    
    @property
    def name(self) -> str:
        return "Phosphorus"
    
    @property
    def atomic_number(self) -> int:
        return 15
    
    @property
    def atomic_mass(self) -> float:
        return 30.974
    
    @property
    def electron_configuration(self) -> str:
        return "[Ne] 3s2 3p3"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 5]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.19
    
    @property
    def atomic_radius(self) -> float:
        return 98.0
    
    @property
    def ionization_energy(self) -> float:
        return 10.487
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.746
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -2, -1, 1, 2, 3, 4, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 15
    
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
        return {31: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 317.3
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 553.6
    
    @property
    def density_value(self) -> Optional[float]:
        return 1.82
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1669
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Hennig Brand"
    
    @property
    def symbol(self) -> str:
        return "P"
