from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Tb(AtomicElement):
    """
    Terbium element (Tb, Z=65).
    """
    
    @property
    def name(self) -> str:
        return "Terbium"
    
    @property
    def atomic_number(self) -> int:
        return 65
    
    @property
    def atomic_mass(self) -> float:
        return 158.93
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f9 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 27, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.2
    
    @property
    def atomic_radius(self) -> float:
        return 175.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.864
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 3, 4]
    
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
        return {159: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1629.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3503.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.23
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1843
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Carl Gustaf Mosander"
    
    @property
    def symbol(self) -> str:
        return "Tb"
