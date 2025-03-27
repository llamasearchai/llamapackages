"""
Package registry functionality for LlamaPackage.

This module provides the core functionality for managing a package registry,
including adding, removing, searching, and retrieving packages.
"""

from typing import Dict, List, Optional, Any, Union
import logging
from datetime import datetime
import json
import os
from pathlib import Path

import requests
from pydantic import BaseModel, Field, validator
import semantic_version

from llamapackage.storage import Storage
from llamapackage.dependency import DependencyResolver
from llamapackage.auth import Authentication, Authorization
from llamapackage.config import Config

logger = logging.getLogger(__name__)


class PackageVersion(BaseModel):
    """Package version information."""
    
    version: str
    upload_date: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    dependencies: Dict[str, str] = Field(default_factory=dict)
    download_url: Optional[str] = None
    sha256: Optional[str] = None
    
    @validator("version")
    def validate_version(cls, v: str) -> str:
        """Validate the version is a valid semantic version."""
        semantic_version.Version.parse(v)
        return v


class Package(BaseModel):
    """Package information."""
    
    name: str
    versions: Dict[str, PackageVersion] = Field(default_factory=dict)
    description: Optional[str] = None
    author: Optional[str] = None
    author_email: Optional[str] = None
    homepage: Optional[str] = None
    repository: Optional[str] = None
    license: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    classifiers: List[str] = Field(default_factory=list)
    
    def add_version(self, version: PackageVersion) -> None:
        """Add a version to the package."""
        self.versions[version.version] = version
    
    def get_version(self, version: str) -> Optional[PackageVersion]:
        """Get a specific version of the package."""
        return self.versions.get(version)
    
    def get_latest_version(self) -> Optional[PackageVersion]:
        """Get the latest version of the package."""
        if not self.versions:
            return None
        
        latest = None
        latest_ver = None
        
        for ver_str, ver_obj in self.versions.items():
            ver = semantic_version.Version.parse(ver_str)
            if latest_ver is None or ver > latest_ver:
                latest_ver = ver
                latest = ver_obj
        
        return latest


class PackageRegistry:
    """Manager for package registry operations."""
    
    def __init__(
        self,
        storage: Optional[Storage] = None,
        resolver: Optional[DependencyResolver] = None,
        auth: Optional[Authentication] = None,
        config: Optional[Config] = None,
    ):
        """Initialize the package registry.
        
        Args:
            storage: Storage backend for packages
            resolver: Dependency resolver
            auth: Authentication provider
            config: Configuration provider
        """
        self.storage = storage or Storage()
        self.resolver = resolver or DependencyResolver()
        self.auth = auth or Authentication()
        self.config = config or Config()
        self.packages: Dict[str, Package] = {}
        self._loaded = False
    
    def load(self) -> None:
        """Load package information from storage."""
        if self._loaded:
            return
        
        try:
            package_index = self.storage.get_index()
            if package_index:
                for name, package_data in package_index.items():
                    self.packages[name] = Package.parse_obj(package_data)
            self._loaded = True
        except Exception as e:
            logger.error(f"Failed to load package index: {e}")
            raise
    
    def save(self) -> None:
        """Save package information to storage."""
        try:
            package_index = {name: package.dict() for name, package in self.packages.items()}
            self.storage.save_index(package_index)
        except Exception as e:
            logger.error(f"Failed to save package index: {e}")
            raise
    
    def add_package(self, package: Package) -> None:
        """Add a package to the registry.
        
        Args:
            package: Package to add
        """
        self.load()
        self.packages[package.name] = package
        self.save()
    
    def get_package(self, name: str) -> Optional[Package]:
        """Get a package from the registry.
        
        Args:
            name: Name of the package
            
        Returns:
            Package or None if not found
        """
        self.load()
        return self.packages.get(name)
    
    def search_packages(self, query: str) -> List[Package]:
        """Search for packages in the registry.
        
        Args:
            query: Search query
            
        Returns:
            List of matching packages
        """
        self.load()
        query = query.lower()
        results = []
        
        for name, package in self.packages.items():
            if query in name.lower():
                results.append(package)
                continue
                
            if package.description and query in package.description.lower():
                results.append(package)
                continue
                
            if any(query in keyword.lower() for keyword in package.keywords):
                results.append(package)
                continue
        
        return results
    
    def publish_package(
        self,
        name: str,
        version: str,
        package_file: Union[str, Path, bytes],
        metadata: Dict[str, Any],
        token: Optional[str] = None,
    ) -> PackageVersion:
        """Publish a package to the registry.
        
        Args:
            name: Package name
            version: Package version
            package_file: Path to package file or file content
            metadata: Package metadata
            token: Authentication token
            
        Returns:
            Published package version
        """
        self.load()
        
        # Verify authentication
        if not self.auth.verify_token(token):
            raise ValueError("Invalid authentication token")
        
        # Check if user is authorized to publish this package
        user = self.auth.get_user_from_token(token)
        if not Authorization().can_publish(user, name):
            raise ValueError(f"User {user} is not authorized to publish package {name}")
        
        # Validate version
        try:
            semantic_version.Version.parse(version)
        except ValueError:
            raise ValueError(f"Invalid version: {version}")
        
        # Get or create package
        package = self.get_package(name)
        if not package:
            package = Package(name=name)
        
        # Check if version already exists
        if version in package.versions:
            raise ValueError(f"Version {version} already exists")
        
        # Upload package file
        file_url = self.storage.upload_package(name, version, package_file)
        
        # Create package version
        package_version = PackageVersion(
            version=version,
            upload_date=datetime.now(),
            metadata=metadata,
            dependencies=metadata.get("dependencies", {}),
            download_url=file_url,
        )
        
        # Add version to package
        package.add_version(package_version)
        
        # Update registry
        self.add_package(package)
        
        return package_version
    
    def download_package(
        self,
        name: str,
        version: Optional[str] = None,
        destination: Optional[Union[str, Path]] = None,
    ) -> Path:
        """Download a package from the registry.
        
        Args:
            name: Package name
            version: Package version, or latest if not specified
            destination: Destination directory
            
        Returns:
            Path to downloaded file
        """
        self.load()
        
        # Get package
        package = self.get_package(name)
        if not package:
            raise ValueError(f"Package {name} not found")
        
        # Get version
        if version:
            package_version = package.get_version(version)
            if not package_version:
                raise ValueError(f"Version {version} not found for package {name}")
        else:
            package_version = package.get_latest_version()
            if not package_version:
                raise ValueError(f"No versions found for package {name}")
        
        # Get download URL
        download_url = package_version.download_url
        if not download_url:
            raise ValueError(f"No download URL for package {name} version {package_version.version}")
        
        # Download package using Storage
        api_token = self.config.get_api_token()
        return self.storage.download_package(
            name, package_version.version, download_url, destination, api_token
        ) 