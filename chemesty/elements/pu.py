from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Pu(AtomicElement):
    """
    Plutonium element (Pu, Z=94).
    """
    
    @property
    def name(self) -> str:
        return "Plutonium"
    
    @property
    def atomic_number(self) -> int:
        return 94
    
    @property
    def atomic_mass(self) -> float:
        return 244.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f6 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 24, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.28
    
    @property
    def atomic_radius(self) -> float:
        return 159.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.06
    
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
        return {244: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 912.5
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3505.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 19.816
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1940
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Glenn T. Seaborg, Arthur C. Wahl, Joseph W. Kennedy, Edwin McMillan"
    
    @property
    def symbol(self) -> str:
        return "Pu"
