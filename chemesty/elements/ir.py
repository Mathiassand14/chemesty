from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ir(AtomicElement):
    """
    Iridium element (Ir, Z=77).
    """
    
    @property
    def name(self) -> str:
        return "Iridium"
    
    @property
    def atomic_number(self) -> int:
        return 77
    
    @property
    def atomic_mass(self) -> float:
        return 192.22
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d7 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 15, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.2
    
    @property
    def atomic_radius(self) -> float:
        return 135.0
    
    @property
    def ionization_energy(self) -> float:
        return 9.1
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.565
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    @property
    def group(self) -> Optional[int]:
        return 9
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {191: 0.373, 193: 0.627}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2719.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4701.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 22.56
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1803
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Smithson Tennant"
    
    @property
    def symbol(self) -> str:
        return "Ir"
