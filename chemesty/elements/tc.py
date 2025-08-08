from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Tc(AtomicElement):
    """
    Technetium element (Tc, Z=43).
    """
    
    @property
    def name(self) -> str:
        return "Technetium"
    
    @property
    def atomic_number(self) -> int:
        return 43
    
    @property
    def atomic_mass(self) -> float:
        return 98.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d5 5s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 13, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.9
    
    @property
    def atomic_radius(self) -> float:
        return 183.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.28
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.55
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -1, 1, 2, 3, 4, 5, 6, 7]
    
    @property
    def group(self) -> Optional[int]:
        return 7
    
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
        return {98: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2430.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4538.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 11.0
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1937
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Carlo Perrier, Emilio Segrè"
    
    @property
    def symbol(self) -> str:
        return "Tc"
