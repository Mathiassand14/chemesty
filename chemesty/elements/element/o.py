from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class O(AtomicElement):
    """
    Oxygen element (O, Z=8).
    """
    
    @property
    def name(self) -> str:
        return "Oxygen"
    
    @property
    def atomic_number(self) -> int:
        return 8
    
    @property
    def atomic_mass(self) -> float:
        return 15.999
    
    @property
    def electron_configuration(self) -> str:
        return "[He] 2s2 2p4"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 6]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 3.44
    
    @property
    def atomic_radius(self) -> float:
        return 60.0
    
    @property
    def ionization_energy(self) -> float:
        return 13.618
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 1.461
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-2, -1, 1, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 16
    
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
        return {16: 0.99757, 17: 0.00038, 18: 0.00205}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 54.36
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 90.2
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.001429
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1774
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Carl Wilhelm Scheele, Joseph Priestley"
    
    @property
    def symbol(self) -> str:
        return "O"
