from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Pm(AtomicElement):
    """
    Promethium element (Pm, Z=61).
    """
    
    @property
    def name(self) -> str:
        return "Promethium"
    
    @property
    def atomic_number(self) -> int:
        return 61
    
    @property
    def atomic_mass(self) -> float:
        return 145.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f5 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 23, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.13
    
    @property
    def atomic_radius(self) -> float:
        return 185.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.55
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [3]
    
    @property
    def group(self) -> Optional[int]:
        return None
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "f"
    
    @property
    def category(self) -> str:
        return "lanthanide"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {145: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1315.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3273.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.26
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1945
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Jacob A. Marinsky, Lawrence E. Glendenin, Charles D. Coryell"
    
    @property
    def symbol(self) -> str:
        return "Pm"
