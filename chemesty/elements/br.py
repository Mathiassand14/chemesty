from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Br(AtomicElement):
    """
    Bromine element (Br, Z=35).
    """
    
    @property
    def name(self) -> str:
        return "Bromine"
    
    @property
    def atomic_number(self) -> int:
        return 35
    
    @property
    def atomic_mass(self) -> float:
        return 79.904
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d10 4s2 4p5"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 7]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.96
    
    @property
    def atomic_radius(self) -> float:
        return 94.0
    
    @property
    def ionization_energy(self) -> float:
        return 11.814
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 3.365
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1, 3, 4, 5, 7]
    
    @property
    def group(self) -> Optional[int]:
        return 17
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "halogen"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {79: 0.5069, 81: 0.4931}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 265.8
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 332.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 3.1028
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1826
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Antoine Jérôme Balard, Carl Jacob Löwig"
    
    @property
    def symbol(self) -> str:
        return "Br"
