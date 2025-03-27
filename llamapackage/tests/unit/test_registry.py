#!/usr/bin/env python3
"""
Unit tests for the PackageRegistry module.
"""

import os
import pytest
import tempfile
import json
from unittest.mock import patch, MagicMock, mock_open

# Add the parent directories to sys.path to make the llamapackage module importable
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from llamapackage.registry import PackageRegistry, Package, PackageVersion
from llamapackage.config import Config

class TestPackage:
    """Test cases for the Package class."""
    
    def test_package_creation(self):
        """Test Package class initialization."""
        package = Package(
            name="test-package",
            description="A test package",
            author="Test Author",
            homepage="https://example.com/test-package",
            license="MIT",
            latest_version="1.0.0"
        )
        
        assert package.name == "test-package"
        assert package.description == "A test package"
        assert package.author == "Test Author"
        assert package.homepage == "https://example.com/test-package"
        assert package.license == "MIT"
        assert package.latest_version == "1.0.0"
    
    def test_package_from_dict(self):
        """Test creating a Package from a dictionary."""
        package_dict = {
            "name": "dict-package",
            "description": "A package from dict",
            "author": "Dict Author",
            "homepage": "https://example.com/dict-package",
            "license": "Apache-2.0",
            "latest_version": "2.1.0",
            "extra_field": "should be ignored"
        }
        
        package = Package.from_dict(package_dict)
        
        assert package.name == "dict-package"
        assert package.description == "A package from dict"
        assert package.author == "Dict Author"
        assert package.homepage == "https://example.com/dict-package"
        assert package.license == "Apache-2.0"
        assert package.latest_version == "2.1.0"
        assert not hasattr(package, "extra_field")
    
    def test_package_to_dict(self):
        """Test converting Package to dictionary."""
        package = Package(
            name="to-dict-package",
            description="A package for to_dict test",
            author="ToDict Author",
            homepage="https://example.com/to-dict-package",
            license="BSD",
            latest_version="0.5.0"
        )
        
        package_dict = package.to_dict()
        
        assert package_dict == {
            "name": "to-dict-package",
            "description": "A package for to_dict test",
            "author": "ToDict Author",
            "homepage": "https://example.com/to-dict-package",
            "license": "BSD",
            "latest_version": "0.5.0"
        }

class TestPackageVersion:
    """Test cases for the PackageVersion class."""
    
    def test_version_creation(self):
        """Test PackageVersion class initialization."""
        version = PackageVersion(
            version="1.0.0",
            package_name="test-package",
            release_date="2023-01-01T00:00:00Z",
            description="Version 1.0.0 release",
            download_url="https://registry.example.com/test-package/1.0.0.tar.gz"
        )
        
        assert version.version == "1.0.0"
        assert version.package_name == "test-package"
        assert version.release_date == "2023-01-01T00:00:00Z"
        assert version.description == "Version 1.0.0 release"
        assert version.download_url == "https://registry.example.com/test-package/1.0.0.tar.gz"
    
    def test_version_from_dict(self):
        """Test creating a PackageVersion from a dictionary."""
        version_dict = {
            "version": "2.0.0",
            "package_name": "dict-package",
            "release_date": "2023-06-15T12:30:45Z",
            "description": "Version 2.0.0 release",
            "download_url": "https://registry.example.com/dict-package/2.0.0.tar.gz",
            "extra_field": "should be ignored"
        }
        
        version = PackageVersion.from_dict(version_dict)
        
        assert version.version == "2.0.0"
        assert version.package_name == "dict-package"
        assert version.release_date == "2023-06-15T12:30:45Z"
        assert version.description == "Version 2.0.0 release"
        assert version.download_url == "https://registry.example.com/dict-package/2.0.0.tar.gz"
        assert not hasattr(version, "extra_field")
    
    def test_version_to_dict(self):
        """Test converting PackageVersion to dictionary."""
        version = PackageVersion(
            version="3.1.4",
            package_name="to-dict-version",
            release_date="2023-09-22T08:15:30Z",
            description="Version 3.1.4 release",
            download_url="https://registry.example.com/to-dict-version/3.1.4.tar.gz"
        )
        
        version_dict = version.to_dict()
        
        assert version_dict == {
            "version": "3.1.4",
            "package_name": "to-dict-version",
            "release_date": "2023-09-22T08:15:30Z",
            "description": "Version 3.1.4 release",
            "download_url": "https://registry.example.com/to-dict-version/3.1.4.tar.gz"
        }
    
    def test_version_comparison(self):
        """Test comparing PackageVersion objects."""
        v1 = PackageVersion(version="1.0.0", package_name="test-package")
        v2 = PackageVersion(version="1.1.0", package_name="test-package")
        v3 = PackageVersion(version="1.0.1", package_name="test-package")
        v4 = PackageVersion(version="1.0.0", package_name="test-package")
        
        assert v1 < v2
        assert v1 < v3
        assert v3 < v2
        assert v1 == v4
        assert v1 != v2
        assert v1 <= v4
        assert v1 >= v4
        assert v2 > v1
        assert v2 > v3

