"""
Parallel processing utilities for computationally intensive chemical operations.

This module provides tools for parallelizing chemical calculations and data processing
to improve performance on multi-core systems.
"""

import multiprocessing as mp
import concurrent.futures
import threading
import asyncio
from typing import List, Dict, Any, Callable, Optional, Union, Iterator, TypeVar, Generic
from functools import partial, wraps
import time
import queue
import logging
from dataclasses import dataclass
from pathlib import Path
import pickle
import os

T = TypeVar('T')
R = TypeVar('R')


@dataclass
class ProcessingResult:
    """Result from parallel processing operation."""
    success: bool
    result: Any = None
    error: Optional[str] = None
    processing_time: float = 0.0
    worker_id: Optional[str] = None


class ParallelProcessor:
    """
    Main parallel processor for chemical operations.
    """
    
    def __init__(self, max_workers: Optional[int] = None, use_processes: bool = True):
        """
        Initialize parallel processor.
        
        Args:
            max_workers: Maximum number of workers (defaults to CPU count)
            use_processes: Use processes instead of threads for CPU-bound tasks
        """
        self.max_workers = max_workers or mp.cpu_count()
        self.use_processes = use_processes
        self.logger = logging.getLogger('chemesty.parallel')
        
    def map_parallel(self, func: Callable[[T], R], items: List[T], 
                    chunk_size: Optional[int] = None) -> List[ProcessingResult]:
        """
        Apply function to items in parallel.
        
        Args:
            func: Function to apply to each item
            items: List of items to process
            chunk_size: Size of chunks for processing
            
        Returns:
            List of ProcessingResult objects
        """
        if not items:
            return []
        
        chunk_size = chunk_size or max(1, len(items) // (self.max_workers * 4))
        results = []
        
        if self.use_processes:
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit tasks
                future_to_item = {}
                for i, item in enumerate(items):
                    future = executor.submit(self._safe_execute, func, item, f"worker_{i % self.max_workers}")
                    future_to_item[future] = item
                
                # Collect results
                for future in concurrent.futures.as_completed(future_to_item):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        self.logger.error(f"Task failed: {e}")
                        results.append(ProcessingResult(
                            success=False,
                            error=str(e)
                        ))
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit tasks
                future_to_item = {}
                for i, item in enumerate(items):
                    future = executor.submit(self._safe_execute, func, item, f"thread_{i % self.max_workers}")
                    future_to_item[future] = item
                
                # Collect results
                for future in concurrent.futures.as_completed(future_to_item):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        self.logger.error(f"Task failed: {e}")
                        results.append(ProcessingResult(
                            success=False,
                            error=str(e)
                        ))
        
        return results
    
    def _safe_execute(self, func: Callable, item: Any, worker_id: str) -> ProcessingResult:
        """
        Safely execute function with error handling and timing.
        
        Args:
            func: Function to execute
            item: Item to process
            worker_id: Worker identifier
            
        Returns:
            ProcessingResult
        """
        start_time = time.perf_counter()
        
        try:
            result = func(item)
            processing_time = time.perf_counter() - start_time
            
            return ProcessingResult(
                success=True,
                result=result,
                processing_time=processing_time,
                worker_id=worker_id
            )
        except Exception as e:
            processing_time = time.perf_counter() - start_time
            
            return ProcessingResult(
                success=False,
                error=str(e),
                processing_time=processing_time,
                worker_id=worker_id
            )
    
    def reduce_parallel(self, func: Callable[[T, T], T], items: List[T]) -> T:
        """
        Parallel reduction operation.
        
        Args:
            func: Reduction function
            items: Items to reduce
            
        Returns:
            Reduced result
        """
        if not items:
            raise ValueError("Cannot reduce empty list")
        
        if len(items) == 1:
            return items[0]
        
        # Parallel tree reduction
        while len(items) > 1:
            # Pair up items for parallel processing
            pairs = []
            for i in range(0, len(items), 2):
                if i + 1 < len(items):
                    pairs.append((items[i], items[i + 1]))
                else:
                    pairs.append((items[i], None))
            
            # Process pairs in parallel
            def reduce_pair(pair):
                a, b = pair
                if b is None:
                    return a
                return func(a, b)
            
            results = self.map_parallel(reduce_pair, pairs)
            items = [r.result for r in results if r.success]
        
        return items[0] if items else None


class MoleculeParallelProcessor:
    """
    Specialized parallel processor for molecule operations.
    """
    
    def __init__(self, max_workers: Optional[int] = None):
        """Initialize molecule parallel processor."""
        self.processor = ParallelProcessor(max_workers, use_processes=True)
        self.logger = logging.getLogger('chemesty.parallel.molecule')
    
    def calculate_properties_parallel(self, molecules: List[Any], 
                                    properties: List[str]) -> List[Dict[str, Any]]:
        """
        Calculate molecular properties in parallel.
        
        Args:
            molecules: List of molecule objects
            properties: List of property names to calculate
            
        Returns:
            List of property dictionaries
        """
        def calculate_props(molecule):
            """Calculate properties for a single molecule."""
            props = {}
            for prop_name in properties:
                try:
                    if hasattr(molecule, prop_name):
                        props[prop_name] = getattr(molecule, prop_name)
                    elif hasattr(molecule, f"get_{prop_name}"):
                        props[prop_name] = getattr(molecule, f"get_{prop_name}")()
                    else:
                        props[prop_name] = None
                except Exception as e:
                    props[prop_name] = f"Error: {str(e)}"
            return props
        
        results = self.processor.map_parallel(calculate_props, molecules)
        return [r.result if r.success else {} for r in results]
    
    def create_molecules_parallel(self, formulas: List[str]) -> List[Any]:
        """
        Create molecules from formulas in parallel.
        
        Args:
            formulas: List of molecular formulas
            
        Returns:
            List of molecule objects
        """
        def create_molecule(formula):
            """Create a molecule from formula."""
            from chemesty.molecules.molecule import Molecule
            return Molecule(formula=formula)
        
        results = self.processor.map_parallel(create_molecule, formulas)
        return [r.result for r in results if r.success]
    
    def batch_molecular_weight_calculation(self, molecules: List[Any]) -> List[float]:
        """
        Calculate molecular weights in parallel.
        
        Args:
            molecules: List of molecule objects
            
        Returns:
            List of molecular weights
        """
        def get_molecular_weight(molecule):
            """Get molecular weight of a molecule."""
            return molecule.molecular_weight
        
        results = self.processor.map_parallel(get_molecular_weight, molecules)
        return [r.result if r.success else 0.0 for r in results]


class AsyncProcessor:
    """
    Asynchronous processor for I/O-bound operations.
    """
    
    def __init__(self, max_concurrent: int = 100):
        """
        Initialize async processor.
        
        Args:
            max_concurrent: Maximum concurrent operations
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.logger = logging.getLogger('chemesty.parallel.async')
    
    async def process_async(self, func: Callable, items: List[Any]) -> List[Any]:
        """
        Process items asynchronously.
        
        Args:
            func: Async function to apply
            items: Items to process
            
        Returns:
            List of results
        """
        async def bounded_func(item):
            async with self.semaphore:
                return await func(item)
        
        tasks = [bounded_func(item) for item in items]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def download_data_parallel(self, urls: List[str]) -> List[Any]:
        """
        Download data from URLs in parallel.
        
        Args:
            urls: List of URLs to download from
            
        Returns:
            List of downloaded data
        """
        import aiohttp
        
        async def download_url(session, url):
            try:
                async with session.get(url) as response:
                    return await response.text()
            except Exception as e:
                self.logger.error(f"Failed to download {url}: {e}")
                return None
        
        async with aiohttp.ClientSession() as session:
            tasks = [download_url(session, url) for url in urls]
            return await asyncio.gather(*tasks, return_exceptions=True)


class ParallelDatabaseProcessor:
    """
    Parallel processor for database operations.
    """
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize parallel database processor.
        
        Args:
            max_workers: Maximum number of database workers
        """
        self.max_workers = max_workers
        self.processor = ParallelProcessor(max_workers, use_processes=False)  # Use threads for I/O
        self.logger = logging.getLogger('chemesty.parallel.database')
    
    def batch_insert_parallel(self, db_path: str, molecules_data: List[Dict[str, Any]]) -> List[bool]:
        """
        Insert molecules into database in parallel batches.
        
        Args:
            db_path: Path to database
            molecules_data: List of molecule data dictionaries
            
        Returns:
            List of success flags
        """
        # Split data into chunks for parallel processing
        chunk_size = max(1, len(molecules_data) // self.max_workers)
        chunks = [molecules_data[i:i + chunk_size] for i in range(0, len(molecules_data), chunk_size)]
        
        def insert_chunk(chunk):
            """Insert a chunk of molecules."""
            from chemesty.data.database import MoleculeDatabase
            
            try:
                with MoleculeDatabase(db_path) as db:
                    return db.batch_add_molecules(chunk)
            except Exception as e:
                self.logger.error(f"Failed to insert chunk: {e}")
                return []
        
        results = self.processor.map_parallel(insert_chunk, chunks)
        
        # Flatten results
        all_ids = []
        for result in results:
            if result.success and result.result:
                all_ids.extend(result.result)
        
        return [bool(id_val) for id_val in all_ids]
    
    def parallel_search(self, db_path: str, queries: List[Dict[str, Any]]) -> List[List[Any]]:
        """
        Perform multiple database searches in parallel.
        
        Args:
            db_path: Path to database
            queries: List of query dictionaries
            
        Returns:
            List of search results
        """
        def execute_query(query):
            """Execute a single query."""
            from chemesty.data.database import MoleculeDatabase
            
            try:
                with MoleculeDatabase(db_path) as db:
                    return db.batch_search_molecules([query])[0]
            except Exception as e:
                self.logger.error(f"Query failed: {e}")
                return []
        
        results = self.processor.map_parallel(execute_query, queries)
        return [r.result if r.success else [] for r in results]


class WorkerPool:
    """
    Custom worker pool for specialized chemical operations.
    """
    
    def __init__(self, worker_count: int = None, worker_type: str = 'process'):
        """
        Initialize worker pool.
        
        Args:
            worker_count: Number of workers
            worker_type: Type of workers ('process' or 'thread')
        """
        self.worker_count = worker_count or mp.cpu_count()
        self.worker_type = worker_type
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.running = False
        self.logger = logging.getLogger('chemesty.parallel.pool')
    
    def start(self):
        """Start the worker pool."""
        if self.running:
            return
        
        self.running = True
        
        if self.worker_type == 'process':
            self.task_queue = mp.Queue()
            self.result_queue = mp.Queue()
            
            for i in range(self.worker_count):
                worker = mp.Process(target=self._worker_process, args=(i,))
                worker.start()
                self.workers.append(worker)
        else:
            for i in range(self.worker_count):
                worker = threading.Thread(target=self._worker_thread, args=(i,))
                worker.start()
                self.workers.append(worker)
    
    def stop(self):
        """Stop the worker pool."""
        if not self.running:
            return
        
        self.running = False
        
        # Send stop signals
        for _ in self.workers:
            self.task_queue.put(None)
        
        # Wait for workers to finish
        for worker in self.workers:
            if self.worker_type == 'process':
                worker.join()
            else:
                worker.join()
        
        self.workers.clear()
    
    def submit_task(self, func: Callable, *args, **kwargs) -> str:
        """
        Submit a task to the worker pool.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Task ID
        """
        task_id = f"task_{time.time()}_{id(func)}"
        task = {
            'id': task_id,
            'func': func,
            'args': args,
            'kwargs': kwargs
        }
        
        self.task_queue.put(task)
        return task_id
    
    def get_result(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Get a result from the worker pool.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Result dictionary or None if timeout
        """
        try:
            return self.result_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def _worker_process(self, worker_id: int):
        """Worker process function."""
        while True:
            try:
                task = self.task_queue.get()
                if task is None:  # Stop signal
                    break
                
                result = self._execute_task(task, worker_id)
                self.result_queue.put(result)
                
            except Exception as e:
                self.logger.error(f"Worker {worker_id} error: {e}")
    
    def _worker_thread(self, worker_id: int):
        """Worker thread function."""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1.0)
                if task is None:  # Stop signal
                    break
                
                result = self._execute_task(task, worker_id)
                self.result_queue.put(result)
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Worker {worker_id} error: {e}")
    
    def _execute_task(self, task: Dict[str, Any], worker_id: int) -> Dict[str, Any]:
        """Execute a task and return result."""
        start_time = time.perf_counter()
        
        try:
            func = task['func']
            args = task.get('args', ())
            kwargs = task.get('kwargs', {})
            
            result = func(*args, **kwargs)
            processing_time = time.perf_counter() - start_time
            
            return {
                'task_id': task['id'],
                'success': True,
                'result': result,
                'processing_time': processing_time,
                'worker_id': worker_id
            }
            
        except Exception as e:
            processing_time = time.perf_counter() - start_time
            
            return {
                'task_id': task['id'],
                'success': False,
                'error': str(e),
                'processing_time': processing_time,
                'worker_id': worker_id
            }


# Global instances
_parallel_processor: Optional[ParallelProcessor] = None
_molecule_processor: Optional[MoleculeParallelProcessor] = None
_async_processor: Optional[AsyncProcessor] = None


def get_parallel_processor() -> ParallelProcessor:
    """Get the global parallel processor instance."""
    global _parallel_processor
    if _parallel_processor is None:
        _parallel_processor = ParallelProcessor()
    return _parallel_processor


def get_molecule_processor() -> MoleculeParallelProcessor:
    """Get the global molecule parallel processor instance."""
    global _molecule_processor
    if _molecule_processor is None:
        _molecule_processor = MoleculeParallelProcessor()
    return _molecule_processor


def get_async_processor() -> AsyncProcessor:
    """Get the global async processor instance."""
    global _async_processor
    if _async_processor is None:
        _async_processor = AsyncProcessor()
    return _async_processor


# Convenience decorators
def parallelize(max_workers: Optional[int] = None, use_processes: bool = True):
    """
    Decorator to parallelize function execution over a list of inputs.
    
    Args:
        max_workers: Maximum number of workers
        use_processes: Use processes instead of threads
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(items: List[Any], *args, **kwargs):
            processor = ParallelProcessor(max_workers, use_processes)
            
            # Create partial function with additional arguments
            if args or kwargs:
                partial_func = partial(func, *args, **kwargs)
            else:
                partial_func = func
            
            results = processor.map_parallel(partial_func, items)
            return [r.result for r in results if r.success]
        
        return wrapper
    return decorator


def parallel_molecule_operation(max_workers: Optional[int] = None):
    """
    Decorator for parallel molecule operations.
    
    Args:
        max_workers: Maximum number of workers
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(molecules: List[Any], *args, **kwargs):
            processor = MoleculeParallelProcessor(max_workers)
            
            def process_molecule(molecule):
                return func(molecule, *args, **kwargs)
            
            results = processor.processor.map_parallel(process_molecule, molecules)
            return [r.result for r in results if r.success]
        
        return wrapper
    return decorator