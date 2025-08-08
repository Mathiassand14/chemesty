from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Rh(AtomicElement):
    """
    Rhodium element (Rh, Z=45).
    """
    
    @property
    def name(self) -> str:
        return "Rhodium"
    
    @property
    def atomic_number(self) -> int:
        return 45
    
    @property
    def atomic_mass(self) -> float:
        return 102.91
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d8 5s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 16, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.28
    
    @property
    def atomic_radius(self) -> float:
        return 173.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.459
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.14
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -1, 1, 2, 3, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 9
    
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
        return {103: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2237.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3968.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 12.41
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1803
    
    @property
    def discoverer(self) -> Optional[str]:
        return "William Hyde Wollaston"
    
    @property
    def symbol(self) -> str:
        return "Rh"
