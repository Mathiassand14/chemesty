from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class C(AtomicElement):
    """
    Carbon element (C, Z=6).
    """
    
    @property
    def name(self) -> str:
        return "Carbon"
    
    @property
    def atomic_number(self) -> int:
        return 6
    
    @property
    def atomic_mass(self) -> float:
        return 12.011
    
    @property
    def electron_configuration(self) -> str:
        return "[He] 2s2 2p2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 4]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.55
    
    @property
    def atomic_radius(self) -> float:
        return 70.0
    
    @property
    def ionization_energy(self) -> float:
        return 11.26
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.263
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 14
    
    @property
    def period(self) -> int:
        return 2
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "nonmetal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {12: 0.9893, 13: 0.0107, 14: 0.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 3823.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4300.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 2.267
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "C"
