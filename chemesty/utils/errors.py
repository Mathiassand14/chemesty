"""
Enhanced error handling and messaging for Chemesty.

This module provides custom exception classes with actionable error messages
that help users understand and fix issues quickly.
"""

import sys
import traceback
from typing import Optional, Dict, Any, List, Union
from pathlib import Path


class ChemestyError(Exception):
    """Base exception class for all Chemesty errors."""
    
    def __init__(self, message: str, suggestion: Optional[str] = None, 
                 error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        """Initialize the error.
        
        Args:
            message: The error message
            suggestion: Actionable suggestion for fixing the error
            error_code: Unique error code for documentation lookup
            context: Additional context information
        """
        super().__init__(message)
        self.message = message
        self.suggestion = suggestion
        self.error_code = error_code
        self.context = context or {}
    
    def __str__(self) -> str:
        """Return a formatted error message."""
        parts = [f"❌ {self.message}"]
        
        if self.error_code:
            parts.append(f"Error Code: {self.error_code}")
        
        if self.suggestion:
            parts.append(f"💡 Suggestion: {self.suggestion}")
        
        if self.context:
            parts.append("📋 Context:")
            for key, value in self.context.items():
                parts.append(f"  - {key}: {value}")
        
        return "\n".join(parts)


class MoleculeError(ChemestyError):
    """Errors related to molecule operations."""
    pass


class ElementError(ChemestyError):
    """Errors related to element operations."""
    pass


class DatabaseError(ChemestyError):
    """Errors related to database operations."""
    pass


class QuantumError(ChemestyError):
    """Errors related to quantum chemistry calculations."""
    pass


class ValidationError(ChemestyError):
    """Errors related to input validation."""
    pass


class FileFormatError(ChemestyError):
    """Errors related to file format handling."""
    pass


class ConfigurationError(ChemestyError):
    """Errors related to configuration and setup."""
    pass


def validate_molecular_formula(formula: str) -> None:
    """Validate a molecular formula and provide helpful error messages.
    
    Args:
        formula: The molecular formula to validate
        
    Raises:
        ValidationError: If the formula is invalid
    """
    if not formula:
        raise ValidationError(
            "Empty molecular formula provided",
            suggestion="Provide a valid molecular formula like 'H2O', 'C6H12O6', or 'NaCl'",
            error_code="EMPTY_FORMULA"
        )
    
    if not isinstance(formula, str):
        raise ValidationError(
            f"Molecular formula must be a string, got {type(formula).__name__}",
            suggestion="Convert your formula to a string: str(formula)",
            error_code="INVALID_FORMULA_TYPE",
            context={"provided_type": type(formula).__name__, "provided_value": str(formula)}
        )
    
    # Check for invalid characters
    import re
    if not re.match(r'^[A-Z][a-z]?(\d+)?([A-Z][a-z]?(\d+)?)*$', formula.strip()):
        raise ValidationError(
            f"Invalid molecular formula format: '{formula}'",
            suggestion="Use proper chemical notation: element symbols (H, He, Li) followed by optional numbers (H2O, CaCl2)",
            error_code="INVALID_FORMULA_FORMAT",
            context={
                "formula": formula,
                "examples": ["H2O", "C6H12O6", "NaCl", "CaCl2", "CH3COOH"]
            }
        )


def validate_file_path(file_path: Union[str, Path], must_exist: bool = True, 
                      expected_extensions: Optional[List[str]] = None) -> Path:
    """Validate a file path and provide helpful error messages.
    
    Args:
        file_path: The file path to validate
        must_exist: Whether the file must exist
        expected_extensions: List of expected file extensions
        
    Returns:
        Validated Path object
        
    Raises:
        ValidationError: If the file path is invalid
    """
    if not file_path:
        raise ValidationError(
            "Empty file path provided",
            suggestion="Provide a valid file path like '/path/to/file.mol' or 'data/molecules.sdf'",
            error_code="EMPTY_FILE_PATH"
        )
    
    path = Path(file_path)
    
    if must_exist and not path.exists():
        raise ValidationError(
            f"File not found: {path}",
            suggestion=f"Check that the file exists and the path is correct. Current working directory: {Path.cwd()}",
            error_code="FILE_NOT_FOUND",
            context={
                "file_path": str(path),
                "absolute_path": str(path.absolute()),
                "current_directory": str(Path.cwd()),
                "parent_exists": path.parent.exists()
            }
        )
    
    if expected_extensions:
        if path.suffix.lower() not in [ext.lower() for ext in expected_extensions]:
            raise ValidationError(
                f"Unsupported file extension: {path.suffix}",
                suggestion=f"Use one of the supported formats: {', '.join(expected_extensions)}",
                error_code="UNSUPPORTED_FILE_FORMAT",
                context={
                    "file_path": str(path),
                    "provided_extension": path.suffix,
                    "supported_extensions": expected_extensions
                }
            )
    
    return path


def handle_import_error(module_name: str, package_name: Optional[str] = None, 
                       install_command: Optional[str] = None) -> ImportError:
    """Create a helpful ImportError with installation instructions.
    
    Args:
        module_name: Name of the module that failed to import
        package_name: Name of the package to install (if different from module)
        install_command: Custom installation command
        
    Returns:
        ImportError with helpful message
    """
    package = package_name or module_name
    command = install_command or f"pip install {package}"
    
    return ImportError(
        f"Required module '{module_name}' not found.\n"
        f"💡 Install it with: {command}\n"
        f"📚 Or add it to your environment: poetry add {package}"
    )


def handle_dependency_error(operation: str, missing_deps: List[str]) -> ConfigurationError:
    """Create a helpful error for missing dependencies.
    
    Args:
        operation: The operation that requires the dependencies
        missing_deps: List of missing dependency names
        
    Returns:
        ConfigurationError with installation instructions
    """
    deps_str = ", ".join(missing_deps)
    install_cmd = f"pip install {' '.join(missing_deps)}"
    poetry_cmd = f"poetry add {' '.join(missing_deps)}"
    
    return ConfigurationError(
        f"Cannot perform {operation}: missing required dependencies: {deps_str}",
        suggestion=f"Install missing dependencies:\n  - With pip: {install_cmd}\n  - With poetry: {poetry_cmd}",
        error_code="MISSING_DEPENDENCIES",
        context={
            "operation": operation,
            "missing_dependencies": missing_deps,
            "install_command": install_cmd,
            "poetry_command": poetry_cmd
        }
    )


def create_molecule_error(formula: str, original_error: Exception) -> MoleculeError:
    """Create a helpful molecule creation error.
    
    Args:
        formula: The molecular formula that caused the error
        original_error: The original exception
        
    Returns:
        MoleculeError with helpful message
    """
    error_type = type(original_error).__name__
    
    suggestions = []
    
    if "invalid" in str(original_error).lower():
        suggestions.append("Check that the molecular formula uses proper chemical notation")
        suggestions.append("Examples: H2O, C6H12O6, NaCl, CaCl2")
    
    if "not found" in str(original_error).lower():
        suggestions.append("Verify that all element symbols are correct")
        suggestions.append("Use proper capitalization: 'Ca' not 'ca', 'Cl' not 'cl'")
    
    if not suggestions:
        suggestions.append("Check the molecular formula format and try again")
        suggestions.append("Consult the documentation for supported formats")
    
    return MoleculeError(
        f"Failed to create molecule from formula '{formula}': {original_error}",
        suggestion="\n".join(f"  • {s}" for s in suggestions),
        error_code="MOLECULE_CREATION_FAILED",
        context={
            "formula": formula,
            "original_error": str(original_error),
            "error_type": error_type
        }
    )


def create_database_error(operation: str, original_error: Exception, 
                         db_path: Optional[str] = None) -> DatabaseError:
    """Create a helpful database error.
    
    Args:
        operation: The database operation that failed
        original_error: The original exception
        db_path: Path to the database file
        
    Returns:
        DatabaseError with helpful message
    """
    suggestions = []
    
    if "no such table" in str(original_error).lower():
        suggestions.append("The database may not be initialized properly")
        suggestions.append("Try running the database setup/migration scripts")
    
    elif "database is locked" in str(original_error).lower():
        suggestions.append("Another process may be using the database")
        suggestions.append("Close other connections or wait for them to finish")
    
    elif "permission denied" in str(original_error).lower():
        suggestions.append("Check file permissions for the database")
        suggestions.append("Ensure the directory is writable")
    
    elif "disk" in str(original_error).lower():
        suggestions.append("Check available disk space")
        suggestions.append("Clean up temporary files if needed")
    
    else:
        suggestions.append("Check database connection and configuration")
        suggestions.append("Verify the database file exists and is accessible")
    
    context = {
        "operation": operation,
        "original_error": str(original_error),
        "error_type": type(original_error).__name__
    }
    
    if db_path:
        context["database_path"] = db_path
        context["database_exists"] = Path(db_path).exists() if db_path else False
    
    return DatabaseError(
        f"Database operation '{operation}' failed: {original_error}",
        suggestion="\n".join(f"  • {s}" for s in suggestions),
        error_code="DATABASE_OPERATION_FAILED",
        context=context
    )


def create_quantum_error(calculation_type: str, original_error: Exception) -> QuantumError:
    """Create a helpful quantum chemistry error.
    
    Args:
        calculation_type: Type of quantum calculation
        original_error: The original exception
        
    Returns:
        QuantumError with helpful message
    """
    suggestions = []
    
    if "convergence" in str(original_error).lower():
        suggestions.append("Try adjusting convergence criteria")
        suggestions.append("Use a different initial guess or method")
        suggestions.append("Check molecular geometry for reasonableness")
    
    elif "memory" in str(original_error).lower():
        suggestions.append("Reduce basis set size or use a smaller model")
        suggestions.append("Increase available memory if possible")
        suggestions.append("Consider using disk-based algorithms")
    
    elif "basis" in str(original_error).lower():
        suggestions.append("Check that the basis set is appropriate for all atoms")
        suggestions.append("Try a different basis set (e.g., STO-3G, 6-31G)")
    
    else:
        suggestions.append("Check input parameters and molecular structure")
        suggestions.append("Consult quantum chemistry documentation")
    
    return QuantumError(
        f"Quantum calculation '{calculation_type}' failed: {original_error}",
        suggestion="\n".join(f"  • {s}" for s in suggestions),
        error_code="QUANTUM_CALCULATION_FAILED",
        context={
            "calculation_type": calculation_type,
            "original_error": str(original_error),
            "error_type": type(original_error).__name__
        }
    )


class ErrorHandler:
    """Context manager for enhanced error handling."""
    
    def __init__(self, operation: str, show_traceback: bool = False):
        """Initialize the error handler.
        
        Args:
            operation: Description of the operation being performed
            show_traceback: Whether to show the full traceback
        """
        self.operation = operation
        self.show_traceback = show_traceback
    
    def __enter__(self):
        """Enter the context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Handle exceptions with enhanced error messages."""
        if exc_type is None:
            return False
        
        # Don't handle ChemestyError exceptions - they're already formatted
        if isinstance(exc_val, ChemestyError):
            return False
        
        # Create enhanced error message
        if self.show_traceback:
            print(f"\n🔍 Full traceback for debugging:")
            traceback.print_exception(exc_type, exc_val, exc_tb)
        
        # Convert common exceptions to ChemestyError
        if exc_type == ImportError:
            enhanced_error = handle_import_error(str(exc_val))
        elif exc_type == FileNotFoundError:
            enhanced_error = ValidationError(
                f"File not found during {self.operation}",
                suggestion="Check that the file path is correct and the file exists",
                error_code="FILE_NOT_FOUND",
                context={"operation": self.operation, "original_error": str(exc_val)}
            )
        elif exc_type == PermissionError:
            enhanced_error = ValidationError(
                f"Permission denied during {self.operation}",
                suggestion="Check file permissions and ensure you have write access",
                error_code="PERMISSION_DENIED",
                context={"operation": self.operation, "original_error": str(exc_val)}
            )
        else:
            enhanced_error = ChemestyError(
                f"Unexpected error during {self.operation}: {exc_val}",
                suggestion="Check your input parameters and try again. If the problem persists, please report this issue.",
                error_code="UNEXPECTED_ERROR",
                context={
                    "operation": self.operation,
                    "error_type": exc_type.__name__,
                    "original_error": str(exc_val)
                }
            )
        
        # Replace the original exception
        raise enhanced_error from exc_val


def with_error_handling(operation: str, show_traceback: bool = False):
    """Decorator to add enhanced error handling to functions.
    
    Args:
        operation: Description of the operation
        show_traceback: Whether to show full tracebacks
        
    Examples:
        >>> @with_error_handling("molecule creation")
        ... def create_molecule(formula):
        ...     return Molecule(formula)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with ErrorHandler(operation, show_traceback):
                return func(*args, **kwargs)
        return wrapper
    return decorator