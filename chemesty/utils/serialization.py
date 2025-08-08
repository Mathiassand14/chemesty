"""
Robust serialization system for Chemesty objects.

This module provides comprehensive serialization and deserialization
capabilities for chemical data structures including molecules, elements,
and database records.
"""

import json
import pickle
import base64
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Type, Protocol
from datetime import datetime
import logging
from pathlib import Path

from chemesty.elements.atomic_element import AtomicElement
from chemesty.molecules.molecule import Molecule
from chemesty.exceptions import ChemestryError


class SerializationError(ChemestryError):
    """Exception raised for serialization-related errors."""
    
    def __init__(self, message: str, format_type: Optional[str] = None, **kwargs):
        super().__init__(
            message, 
            error_code="SERIALIZATION_ERROR",
            context={"format_type": format_type},
            **kwargs
        )


class Serializable(Protocol):
    """Protocol for objects that can be serialized."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dictionary representation."""
        ...
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Serializable':
        """Create object from dictionary representation."""
        ...


class SerializationFormat(ABC):
    """Abstract base class for serialization formats."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the format name."""
        pass
    
    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Get the file extension for this format."""
        pass
    
    @abstractmethod
    def serialize(self, obj: Any) -> Union[str, bytes]:
        """Serialize an object to this format."""
        pass
    
    @abstractmethod
    def deserialize(self, data: Union[str, bytes], obj_type: Optional[Type] = None) -> Any:
        """Deserialize data from this format."""
        pass


class JSONFormat(SerializationFormat):
    """JSON serialization format."""
    
    @property
    def name(self) -> str:
        return "json"
    
    @property
    def file_extension(self) -> str:
        return ".json"
    
    def serialize(self, obj: Any) -> str:
        """Serialize object to JSON string."""
        try:
            if hasattr(obj, 'to_dict'):
                data = obj.to_dict()
            elif isinstance(obj, (dict, list, str, int, float, bool)) or obj is None:
                data = obj
            else:
                # Try to convert to dict if possible
                data = self._object_to_dict(obj)
            
            return json.dumps(data, indent=2, default=self._json_serializer)
        except Exception as e:
            raise SerializationError(f"Failed to serialize to JSON: {e}", format_type="json")
    
    def deserialize(self, data: str, obj_type: Optional[Type] = None) -> Any:
        """Deserialize JSON string to object."""
        try:
            parsed_data = json.loads(data)
            
            if obj_type and hasattr(obj_type, 'from_dict'):
                return obj_type.from_dict(parsed_data)
            
            return parsed_data
        except Exception as e:
            raise SerializationError(f"Failed to deserialize from JSON: {e}", format_type="json")
    
    def _json_serializer(self, obj: Any) -> Any:
        """Custom JSON serializer for special objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return str(obj)
    
    def _object_to_dict(self, obj: Any) -> Dict[str, Any]:
        """Convert object to dictionary representation."""
        if hasattr(obj, '__dict__'):
            result = {'__class__': obj.__class__.__name__}
            result.update(obj.__dict__)
            return result
        else:
            return {'__value__': obj, '__type__': type(obj).__name__}


class PickleFormat(SerializationFormat):
    """Pickle serialization format."""
    
    @property
    def name(self) -> str:
        return "pickle"
    
    @property
    def file_extension(self) -> str:
        return ".pkl"
    
    def serialize(self, obj: Any) -> bytes:
        """Serialize object to pickle bytes."""
        try:
            return pickle.dumps(obj)
        except Exception as e:
            raise SerializationError(f"Failed to serialize to pickle: {e}", format_type="pickle")
    
    def deserialize(self, data: bytes, obj_type: Optional[Type] = None) -> Any:
        """Deserialize pickle bytes to object."""
        try:
            return pickle.loads(data)
        except Exception as e:
            raise SerializationError(f"Failed to deserialize from pickle: {e}", format_type="pickle")


