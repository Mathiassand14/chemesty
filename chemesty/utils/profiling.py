"""
Profiling utilities for performance analysis in Chemesty.

This module provides tools for profiling and benchmarking chemical operations
to identify performance bottlenecks and optimize critical code paths.
"""

import time
import cProfile
import pstats
import io
import functools
import threading
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from collections import defaultdict
import logging
from pathlib import Path


@dataclass
class ProfileResult:
    """Result of a profiling operation."""
    function_name: str
    execution_time: float
    memory_usage: Optional[float] = None
    call_count: int = 1
    args_info: str = ""
    timestamp: float = field(default_factory=time.time)


class PerformanceProfiler:
    """
    Performance profiler for tracking execution times and identifying bottlenecks.
    """
    
    def __init__(self):
        """Initialize the profiler."""
        self._results: Dict[str, List[ProfileResult]] = defaultdict(list)
        self._lock = threading.Lock()
        self.logger = logging.getLogger('chemesty.profiling')
        self._enabled = True
    
    def enable(self) -> None:
        """Enable profiling."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable profiling."""
        self._enabled = False
    
    def profile_function(self, func_name: Optional[str] = None):
        """
        Decorator to profile function execution time.
        
        Args:
            func_name: Optional custom name for the function
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self._enabled:
                    return func(*args, **kwargs)
                
                name = func_name or f"{func.__module__}.{func.__name__}"
                start_time = time.perf_counter()
                
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.perf_counter() - start_time
                    
                    # Create args info (truncated for readability)
                    args_str = str(args)[:100] + "..." if len(str(args)) > 100 else str(args)
                    kwargs_str = str(kwargs)[:100] + "..." if len(str(kwargs)) > 100 else str(kwargs)
                    args_info = f"args={args_str}, kwargs={kwargs_str}"
                    
                    profile_result = ProfileResult(
                        function_name=name,
                        execution_time=execution_time,
                        args_info=args_info
                    )
                    
                    with self._lock:
                        self._results[name].append(profile_result)
                    
                    return result
                    
                except Exception as e:
                    execution_time = time.perf_counter() - start_time
                    self.logger.error(f"Function {name} failed after {execution_time:.4f}s: {e}")
                    raise
            
            return wrapper
        return decorator
    
    def time_operation(self, operation_name: str, operation: Callable, *args, **kwargs) -> Any:
        """
        Time a specific operation.
        
        Args:
            operation_name: Name of the operation
            operation: Function to execute
            *args: Arguments for the operation
            **kwargs: Keyword arguments for the operation
            
        Returns:
            Result of the operation
        """
        if not self._enabled:
            return operation(*args, **kwargs)
        
        start_time = time.perf_counter()
        try:
            result = operation(*args, **kwargs)
            execution_time = time.perf_counter() - start_time
            
            profile_result = ProfileResult(
                function_name=operation_name,
                execution_time=execution_time,
                args_info=f"args={args}, kwargs={kwargs}"
            )
            
            with self._lock:
                self._results[operation_name].append(profile_result)
            
            return result
            
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            self.logger.error(f"Operation {operation_name} failed after {execution_time:.4f}s: {e}")
            raise
    
    def get_stats(self, function_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get profiling statistics.
        
        Args:
            function_name: Optional specific function name to get stats for
            
        Returns:
            Dictionary containing profiling statistics
        """
        with self._lock:
            if function_name:
                if function_name not in self._results:
                    return {}
                
                results = self._results[function_name]
                times = [r.execution_time for r in results]
                
                return {
                    'function_name': function_name,
                    'call_count': len(results),
                    'total_time': sum(times),
                    'average_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'recent_calls': results[-10:]  # Last 10 calls
                }
            else:
                # Return stats for all functions
                stats = {}
                for func_name, results in self._results.items():
                    times = [r.execution_time for r in results]
                    stats[func_name] = {
                        'call_count': len(results),
                        'total_time': sum(times),
                        'average_time': sum(times) / len(times),
                        'min_time': min(times),
                        'max_time': max(times)
                    }
                
                return stats
    
    def get_slowest_functions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the slowest functions by average execution time.
        
        Args:
            limit: Maximum number of functions to return
            
        Returns:
            List of function statistics sorted by average time
        """
        stats = self.get_stats()
        sorted_stats = sorted(
            stats.items(),
            key=lambda x: x[1]['average_time'],
            reverse=True
        )
        
        return [
            {'function_name': name, **data}
            for name, data in sorted_stats[:limit]
        ]
    
    def clear_results(self) -> None:
        """Clear all profiling results."""
        with self._lock:
            self._results.clear()
    
    def export_results(self, filepath: Union[str, Path]) -> None:
        """
        Export profiling results to a file.
        
        Args:
            filepath: Path to export file
        """
        import json
        
        filepath = Path(filepath)
        stats = self.get_stats()
        
        # Convert to JSON-serializable format
        export_data = {
            'timestamp': time.time(),
            'total_functions': len(stats),
            'statistics': stats
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        self.logger.info(f"Exported profiling results to {filepath}")


class MoleculeProfiler:
    """
    Specialized profiler for molecule operations.
    """
    
    def __init__(self):
        """Initialize the molecule profiler."""
        self.profiler = PerformanceProfiler()
        self.logger = logging.getLogger('chemesty.profiling.molecule')
    
    def profile_molecule_creation(self, creation_func: Callable, *args, **kwargs) -> Any:
        """Profile molecule creation operations."""
        return self.profiler.time_operation(
            "molecule_creation",
            creation_func,
            *args, **kwargs
        )
    
    def profile_property_calculation(self, property_name: str, calc_func: Callable, *args, **kwargs) -> Any:
        """Profile molecular property calculations."""
        return self.profiler.time_operation(
            f"property_calculation_{property_name}",
            calc_func,
            *args, **kwargs
        )
    
    def profile_formula_parsing(self, parse_func: Callable, formula: str) -> Any:
        """Profile formula parsing operations."""
        return self.profiler.time_operation(
            "formula_parsing",
            parse_func,
            formula
        )
    
    def benchmark_molecule_operations(self, molecule_formulas: List[str]) -> Dict[str, Any]:
        """
        Benchmark various molecule operations on a set of formulas.
        
        Args:
            molecule_formulas: List of molecular formulas to test
            
        Returns:
            Benchmark results
        """
        from chemesty.molecules.molecule import Molecule
        
        results = {
            'creation_times': [],
            'molecular_weight_times': [],
            'formula_parsing_times': [],
            'total_molecules': len(molecule_formulas)
        }
        
        for formula in molecule_formulas:
            # Benchmark molecule creation
            start_time = time.perf_counter()
            try:
                mol = Molecule(formula=formula)
                creation_time = time.perf_counter() - start_time
                results['creation_times'].append(creation_time)
                
                # Benchmark molecular weight calculation
                start_time = time.perf_counter()
                mol.molecular_weight
                mw_time = time.perf_counter() - start_time
                results['molecular_weight_times'].append(mw_time)
                
            except Exception as e:
                self.logger.warning(f"Failed to benchmark formula {formula}: {e}")
                continue
        
        # Calculate statistics
        if results['creation_times']:
            results['creation_stats'] = {
                'average': sum(results['creation_times']) / len(results['creation_times']),
                'min': min(results['creation_times']),
                'max': max(results['creation_times']),
                'total': sum(results['creation_times'])
            }
        
        if results['molecular_weight_times']:
            results['molecular_weight_stats'] = {
                'average': sum(results['molecular_weight_times']) / len(results['molecular_weight_times']),
                'min': min(results['molecular_weight_times']),
                'max': max(results['molecular_weight_times']),
                'total': sum(results['molecular_weight_times'])
            }
        
        return results


class DetailedProfiler:
    """
    Detailed profiler using cProfile for comprehensive analysis.
    """
    
    def __init__(self):
        """Initialize the detailed profiler."""
        self.logger = logging.getLogger('chemesty.profiling.detailed')
    
    def profile_code(self, code_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Profile code using cProfile.
        
        Args:
            code_func: Function to profile
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Profiling results
        """
        profiler = cProfile.Profile()
        
        # Run the profiler
        profiler.enable()
        try:
            result = code_func(*args, **kwargs)
        finally:
            profiler.disable()
        
        # Get statistics
        stats_stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        
        return {
            'result': result,
            'profile_output': stats_stream.getvalue(),
            'stats': stats
        }
    
    def save_profile(self, code_func: Callable, filepath: Union[str, Path], *args, **kwargs) -> Any:
        """
        Profile code and save results to file.
        
        Args:
            code_func: Function to profile
            filepath: Path to save profile results
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Function result
        """
        filepath = Path(filepath)
        profiler = cProfile.Profile()
        
        # Run the profiler
        profiler.enable()
        try:
            result = code_func(*args, **kwargs)
        finally:
            profiler.disable()
        
        # Save profile data
        profiler.dump_stats(str(filepath))
        self.logger.info(f"Saved detailed profile to {filepath}")
        
        return result


# Global profiler instances
_performance_profiler: Optional[PerformanceProfiler] = None
_molecule_profiler: Optional[MoleculeProfiler] = None


def get_performance_profiler() -> PerformanceProfiler:
    """Get the global performance profiler instance."""
    global _performance_profiler
    if _performance_profiler is None:
        _performance_profiler = PerformanceProfiler()
    return _performance_profiler


def get_molecule_profiler() -> MoleculeProfiler:
    """Get the global molecule profiler instance."""
    global _molecule_profiler
    if _molecule_profiler is None:
        _molecule_profiler = MoleculeProfiler()
    return _molecule_profiler


# Convenience decorators
def profile(func_name: Optional[str] = None):
    """Decorator to profile function execution."""
    profiler = get_performance_profiler()
    return profiler.profile_function(func_name)


def profile_molecule_operation(operation_name: Optional[str] = None):
    """Decorator specifically for molecule operations."""
    def decorator(func: Callable) -> Callable:
        profiler = get_molecule_profiler()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = operation_name or f"molecule_{func.__name__}"
            return profiler.profiler.time_operation(name, func, *args, **kwargs)
        
        return wrapper
    return decorator