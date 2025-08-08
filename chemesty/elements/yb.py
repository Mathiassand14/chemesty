from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Yb(AtomicElement):
    """
    Ytterbium element (Yb, Z=70).
    """
    
    @property
    def name(self) -> str:
        return "Ytterbium"
    
    @property
    def atomic_number(self) -> int:
        return 70
    
    @property
    def atomic_mass(self) -> float:
        return 173.05
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.1
    
    @property
    def atomic_radius(self) -> float:
        return 175.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.254
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [2, 3]
    
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
        return {168: 0.00123, 170: 0.02982, 171: 0.1409, 172: 0.2168, 173: 0.16103, 174: 0.32026, 176: 0.12996}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1097.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1469.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 6.9
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1878
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Jean Charles Galissard de Marignac"
    
    @property
    def symbol(self) -> str:
        return "Yb"
