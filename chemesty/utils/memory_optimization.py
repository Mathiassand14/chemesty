"""
Memory optimization utilities for handling large chemical datasets.

This module provides tools and data structures for efficient memory usage
when working with large collections of molecules and chemical data.
"""

import gc
import sys
import weakref
import psutil
import os
from typing import Iterator, List, Dict, Any, Optional, Union, Callable, TypeVar, Generic
from collections.abc import Sequence
from dataclasses import dataclass
import threading
import time
from pathlib import Path
import pickle
import tempfile
import mmap

T = TypeVar('T')


@dataclass
class MemoryStats:
    """Memory usage statistics."""
    total_memory: float  # Total system memory in MB
    available_memory: float  # Available memory in MB
    used_memory: float  # Used memory in MB
    process_memory: float  # Current process memory in MB
    memory_percent: float  # Memory usage percentage


class MemoryMonitor:
    """
    Monitor memory usage and provide optimization recommendations.
    """
    
    def __init__(self):
        """Initialize the memory monitor."""
        self.process = psutil.Process(os.getpid())
        self._baseline_memory = None
        self._peak_memory = 0.0
        
    def get_memory_stats(self) -> MemoryStats:
        """
        Get current memory statistics.
        
        Returns:
            MemoryStats object with current memory information
        """
        # System memory info
        memory = psutil.virtual_memory()
        
        # Process memory info
        process_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        return MemoryStats(
            total_memory=memory.total / 1024 / 1024,
            available_memory=memory.available / 1024 / 1024,
            used_memory=memory.used / 1024 / 1024,
            process_memory=process_memory,
            memory_percent=memory.percent
        )
    
    def set_baseline(self) -> None:
        """Set the current memory usage as baseline."""
        stats = self.get_memory_stats()
        self._baseline_memory = stats.process_memory
    
    def get_memory_increase(self) -> float:
        """
        Get memory increase since baseline.
        
        Returns:
            Memory increase in MB
        """
        if self._baseline_memory is None:
            return 0.0
        
        current_stats = self.get_memory_stats()
        return current_stats.process_memory - self._baseline_memory
    
    def track_peak_memory(self) -> None:
        """Track peak memory usage."""
        stats = self.get_memory_stats()
        if stats.process_memory > self._peak_memory:
            self._peak_memory = stats.process_memory
    
    def get_peak_memory(self) -> float:
        """Get peak memory usage in MB."""
        return self._peak_memory
    
    def should_optimize_memory(self, threshold_percent: float = 80.0) -> bool:
        """
        Check if memory optimization is recommended.
        
        Args:
            threshold_percent: Memory usage threshold percentage
            
        Returns:
            True if memory optimization is recommended
        """
        stats = self.get_memory_stats()
        return stats.memory_percent > threshold_percent


