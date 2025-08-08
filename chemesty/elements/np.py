from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Np(AtomicElement):
    """
    Neptunium element (Np, Z=93).
    """
    
    @property
    def name(self) -> str:
        return "Neptunium"
    
    @property
    def atomic_number(self) -> int:
        return 93
    
    @property
    def atomic_mass(self) -> float:
        return 237.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f4 6d1 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 22, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.36
    
    @property
    def atomic_radius(self) -> float:
        return 155.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.266
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [3, 4, 5, 6, 7]
    
    @property
    def group(self) -> Optional[int]:
        return None
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "f"
    
    @property
    def category(self) -> str:
        return "actinide"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {237: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 912.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4447.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 20.45
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1940
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Edwin McMillan, Philip H. Abelson"
    
    @property
    def symbol(self) -> str:
        return "Np"
