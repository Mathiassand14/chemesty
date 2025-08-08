from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Cm(AtomicElement):
    """
    Curium element (Cm, Z=96).
    """
    
    @property
    def name(self) -> str:
        return "Curium"
    
    @property
    def atomic_number(self) -> int:
        return 96
    
    @property
    def atomic_mass(self) -> float:
        return 247.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f7 6d1 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 25, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.3
    
    @property
    def atomic_radius(self) -> float:
        return 174.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.02
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [3, 4]
    
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
        return {247: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1613.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3383.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 13.51
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1944
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Glenn T. Seaborg, Ralph A. James, Albert Ghiorso"
    
    @property
    def symbol(self) -> str:
        return "Cm"
