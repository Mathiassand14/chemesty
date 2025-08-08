from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ti(AtomicElement):
    """
    Titanium element (Ti, Z=22).
    """
    
    @property
    def name(self) -> str:
        return "Titanium"
    
    @property
    def atomic_number(self) -> int:
        return 22
    
    @property
    def atomic_mass(self) -> float:
        return 47.867
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d2 4s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 10, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.54
    
    @property
    def atomic_radius(self) -> float:
        return 176.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.828
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.079
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 4
    
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
        return {46: 0.0825, 47: 0.0744, 48: 0.7372, 49: 0.0541, 50: 0.0518}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1941.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3560.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 4.54
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1791
    
    @property
    def discoverer(self) -> Optional[str]:
        return "William Gregor"
    
    @property
    def symbol(self) -> str:
        return "Ti"
