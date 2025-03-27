#!/usr/bin/env python3
"""
Integration tests for the LlamaPackages API.

These tests verify the high-level API functions by testing
the integration between different components.
"""

import os
import sys
import tempfile
import shutil
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directories to sys.path to make the llamapackage module importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from llamapackage import (
    api,
    Config,
    Authentication,
    PackageRegistry,
    Package,
    PackageVersion,
    DependencyResolver
)

class TestAPIIntegration:
    """Integration tests for the API functionality."""
    
    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        config = Config()
        config.registry_url = os.environ.get("LLAMA_TEST_REGISTRY_URL", "http://localhost:8000")
        return config
    
    @pytest.fixture
    def temp_workspace(self):
        """Create a temporary workspace for testing."""
        temp_dir = tempfile.mkdtemp()
        
        # Create package directory
        package_dir = Path(temp_dir) / "workspace"
        package_dir.mkdir(exist_ok=True)
        
        # Create config directory
        config_dir = Path(temp_dir) / "config"
        config_dir.mkdir(exist_ok=True)
        
        # Store original config dir
        original_config_dir = os.environ.get("LLAMA_CONFIG_DIR")
        os.environ["LLAMA_CONFIG_DIR"] = str(config_dir)
        
        yield {
            "root": temp_dir,
            "workspace": package_dir,
            "config": config_dir
        }
        
        # Restore original config dir
        if original_config_dir:
            os.environ["LLAMA_CONFIG_DIR"] = original_config_dir
        else:
            os.environ.pop("LLAMA_CONFIG_DIR", None)
        
        # Clean up
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_init(self, temp_workspace):
        """Test the API initialization."""
        # Test with default config
        llamapackage_api = api.LlamaPackageAPI()
        assert llamapackage_api.config is not None
        assert isinstance(llamapackage_api.auth, Authentication)
        assert isinstance(llamapackage_api.registry, PackageRegistry)
        
        # Test with custom config
        custom_config = Config()
        custom_config.registry_url = "http://test-registry.example.com"
        llamapackage_api = api.LlamaPackageAPI(config=custom_config)
        assert llamapackage_api.config.registry_url == "http://test-registry.example.com"
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_login(self, temp_workspace):
        """Test the API login functionality."""
        # Create API with mocked authentication
        llamapackage_api = api.LlamaPackageAPI()
        
        # Patch the login method to avoid actual network calls
        with patch.object(Authentication, 'login', return_value=True) as mock_login:
            result = llamapackage_api.login("test_user", "test_password")
            assert result is True
            mock_login.assert_called_once_with("test_user", "test_password")
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_search(self, temp_workspace):
        """Test the API search functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Patch the search method to return mock data
        mock_packages = [
            Package(
                name="llamatext",
                description="Text processing utilities",
                author="LlamaSearch.ai",
                homepage="https://llamasearch.ai/packages/llamatext",
                license="MIT",
                latest_version="1.0.0"
            ),
            Package(
                name="llamamath",
                description="Mathematics utilities",
                author="LlamaSearch.ai",
                homepage="https://llamasearch.ai/packages/llamamath",
                license="MIT",
                latest_version="0.5.0"
            )
        ]
        
        with patch.object(PackageRegistry, 'search', return_value=mock_packages) as mock_search:
            results = llamapackage_api.search("llama")
            
            assert len(results) == 2
            assert results[0].name == "llamatext"
            assert results[1].name == "llamamath"
            mock_search.assert_called_once_with("llama")
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_get_package(self, temp_workspace):
        """Test the API get_package functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Create mock package
        mock_package = Package(
            name="llamatext",
            description="Text processing utilities",
            author="LlamaSearch.ai",
            homepage="https://llamasearch.ai/packages/llamatext",
            license="MIT",
            latest_version="1.0.0"
        )
        
        with patch.object(PackageRegistry, 'get_package', return_value=mock_package) as mock_get:
            package = llamapackage_api.get_package("llamatext")
            
            assert package.name == "llamatext"
            assert package.description == "Text processing utilities"
            assert package.latest_version == "1.0.0"
            mock_get.assert_called_once_with("llamatext")
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_get_package_versions(self, temp_workspace):
        """Test the API get_package_versions functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Create mock versions
        mock_versions = [
            PackageVersion("0.9.0", "llamatext", "2023-01-01", "Initial release"),
            PackageVersion("1.0.0", "llamatext", "2023-02-01", "Stable release")
        ]
        
        with patch.object(PackageRegistry, 'get_package_versions', return_value=mock_versions) as mock_get:
            versions = llamapackage_api.get_package_versions("llamatext")
            
            assert len(versions) == 2
            assert versions[0].version == "0.9.0"
            assert versions[1].version == "1.0.0"
            mock_get.assert_called_once_with("llamatext")
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_install_package(self, temp_workspace):
        """Test the API install_package functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Mock is_authenticated to return True
        with patch.object(Authentication, 'is_authenticated', return_value=True):
            # Mock install_package to return True
            with patch.object(PackageRegistry, 'install_package', return_value=True) as mock_install:
                result = llamapackage_api.install_package("llamatext", "1.0.0")
                
                assert result is True
                mock_install.assert_called_once_with("llamatext", "1.0.0")
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_install_unauthenticated(self, temp_workspace):
        """Test that installation fails when not authenticated."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Mock is_authenticated to return False
        with patch.object(Authentication, 'is_authenticated', return_value=False):
            with pytest.raises(ValueError) as excinfo:
                llamapackage_api.install_package("llamatext", "1.0.0")
            
            assert "must be authenticated" in str(excinfo.value).lower()
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_uninstall_package(self, temp_workspace):
        """Test the API uninstall_package functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Mock is_authenticated to return True
        with patch.object(Authentication, 'is_authenticated', return_value=True):
            # Mock uninstall_package to return True
            with patch.object(PackageRegistry, 'uninstall_package', return_value=True) as mock_uninstall:
                result = llamapackage_api.uninstall_package("llamatext")
                
                assert result is True
                mock_uninstall.assert_called_once_with("llamatext")
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_list_installed_packages(self, temp_workspace):
        """Test the API list_installed_packages functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Create mock packages
        mock_packages = [
            Package(
                name="llamatext",
                description="Text processing utilities",
                author="LlamaSearch.ai",
                version="1.0.0"
            ),
            Package(
                name="llamamath",
                description="Mathematics utilities",
                author="LlamaSearch.ai",
                version="0.5.0"
            )
        ]
        
        with patch.object(PackageRegistry, 'list_installed_packages', return_value=mock_packages) as mock_list:
            packages = llamapackage_api.list_installed_packages()
            
            assert len(packages) == 2
            assert packages[0].name == "llamatext"
            assert packages[1].name == "llamamath"
            mock_list.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_publish_package(self, temp_workspace):
        """Test the API publish_package functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Create a test package directory
        package_dir = Path(temp_workspace["workspace"]) / "test-package"
        package_dir.mkdir()
        
        # Create package files
        with open(package_dir / "pyproject.toml", "w") as f:
            f.write("""
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "test-package"
version = "0.1.0"
description = "A test package for integration testing"
authors = [
    {name = "Test Author", email = "test@example.com"}
]
            """)
        
        # Mock is_authenticated to return True
        with patch.object(Authentication, 'is_authenticated', return_value=True):
            # Mock publish_package to return a package
            mock_result = Package(
                name="test-package",
                version="0.1.0",
                description="A test package for integration testing",
                author="Test Author"
            )
            
            with patch.object(PackageRegistry, 'publish_package', return_value=mock_result) as mock_publish:
                result = llamapackage_api.publish_package(str(package_dir))
                
                assert result.name == "test-package"
                assert result.version == "0.1.0"
                mock_publish.assert_called_once_with(str(package_dir))
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_resolve_dependencies(self, temp_workspace):
        """Test the API resolve_dependencies functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Create mock dependencies
        mock_dependencies = [
            Package(name="dep1", version="1.0.0"),
            Package(name="dep2", version="2.0.0")
        ]
        
        with patch.object(DependencyResolver, 'resolve_dependencies', return_value=mock_dependencies) as mock_resolve:
            dependencies = llamapackage_api.resolve_dependencies("llamatext")
            
            assert len(dependencies) == 2
            assert dependencies[0].name == "dep1"
            assert dependencies[1].name == "dep2"
            mock_resolve.assert_called_once_with("llamatext")
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_check_for_updates(self, temp_workspace):
        """Test the API check_for_updates functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Create mock updates
        mock_updates = {
            "llamatext": {"current": "0.9.0", "latest": "1.0.0"},
            "llamamath": {"current": "0.5.0", "latest": "0.5.0"}
        }
        
        with patch.object(PackageRegistry, 'check_for_updates', return_value=mock_updates) as mock_check:
            updates = llamapackage_api.check_for_updates()
            
            assert "llamatext" in updates
            assert updates["llamatext"]["latest"] == "1.0.0"
            assert "llamamath" in updates
            mock_check.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_api_configuration(self, temp_workspace):
        """Test the API configuration functionality."""
        llamapackage_api = api.LlamaPackageAPI()
        
        # Test getting a config value
        with patch.object(Config, 'get', return_value="http://test-registry.example.com") as mock_get:
            value = llamapackage_api.get_config("registry_url")
            
            assert value == "http://test-registry.example.com"
            mock_get.assert_called_once_with("registry_url")
        
        # Test setting a config value
        with patch.object(Config, 'set') as mock_set:
            llamapackage_api.set_config("registry_url", "http://new-registry.example.com")
            
            mock_set.assert_called_once_with("registry_url", "http://new-registry.example.com")
        
        # Test saving the config
        with patch.object(Config, 'save') as mock_save:
            llamapackage_api.save_config()
            
            mock_save.assert_called_once()

if __name__ == "__main__":
    # Enable running the tests directly
    pytest.main(["-xvs", __file__]) 