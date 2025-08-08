from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ho(AtomicElement):
    """
    Holmium element (Ho, Z=67).
    """
    
    @property
    def name(self) -> str:
        return "Holmium"
    
    @property
    def atomic_number(self) -> int:
        return 67
    
    @property
    def atomic_mass(self) -> float:
        return 164.93
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f11 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 29, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.23
    
    @property
    def atomic_radius(self) -> float:
        return 175.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.022
    
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
        return {165: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1734.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2993.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.79
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1878
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Marc Delafontaine, Jacques-Louis Soret"
    
    @property
    def symbol(self) -> str:
        return "Ho"
