from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Rb(AtomicElement):
    """
    Rubidium element (Rb, Z=37).
    """
    
    @property
    def name(self) -> str:
        return "Rubidium"
    
    @property
    def atomic_number(self) -> int:
        return 37
    
    @property
    def atomic_mass(self) -> float:
        return 85.468
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 5s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 8, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 0.82
    
    @property
    def atomic_radius(self) -> float:
        return 265.0
    
    @property
    def ionization_energy(self) -> float:
        return 4.177
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.468
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1]
    
    @property
    def group(self) -> Optional[int]:
        return 1
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkali metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {85: 0.7217, 87: 0.2783}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 312.46
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 961.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 1.532
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1861
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Robert Bunsen, Gustav Kirchhoff"
    
    @property
    def symbol(self) -> str:
        return "Rb"
