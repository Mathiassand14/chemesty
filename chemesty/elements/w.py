from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class W(AtomicElement):
    """
    Tungsten element (W, Z=74).
    """
    
    @property
    def name(self) -> str:
        return "Tungsten"
    
    @property
    def atomic_number(self) -> int:
        return 74
    
    @property
    def atomic_mass(self) -> float:
        return 183.84
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d4 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 12, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 2.36
    
    @property
    def atomic_radius(self) -> float:
        return 135.0
    
    @property
    def ionization_energy(self) -> float:
        return 7.98
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.815
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-4, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    
    @property
    def group(self) -> Optional[int]:
        return 6
    
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
        return {180: 0.0012, 182: 0.265, 183: 0.1431, 184: 0.3064, 186: 0.2843}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 3695.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 5828.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 19.25
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1783
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Fausto Elhuyar, Juan José Elhuyar"
    
    @property
    def symbol(self) -> str:
        return "W"
