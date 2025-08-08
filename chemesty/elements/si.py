from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Si(AtomicElement):
    """
    Silicon element (Si, Z=14).
    """
    
    @property
    def name(self) -> str:
        return "Silicon"
    
    @property
    def atomic_number(self) -> int:
        return 14
    
    @property
    def atomic_mass(self) -> float:
        return 28.085
    
    @property
    def electron_configuration(self) -> str:
        return "[Ne] 3s2 3p2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 4]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.9
    
    @property
    def atomic_radius(self) -> float:
        return 111.0
    
    @property
    def ionization_energy(self) -> float:
        return 8.152
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.385
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -3, -2, -1, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 14
    
    @property
    def period(self) -> int:
        return 3
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "metalloid"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {28: 0.92223, 29: 0.04685, 30: 0.03092}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1687.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3538.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 2.3296
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1824
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Jöns Jacob Berzelius"
    
    @property
    def symbol(self) -> str:
        return "Si"
