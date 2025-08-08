from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Tm(AtomicElement):
    """
    Thulium element (Tm, Z=69).
    """
    
    @property
    def name(self) -> str:
        return "Thulium"
    
    @property
    def atomic_number(self) -> int:
        return 69
    
    @property
    def atomic_mass(self) -> float:
        return 168.93
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f13 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 31, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.25
    
    @property
    def atomic_radius(self) -> float:
        return 175.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.184
    
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
        return {169: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1818.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2223.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 9.32
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1879
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Per Teodor Cleve"
    
    @property
    def symbol(self) -> str:
        return "Tm"
