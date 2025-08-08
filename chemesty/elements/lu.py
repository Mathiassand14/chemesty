from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Lu(AtomicElement):
    """
    Lutetium element (Lu, Z=71).
    """
    
    @property
    def name(self) -> str:
        return "Lutetium"
    
    @property
    def atomic_number(self) -> int:
        return 71
    
    @property
    def atomic_mass(self) -> float:
        return 174.97
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 4f14 5d1 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 9, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.27
    
    @property
    def atomic_radius(self) -> float:
        return 175.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.426
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.5
    
    @property
    def oxidation_states(self) -> List[int]:
        return [3]
    
    @property
    def group(self) -> Optional[int]:
        return 3
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "lanthanide"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {175: 0.9741, 176: 0.0259}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1925.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 3675.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 9.84
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1907
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Georges Urbain, Carl Auer von Welsbach"
    
    @property
    def symbol(self) -> str:
        return "Lu"
