from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Zr(AtomicElement):
    """
    Zirconium element (Zr, Z=40).
    """
    
    @property
    def name(self) -> str:
        return "Zirconium"
    
    @property
    def atomic_number(self) -> int:
        return 40
    
    @property
    def atomic_mass(self) -> float:
        return 91.224
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d2 5s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 10, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.33
    
    @property
    def atomic_radius(self) -> float:
        return 206.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.634
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.426
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 4
    
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
        return {90: 0.5145, 91: 0.1122, 92: 0.1715, 94: 0.1738, 96: 0.028}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2128.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4682.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 6.52
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1789
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Martin Heinrich Klaproth"
    
    @property
    def symbol(self) -> str:
        return "Zr"
