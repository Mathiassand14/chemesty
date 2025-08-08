from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Ba(AtomicElement):
    """
    Barium element (Ba, Z=56).
    """
    
    @property
    def name(self) -> str:
        return "Barium"
    
    @property
    def atomic_number(self) -> int:
        return 56
    
    @property
    def atomic_mass(self) -> float:
        return 137.33
    
    @property
    def electron_configuration(self) -> str:
        return "[Xe] 6s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 18, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 0.89
    
    @property
    def atomic_radius(self) -> float:
        return 253.0
    
    @property
    def ionization_energy(self) -> float:
        return 5.212
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.14
    
    @property
    def oxidation_states(self) -> List[int]:
        return [1, 2]
    
    @property
    def group(self) -> Optional[int]:
        return 2
    
    @property
    def period(self) -> int:
        return 6
    
    @property
    def block(self) -> str:
        return "s"
    
    @property
    def category(self) -> str:
        return "alkaline earth metal"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {130: 0.00106, 132: 0.00101, 134: 0.02417, 135: 0.06592, 136: 0.07854, 137: 0.11232, 138: 0.71698}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1000.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 2170.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 3.51
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1808
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Humphry Davy"
    
    @property
    def symbol(self) -> str:
        return "Ba"
