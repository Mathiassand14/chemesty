#!/usr/bin/env python3
"""
Benchmark script for molecule performance testing.

This script compares the performance of regular molecules vs optimized molecules
to demonstrate the improvements made in molecule operations.
"""

import time
import statistics
from typing import List, Dict, Any
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chemesty.molecules.molecule import Molecule
from chemesty.molecules.optimized_molecule import OptimizedMolecule, create_optimized_molecule, create_molecules_batch
from chemesty.utils.profiling import get_molecule_profiler, DetailedProfiler


def benchmark_molecule_creation(formulas: List[str], iterations: int = 100) -> Dict[str, Any]:
    """
    Benchmark molecule creation performance.
    
    Args:
        formulas: List of molecular formulas to test
        iterations: Number of iterations per formula
        
    Returns:
        Benchmark results
    """
    print(f"Benchmarking molecule creation with {len(formulas)} formulas, {iterations} iterations each...")
    
    # Benchmark regular molecules
    regular_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for formula in formulas:
            try:
                mol = Molecule(formula=formula)
            except Exception:
                continue
        regular_times.append(time.perf_counter() - start_time)
    
    # Benchmark optimized molecules
    optimized_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for formula in formulas:
            try:
                mol = OptimizedMolecule(formula=formula)
            except Exception:
                continue
        optimized_times.append(time.perf_counter() - start_time)
    
    # Benchmark batch creation
    batch_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        try:
            molecules = create_molecules_batch(formulas)
        except Exception:
            pass
        batch_times.append(time.perf_counter() - start_time)
    
    return {
        'regular': {
            'mean': statistics.mean(regular_times),
            'stdev': statistics.stdev(regular_times) if len(regular_times) > 1 else 0,
            'min': min(regular_times),
            'max': max(regular_times)
        },
        'optimized': {
            'mean': statistics.mean(optimized_times),
            'stdev': statistics.stdev(optimized_times) if len(optimized_times) > 1 else 0,
            'min': min(optimized_times),
            'max': max(optimized_times)
        },
        'batch': {
            'mean': statistics.mean(batch_times),
            'stdev': statistics.stdev(batch_times) if len(batch_times) > 1 else 0,
            'min': min(batch_times),
            'max': max(batch_times)
        }
    }


def benchmark_property_calculations(formulas: List[str], iterations: int = 50) -> Dict[str, Any]:
    """
    Benchmark molecular property calculations.
    
    Args:
        formulas: List of molecular formulas to test
        iterations: Number of iterations
        
    Returns:
        Benchmark results
    """
    print(f"Benchmarking property calculations with {len(formulas)} formulas, {iterations} iterations each...")
    
    # Create molecules once
    regular_molecules = []
    optimized_molecules = []
    
    for formula in formulas:
        try:
            regular_molecules.append(Molecule(formula=formula))
            optimized_molecules.append(OptimizedMolecule(formula=formula))
        except Exception:
            continue
    
    # Benchmark molecular weight calculations
    regular_mw_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for mol in regular_molecules:
            try:
                _ = mol.molecular_weight
            except Exception:
                continue
        regular_mw_times.append(time.perf_counter() - start_time)
    
    optimized_mw_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for mol in optimized_molecules:
            try:
                _ = mol.molecular_weight
            except Exception:
                continue
        optimized_mw_times.append(time.perf_counter() - start_time)
    
    # Benchmark formula generation
    regular_formula_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for mol in regular_molecules:
            try:
                _ = mol.molecular_formula
            except Exception:
                continue
        regular_formula_times.append(time.perf_counter() - start_time)
    
    optimized_formula_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for mol in optimized_molecules:
            try:
                _ = mol.molecular_formula
            except Exception:
                continue
        optimized_formula_times.append(time.perf_counter() - start_time)
    
    return {
        'molecular_weight': {
            'regular': {
                'mean': statistics.mean(regular_mw_times),
                'stdev': statistics.stdev(regular_mw_times) if len(regular_mw_times) > 1 else 0
            },
            'optimized': {
                'mean': statistics.mean(optimized_mw_times),
                'stdev': statistics.stdev(optimized_mw_times) if len(optimized_mw_times) > 1 else 0
            }
        },
        'molecular_formula': {
            'regular': {
                'mean': statistics.mean(regular_formula_times),
                'stdev': statistics.stdev(regular_formula_times) if len(regular_formula_times) > 1 else 0
            },
            'optimized': {
                'mean': statistics.mean(optimized_formula_times),
                'stdev': statistics.stdev(optimized_formula_times) if len(optimized_formula_times) > 1 else 0
            }
        }
    }


