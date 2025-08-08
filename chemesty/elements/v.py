from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class V(AtomicElement):
    """
    Vanadium element (V, Z=23).
    """
    
    @property
    def name(self) -> str:
        return "Vanadium"
    
    @property
    def atomic_number(self) -> int:
        return 23
    
    @property
    def atomic_mass(self) -> float:
        return 50.942
    
    @property
    def electron_configuration(self) -> str:
        return "[Ar] 3d3 4s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 11, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.63
    
    @property
    def atomic_radius(self) -> float:
        return 171.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.746
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.525
    
    @property
    def oxidation_states(self) -> List[int]:
        return [-3, -1, 1, 2, 3, 4, 5]
    
    @property
    def group(self) -> Optional[int]:
        return 5
    
    @property
    def period(self) -> int:
        return 4
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {50: 0.0025, 51: 0.9975}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2183.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3680.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 6.11
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1801
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Andrés Manuel del Río"
    
    @property
    def symbol(self) -> str:
        return "V"
