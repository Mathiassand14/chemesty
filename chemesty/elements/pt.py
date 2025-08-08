from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Pt(AtomicElement):
    """
    Platinum element (Pt, Z=78).
    """
    
    @property
    def name(self) -> str:
        return "Platinum"
    
    @property
    def atomic_number(self) -> int:
        return 78
    
    @property
    def atomic_mass(self) -> float:
        return 195.08
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d9 6s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 17, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.28
    
    @property
    def atomic_radius(self) -> float:
        return 135.0
    
    @property
    def ionization_energy(self) -> float:
        return 9.0
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 2.128
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 10
    
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
        return {190: 0.00012, 192: 0.00782, 194: 0.32967, 195: 0.33832, 196: 0.25242, 198: 0.07163}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2041.4
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4098.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 21.45
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Pre-Columbian South American natives"
    
    @property
    def symbol(self) -> str:
        return "Pt"
