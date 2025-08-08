from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ar(AtomicElement):
    """
    Argon element (Ar, Z=18).
    """
    
    @property
    def name(self) -> str:
        return "Argon"
    
    @property
    def atomic_number(self) -> int:
        return 18
    
    @property
    def atomic_mass(self) -> float:
        return 39.948
    
    @property
    def electron_configuration(self) -> str:
        return "[Ne] 3s2 3p6"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 8]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 71.0
    
    @property
    def ionization_energy(self) -> float:
        return 15.76
    
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
        return 3
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "noble gas"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {36: 0.003365, 38: 0.000632, 40: 0.996003}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 83.8
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 87.3
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.0017837
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1894
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Lord Rayleigh, William Ramsay"
    
    @property
    def symbol(self) -> str:
        return "Ar"
