from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Lr(AtomicElement):
    """
    Lawrencium element (Lr, Z=103).
    """
    
    @property
    def name(self) -> str:
        return "Lawrencium"
    
    @property
    def atomic_number(self) -> int:
        return 103
    
    @property
    def atomic_mass(self) -> float:
        return 266.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f14 7s2 7p1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 32, 8, 3]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.3
    
    @property
    def atomic_radius(self) -> float:
        return 186.0
    
    @property
    def ionization_energy(self) -> float:
        return 4.9
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [3]
    
    @property
    def group(self) -> Optional[int]:
        return 3
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "actinide"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {266: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1900.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return None
    
    @property
    def density_value(self) -> Optional[float]:
        return None
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1961
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Albert Ghiorso, Torbjørn Sikkeland, Almon Larsh, Robert M. Latimer"
    
    @property
    def symbol(self) -> str:
        return "Lr"
