from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Y(AtomicElement):
    """
    Yttrium element (Y, Z=39).
    """
    
    @property
    def name(self) -> str:
        return "Yttrium"
    
    @property
    def atomic_number(self) -> int:
        return 39
    
    @property
    def atomic_mass(self) -> float:
        return 88.906
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d1 5s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.22
    
    @property
    def atomic_radius(self) -> float:
        return 212.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.217
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.307
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2, 3]
    
    @property
    def group(self) -> Optional[int]:
        return 3
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {89: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1799.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3609.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 4.47
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1794
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Johan Gadolin"
    
    @property
    def symbol(self) -> str:
        return "Y"
