from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Kr(AtomicElement):
    """
    Krypton element (Kr, Z=36).
    """
    
    @property
    def name(self) -> str:
        return "Krypton"
    
    @property
    def atomic_number(self) -> int:
        return 36
    
    @property
    def atomic_mass(self) -> float:
        return 83.798
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d10 4s2 4p6"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 8]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 3.0
    
    @property
    def atomic_radius(self) -> float:
        return 88.0
    
    @property
    def ionization_energy(self) -> float:
        return 14.0
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return None
    
    @property
    def oxidation_states(self) -> List[int]:
        return [0, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 18
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "noble gas"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {78: 0.0035, 80: 0.0228, 82: 0.1158, 83: 0.1149, 84: 0.57, 86: 0.173}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 115.79
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 119.93
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.003733
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1898
    
    @property
    def discoverer(self) -> Optional[str]:
        return "William Ramsay, Morris Travers"
    
    @property
    def symbol(self) -> str:
        return "Kr"
