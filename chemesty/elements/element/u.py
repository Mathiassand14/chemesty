from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class U(AtomicElement):
    """
    Uranium element (U, Z=92).
    """
    
    @property
    def name(self) -> str:
        return "Uranium"
    
    @property
    def atomic_number(self) -> int:
        return 92
    
    @property
    def atomic_mass(self) -> float:
        return 238.029
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f3 6d1 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 21, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.38
    
    @property
    def atomic_radius(self) -> float:
        return 156.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.194
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2, 3, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return None
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "f"
    
    @property
    def category(self) -> str:
        return "actinide"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {234: 5.5e-05, 235: 0.007204, 238: 0.992742}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1405.3
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4404.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 19.1
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1789
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Martin Heinrich Klaproth"
    
    @property
    def symbol(self) -> str:
        return "U"
