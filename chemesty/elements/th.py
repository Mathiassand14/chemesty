from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Th(AtomicElement):
    """
    Thorium element (Th, Z=90).
    """
    
    @property
    def name(self) -> str:
        return "Thorium"
    
    @property
    def atomic_number(self) -> int:
        return 90
    
    @property
    def atomic_mass(self) -> float:
        return 232.04
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 6d2 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 10, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.3
    
    @property
    def atomic_radius(self) -> float:
        return 180.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.08
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2, 3, 4]
    
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
        return {232: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2115.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 5061.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 11.72
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1829
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Jöns Jakob Berzelius"
    
    @property
    def symbol(self) -> str:
        return "Th"
