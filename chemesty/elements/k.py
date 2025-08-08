from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class K(AtomicElement):
    """
    Potassium element (K, Z=19).
    """
    
    @property
    def name(self) -> str:
        return "Potassium"
    
    @property
    def atomic_number(self) -> int:
        return 19
    
    @property
    def atomic_mass(self) -> float:
        return 39.098
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 4s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 8, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 0.82
    
    @property
    def atomic_radius(self) -> float:
        return 243.0
    
    @property
    def ionization_energy(self) -> float:
        return 4.341
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.501
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1]
    
    @property
    def group(self) -> Optional[int]:
        return 1
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkali metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {39: 0.932581, 40: 0.000117, 41: 0.067302}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 336.53
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1032.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.862
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1807
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Humphry Davy"
    
    @property
    def symbol(self) -> str:
        return "K"
