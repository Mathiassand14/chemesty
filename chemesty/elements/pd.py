from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Pd(AtomicElement):
    """
    Palladium element (Pd, Z=46).
    """
    
    @property
    def name(self) -> str:
        return "Palladium"
    
    @property
    def atomic_number(self) -> int:
        return 46
    
    @property
    def atomic_mass(self) -> float:
        return 106.42
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.2
    
    @property
    def atomic_radius(self) -> float:
        return 169.0
    
    @property
    def ionization_energy(self) -> float:
        return 8.337
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.56
    
    @property
    def oxidation_states(self) -> List[int]:
        return [0, 1, 2, 3, 4, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 10
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {102: 0.0102, 104: 0.1114, 105: 0.2233, 106: 0.2733, 108: 0.2646, 110: 0.1172}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1828.05
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3236.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 12.023
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1803
    
    @property
    def discoverer(self) -> Optional[str]:
        return "William Hyde Wollaston"
    
    @property
    def symbol(self) -> str:
        return "Pd"
