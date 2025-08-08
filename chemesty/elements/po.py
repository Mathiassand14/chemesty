from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Po(AtomicElement):
    """
    Polonium element (Po, Z=84).
    """
    
    @property
    def name(self) -> str:
        return "Polonium"
    
    @property
    def atomic_number(self) -> int:
        return 84
    
    @property
    def atomic_mass(self) -> float:
        return 209.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d10 6s2 6p4"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 6]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.0
    
    @property
    def atomic_radius(self) -> float:
        return 168.0
    
    @property
    def ionization_energy(self) -> float:
        return 8.417
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.9
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, 2, 4, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 16
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "post-transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {209: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 527.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1235.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 9.196
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1898
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Pierre Curie, Marie Curie"
    
    @property
    def symbol(self) -> str:
        return "Po"
