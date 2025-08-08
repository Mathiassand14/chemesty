from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Se(AtomicElement):
    """
    Selenium element (Se, Z=34).
    """
    
    @property
    def name(self) -> str:
        return "Selenium"
    
    @property
    def atomic_number(self) -> int:
        return 34
    
    @property
    def atomic_mass(self) -> float:
        return 78.971
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d10 4s2 4p4"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 6]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.55
    
    @property
    def atomic_radius(self) -> float:
        return 103.0
    
    @property
    def ionization_energy(self) -> float:
        return 9.752
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 2.02
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2, 4, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 16
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "nonmetal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {74: 0.0089, 76: 0.0937, 77: 0.0763, 78: 0.2377, 80: 0.4961, 82: 0.0873}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 494.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 958.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 4.81
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1817
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Jöns Jacob Berzelius, Johann Gottlieb Gahn"
    
    @property
    def symbol(self) -> str:
        return "Se"
