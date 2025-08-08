"""
Custom exceptions for the Chemesty library.

This module defines custom exception classes that provide more specific
error information for different types of failures in chemical calculations
and data operations.
"""

from typing import Optional, Any, Dict, List, Callable
import traceback
import sys
import time
from datetime import datetime
import logging


class ChemestryError(Exception):
    """Base exception class for all Chemesty-related errors with enhanced reporting."""
    
    def __init__(self, message: str, details: Optional[dict] = None, 
                 context: Optional[Dict[str, Any]] = None,
                 suggestions: Optional[List[str]] = None,
                 error_code: Optional[str] = None):
        """
        Initialize a Chemesty error with enhanced reporting capabilities.
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
            context: Optional context information (function, module, etc.)
            suggestions: Optional list of suggestions for fixing the error
            error_code: Optional error code for programmatic handling
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.context = context or {}
        self.suggestions = suggestions or []
        self.error_code = error_code
        self.timestamp = datetime.now()
        self.traceback_info = self._capture_traceback()
        
        # Log the error
        self._log_error()
    
    def _capture_traceback(self) -> Dict[str, Any]:
        """Capture traceback information for debugging."""
        tb = traceback.extract_tb(sys.exc_info()[2])
        if tb:
            frame = tb[-1]
            return {
                'filename': frame.filename,
                'line_number': frame.lineno,
                'function_name': frame.name,
                'code_context': frame.line
            }
        return {}
    
    def _log_error(self) -> None:
        """Log the error with appropriate level."""
        logger = logging.getLogger('chemesty.errors')
        
        log_message = f"{self.__class__.__name__}: {self.message}"
        if self.error_code:
            log_message = f"[{self.error_code}] {log_message}"
        
        # Include context in log
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            log_message += f" (Context: {context_str})"
        
        logger.error(log_message, extra={
            'error_code': self.error_code,
            'details': self.details,
            'context': self.context,
            'suggestions': self.suggestions,
            'traceback_info': self.traceback_info
        })
    
    def get_error_report(self) -> Dict[str, Any]:
        """
        Get a comprehensive error report.
        
        Returns:
            Dictionary containing all error information
        """
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'timestamp': self.timestamp.isoformat(),
            'details': self.details,
            'context': self.context,
            'suggestions': self.suggestions,
            'traceback_info': self.traceback_info
        }
    
    def add_context(self, key: str, value: Any) -> 'ChemestryError':
        """
        Add context information to the error.
        
        Args:
            key: Context key
            value: Context value
            
        Returns:
            Self for method chaining
        """
        self.context[key] = value
        return self
    
    def add_suggestion(self, suggestion: str) -> 'ChemestryError':
        """
        Add a suggestion for fixing the error.
        
        Args:
            suggestion: Suggestion text
            
        Returns:
            Self for method chaining
        """
        self.suggestions.append(suggestion)
        return self
    
    def __str__(self) -> str:
        """Return a formatted error message with enhanced information."""
        parts = [self.message]
        
        if self.error_code:
            parts[0] = f"[{self.error_code}] {parts[0]}"
        
        if self.details:
            detail_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            parts.append(f"Details: {detail_str}")
        
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            parts.append(f"Context: {context_str}")
        
        if self.suggestions:
            suggestions_str = "; ".join(self.suggestions)
            parts.append(f"Suggestions: {suggestions_str}")
        
        return " | ".join(parts)


class ElementError(ChemestryError):
    """Exception raised for element-related errors."""
    
    def __init__(self, message: str, element_symbol: Optional[str] = None, **kwargs):
        """
        Initialize an element error.
        
        Args:
            message: Error message
            element_symbol: Symbol of the problematic element
            **kwargs: Additional details
        """
        details = kwargs
        if element_symbol:
            details["element_symbol"] = element_symbol
        super().__init__(message, details)


class InvalidElementError(ElementError):
    """Exception raised when an invalid element symbol is provided."""
    
    def __init__(self, symbol: str):
        """
        Initialize an invalid element error.
        
        Args:
            symbol: The invalid element symbol
        """
        message = f"Invalid element symbol: '{symbol}'"
        super().__init__(message, element_symbol=symbol)


class MoleculeError(ChemestryError):
    """Exception raised for molecule-related errors."""
    
    def __init__(self, message: str, formula: Optional[str] = None, **kwargs):
        """
        Initialize a molecule error.
        
        Args:
            message: Error message
            formula: Molecular formula if applicable
            **kwargs: Additional details
        """
        details = kwargs
        if formula:
            details["formula"] = formula
        super().__init__(message, details)


class InvalidFormulaError(MoleculeError):
    """Exception raised when an invalid molecular formula is provided."""
    
    def __init__(self, formula: str, reason: Optional[str] = None):
        """
        Initialize an invalid formula error.
        
        Args:
            formula: The invalid molecular formula
            reason: Optional reason why the formula is invalid
        """
        message = f"Invalid molecular formula: '{formula}'"
        if reason:
            message += f" - {reason}"
        super().__init__(message, formula=formula, reason=reason)


class InvalidSMILESError(MoleculeError):
    """Exception raised when an invalid SMILES string is provided."""
    
    def __init__(self, smiles: str, reason: Optional[str] = None):
        """
        Initialize an invalid SMILES error.
        
        Args:
            smiles: The invalid SMILES string
            reason: Optional reason why the SMILES is invalid
        """
        message = f"Invalid SMILES string: '{smiles}'"
        if reason:
            message += f" - {reason}"
        super().__init__(message, smiles=smiles, reason=reason)


class CalculationError(ChemestryError):
    """Exception raised for calculation-related errors."""
    
    def __init__(self, message: str, calculation_type: Optional[str] = None, **kwargs):
        """
        Initialize a calculation error.
        
        Args:
            message: Error message
            calculation_type: Type of calculation that failed
            **kwargs: Additional details
        """
        details = kwargs
        if calculation_type:
            details["calculation_type"] = calculation_type
        super().__init__(message, details)


class PropertyNotAvailableError(CalculationError):
    """Exception raised when a requested property is not available."""
    
    def __init__(self, property_name: str, element_or_molecule: str):
        """
        Initialize a property not available error.
        
        Args:
            property_name: Name of the unavailable property
            element_or_molecule: Element symbol or molecule formula
        """
        message = f"Property '{property_name}' is not available for '{element_or_molecule}'"
        super().__init__(
            message, 
            calculation_type="property_lookup",
            property_name=property_name,
            target=element_or_molecule
        )


class DatabaseError(ChemestryError):
    """Exception raised for database-related errors."""
    
    def __init__(self, message: str, operation: Optional[str] = None, **kwargs):
        """
        Initialize a database error.
        
        Args:
            message: Error message
            operation: Database operation that failed
            **kwargs: Additional details
        """
        details = kwargs
        if operation:
            details["operation"] = operation
        super().__init__(message, details)


class MoleculeNotFoundError(DatabaseError):
    """Exception raised when a molecule is not found in the database."""
    
    def __init__(self, identifier: str, search_type: str = "name"):
        """
        Initialize a molecule not found error.
        
        Args:
            identifier: The molecule identifier that wasn't found
            search_type: Type of search (name, formula, id, etc.)
        """
        message = f"Molecule not found: {search_type}='{identifier}'"
        super().__init__(
            message, 
            operation="search",
            identifier=identifier,
            search_type=search_type
        )


class ValidationError(ChemestryError):
    """Exception raised for input validation errors."""
    
    def __init__(self, message: str, parameter: Optional[str] = None, value: Any = None, **kwargs):
        """
        Initialize a validation error.
        
        Args:
            message: Error message
            parameter: Name of the invalid parameter
            value: The invalid value
            **kwargs: Additional details
        """
        details = kwargs
        if parameter:
            details["parameter"] = parameter
        if value is not None:
            details["value"] = value
        super().__init__(message, details)


class QuantityError(ValidationError):
    """Exception raised for invalid quantity values."""
    
    def __init__(self, quantity: Any, reason: str = "must be a positive integer"):
        """
        Initialize a quantity error.
        
        Args:
            quantity: The invalid quantity value
            reason: Reason why the quantity is invalid
        """
        message = f"Invalid quantity: {quantity} - {reason}"
        super().__init__(message, parameter="quantity", value=quantity, reason=reason)


class DataDownloadError(ChemestryError):
    """Exception raised for data download errors."""
    
    def __init__(self, message: str, source: Optional[str] = None, **kwargs):
        """
        Initialize a data download error.
        
        Args:
            message: Error message
            source: Data source that failed
            **kwargs: Additional details
        """
        details = kwargs
        if source:
            details["source"] = source
        super().__init__(message, details)


# Convenience function for creating appropriate exceptions
def create_element_error(symbol: str, operation: str, reason: str) -> ElementError:
    """
    Create an appropriate element error based on the context.
    
    Args:
        symbol: Element symbol
        operation: Operation that failed
        reason: Reason for failure
        
    Returns:
        Appropriate ElementError subclass
    """
    if "invalid" in reason.lower() or "unknown" in reason.lower():
        return InvalidElementError(symbol)
    else:
        return ElementError(f"Element operation failed: {operation} - {reason}", symbol)


def create_molecule_error(formula: str, operation: str, reason: str) -> MoleculeError:
    """
    Create an appropriate molecule error based on the context.
    
    Args:
        formula: Molecular formula or SMILES
        operation: Operation that failed
        reason: Reason for failure
        
    Returns:
        Appropriate MoleculeError subclass
    """
    if "formula" in operation.lower() and ("invalid" in reason.lower() or "parse" in reason.lower()):
        return InvalidFormulaError(formula, reason)
    elif "smiles" in operation.lower() and ("invalid" in reason.lower() or "parse" in reason.lower()):
        return InvalidSMILESError(formula, reason)
    else:
        return MoleculeError(f"Molecule operation failed: {operation} - {reason}", formula)


# Error reporting system
class ErrorReporter:
    """
    Centralized error reporting system for Chemesty.
    
    Collects and manages error reports for analysis and debugging.
    """
    
    def __init__(self):
        """Initialize the error reporter."""
        self._error_reports: List[Dict[str, Any]] = []
        self._error_handlers: List[Callable[[Dict[str, Any]], None]] = []
        self.logger = logging.getLogger('chemesty.error_reporter')
    
    def add_error_handler(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Add a custom error handler.
        
        Args:
            handler: Function that takes an error report dictionary
        """
        self._error_handlers.append(handler)
    
    def report_error(self, error: ChemestryError) -> None:
        """
        Report an error to the system.
        
        Args:
            error: ChemestryError instance to report
        """
        report = error.get_error_report()
        self._error_reports.append(report)
        
        # Call custom handlers
        for handler in self._error_handlers:
            try:
                handler(report)
            except Exception as e:
                self.logger.warning(f"Error handler failed: {e}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all reported errors.
        
        Returns:
            Dictionary containing error statistics and summaries
        """
        if not self._error_reports:
            return {'total_errors': 0, 'error_types': {}, 'recent_errors': []}
        
        # Count error types
        error_types = {}
        for report in self._error_reports:
            error_type = report['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Get recent errors (last 10)
        recent_errors = self._error_reports[-10:]
        
        return {
            'total_errors': len(self._error_reports),
            'error_types': error_types,
            'recent_errors': recent_errors,
            'most_common_error': max(error_types.items(), key=lambda x: x[1])[0] if error_types else None
        }
    
    def clear_reports(self) -> None:
        """Clear all error reports."""
        self._error_reports.clear()
    
    def export_reports(self, filename: str) -> None:
        """
        Export error reports to a JSON file.
        
        Args:
            filename: Output filename
        """
        import json
        
        try:
            with open(filename, 'w') as f:
                json.dump(self._error_reports, f, indent=2, default=str)
            self.logger.info(f"Exported {len(self._error_reports)} error reports to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to export error reports: {e}")


# Global error reporter instance
_error_reporter: Optional[ErrorReporter] = None


def get_error_reporter() -> ErrorReporter:
    """
    Get the global error reporter instance.
    
    Returns:
        Global ErrorReporter instance
    """
    global _error_reporter
    if _error_reporter is None:
        _error_reporter = ErrorReporter()
    return _error_reporter


def report_error(error: ChemestryError) -> None:
    """
    Report an error to the global error reporter.
    
    Args:
        error: ChemestryError instance to report
    """
    reporter = get_error_reporter()
    reporter.report_error(error)


# Context manager for error handling
class error_context:
    """
    Context manager for enhanced error handling with automatic reporting.
    
    Usage:
        with error_context("molecule_creation", molecule_formula="H2O"):
            # Code that might raise errors
            pass
    """
    
    def __init__(self, operation: str, **context_data):
        """
        Initialize error context.
        
        Args:
            operation: Name of the operation being performed
            **context_data: Additional context data
        """
        self.operation = operation
        self.context_data = context_data
        self.start_time = None
    
    def __enter__(self):
        """Enter the error context."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the error context and handle any exceptions."""
        if exc_type and issubclass(exc_type, ChemestryError):
            # Add context to the error
            exc_val.add_context("operation", self.operation)
            exc_val.add_context("duration_seconds", time.time() - self.start_time)
            
            for key, value in self.context_data.items():
                exc_val.add_context(key, value)
            
            # Report the error
            report_error(exc_val)
        
        # Don't suppress the exception
        return False