from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Sc(AtomicElement):
    """
    Scandium element (Sc, Z=21).
    """
    
    @property
    def name(self) -> str:
        return "Scandium"
    
    @property
    def atomic_number(self) -> int:
        return 21
    
    @property
    def atomic_mass(self) -> float:
        return 44.956
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d1 4s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.36
    
    @property
    def atomic_radius(self) -> float:
        return 184.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.561
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.188
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2, 3]
    
    @property
    def group(self) -> Optional[int]:
        return 3
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {45: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1814.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3109.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 2.989
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1879
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Lars Fredrik Nilson"
    
    @property
    def symbol(self) -> str:
        return "Sc"