class XMLFormat(SerializationFormat):
    """XML serialization format."""
    
    @property
    def name(self) -> str:
        return "xml"
    
    @property
    def file_extension(self) -> str:
        return ".xml"
    
    def serialize(self, obj: Any) -> str:
        """Serialize object to XML string."""
        try:
            if hasattr(obj, 'to_dict'):
                data = obj.to_dict()
            else:
                data = self._object_to_dict(obj)
            
            return self._dict_to_xml(data, root_name=obj.__class__.__name__ if hasattr(obj, '__class__') else 'object')
        except Exception as e:
            raise SerializationError(f"Failed to serialize to XML: {e}", format_type="xml")
    
    def deserialize(self, data: str, obj_type: Optional[Type] = None) -> Any:
        """Deserialize XML string to object."""
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(data)
            parsed_data = self._xml_to_dict(root)
            
            if obj_type and hasattr(obj_type, 'from_dict'):
                return obj_type.from_dict(parsed_data)
            
            return parsed_data
        except Exception as e:
            raise SerializationError(f"Failed to deserialize from XML: {e}", format_type="xml")
    
    def _dict_to_xml(self, data: Dict[str, Any], root_name: str = 'root') -> str:
        """Convert dictionary to XML string."""
        import xml.etree.ElementTree as ET
        
        def build_element(name: str, value: Any) -> ET.Element:
            element = ET.Element(name)
            
            if isinstance(value, dict):
                for k, v in value.items():
                    element.append(build_element(k, v))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    element.append(build_element(f"item_{i}", item))
            else:
                element.text = str(value)
            
            return element
        
        root = build_element(root_name, data)
        return ET.tostring(root, encoding='unicode')
    
    def _xml_to_dict(self, element) -> Dict[str, Any]:
        """Convert XML element to dictionary."""
        result = {}
        
        if element.text and element.text.strip():
            return element.text
        
        for child in element:
            child_data = self._xml_to_dict(child)
            
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    def _object_to_dict(self, obj: Any) -> Dict[str, Any]:
        """Convert object to dictionary representation."""
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return {'value': obj}


