from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Rf(AtomicElement):
    """
    Rutherfordium element (Rf, Z=104).
    """
    
    @property
    def name(self) -> str:
        return "Rutherfordium"
    
    @property
    def atomic_number(self) -> int:
        return 104
    
    @property
    def atomic_mass(self) -> float:
        return 267.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f14 6d2 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 32, 10, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 157.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.0
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [4]
    
    @property
    def group(self) -> Optional[int]:
        return 4
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {267: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2400.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 5800.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 23.2
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1964
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Joint Institute for Nuclear Research, Lawrence Berkeley National Laboratory"
    
    @property
    def symbol(self) -> str:
        return "Rf"
