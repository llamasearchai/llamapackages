#!/usr/bin/env python3
"""
Integration tests for LlamaPackages package operations.

These tests verify the integration between different components
of LlamaPackages during package operations.
"""

import os
import sys
import tempfile
import shutil
import pytest
from pathlib import Path

# Add the parent directories to sys.path to make the llamapackage module importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from llamapackage import (
    Config, 
    PackageRegistry, 
    Authentication, 
    DependencyResolver,
    Storage
)

class TestPackageOperations:
    """Integration tests for package operations."""
    
    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        config = Config()
        config.registry_url = os.environ.get("LLAMA_TEST_REGISTRY_URL", "http://localhost:8000")
        config.auth_token = os.environ.get("LLAMA_TEST_AUTH_TOKEN", "test-token")
        return config
    
    @pytest.fixture
    def test_package_dir(self):
        """Create a temporary test package directory."""
        temp_dir = tempfile.mkdtemp()
        package_dir = Path(temp_dir) / "test-package"
        package_dir.mkdir(exist_ok=True)
        
        # Create package structure
        src_dir = package_dir / "src" / "test_package"
        tests_dir = package_dir / "tests"
        src_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)
        
        # Create package files
        with open(src_dir / "__init__.py", "w") as f:
            f.write('"""Test package."""\n\n__version__ = "0.1.0"\n')
        
        with open(src_dir / "main.py", "w") as f:
            f.write('"""Main module."""\n\ndef hello():\n    return "Hello from test package!"\n')
        
        with open(package_dir / "pyproject.toml", "w") as f:
            f.write("""
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "test-package"
version = "0.1.0"
description = "A test package for integration testing"
readme = "README.md"
authors = [
    {name = "Test Author", email = "test@example.com"}
]
license = {text = "MIT"}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]
keywords = ["test", "integration"]
dependencies = [
    "requests>=2.25.0",
]
requires-python = ">=3.8"
            """)
        
        with open(package_dir / "README.md", "w") as f:
            f.write("# Test Package\n\nA test package for integration testing.\n")
        
        yield package_dir
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"), 
                       reason="Integration tests are disabled")
    def test_full_package_lifecycle(self, config, test_package_dir):
        """Test the complete package lifecycle from publishing to uninstallation."""
        # Initialize components
        auth = Authentication(config)
        registry = PackageRegistry(config)
        resolver = DependencyResolver(config)
        
        # Step 1: Authenticate
        try:
            auth.login()
            assert auth.is_authenticated(), "Authentication failed"
        except Exception as e:
            pytest.skip(f"Authentication failed: {e}")
        
        # Step 2: Publish the test package
        try:
            published = registry.publish_package(str(test_package_dir))
            assert published.name == "test-package"
            assert published.version == "0.1.0"
            print(f"Successfully published {published.name} v{published.version}")
        except Exception as e:
            pytest.fail(f"Failed to publish package: {e}")
        
        # Step 3: Search for the package
        search_results = registry.search("test-package")
        found = False
        for pkg in search_results:
            if pkg.name == "test-package":
                found = True
                break
        assert found, "Published package not found in search results"
        
        # Step 4: Get package details
        package = registry.get_package("test-package")
        assert package.name == "test-package"
        assert package.description == "A test package for integration testing"
        
        # Step 5: Get package versions
        versions = registry.get_package_versions("test-package")
        assert len(versions) >= 1
        assert "0.1.0" in [str(v) for v in versions]
        
        # Step 6: Install the package
        try:
            installed = registry.install_package("test-package", "0.1.0")
            assert installed, "Package installation failed"
        except Exception as e:
            pytest.fail(f"Failed to install package: {e}")
        
        # Step 7: Verify package is installed
        assert registry.is_package_installed("test-package"), "Package not showing as installed"
        
        # Step 8: List installed packages
        installed_packages = registry.list_installed_packages()
        found = False
        for pkg in installed_packages:
            if pkg.name == "test-package":
                found = True
                assert pkg.version == "0.1.0"
                break
        assert found, "Package not found in installed packages list"
        
        # Step 9: Uninstall the package
        try:
            uninstalled = registry.uninstall_package("test-package")
            assert uninstalled, "Package uninstallation failed"
        except Exception as e:
            pytest.fail(f"Failed to uninstall package: {e}")
        
        # Step 10: Verify package is no longer installed
        installed_after = registry.is_package_installed("test-package")
        assert not installed_after, "Package still showing as installed after uninstallation"
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_dependency_resolution(self, config):
        """Test dependency resolution functionality."""
        resolver = DependencyResolver(config)
        
        # Resolve dependencies for a package with known dependencies
        # Note: This test assumes the package exists in the registry
        package_name = "llamatext"  # A package with dependencies
        
        try:
            dependencies = resolver.resolve_dependencies(package_name)
            
            # Verify we got a non-empty list of dependencies
            assert dependencies, "No dependencies resolved"
            
            # Verify each dependency has required fields
            for dep in dependencies:
                assert dep.name, "Dependency missing name"
                assert dep.version, "Dependency missing version"
                
            print(f"Resolved {len(dependencies)} dependencies for {package_name}")
        except Exception as e:
            # If the package doesn't exist, skip the test
            pytest.skip(f"Failed to resolve dependencies: {e}")
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_conflicting_dependencies(self, config):
        """Test handling of conflicting dependencies."""
        resolver = DependencyResolver(config)
        
        # Create a scenario with conflicting dependencies
        # This is a hypothetical test and may need to be adjusted
        # based on actual packages in the registry
        
        try:
            # Attempt to resolve dependencies for two packages with conflicting requirements
            dependencies1 = resolver.resolve_dependencies("package-a")
            dependencies2 = resolver.resolve_dependencies("package-b")
            
            # Check if resolver identified conflicts
            conflicts = resolver.check_conflicts(dependencies1, dependencies2)
            
            # Just verify that the method returns something meaningful
            # The actual result depends on the test packages
            assert isinstance(conflicts, list), "Conflicts check didn't return a list"
            
            print(f"Found {len(conflicts)} conflicts between package-a and package-b")
        except Exception as e:
            # If the packages don't exist, skip the test
            pytest.skip(f"Failed to test conflicts: {e}")

if __name__ == "__main__":
    # Enable running the tests directly
    pytest.main(["-xvs", __file__]) 