class LazyList(Generic[T]):
    """
    Memory-efficient lazy list that loads items on demand.
    """
    
    def __init__(self, loader_func: Callable[[int], T], length: int):
        """
        Initialize lazy list.
        
        Args:
            loader_func: Function to load item by index
            length: Total number of items
        """
        self._loader_func = loader_func
        self._length = length
        self._cache: Dict[int, T] = {}
        self._cache_size_limit = 1000  # Limit cache size
    
    def __len__(self) -> int:
        """Get the length of the list."""
        return self._length
    
    def __getitem__(self, index: int) -> T:
        """Get item by index, loading on demand."""
        if index < 0:
            index = self._length + index
        
        if index < 0 or index >= self._length:
            raise IndexError("Index out of range")
        
        # Check cache first
        if index in self._cache:
            return self._cache[index]
        
        # Load item
        item = self._loader_func(index)
        
        # Add to cache if not full
        if len(self._cache) < self._cache_size_limit:
            self._cache[index] = item
        
        return item
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over items, loading on demand."""
        for i in range(self._length):
            yield self[i]
    
    def clear_cache(self) -> None:
        """Clear the internal cache."""
        self._cache.clear()
        gc.collect()


class ChunkedDataset(Generic[T]):
    """
    Memory-efficient dataset that processes data in chunks.
    """
    
    def __init__(self, data_source: Union[List[T], Callable[[], Iterator[T]]], 
                 chunk_size: int = 1000):
        """
        Initialize chunked dataset.
        
        Args:
            data_source: List of data or function that returns iterator
            chunk_size: Size of each chunk
        """
        self.data_source = data_source
        self.chunk_size = chunk_size
        self._total_size = None
        
        if isinstance(data_source, list):
            self._total_size = len(data_source)
    
    def chunks(self) -> Iterator[List[T]]:
        """
        Iterate over data in chunks.
        
        Yields:
            Chunks of data
        """
        if isinstance(self.data_source, list):
            # Process list in chunks
            for i in range(0, len(self.data_source), self.chunk_size):
                yield self.data_source[i:i + self.chunk_size]
        else:
            # Process iterator in chunks
            chunk = []
            for item in self.data_source():
                chunk.append(item)
                if len(chunk) >= self.chunk_size:
                    yield chunk
                    chunk = []
            
            # Yield remaining items
            if chunk:
                yield chunk
    
    def process_chunks(self, processor_func: Callable[[List[T]], Any]) -> Iterator[Any]:
        """
        Process each chunk with a function.
        
        Args:
            processor_func: Function to process each chunk
            
        Yields:
            Results from processing each chunk
        """
        for chunk in self.chunks():
            try:
                result = processor_func(chunk)
                yield result
            finally:
                # Force garbage collection after each chunk
                del chunk
                gc.collect()


class MemoryMappedStorage:
    """
    Memory-mapped storage for large datasets.
    """
    
    def __init__(self, filepath: Optional[Path] = None):
        """
        Initialize memory-mapped storage.
        
        Args:
            filepath: Path to storage file (temporary if None)
        """
        self.filepath = filepath or Path(tempfile.mktemp(suffix='.mmap'))
        self._file = None
        self._mmap = None
        self._data = {}
    
    def __enter__(self):
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.close()
    
    def store_data(self, key: str, data: Any) -> None:
        """
        Store data with memory mapping.
        
        Args:
            key: Storage key
            data: Data to store
        """
        # Serialize data
        serialized_data = pickle.dumps(data)
        
        # Store in memory-mapped file
        with open(self.filepath, 'ab') as f:
            offset = f.tell()
            f.write(serialized_data)
            
            # Store metadata
            self._data[key] = {
                'offset': offset,
                'size': len(serialized_data)
            }
    
    def load_data(self, key: str) -> Any:
        """
        Load data from memory-mapped storage.
        
        Args:
            key: Storage key
            
        Returns:
            Loaded data
        """
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found in storage")
        
        metadata = self._data[key]
        
        # Open memory-mapped file if not already open
        if self._mmap is None:
            self._file = open(self.filepath, 'rb')
            self._mmap = mmap.mmap(self._file.fileno(), 0, access=mmap.ACCESS_READ)
        
        # Read data from memory-mapped file
        self._mmap.seek(metadata['offset'])
        serialized_data = self._mmap.read(metadata['size'])
        
        return pickle.loads(serialized_data)
    
    def close(self) -> None:
        """Close memory-mapped storage."""
        if self._mmap:
            self._mmap.close()
            self._mmap = None
        
        if self._file:
            self._file.close()
            self._file = None
    
    def cleanup(self) -> None:
        """Clean up storage file."""
        self.close()
        if self.filepath.exists():
            self.filepath.unlink()


class WeakValueCache(Generic[T]):
    """
    Cache that uses weak references to avoid memory leaks.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize weak value cache.
        
        Args:
            max_size: Maximum cache size
        """
        self._cache: Dict[str, weakref.ref] = {}
        self._max_size = max_size
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[T]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or garbage collected
        """
        with self._lock:
            if key in self._cache:
                ref = self._cache[key]
                value = ref()
                if value is not None:
                    return value
                else:
                    # Remove dead reference
                    del self._cache[key]
            return None
    
    def put(self, key: str, value: T) -> None:
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            # Clean up dead references
            self._cleanup_dead_refs()
            
            # Remove oldest entries if cache is full
            if len(self._cache) >= self._max_size:
                # Remove first entry (simple FIFO)
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            
            # Create weak reference with cleanup callback
            def cleanup_callback(ref):
                with self._lock:
                    if key in self._cache and self._cache[key] is ref:
                        del self._cache[key]
            
            self._cache[key] = weakref.ref(value, cleanup_callback)
    
    def _cleanup_dead_refs(self) -> None:
        """Clean up dead weak references."""
        dead_keys = []
        for key, ref in self._cache.items():
            if ref() is None:
                dead_keys.append(key)
        
        for key in dead_keys:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear the cache."""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        with self._lock:
            self._cleanup_dead_refs()
            return len(self._cache)


class MemoryOptimizer:
    """
    Main memory optimizer with various optimization strategies.
    """
    
    def __init__(self):
        """Initialize memory optimizer."""
        self.monitor = MemoryMonitor()
        self._optimization_strategies = []
    
    def add_optimization_strategy(self, strategy: Callable[[], None]) -> None:
        """
        Add a memory optimization strategy.
        
        Args:
            strategy: Function that performs memory optimization
        """
        self._optimization_strategies.append(strategy)
    
    def optimize_memory(self, force: bool = False) -> Dict[str, Any]:
        """
        Perform memory optimization.
        
        Args:
            force: Force optimization even if not recommended
            
        Returns:
            Optimization results
        """
        stats_before = self.monitor.get_memory_stats()
        
        if not force and not self.monitor.should_optimize_memory():
            return {
                'optimized': False,
                'reason': 'Memory usage below threshold',
                'memory_before': stats_before.process_memory
            }
        
        # Run optimization strategies
        strategies_run = 0
        for strategy in self._optimization_strategies:
            try:
                strategy()
                strategies_run += 1
            except Exception as e:
                print(f"Warning: Optimization strategy failed: {e}")
        
        # Force garbage collection
        gc.collect()
        
        stats_after = self.monitor.get_memory_stats()
        memory_saved = stats_before.process_memory - stats_after.process_memory
        
        return {
            'optimized': True,
            'strategies_run': strategies_run,
            'memory_before': stats_before.process_memory,
            'memory_after': stats_after.process_memory,
            'memory_saved': memory_saved,
            'memory_saved_percent': (memory_saved / stats_before.process_memory) * 100 if stats_before.process_memory > 0 else 0
        }
    
    def create_chunked_processor(self, chunk_size: int = 1000) -> ChunkedDataset:
        """
        Create a chunked dataset processor.
        
        Args:
            chunk_size: Size of each chunk
            
        Returns:
            ChunkedDataset instance
        """
        return ChunkedDataset([], chunk_size)
    
    def create_lazy_list(self, loader_func: Callable[[int], T], length: int) -> LazyList[T]:
        """
        Create a lazy list.
        
        Args:
            loader_func: Function to load items
            length: Total length
            
        Returns:
            LazyList instance
        """
        return LazyList(loader_func, length)
    
    def create_weak_cache(self, max_size: int = 1000) -> WeakValueCache:
        """
        Create a weak value cache.
        
        Args:
            max_size: Maximum cache size
            
        Returns:
            WeakValueCache instance
        """
        return WeakValueCache(max_size)


# Global memory optimizer instance
_memory_optimizer: Optional[MemoryOptimizer] = None


def get_memory_optimizer() -> MemoryOptimizer:
    """Get the global memory optimizer instance."""
    global _memory_optimizer
    if _memory_optimizer is None:
        _memory_optimizer = MemoryOptimizer()
    return _memory_optimizer


def monitor_memory(func: Callable) -> Callable:
    """
    Decorator to monitor memory usage of a function.
    
    Args:
        func: Function to monitor
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        optimizer = get_memory_optimizer()
        optimizer.monitor.set_baseline()
        
        try:
            result = func(*args, **kwargs)
            memory_increase = optimizer.monitor.get_memory_increase()
            
            if memory_increase > 100:  # More than 100MB increase
                print(f"Warning: Function {func.__name__} used {memory_increase:.2f}MB of memory")
            
            return result
        finally:
            optimizer.monitor.track_peak_memory()
    
    return wrapper


def optimize_for_large_datasets(chunk_size: int = 1000):
    """
    Decorator to optimize functions for large datasets.
    
    Args:
        chunk_size: Chunk size for processing
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            optimizer = get_memory_optimizer()
            
            # Check if optimization is needed
            if optimizer.monitor.should_optimize_memory():
                optimizer.optimize_memory()
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator