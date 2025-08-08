from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Pb(AtomicElement):
    """
    Lead element (Pb, Z=82).
    """
    
    @property
    def name(self) -> str:
        return "Lead"
    
    @property
    def atomic_number(self) -> int:
        return 82
    
    @property
    def atomic_mass(self) -> float:
        return 207.2
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d10 6s2 6p2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 4]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.87
    
    @property
    def atomic_radius(self) -> float:
        return 180.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.417
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.364
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -2, -1, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 14
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "post-transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {204: 0.014, 206: 0.241, 207: 0.221, 208: 0.524}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 600.61
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2022.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 11.34
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "Pb"
