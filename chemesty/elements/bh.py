from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Bh(AtomicElement):
    """
    Bohrium element (Bh, Z=107).
    """
    
    @property
    def name(self) -> str:
        return "Bohrium"
    
    @property
    def atomic_number(self) -> int:
        return 107
    
    @property
    def atomic_mass(self) -> float:
        return 270.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f14 6d5 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 32, 13, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 141.0
    
    @property
    def ionization_energy(self) -> float:
        return None
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return None
    
    @property
    def oxidation_states(self) -> List[int]:
        return [7]
    
    @property
    def group(self) -> Optional[int]:
        return 7
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {270: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return None
    
    @property
    def boiling_point(self) -> Optional[float]:
        return None
    
    @property
    def density_value(self) -> Optional[float]:
        return 37.1
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1981
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Gesellschaft für Schwerionenforschung"
    
    @property
    def symbol(self) -> str:
        return "Bh"
