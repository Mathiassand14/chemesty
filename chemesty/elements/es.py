from typing import Optional, List, Dict
from chemesty.elements.atomic_element import AtomicElement

class Es(AtomicElement):
    """
    Einsteinium element (Es, Z=99).
    """
    
    @property
    def name(self) -> str:
        return "Einsteinium"
    
    @property
    def atomic_number(self) -> int:
        return 99
    
    @property
    def atomic_mass(self) -> float:
        return 252.0
    
    @property
    def electron_configuration(self) -> str:
        return "[Rn] 5f11 7s2"
    
    @property
    def electron_shells(self) -> List[int]:
        return [2, 8, 18, 32, 29, 8, 2]
    
    @property
    def electronegativity(self) -> Optional[float]:
        return 1.3
    
    @property
    def atomic_radius(self) -> float:
        return 186.0
    
    @property
    def ionization_energy(self) -> float:
        return 6.42
    
    @property
    def electron_affinity(self) -> Optional[float]:
        return 0.0
    
    @property
    def oxidation_states(self) -> List[int]:
        return [2, 3, 4]
    
    @property
    def group(self) -> Optional[int]:
        return None
    
    @property
    def period(self) -> int:
        return 7
    
    @property
    def block(self) -> str:
        return "f"
    
    @property
    def category(self) -> str:
        return "actinide"
    
    @property
    def isotopes(self) -> Dict[int, float]:
        return {252: 1.0}
    
    @property
    def melting_point(self) -> Optional[float]:
        return 1133.0
    
    @property
    def boiling_point(self) -> Optional[float]:
        return 1269.0
    
    @property
    def density_value(self) -> Optional[float]:
        return 8.84
    
    @property
    def year_discovered(self) -> Optional[int]:
        return 1952
    
    @property
    def discoverer(self) -> Optional[str]:
        return "Albert Ghiorso, Glenn T. Seaborg"
    
    @property
    def symbol(self) -> str:
        return "Es"
