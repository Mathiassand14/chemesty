from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Hg(AtomicElement):
    """
    Mercury element (Hg, Z=80).
    """
    
    @property
    def name(self) -> str:
        return "Mercury"
    
    @property
    def atomic_number(self) -> int:
        return 80
    
    @property
    def atomic_mass(self) -> float:
        return 200.59
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d10 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 18, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.0
    
    @property
    def atomic_radius(self) -> float:
        return 150.0
    
    @property
    def ionization_energy(self) -> float:
        return 10.438
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 12
    
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
        return {196: 0.0015, 198: 0.0997, 199: 0.1687, 200: 0.231, 201: 0.1318, 202: 0.2986, 204: 0.0687}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 234.32
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 629.88
    
    @property
    def density_value(self) -> Optional[float]:
        return 13.5336
    
    @property
    def year_discovered(self) -> Optional[int]:
        return None
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Prehistoric"
    
    @property
    def symbol(self) -> str:
        return "Hg"
