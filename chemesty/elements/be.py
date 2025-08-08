from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Be(AtomicElement):
    """
    Beryllium element (Be, Z=4).
    """
    
    @property
    def name(self) -> str:
        return "Beryllium"
    
    @property
    def atomic_number(self) -> int:
        return 4
    
    @property
    def atomic_mass(self) -> float:
        return 9.0122
    
    @property
    def electron_configuration(self) -> str:
        return "[He] 2s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.57
    
    @property
    def atomic_radius(self) -> float:
        return 112.0
    
    @property
    def ionization_energy(self) -> float:
        return 9.323
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 2
    
    @property
    def period(self) -> int:
        return 2
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkaline earth metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {9: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1560.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2742.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 1.85
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1798
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Louis Nicolas Vauquelin"
    
    @property
    def symbol(self) -> str:
        return "Be"
