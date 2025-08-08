from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Nd(AtomicElement):
    """
    Neodymium element (Nd, Z=60).
    """
    
    @property
    def name(self) -> str:
        return "Neodymium"
    
    @property
    def atomic_number(self) -> int:
        return 60
    
    @property
    def atomic_mass(self) -> float:
        return 144.24
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f4 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 22, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.14
    
    @property
    def atomic_radius(self) -> float:
        return 185.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.525
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return None
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "f"
    
    @property
    def category(self) -> str:
        return "lanthanide"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {142: 0.272, 143: 0.122, 144: 0.238, 145: 0.083, 146: 0.172, 148: 0.057, 150: 0.056}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1297.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3347.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.01
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1885
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Carl Auer von Welsbach"
    
    @property
    def symbol(self) -> str:
        return "Nd"
