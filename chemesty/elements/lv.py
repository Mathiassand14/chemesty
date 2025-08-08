from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Lv(AtomicElement):
    """
    Livermorium element (Lv, Z=116).
    """
    
    @property
    def name(self) -> str:
        return "Livermorium"
    
    @property
    def atomic_number(self) -> int:
        return 116
    
    @property
    def atomic_mass(self) -> float:
        return 293.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f14 6d10 7s2 7p4"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 32, 18, 6]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 175.0
    
    @property
    def ionization_energy(self) -> float:
        return None
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return None
    
    @property
    def oxidation_states(self) -> List[int]:
        return [2, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 16
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "p"
    
    @property
    def category(self) -> str:
        return "post-transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {293: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 709.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1085.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 12.9
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 2000
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Joint Institute for Nuclear Research, Lawrence Livermore National Laboratory"
    
    @property
    def symbol(self) -> str:
        return "Lv"
