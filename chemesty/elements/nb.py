from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Nb(AtomicElement):
    """
    Niobium element (Nb, Z=41).
    """
    
    @property
    def name(self) -> str:
        return "Niobium"
    
    @property
    def atomic_number(self) -> int:
        return 41
    
    @property
    def atomic_mass(self) -> float:
        return 92.906
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d4 5s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 12, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.6
    
    @property
    def atomic_radius(self) -> float:
        return 198.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.759
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.893
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -1, 1, 2, 3, 4, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 5
    
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
        return {93: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2750.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 5017.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.57
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1801
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Charles Hatchett"
    
    @property
    def symbol(self) -> str:
        return "Nb"
