from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class He(AtomicElement):
    """
    Helium element (He, Z=2).
    """
    
    @property
    def name(self) -> str:
        return "Helium"
    
    @property
    def atomic_number(self) -> int:
        return 2
    
    @property
    def atomic_mass(self) -> float:
        return 4.0026
    
    @property
    def electron_configuration(self) -> str:
        return "1s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 31.0
    
    @property
    def ionization_energy(self) -> float:
        return 24.587
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return None
    
    @property
    def oxidation_states(self) -> List[int]:
        return [0]
    
    @property
    def group(self) -> Optional[int]:
        return 18
    
    @property
    def period(self) -> int:
        return 1
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "noble gas"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {3: 1e-06, 4: 0.999999}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 0.95
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4.22
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.0001785
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1868
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Pierre Janssen, Norman Lockyer"
    
    @property
    def symbol(self) -> str:
        return "He"
