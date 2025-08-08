from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ts(AtomicElement):
    """
    Tennessine element (Ts, Z=117).
    """
    
    @property
    def name(self) -> str:
        return "Tennessine"
    
    @property
    def atomic_number(self) -> int:
        return 117
    
    @property
    def atomic_mass(self) -> float:
        return 294.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f14 6d10 7s2 7p5"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 32, 18, 7]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 165.0
    
    @property
    def ionization_energy(self) -> float:
        return None
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return None
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1, 3, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 17
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "halogen"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {294: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 723.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 883.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.2
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 2010
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Joint Institute for Nuclear Research, Oak Ridge National Laboratory, Vanderbilt University"
    
    @property
    def symbol(self) -> str:
        return "Ts"
