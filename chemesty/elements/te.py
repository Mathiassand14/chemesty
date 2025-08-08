from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Te(AtomicElement):
    """
    Tellurium element (Te, Z=52).
    """
    
    @property
    def name(self) -> str:
        return "Tellurium"
    
    @property
    def atomic_number(self) -> int:
        return 52
    
    @property
    def atomic_mass(self) -> float:
        return 127.6
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10 5s2 5p4"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 6]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.1
    
    @property
    def atomic_radius(self) -> float:
        return 123.0
    
    @property
    def ionization_energy(self) -> float:
        return 9.01
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.971
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 16
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "metalloid"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {120: 0.0009, 122: 0.0255, 123: 0.0089, 124: 0.0474, 125: 0.0707, 126: 0.1884, 128: 0.3174, 130: 0.3408}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 722.66
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1261.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 6.232
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1782
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Franz-Joseph Müller von Reichenstein"
    
    @property
    def symbol(self) -> str:
        return "Te"
