from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Er(AtomicElement):
    """
    Erbium element (Er, Z=68).
    """
    
    @property
    def name(self) -> str:
        return "Erbium"
    
    @property
    def atomic_number(self) -> int:
        return 68
    
    @property
    def atomic_mass(self) -> float:
        return 167.26
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f12 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 30, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.24
    
    @property
    def atomic_radius(self) -> float:
        return 175.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.108
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [3]
    
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
        return {162: 0.00139, 164: 0.01601, 166: 0.33503, 167: 0.22869, 168: 0.26978, 170: 0.1491}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1802.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3141.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 9.07
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1842
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Carl Gustaf Mosander"
    
    @property
    def symbol(self) -> str:
        return "Er"
