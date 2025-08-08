from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Co(AtomicElement):
    """
    Cobalt element (Co, Z=27).
    """
    
    @property
    def name(self) -> str:
        return "Cobalt"
    
    @property
    def atomic_number(self) -> int:
        return 27
    
    @property
    def atomic_mass(self) -> float:
        return 58.933
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d7 4s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 15, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.88
    
    @property
    def atomic_radius(self) -> float:
        return 152.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.881
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.661
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -1, 1, 2, 3, 4, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 9
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {59: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1768.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3200.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.86
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1735
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Georg Brandt"
    
    @property
    def symbol(self) -> str:
        return "Co"
