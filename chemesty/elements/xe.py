from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Xe(AtomicElement):
    """
    Xenon element (Xe, Z=54).
    """
    
    @property
    def name(self) -> str:
        return "Xenon"
    
    @property
    def atomic_number(self) -> int:
        return 54
    
    @property
    def atomic_mass(self) -> float:
        return 131.29
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10 5s2 5p6"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 8]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.6
    
    @property
    def atomic_radius(self) -> float:
        return 108.0
    
    @property
    def ionization_energy(self) -> float:
        return 12.13
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [0, 1, 2, 4, 6, 8]
    
    @property
    def group(self) -> Optional[int]:
        return 18
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "noble gas"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {124: 0.0009, 126: 0.0009, 128: 0.0192, 129: 0.2644, 130: 0.0408, 131: 0.2118, 132: 0.2689, 134: 0.1044, 136: 0.0887}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 161.4
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 165.03
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.005887
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1898
    
    @property
    def discoverer(self) -> Optional[str]:
        return "William Ramsay, Morris Travers"
    
    @property
    def symbol(self) -> str:
        return "Xe"
