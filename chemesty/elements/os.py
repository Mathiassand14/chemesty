from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Os(AtomicElement):
    """
    Osmium element (Os, Z=76).
    """
    
    @property
    def name(self) -> str:
        return "Osmium"
    
    @property
    def atomic_number(self) -> int:
        return 76
    
    @property
    def atomic_mass(self) -> float:
        return 190.23
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d6 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 14, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.2
    
    @property
    def atomic_radius(self) -> float:
        return 130.0
    
    @property
    def ionization_energy(self) -> float:
        return 8.7
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.1
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    @property
    def group(self) -> Optional[int]:
        return 8
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {184: 0.0002, 186: 0.0159, 187: 0.0196, 188: 0.1324, 189: 0.1615, 190: 0.2626, 192: 0.4078}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 3306.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 5285.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 22.59
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1803
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Smithson Tennant"
    
    @property
    def symbol(self) -> str:
        return "Os"
