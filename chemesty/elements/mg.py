from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Mg(AtomicElement):
    """
    Magnesium element (Mg, Z=12).
    """
    
    @property
    def name(self) -> str:
        return "Magnesium"
    
    @property
    def atomic_number(self) -> int:
        return 12
    
    @property
    def atomic_mass(self) -> float:
        return 24.305
    
    @property
    def electron_configuration(self) -> str:
        return "[Ne] 3s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.31
    
    @property
    def atomic_radius(self) -> float:
        return 145.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.646
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 2
    
    @property
    def period(self) -> int:
        return 3
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkaline earth metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {24: 0.7899, 25: 0.1, 26: 0.1101}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 923.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1363.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 1.738
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1808
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Humphry Davy"
    
    @property
    def symbol(self) -> str:
        return "Mg"
