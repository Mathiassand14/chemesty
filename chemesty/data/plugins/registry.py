"""
Global plugin registry for data source plugins.

This module provides a global registry for managing data source plugins
across the Chemesty library.
"""

from typing import Optional, Type
from .base import DataSourcePlugin, PluginManager, DataSourceConfig

# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """
    Get the global plugin manager instance.
    
    Returns:
        Global PluginManager instance
    """
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


def register_plugin(plugin_class: Type[DataSourcePlugin], config: DataSourceConfig) -> bool:
    """
    Register a plugin with the global plugin manager.
    
    Args:
        plugin_class: Plugin class to register
        config: Plugin configuration
        
    Returns:
        True if registration successful, False otherwise
    """
    manager = get_plugin_manager()
    return manager.register_plugin(plugin_class, config)


def get_plugin(name: str, **init_kwargs) -> Optional[DataSourcePlugin]:
    """
    Get a plugin instance from the global registry.
    
    Args:
        name: Plugin name
        **init_kwargs: Plugin initialization parameters
        
    Returns:
        Plugin instance or None if not found
    """
    manager = get_plugin_manager()
    return manager.get_plugin(name, **init_kwargs)


def list_available_plugins() -> list[str]:
    """
    Get list of all registered plugins.
    
    Returns:
        List of plugin names
    """
    manager = get_plugin_manager()
    return manager.list_plugins()


def list_active_plugins() -> list[str]:
    """
    Get list of all active plugins.
    
    Returns:
        List of active plugin names
    """
    manager = get_plugin_manager()
    return manager.list_active_plugins()


def cleanup_plugins() -> None:
    """Clean up all active plugins."""
    manager = get_plugin_manager()
    manager.cleanup_all()


# Decorator for easy plugin registration
def plugin(name: str, description: str, version: str = "1.0.0", author: str = "Unknown", **config_kwargs):
    """
    Decorator for registering a plugin class.
    
    Args:
        name: Plugin name
        description: Plugin description
        version: Plugin version
        author: Plugin author
        **config_kwargs: Additional configuration parameters
        
    Returns:
        Decorator function
    """
    def decorator(plugin_class: Type[DataSourcePlugin]) -> Type[DataSourcePlugin]:
        config = DataSourceConfig(
            name=name,
            description=description,
            version=version,
            author=author,
            **config_kwargs
        )
        
        # Register the plugin
        register_plugin(plugin_class, config)
        
        return plugin_class
    
    return decorator