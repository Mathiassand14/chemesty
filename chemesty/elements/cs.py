from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Cs(AtomicElement):
    """
    Cesium element (Cs, Z=55).
    """
    
    @property
    def name(self) -> str:
        return "Cesium"
    
    @property
    def atomic_number(self) -> int:
        return 55
    
    @property
    def atomic_mass(self) -> float:
        return 132.91
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 6s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 8, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 0.79
    
    @property
    def atomic_radius(self) -> float:
        return 298.0
    
    @property
    def ionization_energy(self) -> float:
        return 3.894
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.472
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1]
    
    @property
    def group(self) -> Optional[int]:
        return 1
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkali metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {133: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 301.59
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 944.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 1.93
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1860
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Robert Bunsen, Gustav Kirchhoff"
    
    @property
    def symbol(self) -> str:
        return "Cs"
