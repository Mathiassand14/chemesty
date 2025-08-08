from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Sm(AtomicElement):
    """
    Samarium element (Sm, Z=62).
    """
    
    @property
    def name(self) -> str:
        return "Samarium"
    
    @property
    def atomic_number(self) -> int:
        return 62
    
    @property
    def atomic_mass(self) -> float:
        return 150.36
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f6 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 24, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.17
    
    @property
    def atomic_radius(self) -> float:
        return 185.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.644
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [2, 3]
    
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
        return {144: 0.0307, 147: 0.1499, 148: 0.1124, 149: 0.1382, 150: 0.0738, 152: 0.2675, 154: 0.2275}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1345.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2067.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 7.52
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1879
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Paul Émile Lecoq de Boisbaudran"
    
    @property
    def symbol(self) -> str:
        return "Sm"
