from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Cd(AtomicElement):
    """
    Cadmium element (Cd, Z=48).
    """
    
    @property
    def name(self) -> str:
        return "Cadmium"
    
    @property
    def atomic_number(self) -> int:
        return 48
    
    @property
    def atomic_mass(self) -> float:
        return 112.41
    
    @property
    def electron_configuration(self) -> str:
        return "[Kr] 4d10 5s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.69
    
    @property
    def atomic_radius(self) -> float:
        return 161.0
    
    @property
    def ionization_energy(self) -> float:
        return 8.994
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 12
    
    @property
    def period(self) -> int:
        return 5
    
    @property
    def block(self) -> str:
        return "d"
    
    @property
    def category(self) -> str:
        return "transition metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {106: 0.0125, 108: 0.0089, 110: 0.1249, 111: 0.128, 112: 0.2413, 113: 0.1222, 114: 0.2873, 116: 0.0749}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 594.22
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1040.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.65
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1817
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Friedrich Stromeyer, Karl Samuel Leberecht Hermann"
    
    @property
    def symbol(self) -> str:
        return "Cd"
