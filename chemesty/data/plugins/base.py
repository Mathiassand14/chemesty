"""
Base classes and interfaces for the data source plugin system.

This module defines the abstract base classes and interfaces that all
data source plugins must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Iterator, Type
import logging
from dataclasses import dataclass


@dataclass
class DataSourceConfig:
    """Configuration for a data source plugin."""
    name: str
    description: str
    version: str
    author: str
    url: Optional[str] = None
    api_key_required: bool = False
    rate_limit: Optional[int] = None
    supported_formats: List[str] = None
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ['json']


@dataclass
class QueryResult:
    """Result from a data source query."""
    data: List[Dict[str, Any]]
    total_count: int
    source: str
    query_time: float
    metadata: Optional[Dict[str, Any]] = None


class DataSourcePlugin(ABC):
    """
    Abstract base class for all data source plugins.
    
    All data source plugins must inherit from this class and implement
    the required abstract methods.
    """
    
    def __init__(self, config: DataSourceConfig):
        """
        Initialize the plugin with configuration.
        
        Args:
            config: Plugin configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"chemesty.plugins.{config.name}")
        self._initialized = False
    
    @abstractmethod
    def initialize(self, **kwargs) -> bool:
        """
        Initialize the plugin with any required setup.
        
        Args:
            **kwargs: Plugin-specific initialization parameters
            
        Returns:
            True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def search_molecules(self, query: str, limit: int = 100, **kwargs) -> QueryResult:
        """
        Search for molecules using the data source.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            **kwargs: Plugin-specific search parameters
            
        Returns:
            QueryResult containing the search results
        """
        pass
    
    @abstractmethod
    def get_molecule_by_id(self, molecule_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get a specific molecule by its ID.
        
        Args:
            molecule_id: Unique identifier for the molecule
            **kwargs: Plugin-specific parameters
            
        Returns:
            Molecule data dictionary or None if not found
        """
        pass
    
    @abstractmethod
    def get_molecule_properties(self, molecule_id: str, properties: List[str], **kwargs) -> Dict[str, Any]:
        """
        Get specific properties for a molecule.
        
        Args:
            molecule_id: Unique identifier for the molecule
            properties: List of property names to retrieve
            **kwargs: Plugin-specific parameters
            
        Returns:
            Dictionary of property values
        """
        pass
    
    def validate_query(self, query: str) -> bool:
        """
        Validate a search query for this data source.
        
        Args:
            query: Query string to validate
            
        Returns:
            True if query is valid, False otherwise
        """
        return bool(query and query.strip())
    
    def get_supported_properties(self) -> List[str]:
        """
        Get list of properties supported by this data source.
        
        Returns:
            List of supported property names
        """
        return []
    
    def cleanup(self) -> None:
        """Clean up any resources used by the plugin."""
        pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


class PluginManager:
    """
    Manager for data source plugins.
    
    Handles plugin registration, discovery, and lifecycle management.
    """
    
    def __init__(self):
        """Initialize the plugin manager."""
        self._plugins: Dict[str, Type[DataSourcePlugin]] = {}
        self._active_plugins: Dict[str, DataSourcePlugin] = {}
        self.logger = logging.getLogger("chemesty.plugins.manager")
    
    def register_plugin(self, plugin_class: Type[DataSourcePlugin], config: DataSourceConfig) -> bool:
        """
        Register a plugin class with the manager.
        
        Args:
            plugin_class: Plugin class to register
            config: Plugin configuration
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            if not issubclass(plugin_class, DataSourcePlugin):
                self.logger.error(f"Plugin {config.name} does not inherit from DataSourcePlugin")
                return False
            
            self._plugins[config.name] = plugin_class
            self.logger.info(f"Registered plugin: {config.name} v{config.version}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register plugin {config.name}: {e}")
            return False
    
    def get_plugin(self, name: str, **init_kwargs) -> Optional[DataSourcePlugin]:
        """
        Get an initialized plugin instance.
        
        Args:
            name: Plugin name
            **init_kwargs: Plugin initialization parameters
            
        Returns:
            Plugin instance or None if not found
        """
        if name in self._active_plugins:
            return self._active_plugins[name]
        
        if name not in self._plugins:
            self.logger.error(f"Plugin {name} not found")
            return None
        
        try:
            plugin_class = self._plugins[name]
            # Create a basic config - in practice this would come from configuration
            config = DataSourceConfig(
                name=name,
                description=f"Plugin {name}",
                version="1.0.0",
                author="Unknown"
            )
            
            plugin = plugin_class(config)
            if plugin.initialize(**init_kwargs):
                self._active_plugins[name] = plugin
                return plugin
            else:
                self.logger.error(f"Failed to initialize plugin {name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to create plugin {name}: {e}")
            return None
    
    def list_plugins(self) -> List[str]:
        """
        Get list of registered plugin names.
        
        Returns:
            List of plugin names
        """
        return list(self._plugins.keys())
    
    def list_active_plugins(self) -> List[str]:
        """
        Get list of active plugin names.
        
        Returns:
            List of active plugin names
        """
        return list(self._active_plugins.keys())
    
    def unload_plugin(self, name: str) -> bool:
        """
        Unload an active plugin.
        
        Args:
            name: Plugin name
            
        Returns:
            True if unloaded successfully, False otherwise
        """
        if name in self._active_plugins:
            try:
                self._active_plugins[name].cleanup()
                del self._active_plugins[name]
                self.logger.info(f"Unloaded plugin: {name}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to unload plugin {name}: {e}")
                return False
        return False
    
    def search_all_sources(self, query: str, limit: int = 100, sources: Optional[List[str]] = None) -> Dict[str, QueryResult]:
        """
        Search across multiple data sources.
        
        Args:
            query: Search query
            limit: Maximum results per source
            sources: List of source names to search (None for all active)
            
        Returns:
            Dictionary mapping source names to query results
        """
        if sources is None:
            sources = self.list_active_plugins()
        
        results = {}
        for source_name in sources:
            plugin = self.get_plugin(source_name)
            if plugin:
                try:
                    result = plugin.search_molecules(query, limit)
                    results[source_name] = result
                except Exception as e:
                    self.logger.error(f"Search failed for {source_name}: {e}")
        
        return results
    
    def cleanup_all(self) -> None:
        """Clean up all active plugins."""
        for name in list(self._active_plugins.keys()):
            self.unload_plugin(name)