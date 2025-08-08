from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ce(AtomicElement):
    """
    Cerium element (Ce, Z=58).
    """
    
    @property
    def name(self) -> str:
        return "Cerium"
    
    @property
    def atomic_number(self) -> int:
        return 58
    
    @property
    def atomic_mass(self) -> float:
        return 140.12
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f1 5d1 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 19, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.12
    
    @property
    def atomic_radius(self) -> float:
        return 185.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.539
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [2, 3, 4]
    
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
        return {136: 0.00185, 138: 0.00251, 140: 0.8845, 142: 0.11114}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1068.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3716.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 6.77
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1803
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Jöns Jakob Berzelius, Wilhelm Hisinger, Martin Heinrich Klaproth"
    
    @property
    def symbol(self) -> str:
        return "Ce"
