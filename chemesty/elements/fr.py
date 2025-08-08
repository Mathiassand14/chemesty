from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Fr(AtomicElement):
    """
    Francium element (Fr, Z=87).
    """
    
    @property
    def name(self) -> str:
        return "Francium"
    
    @property
    def atomic_number(self) -> int:
        return 87
    
    @property
    def atomic_mass(self) -> float:
        return 223.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 7s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 8, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 0.7
    
    @property
    def atomic_radius(self) -> float:
        return 260.0
    
    @property
    def ionization_energy(self) -> float:
        return 4.0
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.47
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1]
    
    @property
    def group(self) -> Optional[int]:
        return 1
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkali metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {223: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 300.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 950.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 1.87
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1939
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Marguerite Perey"
    
    @property
    def symbol(self) -> str:
        return "Fr"
