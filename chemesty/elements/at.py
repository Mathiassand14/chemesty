from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class At(AtomicElement):
    """
    Astatine element (At, Z=85).
    """
    
    @property
    def name(self) -> str:
        return "Astatine"
    
    @property
    def atomic_number(self) -> int:
        return 85
    
    @property
    def atomic_mass(self) -> float:
        return 210.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d10 6s2 6p5"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 7]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.2
    
    @property
    def atomic_radius(self) -> float:
        return 150.0
    
    @property
    def ionization_energy(self) -> float:
        return 9.5
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 2.8
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-1, 1, 3, 5, 7]
    
    @property
    def group(self) -> Optional[int]:
        return 17
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "halogen"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {210: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 575.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 610.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.0
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1940
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Dale R. Corson, Kenneth Ross MacKenzie, Emilio Segrè"
    
    @property
    def symbol(self) -> str:
        return "At"
