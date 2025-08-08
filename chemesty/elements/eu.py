from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Eu(AtomicElement):
    """
    Europium element (Eu, Z=63).
    """
    
    @property
    def name(self) -> str:
        return "Europium"
    
    @property
    def atomic_number(self) -> int:
        return 63
    
    @property
    def atomic_mass(self) -> float:
        return 151.96
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f7 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 25, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.2
    
    @property
    def atomic_radius(self) -> float:
        return 185.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.67
    
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
        return {151: 0.4781, 153: 0.5219}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1099.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1802.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 5.24
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1901
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Eugène-Anatole Demarçay"
    
    @property
    def symbol(self) -> str:
        return "Eu"
