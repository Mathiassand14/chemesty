"""
Progress reporting utilities for Chemesty.

This module provides consistent progress reporting functionality across the entire
codebase using tqdm for long-running operations.
"""

import time
from typing import Optional, Any, Iterator, Callable, Union, List
from contextlib import contextmanager
from functools import wraps
from tqdm import tqdm


class ProgressReporter:
    """A flexible progress reporter that can be used for various operations."""
    
    def __init__(self, total: Optional[int] = None, desc: str = "Processing", 
                 unit: str = "items", disable: bool = False):
        """Initialize the progress reporter.
        
        Args:
            total: Total number of items to process
            desc: Description of the operation
            unit: Unit of measurement for progress
            disable: Whether to disable progress reporting
        """
        self.total = total
        self.desc = desc
        self.unit = unit
        self.disable = disable
        self._pbar: Optional[tqdm] = None
        self._start_time: Optional[float] = None
    
    def __enter__(self) -> 'ProgressReporter':
        """Enter the context manager."""
        self._start_time = time.time()
        self._pbar = tqdm(
            total=self.total,
            desc=self.desc,
            unit=self.unit,
            disable=self.disable
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        if self._pbar:
            self._pbar.close()
        
        if self._start_time and not self.disable:
            elapsed = time.time() - self._start_time
            print(f"\n{self.desc} completed in {elapsed:.2f} seconds")
    
    def update(self, n: int = 1) -> None:
        """Update the progress bar.
        
        Args:
            n: Number of items processed
        """
        if self._pbar:
            self._pbar.update(n)
    
    def set_description(self, desc: str) -> None:
        """Update the description.
        
        Args:
            desc: New description
        """
        if self._pbar:
            self._pbar.set_description(desc)
    
    def set_postfix(self, **kwargs) -> None:
        """Set postfix information.
        
        Args:
            **kwargs: Key-value pairs to display as postfix
        """
        if self._pbar:
            self._pbar.set_postfix(**kwargs)


def progress_bar(iterable: Iterator[Any], desc: str = "Processing", 
                unit: str = "items", total: Optional[int] = None,
                disable: bool = False) -> Iterator[Any]:
    """Create a progress bar for an iterable.
    
    Args:
        iterable: The iterable to wrap
        desc: Description of the operation
        unit: Unit of measurement
        total: Total number of items (if known)
        disable: Whether to disable progress reporting
        
    Yields:
        Items from the iterable with progress reporting
        
    Examples:
        >>> for item in progress_bar(items, desc="Processing molecules"):
        ...     process_item(item)
    """
    return tqdm(iterable, desc=desc, unit=unit, total=total, disable=disable)


def with_progress(desc: str = "Processing", unit: str = "items", 
                 disable: bool = False):
    """Decorator to add progress reporting to functions that process iterables.
    
    Args:
        desc: Description of the operation
        unit: Unit of measurement
        disable: Whether to disable progress reporting
        
    Examples:
        >>> @with_progress(desc="Creating molecules", unit="molecules")
        ... def create_molecules(formulas):
        ...     for formula in formulas:
        ...         yield create_molecule(formula)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # If the function returns an iterable, wrap it with progress
            if hasattr(result, '__iter__') and not isinstance(result, (str, bytes)):
                try:
                    # Try to get the length for total count
                    total = len(result) if hasattr(result, '__len__') else None
                    return progress_bar(result, desc=desc, unit=unit, 
                                     total=total, disable=disable)
                except (TypeError, AttributeError):
                    # If we can't wrap it, return as-is
                    return result
            
            return result
        return wrapper
    return decorator


@contextmanager
def progress_context(total: Optional[int] = None, desc: str = "Processing",
                    unit: str = "items", disable: bool = False):
    """Context manager for manual progress reporting.
    
    Args:
        total: Total number of items to process
        desc: Description of the operation
        unit: Unit of measurement
        disable: Whether to disable progress reporting
        
    Yields:
        ProgressReporter instance
        
    Examples:
        >>> with progress_context(total=100, desc="Processing data") as progress:
        ...     for i in range(100):
        ...         # Do some work
        ...         progress.update(1)
    """
    reporter = ProgressReporter(total=total, desc=desc, unit=unit, disable=disable)
    with reporter as progress:
        yield progress


def batch_progress(items: List[Any], batch_size: int = 100, 
                  desc: str = "Processing batches", unit: str = "batches",
                  disable: bool = False) -> Iterator[List[Any]]:
    """Process items in batches with progress reporting.
    
    Args:
        items: List of items to process
        batch_size: Size of each batch
        desc: Description of the operation
        unit: Unit of measurement
        disable: Whether to disable progress reporting
        
    Yields:
        Batches of items with progress reporting
        
    Examples:
        >>> for batch in batch_progress(molecules, batch_size=50, desc="Processing molecules"):
        ...     process_batch(batch)
    """
    total_batches = (len(items) + batch_size - 1) // batch_size
    
    with progress_bar(range(total_batches), desc=desc, unit=unit, disable=disable):
        for i in range(0, len(items), batch_size):
            yield items[i:i + batch_size]


class TimedProgress:
    """Progress reporter with timing information."""
    
    def __init__(self, total: Optional[int] = None, desc: str = "Processing",
                 unit: str = "items", disable: bool = False):
        """Initialize the timed progress reporter.
        
        Args:
            total: Total number of items to process
            desc: Description of the operation
            unit: Unit of measurement
            disable: Whether to disable progress reporting
        """
        self.reporter = ProgressReporter(total, desc, unit, disable)
        self.start_time: Optional[float] = None
        self.item_times: List[float] = []
    
    def __enter__(self) -> 'TimedProgress':
        """Enter the context manager."""
        self.start_time = time.time()
        self.reporter.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        self.reporter.__exit__(exc_type, exc_val, exc_tb)
        
        if self.item_times and not self.reporter.disable:
            avg_time = sum(self.item_times) / len(self.item_times)
            print(f"Average time per {self.reporter.unit}: {avg_time:.4f} seconds")
    
    def update(self, n: int = 1) -> None:
        """Update progress with timing.
        
        Args:
            n: Number of items processed
        """
        current_time = time.time()
        if self.start_time:
            item_time = (current_time - self.start_time) / n
            self.item_times.append(item_time)
            
            # Update postfix with timing info
            if len(self.item_times) > 1:
                avg_time = sum(self.item_times[-10:]) / min(10, len(self.item_times))
                self.reporter.set_postfix(avg_time=f"{avg_time:.4f}s")
        
        self.reporter.update(n)
        self.start_time = current_time


def estimate_time_remaining(current: int, total: int, elapsed_time: float) -> str:
    """Estimate time remaining for an operation.
    
    Args:
        current: Current progress
        total: Total items to process
        elapsed_time: Time elapsed so far
        
    Returns:
        Formatted string with time estimate
    """
    if current == 0:
        return "Unknown"
    
    rate = current / elapsed_time
    remaining = total - current
    eta_seconds = remaining / rate
    
    if eta_seconds < 60:
        return f"{eta_seconds:.0f}s"
    elif eta_seconds < 3600:
        return f"{eta_seconds/60:.1f}m"
    else:
        return f"{eta_seconds/3600:.1f}h"


# Convenience functions for common operations
def molecule_progress(molecules: Iterator[Any], desc: str = "Processing molecules") -> Iterator[Any]:
    """Progress bar specifically for molecule operations."""
    return progress_bar(molecules, desc=desc, unit="molecules")


def element_progress(elements: Iterator[Any], desc: str = "Processing elements") -> Iterator[Any]:
    """Progress bar specifically for element operations."""
    return progress_bar(elements, desc=desc, unit="elements")


def database_progress(records: Iterator[Any], desc: str = "Processing records") -> Iterator[Any]:
    """Progress bar specifically for database operations."""
    return progress_bar(records, desc=desc, unit="records")


def calculation_progress(calculations: Iterator[Any], desc: str = "Running calculations") -> Iterator[Any]:
    """Progress bar specifically for calculation operations."""
    return progress_bar(calculations, desc=desc, unit="calculations")


# Global settings for progress reporting
_GLOBAL_DISABLE = False


def set_global_progress_disable(disable: bool) -> None:
    """Globally enable or disable progress reporting.
    
    Args:
        disable: Whether to disable all progress reporting
    """
    global _GLOBAL_DISABLE
    _GLOBAL_DISABLE = disable


def is_progress_disabled() -> bool:
    """Check if progress reporting is globally disabled.
    
    Returns:
        True if progress reporting is disabled
    """
    return _GLOBAL_DISABLE