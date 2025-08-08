from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Re(AtomicElement):
    """
    Rhenium element (Re, Z=75).
    """
    
    @property
    def name(self) -> str:
        return "Rhenium"
    
    @property
    def atomic_number(self) -> int:
        return 75
    
    @property
    def atomic_mass(self) -> float:
        return 186.21
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d5 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 13, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.9
    
    @property
    def atomic_radius(self) -> float:
        return 135.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.88
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.15
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -1, 0, 1, 2, 3, 4, 5, 6, 7]
    
    @property
    def group(self) -> Optional[int]:
        return 7
    
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
        return {185: 0.374, 187: 0.626}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 3459.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 5869.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 21.02
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1925
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Masataka Ogawa, Walter Noddack, Ida Tacke, Otto Berg"
    
    @property
    def symbol(self) -> str:
        return "Re"