class TestPackageRegistry:
    """Test cases for the PackageRegistry class."""
    
    @pytest.fixture
    def registry_config(self):
        """Create a test configuration."""
        config = Config()
        config.registry_url = "https://test-registry.llamasearch.ai"
        config.auth_token = "test-token"
        return config
    
    @pytest.fixture
    def registry(self, registry_config):
        """Create a PackageRegistry instance for testing."""
        return PackageRegistry(registry_config)
    
    @patch('llamapackage.registry.requests.get')
    def test_search(self, mock_get, registry):
        """Test searching for packages."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "packages": [
                {
                    "name": "test-package1",
                    "description": "Test package 1",
                    "author": "Test Author",
                    "homepage": "https://example.com/test-package1",
                    "license": "MIT",
                    "latest_version": "1.0.0"
                },
                {
                    "name": "test-package2",
                    "description": "Test package 2",
                    "author": "Test Author",
                    "homepage": "https://example.com/test-package2",
                    "license": "Apache-2.0",
                    "latest_version": "0.5.0"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Search for packages
        results = registry.search("test")
        
        # Assertions
        assert len(results) == 2
        assert isinstance(results[0], Package)
        assert results[0].name == "test-package1"
        assert results[1].name == "test-package2"
        mock_get.assert_called_once_with(
            f"{registry.config.registry_url}/packages/search",
            params={"q": "test"},
            headers={"Authorization": f"Bearer {registry.config.auth_token}"}
        )
    
    @patch('llamapackage.registry.requests.get')
    def test_get_package(self, mock_get, registry):
        """Test getting package information."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "test-package",
            "description": "A test package",
            "author": "Test Author",
            "homepage": "https://example.com/test-package",
            "license": "MIT",
            "latest_version": "1.0.0"
        }
        mock_get.return_value = mock_response
        
        # Get package
        package = registry.get_package("test-package")
        
        # Assertions
        assert isinstance(package, Package)
        assert package.name == "test-package"
        assert package.description == "A test package"
        assert package.author == "Test Author"
        assert package.license == "MIT"
        assert package.latest_version == "1.0.0"
        mock_get.assert_called_once_with(
            f"{registry.config.registry_url}/packages/test-package",
            headers={"Authorization": f"Bearer {registry.config.auth_token}"}
        )
    
    @patch('llamapackage.registry.requests.get')
    def test_get_package_versions(self, mock_get, registry):
        """Test getting package versions."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "versions": [
                {
                    "version": "1.0.0",
                    "package_name": "test-package",
                    "release_date": "2023-01-01T00:00:00Z",
                    "description": "Initial release"
                },
                {
                    "version": "1.1.0",
                    "package_name": "test-package",
                    "release_date": "2023-02-01T00:00:00Z",
                    "description": "Feature update"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Get package versions
        versions = registry.get_package_versions("test-package")
        
        # Assertions
        assert len(versions) == 2
        assert str(versions[0]) == "1.0.0"
        assert str(versions[1]) == "1.1.0"
        mock_get.assert_called_once_with(
            f"{registry.config.registry_url}/packages/test-package/versions",
            headers={"Authorization": f"Bearer {registry.config.auth_token}"}
        )
    
    @patch('llamapackage.registry.requests.post')
    @patch('llamapackage.registry.os.path.exists')
    @patch('llamapackage.registry.os.path.isdir')
    def test_publish_package(self, mock_isdir, mock_exists, mock_post, registry, tmp_path):
        """Test publishing a package."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "name": "test-package",
            "version": "1.0.0",
            "description": "A test package",
            "published_at": "2023-10-01T12:00:00Z"
        }
        mock_post.return_value = mock_response
        
        # Mock file existence check
        mock_exists.return_value = True
        mock_isdir.return_value = True
        
        # Create a temporary pyproject.toml file for testing
        pyproject_content = """
        [project]
        name = "test-package"
        version = "1.0.0"
        description = "A test package"
        """
        
        package_dir = tmp_path / "test-package"
        package_dir.mkdir()
        pyproject_path = package_dir / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)
        
        # Publish package
        with patch('builtins.open', mock_open(read_data=pyproject_content)):
            result = registry.publish_package(str(package_dir))
        
        # Assertions
        assert result.name == "test-package"
        assert result.version == "1.0.0"
        assert result.description == "A test package"
        mock_post.assert_called_once()
    
    @patch('llamapackage.registry.requests.get')
    @patch('llamapackage.registry.requests.post')
    def test_install_package(self, mock_post, mock_get, registry):
        """Test installing a package."""
        # Mock version response
        mock_version_response = MagicMock()
        mock_version_response.status_code = 200
        mock_version_response.json.return_value = {
            "version": "1.0.0",
            "package_name": "test-package",
            "release_date": "2023-01-01T00:00:00Z",
            "description": "Initial release",
            "download_url": "https://test-registry.llamasearch.ai/packages/test-package/1.0.0.tar.gz"
        }
        
        # Mock install response
        mock_install_response = MagicMock()
        mock_install_response.status_code = 200
        mock_install_response.json.return_value = {
            "success": True,
            "message": "Package installed successfully",
            "package": "test-package",
            "version": "1.0.0"
        }
        
        # Set up the mocks
        mock_get.return_value = mock_version_response
        mock_post.return_value = mock_install_response
        
        # Install package
        result = registry.install_package("test-package", "1.0.0")
        
        # Assertions
        assert result is True
        mock_get.assert_called_once_with(
            f"{registry.config.registry_url}/packages/test-package/versions/1.0.0",
            headers={"Authorization": f"Bearer {registry.config.auth_token}"}
        )
        mock_post.assert_called_once_with(
            f"{registry.config.registry_url}/packages/install",
            json={"package_name": "test-package", "version": "1.0.0"},
            headers={"Authorization": f"Bearer {registry.config.auth_token}"}
        )
    
    @patch('llamapackage.registry.requests.get')
    def test_list_installed_packages(self, mock_get, registry):
        """Test listing installed packages."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "installed_packages": [
                {
                    "name": "package1",
                    "version": "1.0.0",
                    "install_time": "2023-05-01T10:00:00Z"
                },
                {
                    "name": "package2",
                    "version": "0.5.0",
                    "install_time": "2023-06-01T15:30:00Z"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # List installed packages
        installed = registry.list_installed_packages()
        
        # Assertions
        assert len(installed) == 2
        assert installed[0].name == "package1"
        assert installed[0].version == "1.0.0"
        assert installed[1].name == "package2"
        assert installed[1].version == "0.5.0"
        mock_get.assert_called_once_with(
            f"{registry.config.registry_url}/packages/installed",
            headers={"Authorization": f"Bearer {registry.config.auth_token}"}
        )
    
    @patch('llamapackage.registry.requests.delete')
    def test_uninstall_package(self, mock_delete, registry):
        """Test uninstalling a package."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "message": "Package uninstalled successfully",
            "package": "test-package"
        }
        mock_delete.return_value = mock_response
        
        # Uninstall package
        result = registry.uninstall_package("test-package")
        
        # Assertions
        assert result is True
        mock_delete.assert_called_once_with(
            f"{registry.config.registry_url}/packages/test-package/uninstall",
            headers={"Authorization": f"Bearer {registry.config.auth_token}"}
        )
    
    @patch('llamapackage.registry.requests.get')
    def test_is_package_installed(self, mock_get, registry):
        """Test checking if a package is installed."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "installed": True,
            "version": "1.0.0"
        }
        mock_get.return_value = mock_response
        
        # Check if package is installed
        result = registry.is_package_installed("test-package")
        
        # Assertions
        assert result is True
        mock_get.assert_called_once_with(
            f"{registry.config.registry_url}/packages/test-package/installed",
            headers={"Authorization": f"Bearer {registry.config.auth_token}"}
        ) 