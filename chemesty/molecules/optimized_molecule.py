"""
Optimized molecule operations for improved performance.

This module provides optimized implementations of molecule operations
with caching, lazy evaluation, and performance enhancements.
"""

import functools
from typing import Dict, Optional, Any, Tuple
from collections import OrderedDict
import weakref
import threading

from chemesty.molecules.molecule import Molecule
from chemesty.elements.atomic_element import AtomicElement
from chemesty.utils.cache import cached_method, get_cache_manager
from chemesty.utils.profiling import profile_molecule_operation
from chemesty.utils.parallel_processing import get_molecule_processor


class OptimizedMolecule(Molecule):
    """
    Optimized version of the Molecule class with performance enhancements.
    
    Features:
    - Cached property calculations
    - Lazy evaluation of expensive operations
    - Optimized formula parsing
    - Memory-efficient storage
    """
    
    def __init__(self, formula: Optional[str] = None, smiles: Optional[str] = None):
        """Initialize optimized molecule with caching support."""
        super().__init__(formula, smiles)
        self._cache_id = id(self)
        self._property_cache = {}
        self._cache_lock = threading.RLock()
        
        # Pre-compute commonly used properties
        self._cached_molecular_weight = None
        self._cached_formula = None
        self._cached_composition = None
    
    @cached_method(cache_type='molecule')
    @profile_molecule_operation('molecular_weight_optimized')
    def molecular_weight(self) -> float:
        """Optimized molecular weight calculation with caching."""
        if self._cached_molecular_weight is not None:
            return self._cached_molecular_weight
        
        # Use parent implementation but cache result
        weight = super().molecular_weight
        self._cached_molecular_weight = weight
        return weight
    
    @cached_method(cache_type='molecule')
    @profile_molecule_operation('molecular_formula_optimized')
    def molecular_formula(self) -> str:
        """Optimized molecular formula generation with caching."""
        if self._cached_formula is not None:
            return self._cached_formula
        
        formula = super().molecular_formula
        self._cached_formula = formula
        return formula
    
    @cached_method(cache_type='molecule')
    @profile_molecule_operation('composition_optimized')
    def composition(self) -> Dict[AtomicElement, int]:
        """Optimized composition calculation with caching."""
        if self._cached_composition is not None:
            return self._cached_composition.copy()
        
        composition = self._elements.copy()
        self._cached_composition = composition
        return composition
    
    @profile_molecule_operation('add_element_optimized')
    def add_element(self, element: AtomicElement, quantity: int = 1) -> None:
        """Optimized element addition with cache invalidation."""
        super().add_element(element, quantity)
        self._invalidate_cache()
    
    @profile_molecule_operation('remove_element_optimized')
    def remove_element(self, element: AtomicElement, quantity: Optional[int] = None) -> None:
        """Optimized element removal with cache invalidation."""
        super().remove_element(element, quantity)
        self._invalidate_cache()
    
    def _invalidate_cache(self) -> None:
        """Invalidate cached properties when molecule changes."""
        with self._cache_lock:
            self._cached_molecular_weight = None
            self._cached_formula = None
            self._cached_composition = None
            self._property_cache.clear()
    
    @profile_molecule_operation('batch_property_calculation')
    def calculate_properties_batch(self, properties: list[str]) -> Dict[str, Any]:
        """
        Calculate multiple properties in a single operation for efficiency.
        
        Args:
            properties: List of property names to calculate
            
        Returns:
            Dictionary of property values
        """
        results = {}
        
        # Group properties by calculation type to minimize redundant work
        basic_props = {'molecular_weight', 'molecular_formula', 'atom_count', 'element_count'}
        volume_props = {'volume', 'density', 'molar_volume'}
        
        requested_basic = [p for p in properties if p in basic_props]
        requested_volume = [p for p in properties if p in volume_props]
        
        # Calculate basic properties
        if requested_basic:
            if 'molecular_weight' in requested_basic:
                results['molecular_weight'] = self.molecular_weight
            if 'molecular_formula' in requested_basic:
                results['molecular_formula'] = self.molecular_formula
            if 'atom_count' in requested_basic:
                results['atom_count'] = self.atom_count
            if 'element_count' in requested_basic:
                results['element_count'] = self.element_count
        
        # Calculate volume-related properties together
        if requested_volume:
            volume_val = self.volume_value
            if volume_val is not None:
                if 'volume' in requested_volume:
                    results['volume'] = volume_val
                if 'density' in requested_volume:
                    results['density'] = self.density_value
                if 'molar_volume' in requested_volume:
                    results['molar_volume'] = self.molar_volume
        
        return results


