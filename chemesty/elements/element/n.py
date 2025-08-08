from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class N(AtomicElement):
    """
    Nitrogen element (N, Z=7).
    """
    
    @property
    def name(self) -> str:
        return "Nitrogen"
    
    @property
    def atomic_number(self) -> int:
        return 7
    
    @property
    def atomic_mass(self) -> float:
        return 14.007
    
    @property
    def electron_configuration(self) -> str:
        return "[He] 2s2 2p3"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 5]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 3.04
    
    @property
    def atomic_radius(self) -> float:
        return 65.0
    
    @property
    def ionization_energy(self) -> float:
        return 14.534
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -2, -1, 1, 2, 3, 4, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 15
    
    @property
    def period(self) -> int:
        return 2
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "nonmetal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {14: 0.99636, 15: 0.00364}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 63.15
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 77.36
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.001251
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1772
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Daniel Rutherford"
    
    @property
    def symbol(self) -> str:
        return "N"
