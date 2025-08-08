from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ru(AtomicElement):
    """
    Ruthenium element (Ru, Z=44).
    """
    
    @property
    def name(self) -> str:
        return "Ruthenium"
    
    @property
    def atomic_number(self) -> int:
        return 44
    
    @property
    def atomic_mass(self) -> float:
        return 101.07
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d7 5s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 15, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.2
    
    @property
    def atomic_radius(self) -> float:
        return 178.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.361
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.05
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -2, 1, 2, 3, 4, 5, 6, 7, 8]
    
    @property
    def group(self) -> Optional[int]:
        return 8
    
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
        return {96: 0.0554, 98: 0.0187, 99: 0.1276, 100: 0.126, 101: 0.1706, 102: 0.3155, 104: 0.1862}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2607.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4423.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 12.45
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1844
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Karl Ernst Claus"
    
    @property
    def symbol(self) -> str:
        return "Ru"
