from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ga(AtomicElement):
    """
    Gallium element (Ga, Z=31).
    """
    
    @property
    def name(self) -> str:
        return "Gallium"
    
    @property
    def atomic_number(self) -> int:
        return 31
    
    @property
    def atomic_mass(self) -> float:
        return 69.723
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d10 4s2 4p1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 3]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.81
    
    @property
    def atomic_radius(self) -> float:
        return 136.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.999
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.3
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-5, -4, -3, -2, -1, 1, 2, 3]
    
    @property
    def group(self) -> Optional[int]:
        return 13
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "post-transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {69: 0.60108, 71: 0.39892}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 302.91
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2477.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 5.91
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1875
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Lecoq de Boisbaudran"
    
    @property
    def symbol(self) -> str:
        return "Ga"
