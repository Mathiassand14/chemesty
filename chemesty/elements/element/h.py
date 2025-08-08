from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class H(AtomicElement):
    """
    Hydrogen element (H, Z=1).
    """
    
    @property
    def name(self) -> str:
        return "Hydrogen"
    
    @property
    def atomic_number(self) -> int:
        return 1
    
    @property
    def atomic_mass(self) -> float:
        return 1.008
    
    @property
    def electron_configuration(self) -> str:
        return "1s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.2
    
    @property
    def atomic_radius(self) -> float:
        return 53.0
    
    @property
    def ionization_energy(self) -> float:
        return 13.598
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.754
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1]
    
    @property
    def group(self) -> Optional[int]:
        return 1
    
    @property
    def period(self) -> int:
        return 1
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "nonmetal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {1: 0.999885, 2: 0.000115}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 14.01
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 20.28
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.988e-05
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1766
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Henry Cavendish"
    
    @property
    def symbol(self) -> str:
        return "H"
