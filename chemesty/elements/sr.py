from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Sr(AtomicElement):
    """
    Strontium element (Sr, Z=38).
    """
    
    @property
    def name(self) -> str:
        return "Strontium"
    
    @property
    def atomic_number(self) -> int:
        return 38
    
    @property
    def atomic_mass(self) -> float:
        return 87.62
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 5s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 0.95
    
    @property
    def atomic_radius(self) -> float:
        return 219.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.695
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.05
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 2
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkaline earth metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {84: 0.0056, 86: 0.0986, 87: 0.07, 88: 0.8258}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1050.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1655.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 2.64
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1790
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Adair Crawford"
    
    @property
    def symbol(self) -> str:
        return "Sr"
