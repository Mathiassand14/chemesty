from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Gd(AtomicElement):
    """
    Gadolinium element (Gd, Z=64).
    """
    
    @property
    def name(self) -> str:
        return "Gadolinium"
    
    @property
    def atomic_number(self) -> int:
        return 64
    
    @property
    def atomic_mass(self) -> float:
        return 157.25
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f7 5d1 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 25, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.2
    
    @property
    def atomic_radius(self) -> float:
        return 180.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.15
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2, 3]
    
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
        return {152: 0.002, 154: 0.0218, 155: 0.148, 156: 0.2047, 157: 0.1565, 158: 0.2484, 160: 0.2186}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1585.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3546.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.9
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1880
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Jean Charles Galissard de Marignac"
    
    @property
    def symbol(self) -> str:
        return "Gd"
