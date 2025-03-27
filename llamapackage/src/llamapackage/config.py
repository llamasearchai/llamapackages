"""
Configuration management for LlamaPackage.

This module provides functionality for managing configuration settings.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for LlamaPackage."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_dir: Configuration directory path, or None to use default
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".llamapackage"
        
        self.config_file = self.config_dir / "config.json"
        self._config: Dict[str, Any] = {}
        self._load()
    
    def _load(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    self._config = json.load(f)
            else:
                self._config = {}
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self._config = {}
    
    def save(self) -> bool:
        """Save configuration to file.
        
        Returns:
            True if configuration was saved successfully, False otherwise
        """
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self._config, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value to return if key is not found
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def delete(self, key: str) -> bool:
        """Delete configuration value.
        
        Args:
            key: Configuration key
            
        Returns:
            True if key was deleted, False if key was not found
        """
        if key in self._config:
            del self._config[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all configuration values."""
        self._config.clear()
    
    def get_registry_url(self) -> str:
        """Get registry URL.
        
        Returns:
            Registry URL or default
        """
        return self.get("registry_url", "https://packages.llamasearch.ai")
    
    def get_api_token(self) -> Optional[str]:
        """Get API token.
        
        Returns:
            API token or None if not set
        """
        return self.get("api_token")
    
    # Dictionary-like access
    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dictionary syntax.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value
            
        Raises:
            KeyError: If key is not found
        """
        if key in self._config:
            return self._config[key]
        raise KeyError(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set configuration value using dictionary syntax.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def __delitem__(self, key: str) -> None:
        """Delete configuration value using dictionary syntax.
        
        Args:
            key: Configuration key
            
        Raises:
            KeyError: If key is not found
        """
        if key in self._config:
            del self._config[key]
        else:
            raise KeyError(key)
    
    def __contains__(self, key: str) -> bool:
        """Check if configuration contains key.
        
        Args:
            key: Configuration key
            
        Returns:
            True if key exists, False otherwise
        """
        return key in self._config 