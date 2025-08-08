from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Dy(AtomicElement):
    """
    Dysprosium element (Dy, Z=66).
    """
    
    @property
    def name(self) -> str:
        return "Dysprosium"
    
    @property
    def atomic_number(self) -> int:
        return 66
    
    @property
    def atomic_mass(self) -> float:
        return 162.5
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f10 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 28, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.22
    
    @property
    def atomic_radius(self) -> float:
        return 175.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.939
    
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
        return {156: 0.00056, 158: 0.00095, 160: 0.02329, 161: 0.18889, 162: 0.25475, 163: 0.24896, 164: 0.2826}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1680.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2840.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.54
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1886
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Paul Émile Lecoq de Boisbaudran"
    
    @property
    def symbol(self) -> str:
        return "Dy"
