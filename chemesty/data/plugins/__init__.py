"""
Plugin system for data sources in Chemesty.

This module provides a flexible plugin architecture for integrating
various chemical data sources.
"""

from .base import DataSourcePlugin, PluginManager
from .registry import get_plugin_manager, register_plugin

__all__ = [
    'DataSourcePlugin',
    'PluginManager', 
    'get_plugin_manager',
    'register_plugin'
]