class MoleculeFactory:
    """
    Factory for creating optimized molecules with caching and reuse.
    """
    
    def __init__(self, cache_size: int = 1000):
        """Initialize the molecule factory with caching."""
        self._cache = {}
        self._cache_size = cache_size
        self._access_order = []
        self._lock = threading.RLock()
    
    @profile_molecule_operation('factory_create_molecule')
    def create_molecule(self, formula: Optional[str] = None, 
                       smiles: Optional[str] = None,
                       use_cache: bool = True) -> OptimizedMolecule:
        """
        Create a molecule with optional caching.
        
        Args:
            formula: Molecular formula
            smiles: SMILES string
            use_cache: Whether to use caching
            
        Returns:
            OptimizedMolecule instance
        """
        if not use_cache:
            return OptimizedMolecule(formula, smiles)
        
        # Create cache key
        cache_key = f"formula:{formula}" if formula else f"smiles:{smiles}"
        
        with self._lock:
            # Check cache
            if cache_key in self._cache:
                # Move to end of access order
                self._access_order.remove(cache_key)
                self._access_order.append(cache_key)
                
                # Return a copy to avoid shared state issues
                cached_mol = self._cache[cache_key]
                new_mol = OptimizedMolecule()
                new_mol._elements = cached_mol._elements.copy()
                new_mol._cached_molecular_weight = cached_mol._cached_molecular_weight
                new_mol._cached_formula = cached_mol._cached_formula
                new_mol._cached_composition = cached_mol._cached_composition
                return new_mol
            
            # Create new molecule
            mol = OptimizedMolecule(formula, smiles)
            
            # Add to cache
            self._cache[cache_key] = mol
            self._access_order.append(cache_key)
            
            # Evict oldest if cache is full
            if len(self._cache) > self._cache_size:
                oldest_key = self._access_order.pop(0)
                del self._cache[oldest_key]
            
            return mol
    
    def clear_cache(self) -> None:
        """Clear the molecule cache."""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            return {
                'cache_size': len(self._cache),
                'max_cache_size': self._cache_size,
                'cache_keys': list(self._cache.keys())
            }


class BatchMoleculeProcessor:
    """
    Processor for handling multiple molecules efficiently in batch operations.
    """
    
    def __init__(self):
        """Initialize the batch processor."""
        self.factory = MoleculeFactory()
    
    @profile_molecule_operation('batch_create_molecules')
    def create_molecules_batch(self, formulas: list[str]) -> list[OptimizedMolecule]:
        """
        Create multiple molecules in batch for better performance using parallel processing.
        
        Args:
            formulas: List of molecular formulas
            
        Returns:
            List of OptimizedMolecule instances
        """
        if not formulas:
            return []
        
        # Use parallel processing for large batches
        if len(formulas) > 10:
            processor = get_molecule_processor()
            results = processor.create_molecules_parallel(formulas)
            # Filter out None results from failed creations
            return [mol for mol in results if mol is not None]
        
        # Use sequential processing for small batches
        molecules = []
        
        # Pre-sort formulas to improve cache locality
        sorted_formulas = sorted(formulas)
        
        for formula in sorted_formulas:
            try:
                mol = self.factory.create_molecule(formula=formula)
                molecules.append(mol)
            except Exception as e:
                # Log error but continue processing
                print(f"Warning: Failed to create molecule for formula {formula}: {e}")
                continue
        
        return molecules
    
    @profile_molecule_operation('batch_calculate_properties')
    def calculate_properties_batch(self, molecules: list[OptimizedMolecule], 
                                 properties: list[str]) -> list[Dict[str, Any]]:
        """
        Calculate properties for multiple molecules in batch using parallel processing.
        
        Args:
            molecules: List of molecules
            properties: List of property names
            
        Returns:
            List of property dictionaries
        """
        if not molecules:
            return []
        
        # Use parallel processing for large batches
        if len(molecules) > 10:
            processor = get_molecule_processor()
            results = processor.calculate_properties_parallel(molecules, properties)
            return results
        
        # Use sequential processing for small batches
        results = []
        
        for mol in molecules:
            try:
                props = mol.calculate_properties_batch(properties)
                results.append(props)
            except Exception as e:
                # Log error but continue processing
                print(f"Warning: Failed to calculate properties for molecule: {e}")
                results.append({})
        
        return results
    
    @profile_molecule_operation('batch_molecular_weights')
    def get_molecular_weights_batch(self, molecules: list[OptimizedMolecule]) -> list[float]:
        """
        Get molecular weights for multiple molecules efficiently using parallel processing.
        
        Args:
            molecules: List of molecules
            
        Returns:
            List of molecular weights
        """
        if not molecules:
            return []
        
        # Use parallel processing for large batches
        if len(molecules) > 10:
            processor = get_molecule_processor()
            return processor.batch_molecular_weight_calculation(molecules)
        
        # Use sequential processing for small batches
        weights = []
        for mol in molecules:
            try:
                weight = mol.molecular_weight
                weights.append(weight)
            except Exception as e:
                print(f"Warning: Failed to calculate molecular weight: {e}")
                weights.append(0.0)
        
        return weights


# Global instances
_molecule_factory: Optional[MoleculeFactory] = None
_batch_processor: Optional[BatchMoleculeProcessor] = None


def get_molecule_factory() -> MoleculeFactory:
    """Get the global molecule factory instance."""
    global _molecule_factory
    if _molecule_factory is None:
        _molecule_factory = MoleculeFactory()
    return _molecule_factory


def get_batch_processor() -> BatchMoleculeProcessor:
    """Get the global batch processor instance."""
    global _batch_processor
    if _batch_processor is None:
        _batch_processor = BatchMoleculeProcessor()
    return _batch_processor


# Convenience functions
def create_optimized_molecule(formula: Optional[str] = None, 
                            smiles: Optional[str] = None) -> OptimizedMolecule:
    """Create an optimized molecule using the global factory."""
    factory = get_molecule_factory()
    return factory.create_molecule(formula, smiles)


def create_molecules_batch(formulas: list[str]) -> list[OptimizedMolecule]:
    """Create multiple molecules in batch using the global processor."""
    processor = get_batch_processor()
    return processor.create_molecules_batch(formulas)