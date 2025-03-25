"""
Dependency resolution for LlamaPackage.

This module provides functionality for resolving package dependencies.
"""

import logging
from typing import Dict, List, Set, Optional, Tuple
import subprocess
import sys

import semantic_version

from llamapackage.config import Config

logger = logging.getLogger(__name__)


class DependencyConflict(Exception):
    """Exception raised when dependency conflicts cannot be resolved."""
    
    def __init__(self, package: str, required_versions: Dict[str, str]):
        """Initialize a dependency conflict exception.
        
        Args:
            package: Package with conflicting requirements
            required_versions: Dictionary of package -> version required by different packages
        """
        self.package = package
        self.required_versions = required_versions
        versions_str = ", ".join(f"{pkg} requires {ver}" for pkg, ver in required_versions.items())
        super().__init__(f"Dependency conflict for {package}: {versions_str}")


class DependencyResolver:
    """Resolver for package dependencies."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the dependency resolver.
        
        Args:
            config: Configuration provider
        """
        self.config = config or Config()
    
    def resolve_dependencies(
        self,
        dependencies: Dict[str, str],
        installed: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """Resolve dependencies for a set of packages.
        
        Args:
            dependencies: Dictionary of package name -> version constraint
            installed: Dictionary of already installed package name -> version,
                or None to detect from the environment
                
        Returns:
            Dictionary of package name -> version to install
            
        Raises:
            DependencyConflict: If dependencies cannot be resolved
        """
        # Get installed packages if not provided
        if installed is None:
            installed = self.get_installed_packages()
        
        # Create a map of package -> set of required versions
        required_versions: Dict[str, Dict[str, str]] = {}
        for pkg, version in dependencies.items():
            required_versions.setdefault(pkg, {})["root"] = version
        
        # Recursively get transitive dependencies
        visited: Set[str] = set()
        to_install: Dict[str, str] = {}
        
        for pkg, version in dependencies.items():
            self._resolve_package(
                pkg,
                version,
                required_versions,
                installed,
                to_install,
                visited,
            )
        
        return to_install
    
    def _resolve_package(
        self,
        package: str,
        version_constraint: str,
        required_versions: Dict[str, Dict[str, str]],
        installed: Dict[str, str],
        to_install: Dict[str, str],
        visited: Set[str],
    ) -> None:
        """Recursively resolve dependencies for a package.
        
        Args:
            package: Package name
            version_constraint: Version constraint
            required_versions: Map of package -> (requirer -> version)
            installed: Dictionary of installed package name -> version
            to_install: Dictionary of package name -> version to install (output)
            visited: Set of packages already visited (to prevent cycles)
            
        Raises:
            DependencyConflict: If dependencies cannot be resolved
        """
        # Check if we've already visited this package
        if package in visited:
            return
        
        visited.add(package)
        
        # Check if the package is already installed
        if package in installed:
            installed_version = semantic_version.Version.coerce(installed[package])
            if self._satisfies(installed_version, version_constraint):
                # Already installed and satisfies the constraint
                return
        
        # Get the best version that satisfies all constraints
        best_version = self._get_best_version(package, required_versions.get(package, {}))
        if best_version is None:
            # Can't satisfy all constraints
            raise DependencyConflict(package, required_versions.get(package, {}))
        
        # Add to the installation list
        to_install[package] = str(best_version)
        
        # Get dependencies for this version
        deps = self._get_dependencies(package, best_version)
        
        # Add to required versions
        for dep, dep_constraint in deps.items():
            required_versions.setdefault(dep, {})[package] = dep_constraint
        
        # Recursively resolve dependencies
        for dep, dep_constraint in deps.items():
            self._resolve_package(
                dep,
                dep_constraint,
                required_versions,
                installed,
                to_install,
                visited,
            )
    
    def _get_best_version(
        self,
        package: str,
        constraints: Dict[str, str],
    ) -> Optional[semantic_version.Version]:
        """Get the best version that satisfies all constraints.
        
        Args:
            package: Package name
            constraints: Dictionary of requirer -> version constraint
            
        Returns:
            Best version that satisfies all constraints, or None if no such version exists
        """
        if not constraints:
            return None
        
        # Get all available versions
        versions = self._get_available_versions(package)
        if not versions:
            return None
        
        # Filter versions that satisfy all constraints
        valid_versions = []
        for version in versions:
            if all(self._satisfies(version, constraint) for constraint in constraints.values()):
                valid_versions.append(version)
        
        if not valid_versions:
            return None
        
        # Return the latest valid version
        return max(valid_versions)
    
    def _satisfies(self, version: semantic_version.Version, constraint: str) -> bool:
        """Check if a version satisfies a constraint.
        
        Args:
            version: Version to check
            constraint: Version constraint
            
        Returns:
            True if the version satisfies the constraint, False otherwise
        """
        # Simple version comparison for now, could be expanded for more complex constraints
        if constraint.startswith("=="):
            required = semantic_version.Version.coerce(constraint[2:])
            return version == required
        elif constraint.startswith(">="):
            required = semantic_version.Version.coerce(constraint[2:])
            return version >= required
        elif constraint.startswith(">"):
            required = semantic_version.Version.coerce(constraint[1:])
            return version > required
        elif constraint.startswith("<="):
            required = semantic_version.Version.coerce(constraint[2:])
            return version <= required
        elif constraint.startswith("<"):
            required = semantic_version.Version.coerce(constraint[1:])
            return version < required
        elif constraint.startswith("~="):
            required = semantic_version.Version.coerce(constraint[2:])
            return (
                version >= required and
                version.major == required.major and
                (version.major > 0 or version.minor == required.minor)
            )
        else:
            # Assume exact version
            required = semantic_version.Version.coerce(constraint)
            return version == required
    
    def _get_available_versions(self, package: str) -> List[semantic_version.Version]:
        """Get available versions for a package.
        
        Args:
            package: Package name
            
        Returns:
            List of available versions
        """
        try:
            # Try to get versions from PyPI
            import requests
            response = requests.get(f"https://pypi.org/pypi/{package}/json")
            if response.status_code == 200:
                data = response.json()
                return [
                    semantic_version.Version.coerce(v)
                    for v in data.get("releases", {}).keys()
                ]
            
            # Fall back to package registry
            registry_url = self.config.get_registry_url()
            response = requests.get(f"{registry_url}/api/v1/packages/{package}")
            if response.status_code == 200:
                data = response.json()
                return [
                    semantic_version.Version.coerce(v)
                    for v in data.get("versions", {}).keys()
                ]
            
            return []
        
        except Exception as e:
            logger.error(f"Error getting available versions for {package}: {e}")
            return []
    
    def _get_dependencies(
        self,
        package: str,
        version: semantic_version.Version,
    ) -> Dict[str, str]:
        """Get dependencies for a package version.
        
        Args:
            package: Package name
            version: Package version
            
        Returns:
            Dictionary of package name -> version constraint
        """
        try:
            # Try to get dependencies from PyPI
            import requests
            response = requests.get(f"https://pypi.org/pypi/{package}/{version}/json")
            if response.status_code == 200:
                data = response.json()
                requires_dist = data.get("info", {}).get("requires_dist", [])
                return self._parse_requirements(requires_dist)
            
            # Fall back to package registry
            registry_url = self.config.get_registry_url()
            response = requests.get(f"{registry_url}/api/v1/packages/{package}/{version}")
            if response.status_code == 200:
                data = response.json()
                return data.get("dependencies", {})
            
            return {}
        
        except Exception as e:
            logger.error(f"Error getting dependencies for {package} {version}: {e}")
            return {}
    
    def _parse_requirements(self, requires_dist: List[str]) -> Dict[str, str]:
        """Parse requirements from requires_dist format.
        
        Args:
            requires_dist: List of requirement strings
            
        Returns:
            Dictionary of package name -> version constraint
        """
        result = {}
        for req in requires_dist:
            # Strip environment markers
            if ";" in req:
                req = req.split(";")[0].strip()
            
            # Parse package name and version constraint
            if "(" in req and ")" in req:
                name, constraint = req.split("(", 1)
                constraint = constraint.split(")", 1)[0].strip()
                name = name.strip()
                result[name] = constraint
            else:
                name = req.strip()
                result[name] = ""
        
        return result
    
    def get_installed_packages(self) -> Dict[str, str]:
        """Get installed packages in the current environment.
        
        Returns:
            Dictionary of package name -> version
        """
        try:
            # Use pip to get installed packages
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                logger.error(f"Error getting installed packages: {result.stderr}")
                return {}
            
            import json
            packages = json.loads(result.stdout)
            return {pkg["name"]: pkg["version"] for pkg in packages}
        
        except Exception as e:
            logger.error(f"Error getting installed packages: {e}")
            return {} 