def print_benchmark_results(results: Dict[str, Any], title: str) -> None:
    """Print benchmark results in a formatted way."""
    print(f"\n{title}")
    print("=" * len(title))
    
    if 'regular' in results and 'optimized' in results:
        regular = results['regular']
        optimized = results['optimized']
        
        print(f"Regular molecules:")
        print(f"  Mean: {regular['mean']:.6f}s")
        print(f"  Std:  {regular['stdev']:.6f}s")
        
        print(f"Optimized molecules:")
        print(f"  Mean: {optimized['mean']:.6f}s")
        print(f"  Std:  {optimized['stdev']:.6f}s")
        
        if regular['mean'] > 0:
            speedup = regular['mean'] / optimized['mean']
            print(f"Speedup: {speedup:.2f}x")
        
        if 'batch' in results:
            batch = results['batch']
            print(f"Batch processing:")
            print(f"  Mean: {batch['mean']:.6f}s")
            print(f"  Std:  {batch['stdev']:.6f}s")
            
            if regular['mean'] > 0:
                batch_speedup = regular['mean'] / batch['mean']
                print(f"Batch speedup: {batch_speedup:.2f}x")
    
    elif 'molecular_weight' in results:
        for prop_name, prop_data in results.items():
            print(f"\n{prop_name.replace('_', ' ').title()}:")
            regular = prop_data['regular']
            optimized = prop_data['optimized']
            
            print(f"  Regular:   {regular['mean']:.6f}s ± {regular['stdev']:.6f}s")
            print(f"  Optimized: {optimized['mean']:.6f}s ± {optimized['stdev']:.6f}s")
            
            if regular['mean'] > 0:
                speedup = regular['mean'] / optimized['mean']
                print(f"  Speedup:   {speedup:.2f}x")


def main():
    """Run the molecule performance benchmarks."""
    print("Molecule Performance Benchmark")
    print("=" * 40)
    
    # Test formulas of varying complexity
    test_formulas = [
        # Simple molecules
        "H2O", "CO2", "NH3", "CH4", "O2", "N2",
        # Medium complexity
        "C2H6", "C2H4", "C2H2", "CH3OH", "C2H5OH", "C6H6",
        # Complex molecules
        "C6H12O6", "C8H10N4O2", "C9H8O4", "C13H18O2", "C8H9NO2",
        "C27H46O", "C16H18N2O4S", "C21H30O2", "C17H21NO4", "C43H66N12O12S2"
    ]
    
    # Run benchmarks
    creation_results = benchmark_molecule_creation(test_formulas, iterations=20)
    property_results = benchmark_property_calculations(test_formulas, iterations=30)
    
    # Print results
    print_benchmark_results(creation_results, "Molecule Creation Performance")
    print_benchmark_results(property_results, "Property Calculation Performance")
    
    # Test profiling
    print("\nProfiling Results:")
    print("=" * 20)
    
    profiler = get_molecule_profiler()
    stats = profiler.profiler.get_stats()
    
    if stats:
        print("Top operations by average time:")
        slowest = profiler.profiler.get_slowest_functions(5)
        for i, func_data in enumerate(slowest, 1):
            print(f"{i}. {func_data['function_name']}: {func_data['average_time']:.6f}s avg ({func_data['call_count']} calls)")
    else:
        print("No profiling data available")
    
    print("\nBenchmark completed!")


if __name__ == "__main__":
    main()