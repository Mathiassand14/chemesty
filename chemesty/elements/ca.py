from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ca(AtomicElement):
    """
    Calcium element (Ca, Z=20).
    """
    
    @property
    def name(self) -> str:
        return "Calcium"
    
    @property
    def atomic_number(self) -> int:
        return 20
    
    @property
    def atomic_mass(self) -> float:
        return 40.078
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 4s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.0
    
    @property
    def atomic_radius(self) -> float:
        return 194.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.113
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.025
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 2
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkaline earth metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {40: 0.96941, 42: 0.00647, 43: 0.00135, 44: 0.02086, 46: 4e-05, 48: 0.00187}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1115.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1757.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 1.54
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1808
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Humphry Davy"
    
    @property
    def symbol(self) -> str:
        return "Ca"
