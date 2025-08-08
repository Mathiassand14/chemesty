from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Al(AtomicElement):
    """
    Aluminum element (Al, Z=13).
    """
    
    @property
    def name(self) -> str:
        return "Aluminum"
    
    @property
    def atomic_number(self) -> int:
        return 13
    
    @property
    def atomic_mass(self) -> float:
        return 26.982
    
    @property
    def electron_configuration(self) -> str:
        return "[Ne] 3s2 3p1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 3]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.61
    
    @property
    def atomic_radius(self) -> float:
        return 118.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.986
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.441
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2, 3]
    
    @property
    def group(self) -> Optional[int]:
        return 13
    
    @property
    def period(self) -> int:
        return 3
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "post-transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {27: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 933.47
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2792.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 2.698
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1825
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Hans Christian Ørsted"
    
    @property
    def symbol(self) -> str:
        return "Al"
