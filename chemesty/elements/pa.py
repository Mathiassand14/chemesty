from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Pa(AtomicElement):
    """
    Protactinium element (Pa, Z=91).
    """
    
    @property
    def name(self) -> str:
        return "Protactinium"
    
    @property
    def atomic_number(self) -> int:
        return 91
    
    @property
    def atomic_mass(self) -> float:
        return 231.04
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f2 6d1 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 20, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.5
    
    @property
    def atomic_radius(self) -> float:
        return 180.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.89
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [3, 4, 5]
    
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
        return {231: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1841.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4300.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 15.37
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1913
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Kasimir Fajans, Oswald Helmuth Göhring, Otto Hahn, Lise Meitner"
    
    @property
    def symbol(self) -> str:
        return "Pa"
