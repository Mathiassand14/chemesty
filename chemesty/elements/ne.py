from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ne(AtomicElement):
    """
    Neon element (Ne, Z=10).
    """
    
    @property
    def name(self) -> str:
        return "Neon"
    
    @property
    def atomic_number(self) -> int:
        return 10
    
    @property
    def atomic_mass(self) -> float:
        return 20.18
    
    @property
    def electron_configuration(self) -> str:
        return "[He] 2s2 2p6"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 38.0
    
    @property
    def ionization_energy(self) -> float:
        return 21.565
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return None
    
    @property
    def oxidation_states(self) -> List[int]:
        return [0]
    
    @property
    def group(self) -> Optional[int]:
        return 18
    
    @property
    def period(self) -> int:
        return 2
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "noble gas"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {20: 0.9048, 21: 0.0027, 22: 0.0925}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 24.56
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 27.07
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.0008999
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1898
    
    @property
    def discoverer(self) -> Optional[str]:
        return "William Ramsay, Morris Travers"
    
    @property
    def symbol(self) -> str:
        return "Ne"
