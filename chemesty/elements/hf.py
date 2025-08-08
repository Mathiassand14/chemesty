from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Hf(AtomicElement):
    """
    Hafnium element (Hf, Z=72).
    """
    
    @property
    def name(self) -> str:
        return "Hafnium"
    
    @property
    def atomic_number(self) -> int:
        return 72
    
    @property
    def atomic_mass(self) -> float:
        return 178.49
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d2 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 10, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.3
    
    @property
    def atomic_radius(self) -> float:
        return 155.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.825
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return 4
    
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
        return {174: 0.0016, 176: 0.0526, 177: 0.186, 178: 0.2728, 179: 0.1362, 180: 0.3508}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 2506.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 4876.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 13.31
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1923
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Dirk Coster, George de Hevesy"
    
    @property
    def symbol(self) -> str:
        return "Hf"
