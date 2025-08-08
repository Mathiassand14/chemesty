from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class B(AtomicElement):
    """
    Boron element (B, Z=5).
    """
    
    @property
    def name(self) -> str:
        return "Boron"
    
    @property
    def atomic_number(self) -> int:
        return 5
    
    @property
    def atomic_mass(self) -> float:
        return 10.81
    
    @property
    def electron_configuration(self) -> str:
        return "[He] 2s2 2p1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 3]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.04
    
    @property
    def atomic_radius(self) -> float:
        return 87.0
    
    @property
    def ionization_energy(self) -> float:
        return 8.298
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.277
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-5, -1, 1, 2, 3]
    
    @property
    def group(self) -> Optional[int]:
        return 13
    
    @property
    def period(self) -> int:
        return 2
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "metalloid"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {10: 0.199, 11: 0.801}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2349.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4200.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 2.34
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1808
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Joseph Louis Gay-Lussac, Louis Jacques Thénard, Humphry Davy"
    
    @property
    def symbol(self) -> str:
        return "B"
