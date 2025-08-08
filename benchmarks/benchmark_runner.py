#!/usr/bin/env python3
"""
Comprehensive benchmark runner for Chemesty performance monitoring.

This script runs all benchmarks and provides performance monitoring capabilities
including results storage, comparison, and regression detection.
"""

import json
import time
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import statistics

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from molecule_performance import benchmark_molecule_creation, benchmark_property_calculations


class BenchmarkRunner:
    """Main benchmark runner with results storage and comparison."""
    
    def __init__(self, results_dir: str = "benchmark_results"):
        """Initialize the benchmark runner.
        
        Args:
            results_dir: Directory to store benchmark results
        """
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
    def run_all_benchmarks(self, iterations: int = 50) -> Dict[str, Any]:
        """Run all available benchmarks.
        
        Args:
            iterations: Number of iterations for each benchmark
            
        Returns:
            Complete benchmark results
        """
        print("Running comprehensive Chemesty benchmarks...")
        print(f"Iterations: {iterations}")
        print("=" * 50)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'iterations': iterations,
            'system_info': self._get_system_info(),
            'benchmarks': {}
        }
        
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
        
        # Run molecule benchmarks
        print("Running molecule creation benchmarks...")
        results['benchmarks']['molecule_creation'] = benchmark_molecule_creation(
            test_formulas, iterations
        )
        
        print("Running property calculation benchmarks...")
        results['benchmarks']['property_calculations'] = benchmark_property_calculations(
            test_formulas, iterations // 2
        )
        
        # Run database benchmarks if available
        try:
            results['benchmarks']['database'] = self._benchmark_database_operations(iterations)
        except Exception as e:
            print(f"Database benchmarks skipped: {e}")
            results['benchmarks']['database'] = {'error': str(e)}
        
        # Run element benchmarks
        try:
            results['benchmarks']['elements'] = self._benchmark_element_operations(iterations)
        except Exception as e:
            print(f"Element benchmarks skipped: {e}")
            results['benchmarks']['elements'] = {'error': str(e)}
        
        return results
    
    def _benchmark_database_operations(self, iterations: int) -> Dict[str, Any]:
        """Benchmark database operations."""
        print("Running database operation benchmarks...")
        
        try:
            from chemesty.data.database import ChemicalDatabase
            
            db_times = []
            query_times = []
            
            for _ in range(iterations):
                # Benchmark database initialization
                start_time = time.perf_counter()
                db = ChemicalDatabase()
                db_times.append(time.perf_counter() - start_time)
                
                # Benchmark simple queries
                start_time = time.perf_counter()
                try:
                    # Example query - adjust based on actual database API
                    results = db.search_molecules(limit=10)
                except Exception:
                    pass
                query_times.append(time.perf_counter() - start_time)
            
            return {
                'initialization': {
                    'mean': statistics.mean(db_times),
                    'stdev': statistics.stdev(db_times) if len(db_times) > 1 else 0,
                    'min': min(db_times),
                    'max': max(db_times)
                },
                'queries': {
                    'mean': statistics.mean(query_times),
                    'stdev': statistics.stdev(query_times) if len(query_times) > 1 else 0,
                    'min': min(query_times),
                    'max': max(query_times)
                }
            }
        except ImportError:
            return {'error': 'Database module not available'}
    
    def _benchmark_element_operations(self, iterations: int) -> Dict[str, Any]:
        """Benchmark element operations."""
        print("Running element operation benchmarks...")
        
        try:
            from chemesty.elements import H, C, N, O, Fe, Au
            
            creation_times = []
            property_times = []
            
            elements = [H, C, N, O, Fe, Au]
            
            for _ in range(iterations):
                # Benchmark element creation
                start_time = time.perf_counter()
                for element_class in elements:
                    element = element_class()
                creation_times.append(time.perf_counter() - start_time)
                
                # Benchmark property access
                start_time = time.perf_counter()
                for element_class in elements:
                    element = element_class()
                    _ = element.atomic_mass
                    _ = element.atomic_number
                    _ = element.symbol
                    _ = element.is_metal()
                property_times.append(time.perf_counter() - start_time)
            
            return {
                'creation': {
                    'mean': statistics.mean(creation_times),
                    'stdev': statistics.stdev(creation_times) if len(creation_times) > 1 else 0,
                    'min': min(creation_times),
                    'max': max(creation_times)
                },
                'properties': {
                    'mean': statistics.mean(property_times),
                    'stdev': statistics.stdev(property_times) if len(property_times) > 1 else 0,
                    'min': min(property_times),
                    'max': max(property_times)
                }
            }
        except ImportError:
            return {'error': 'Elements module not available'}
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information for benchmark context."""
        import platform
        import psutil
        
        return {
            'python_version': platform.python_version(),
            'platform': platform.platform(),
            'processor': platform.processor(),
            'cpu_count': psutil.cpu_count(),
            'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2)
        }
    
    def save_results(self, results: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Save benchmark results to file.
        
        Args:
            results: Benchmark results to save
            filename: Optional filename, defaults to timestamp-based name
            
        Returns:
            Path to saved results file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {filepath}")
        return str(filepath)
    
    def compare_results(self, current_results: Dict[str, Any], 
                       baseline_file: Optional[str] = None) -> Dict[str, Any]:
        """Compare current results with baseline.
        
        Args:
            current_results: Current benchmark results
            baseline_file: Path to baseline results file
            
        Returns:
            Comparison results
        """
        if baseline_file is None:
            # Find the most recent baseline
            result_files = list(self.results_dir.glob("benchmark_results_*.json"))
            if not result_files:
                print("No baseline results found for comparison")
                return {}
            
            baseline_file = max(result_files, key=lambda x: x.stat().st_mtime)
        
        try:
            with open(baseline_file, 'r') as f:
                baseline_results = json.load(f)
        except Exception as e:
            print(f"Error loading baseline results: {e}")
            return {}
        
        print(f"Comparing with baseline: {baseline_file}")
        
        comparison = {
            'baseline_timestamp': baseline_results.get('timestamp'),
            'current_timestamp': current_results.get('timestamp'),
            'regressions': [],
            'improvements': [],
            'comparisons': {}
        }
        
        # Compare each benchmark
        for benchmark_name, current_data in current_results.get('benchmarks', {}).items():
            if benchmark_name not in baseline_results.get('benchmarks', {}):
                continue
                
            baseline_data = baseline_results['benchmarks'][benchmark_name]
            benchmark_comparison = self._compare_benchmark_data(
                current_data, baseline_data, benchmark_name
            )
            
            comparison['comparisons'][benchmark_name] = benchmark_comparison
            
            # Check for significant changes (>10% regression/improvement)
            for change in benchmark_comparison.get('significant_changes', []):
                if change['change_percent'] > 10:
                    comparison['regressions'].append({
                        'benchmark': benchmark_name,
                        'operation': change['operation'],
                        'change_percent': change['change_percent']
                    })
                elif change['change_percent'] < -10:
                    comparison['improvements'].append({
                        'benchmark': benchmark_name,
                        'operation': change['operation'],
                        'change_percent': abs(change['change_percent'])
                    })
        
        return comparison
    
    def _compare_benchmark_data(self, current: Dict[str, Any], 
                               baseline: Dict[str, Any], 
                               benchmark_name: str) -> Dict[str, Any]:
        """Compare two benchmark datasets."""
        comparison = {
            'benchmark_name': benchmark_name,
            'significant_changes': []
        }
        
        def compare_timing_data(current_timing, baseline_timing, operation_name):
            if 'mean' in current_timing and 'mean' in baseline_timing:
                current_mean = current_timing['mean']
                baseline_mean = baseline_timing['mean']
                
                if baseline_mean > 0:
                    change_percent = ((current_mean - baseline_mean) / baseline_mean) * 100
                    
                    if abs(change_percent) > 5:  # 5% threshold for significance
                        comparison['significant_changes'].append({
                            'operation': operation_name,
                            'current_mean': current_mean,
                            'baseline_mean': baseline_mean,
                            'change_percent': change_percent
                        })
        
        # Compare different types of benchmark data
        if isinstance(current, dict) and isinstance(baseline, dict):
            for key, current_value in current.items():
                if key in baseline:
                    baseline_value = baseline[key]
                    
                    if isinstance(current_value, dict) and 'mean' in current_value:
                        compare_timing_data(current_value, baseline_value, key)
                    elif isinstance(current_value, dict):
                        # Recursively compare nested data
                        nested_comparison = self._compare_benchmark_data(
                            current_value, baseline_value, f"{benchmark_name}.{key}"
                        )
                        comparison['significant_changes'].extend(
                            nested_comparison.get('significant_changes', [])
                        )
        
        return comparison
    
    def print_comparison_summary(self, comparison: Dict[str, Any]) -> None:
        """Print a summary of benchmark comparison results."""
        print("\nBenchmark Comparison Summary")
        print("=" * 40)
        
        if comparison.get('regressions'):
            print(f"\n⚠️  Performance Regressions ({len(comparison['regressions'])}):")
            for regression in comparison['regressions']:
                print(f"  - {regression['benchmark']}.{regression['operation']}: "
                      f"+{regression['change_percent']:.1f}% slower")
        
        if comparison.get('improvements'):
            print(f"\n✅ Performance Improvements ({len(comparison['improvements'])}):")
            for improvement in comparison['improvements']:
                print(f"  - {improvement['benchmark']}.{improvement['operation']}: "
                      f"{improvement['change_percent']:.1f}% faster")
        
        if not comparison.get('regressions') and not comparison.get('improvements'):
            print("\n✅ No significant performance changes detected")


def main():
    """Main entry point for benchmark runner."""
    parser = argparse.ArgumentParser(description='Run Chemesty performance benchmarks')
    parser.add_argument('--iterations', type=int, default=50,
                       help='Number of iterations for each benchmark')
    parser.add_argument('--compare', type=str, metavar='BASELINE_FILE',
                       help='Compare results with baseline file')
    parser.add_argument('--save', type=str, metavar='FILENAME',
                       help='Save results to specific filename')
    parser.add_argument('--results-dir', type=str, default='benchmark_results',
                       help='Directory to store results')
    
    args = parser.parse_args()
    
    runner = BenchmarkRunner(args.results_dir)
    
    # Run benchmarks
    results = runner.run_all_benchmarks(args.iterations)
    
    # Save results
    results_file = runner.save_results(results, args.save)
    
    # Compare with baseline if requested
    if args.compare:
        comparison = runner.compare_results(results, args.compare)
        runner.print_comparison_summary(comparison)
    
    print(f"\nBenchmark completed! Results saved to: {results_file}")


if __name__ == "__main__":
    main()