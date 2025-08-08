"""
Logging configuration for the Chemesty library.

This module provides centralized logging configuration and utilities
for consistent logging throughout the codebase.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union


def setup_logging(
    level: Union[str, int] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    format_string: Optional[str] = None,
    include_timestamp: bool = True
) -> logging.Logger:
    """
    Set up logging configuration for Chemesty.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, logs to console only
        format_string: Custom format string for log messages
        include_timestamp: Whether to include timestamp in log messages
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('chemesty')
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Default format string
    if format_string is None:
        if include_timestamp:
            format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        else:
            format_string = '%(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = 'chemesty') -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically module name)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class ChemestryLogger:
    """
    Context manager for temporary logging configuration.
    
    Useful for operations that need specific logging settings.
    """
    
    def __init__(
        self,
        level: Union[str, int] = logging.INFO,
        log_file: Optional[Union[str, Path]] = None,
        suppress_console: bool = False
    ):
        """
        Initialize the logger context manager.
        
        Args:
            level: Logging level for this context
            log_file: Optional log file for this context
            suppress_console: Whether to suppress console output
        """
        self.level = level
        self.log_file = log_file
        self.suppress_console = suppress_console
        self.original_handlers = []
        self.logger = get_logger()
    
    def __enter__(self) -> logging.Logger:
        """Enter the logging context."""
        # Save original handlers
        self.original_handlers = self.logger.handlers.copy()
        self.original_level = self.logger.level
        
        # Clear handlers
        self.logger.handlers.clear()
        self.logger.setLevel(self.level)
        
        # Set up new handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if not self.suppress_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        if self.log_file:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the logging context."""
        # Restore original handlers
        self.logger.handlers.clear()
        self.logger.handlers.extend(self.original_handlers)
        self.logger.setLevel(self.original_level)


# Initialize default logger
_default_logger = setup_logging()


def log_operation(operation_name: str, logger: Optional[logging.Logger] = None):
    """
    Decorator to log function operations.
    
    Args:
        operation_name: Name of the operation being logged
        logger: Optional logger instance
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            log = logger or get_logger()
            log.debug(f"Starting {operation_name}")
            
            try:
                result = func(*args, **kwargs)
                log.debug(f"Completed {operation_name} successfully")
                return result
            except Exception as e:
                log.error(f"Error in {operation_name}: {str(e)}")
                raise
        
        return wrapper
    return decorator