from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Zn(AtomicElement):
    """
    Zinc element (Zn, Z=30).
    """
    
    @property
    def name(self) -> str:
        return "Zinc"
    
    @property
    def atomic_number(self) -> int:
        return 30
    
    @property
    def atomic_mass(self) -> float:
        return 65.38
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d10 4s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.65
    
    @property
    def atomic_radius(self) -> float:
        return 142.0
    
    @property
    def ionization_energy(self) -> float:
        return 9.394
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, 1, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 12
    
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
        return {64: 0.4917, 66: 0.2773, 67: 0.0404, 68: 0.1845, 70: 0.0061}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 692.68
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1180.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.134
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Indian metallurgists (before 1000 BCE)"
    
    @property
    def symbol(self) -> str:
        return "Zn"
