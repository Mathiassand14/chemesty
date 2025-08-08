from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Li(AtomicElement):
    """
    Lithium element (Li, Z=3).
    """
    
    @property
    def name(self) -> str:
        return "Lithium"
    
    @property
    def atomic_number(self) -> int:
        return 3
    
    @property
    def atomic_mass(self) -> float:
        return 6.94
    
    @property
    def electron_configuration(self) -> str:
        return "[He] 2s1"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 1]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 0.98
    
    @property
    def atomic_radius(self) -> float:
        return 167.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.392
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.618
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1]
    
    @property
    def group(self) -> Optional[int]:
        return 1
    
    @property
    def period(self) -> int:
        return 2
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkali metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {6: 0.0759, 7: 0.9241}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 453.69
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1615.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 0.534
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1817
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Johan August Arfwedson"
    
    @property
    def symbol(self) -> str:
        return "Li"
