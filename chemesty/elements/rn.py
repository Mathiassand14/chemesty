from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Rn(AtomicElement):
    """
    Radon element (Rn, Z=86).
    """
    
    @property
    def name(self) -> str:
        return "Radon"
    
    @property
    def atomic_number(self) -> int:
        return 86
    
    @property
    def atomic_mass(self) -> float:
        return 222.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d10 6s2 6p6"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 8]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.2
    
    @property
    def atomic_radius(self) -> float:
        return 120.0
    
    @property
    def ionization_energy(self) -> float:
        return 10.745
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [0, 2, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 18
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "noble gas"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {222: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 202.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 211.3
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.00973
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1900
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Friedrich Ernst Dorn"
    
    @property
    def symbol(self) -> str:
        return "Rn"
