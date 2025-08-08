from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Fl(AtomicElement):
    """
    Flerovium element (Fl, Z=114).
    """
    
    @property
    def name(self) -> str:
        return "Flerovium"
    
    @property
    def atomic_number(self) -> int:
        return 114
    
    @property
    def atomic_mass(self) -> float:
        return 289.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f14 6d10 7s2 7p2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 32, 18, 4]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return None
    
    @property
    def atomic_radius(self) -> float:
        return 143.0
    
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
        return 14
    
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
        return {289: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 340.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 420.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 14.0
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1998
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Joint Institute for Nuclear Research, Lawrence Livermore National Laboratory"
    
    @property
    def symbol(self) -> str:
        return "Fl"