class SerializationManager:
    """
    Manager for handling different serialization formats.
    
    Provides a unified interface for serializing and deserializing
    objects in various formats.
    """
    
    def __init__(self):
        """Initialize the serialization manager."""
        self._formats: Dict[str, SerializationFormat] = {}
        self.logger = logging.getLogger('chemesty.serialization')
        
        # Register default formats
        self.register_format(JSONFormat())
        self.register_format(PickleFormat())
        self.register_format(XMLFormat())
    
    def register_format(self, format_impl: SerializationFormat) -> None:
        """
        Register a serialization format.
        
        Args:
            format_impl: Serialization format implementation
        """
        self._formats[format_impl.name] = format_impl
        self.logger.info(f"Registered serialization format: {format_impl.name}")
    
    def get_format(self, name: str) -> Optional[SerializationFormat]:
        """
        Get a serialization format by name.
        
        Args:
            name: Format name
            
        Returns:
            SerializationFormat instance or None if not found
        """
        return self._formats.get(name.lower())
    
    def list_formats(self) -> List[str]:
        """
        Get list of available format names.
        
        Returns:
            List of format names
        """
        return list(self._formats.keys())
    
    def serialize(self, obj: Any, format_name: str = "json") -> Union[str, bytes]:
        """
        Serialize an object using the specified format.
        
        Args:
            obj: Object to serialize
            format_name: Name of the serialization format
            
        Returns:
            Serialized data
            
        Raises:
            SerializationError: If serialization fails
        """
        format_impl = self.get_format(format_name)
        if not format_impl:
            raise SerializationError(f"Unknown serialization format: {format_name}")
        
        return format_impl.serialize(obj)
    
    def deserialize(self, data: Union[str, bytes], format_name: str = "json", 
                   obj_type: Optional[Type] = None) -> Any:
        """
        Deserialize data using the specified format.
        
        Args:
            data: Data to deserialize
            format_name: Name of the serialization format
            obj_type: Optional target object type
            
        Returns:
            Deserialized object
            
        Raises:
            SerializationError: If deserialization fails
        """
        format_impl = self.get_format(format_name)
        if not format_impl:
            raise SerializationError(f"Unknown serialization format: {format_name}")
        
        return format_impl.deserialize(data, obj_type)
    
    def save_to_file(self, obj: Any, filepath: Union[str, Path], 
                     format_name: Optional[str] = None) -> None:
        """
        Save an object to a file.
        
        Args:
            obj: Object to save
            filepath: Path to save the file
            format_name: Serialization format (auto-detected from extension if None)
        """
        filepath = Path(filepath)
        
        if format_name is None:
            # Auto-detect format from file extension
            format_name = self._detect_format_from_extension(filepath.suffix)
        
        format_impl = self.get_format(format_name)
        if not format_impl:
            raise SerializationError(f"Unknown serialization format: {format_name}")
        
        try:
            data = format_impl.serialize(obj)
            
            if isinstance(data, bytes):
                filepath.write_bytes(data)
            else:
                filepath.write_text(data, encoding='utf-8')
            
            self.logger.info(f"Saved object to {filepath} using {format_name} format")
            
        except Exception as e:
            raise SerializationError(f"Failed to save to file {filepath}: {e}")
    
    def load_from_file(self, filepath: Union[str, Path], 
                      format_name: Optional[str] = None,
                      obj_type: Optional[Type] = None) -> Any:
        """
        Load an object from a file.
        
        Args:
            filepath: Path to the file
            format_name: Serialization format (auto-detected from extension if None)
            obj_type: Optional target object type
            
        Returns:
            Loaded object
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise SerializationError(f"File not found: {filepath}")
        
        if format_name is None:
            # Auto-detect format from file extension
            format_name = self._detect_format_from_extension(filepath.suffix)
        
        format_impl = self.get_format(format_name)
        if not format_impl:
            raise SerializationError(f"Unknown serialization format: {format_name}")
        
        try:
            if format_name == "pickle":
                data = filepath.read_bytes()
            else:
                data = filepath.read_text(encoding='utf-8')
            
            result = format_impl.deserialize(data, obj_type)
            self.logger.info(f"Loaded object from {filepath} using {format_name} format")
            return result
            
        except Exception as e:
            raise SerializationError(f"Failed to load from file {filepath}: {e}")
    
    def _detect_format_from_extension(self, extension: str) -> str:
        """
        Detect serialization format from file extension.
        
        Args:
            extension: File extension
            
        Returns:
            Format name
        """
        extension = extension.lower()
        
        for format_impl in self._formats.values():
            if format_impl.file_extension == extension:
                return format_impl.name
        
        # Default to JSON
        return "json"


# Global serialization manager instance
_serialization_manager: Optional[SerializationManager] = None


def get_serialization_manager() -> SerializationManager:
    """
    Get the global serialization manager instance.
    
    Returns:
        Global SerializationManager instance
    """
    global _serialization_manager
    if _serialization_manager is None:
        _serialization_manager = SerializationManager()
    return _serialization_manager


# Convenience functions
def serialize(obj: Any, format_name: str = "json") -> Union[str, bytes]:
    """
    Serialize an object using the global serialization manager.
    
    Args:
        obj: Object to serialize
        format_name: Serialization format name
        
    Returns:
        Serialized data
    """
    manager = get_serialization_manager()
    return manager.serialize(obj, format_name)


def deserialize(data: Union[str, bytes], format_name: str = "json", 
               obj_type: Optional[Type] = None) -> Any:
    """
    Deserialize data using the global serialization manager.
    
    Args:
        data: Data to deserialize
        format_name: Serialization format name
        obj_type: Optional target object type
        
    Returns:
        Deserialized object
    """
    manager = get_serialization_manager()
    return manager.deserialize(data, format_name, obj_type)


def save_to_file(obj: Any, filepath: Union[str, Path], 
                format_name: Optional[str] = None) -> None:
    """
    Save an object to a file using the global serialization manager.
    
    Args:
        obj: Object to save
        filepath: File path
        format_name: Serialization format (auto-detected if None)
    """
    manager = get_serialization_manager()
    manager.save_to_file(obj, filepath, format_name)


def load_from_file(filepath: Union[str, Path], 
                  format_name: Optional[str] = None,
                  obj_type: Optional[Type] = None) -> Any:
    """
    Load an object from a file using the global serialization manager.
    
    Args:
        filepath: File path
        format_name: Serialization format (auto-detected if None)
        obj_type: Optional target object type
        
    Returns:
        Loaded object
    """
    manager = get_serialization_manager()
    return manager.load_from_file(filepath, format_name, obj_type)