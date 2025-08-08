"""
Caching utilities for the Chemesty library.

This module provides caching mechanisms for frequently accessed data
to improve performance across the library.
"""

import time
import threading
from typing import Any, Dict, Optional, Callable, TypeVar, Generic
from functools import wraps
from collections import OrderedDict

T = TypeVar('T')


class LRUCache(Generic[T]):
    """
    Thread-safe Least Recently Used (LRU) cache implementation.
    """
    
    def __init__(self, max_size: int = 128):
        """
        Initialize the LRU cache.
        
        Args:
            max_size: Maximum number of items to store in cache
        """
        self.max_size = max_size
        self._cache: OrderedDict[str, T] = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[T]:
        """
        Get an item from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        with self._lock:
            if key in self._cache:
                # Move to end (most recently used)
                value = self._cache.pop(key)
                self._cache[key] = value
                return value
            return None
    
    def put(self, key: str, value: T) -> None:
        """
        Put an item in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            if key in self._cache:
                # Update existing key
                self._cache.pop(key)
            elif len(self._cache) >= self.max_size:
                # Remove least recently used item
                self._cache.popitem(last=False)
            
            self._cache[key] = value
    
    def clear(self) -> None:
        """Clear all items from the cache."""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Get the current size of the cache."""
        with self._lock:
            return len(self._cache)
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'keys': list(self._cache.keys())
            }


class TTLCache(Generic[T]):
    """
    Time-To-Live cache with automatic expiration.
    """
    
    def __init__(self, max_size: int = 128, ttl_seconds: float = 300):
        """
        Initialize the TTL cache.
        
        Args:
            max_size: Maximum number of items to store
            ttl_seconds: Time to live for cached items in seconds
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple[T, float]] = {}
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[T]:
        """
        Get an item from the cache if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self.ttl_seconds:
                    return value
                else:
                    # Remove expired item
                    del self._cache[key]
            return None
    
    def put(self, key: str, value: T) -> None:
        """
        Put an item in the cache with current timestamp.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            # Clean up expired items if cache is full
            if len(self._cache) >= self.max_size:
                self._cleanup_expired()
                
                # If still full, remove oldest item
                if len(self._cache) >= self.max_size:
                    oldest_key = min(self._cache.keys(), 
                                   key=lambda k: self._cache[k][1])
                    del self._cache[oldest_key]
            
            self._cache[key] = (value, time.time())
    
    def _cleanup_expired(self) -> None:
        """Remove expired items from cache."""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self._cache.items()
            if current_time - timestamp >= self.ttl_seconds
        ]
        for key in expired_keys:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all items from the cache."""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Get the current size of the cache."""
        with self._lock:
            return len(self._cache)


class CacheManager:
    """
    Central cache manager for the Chemesty library.
    """
    
    def __init__(self):
        """Initialize the cache manager with different cache types."""
        # Element cache - elements don't change, so use LRU
        self.element_cache = LRUCache[Any](max_size=200)
        
        # Molecule property cache - properties might be recalculated, so use TTL
        self.molecule_cache = TTLCache[Any](max_size=1000, ttl_seconds=3600)
        
        # Database query cache - queries might become stale, so use TTL
        self.query_cache = TTLCache[Any](max_size=500, ttl_seconds=1800)
        
        # Calculation cache - for expensive calculations
        self.calculation_cache = LRUCache[Any](max_size=100)
    
    def get_element(self, symbol: str) -> Optional[Any]:
        """Get cached element by symbol."""
        return self.element_cache.get(f"element_{symbol}")
    
    def cache_element(self, symbol: str, element: Any) -> None:
        """Cache an element."""
        self.element_cache.put(f"element_{symbol}", element)
    
    def get_molecule_property(self, molecule_id: str, property_name: str) -> Optional[Any]:
        """Get cached molecule property."""
        return self.molecule_cache.get(f"mol_{molecule_id}_{property_name}")
    
    def cache_molecule_property(self, molecule_id: str, property_name: str, value: Any) -> None:
        """Cache a molecule property."""
        self.molecule_cache.put(f"mol_{molecule_id}_{property_name}", value)
    
    def get_query_result(self, query_hash: str) -> Optional[Any]:
        """Get cached query result."""
        return self.query_cache.get(f"query_{query_hash}")
    
    def cache_query_result(self, query_hash: str, result: Any) -> None:
        """Cache a query result."""
        self.query_cache.put(f"query_{query_hash}", result)
    
    def get_calculation(self, calc_key: str) -> Optional[Any]:
        """Get cached calculation result."""
        return self.calculation_cache.get(f"calc_{calc_key}")
    
    def cache_calculation(self, calc_key: str, result: Any) -> None:
        """Cache a calculation result."""
        self.calculation_cache.put(f"calc_{calc_key}", result)
    
    def clear_all(self) -> None:
        """Clear all caches."""
        self.element_cache.clear()
        self.molecule_cache.clear()
        self.query_cache.clear()
        self.calculation_cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for all caches."""
        return {
            'element_cache': self.element_cache.stats(),
            'molecule_cache': {
                'size': self.molecule_cache.size(),
                'max_size': self.molecule_cache.max_size,
                'ttl_seconds': self.molecule_cache.ttl_seconds
            },
            'query_cache': {
                'size': self.query_cache.size(),
                'max_size': self.query_cache.max_size,
                'ttl_seconds': self.query_cache.ttl_seconds
            },
            'calculation_cache': self.calculation_cache.stats()
        }


# Global cache manager instance
_cache_manager = CacheManager()


def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance."""
    return _cache_manager


def cached_property(cache_key_func: Optional[Callable] = None, ttl_seconds: float = 3600):
    """
    Decorator for caching property calculations.
    
    Args:
        cache_key_func: Function to generate cache key from arguments
        ttl_seconds: Time to live for cached values
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if cache_key_func:
                cache_key = cache_key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cache_manager = get_cache_manager()
            cached_result = cache_manager.get_calculation(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            # Calculate and cache result
            result = func(*args, **kwargs)
            cache_manager.cache_calculation(cache_key, result)
            
            return result
        
        return wrapper
    return decorator


def cached_method(cache_type: str = 'calculation', ttl_seconds: float = 3600):
    """
    Decorator for caching method results.
    
    Args:
        cache_type: Type of cache to use ('calculation', 'molecule', 'query')
        ttl_seconds: Time to live for cached values (for TTL caches)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Generate cache key based on object and method
            obj_id = getattr(self, '_cache_id', id(self))
            cache_key = f"{obj_id}_{func.__name__}_{hash(str(args) + str(kwargs))}"
            
            cache_manager = get_cache_manager()
            
            # Get cached result based on cache type
            if cache_type == 'molecule':
                cached_result = cache_manager.get_molecule_property(str(obj_id), func.__name__)
            elif cache_type == 'query':
                cached_result = cache_manager.get_query_result(cache_key)
            else:  # calculation
                cached_result = cache_manager.get_calculation(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            # Calculate and cache result
            result = func(self, *args, **kwargs)
            
            if cache_type == 'molecule':
                cache_manager.cache_molecule_property(str(obj_id), func.__name__, result)
            elif cache_type == 'query':
                cache_manager.cache_query_result(cache_key, result)
            else:  # calculation
                cache_manager.cache_calculation(cache_key, result)
            
            return result
        
        return wrapper
    return decorator