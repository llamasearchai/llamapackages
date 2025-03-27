"""
Pytest configuration file for LlamaPackages test suite.

This file contains shared fixtures and configuration for the test suite.
"""

import os
import sys
import pytest
from pathlib import Path

# Add the package source directory to the path
# This allows imports to work correctly during testing
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

# Define test markers
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: mark a test as a unit test")
    config.addinivalue_line("markers", "integration: mark a test as an integration test")
    config.addinivalue_line("markers", "slow: mark a test as slow running")
    config.addinivalue_line("markers", "requires_auth: mark a test that requires authentication")
    config.addinivalue_line("markers", "requires_internet: mark a test that requires internet connection")

# Skip integration tests unless explicitly enabled
def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to skip integration tests by default.
    
    Integration tests are only run when the LLAMA_RUN_INTEGRATION_TESTS
    environment variable is set.
    """
    if not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"):
        skip_integration = pytest.mark.skip(reason="Integration tests are disabled")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
    
    # Skip tests requiring authentication unless credentials are available
    if not os.environ.get("LLAMA_TEST_AUTH_TOKEN"):
        skip_auth = pytest.mark.skip(reason="Authentication required but no credentials available")
        for item in items:
            if "requires_auth" in item.keywords:
                item.add_marker(skip_auth)
    
    # Skip tests requiring internet unless explicitly enabled
    if not os.environ.get("LLAMA_ALLOW_INTERNET_TESTS"):
        skip_internet = pytest.mark.skip(reason="Internet tests are disabled")
        for item in items:
            if "requires_internet" in item.keywords:
                item.add_marker(skip_internet)

@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary configuration directory for tests."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Store the original config dir environment variable
    original_config_dir = os.environ.get("LLAMA_CONFIG_DIR")
    
    # Set the environment variable to the test directory
    os.environ["LLAMA_CONFIG_DIR"] = str(config_dir)
    
    yield config_dir
    
    # Restore the original environment variable
    if original_config_dir:
        os.environ["LLAMA_CONFIG_DIR"] = original_config_dir
    else:
        del os.environ["LLAMA_CONFIG_DIR"]

@pytest.fixture
def mock_registry_response():
    """Return mock responses for registry API calls."""
    return {
        "packages": [
            {
                "name": "llamatext",
                "description": "Text processing utilities",
                "author": "LlamaSearch.ai",
                "homepage": "https://llamasearch.ai/packages/llamatext",
                "license": "MIT",
                "latest_version": "1.0.0"
            },
            {
                "name": "llamamath",
                "description": "Mathematics utilities",
                "author": "LlamaSearch.ai",
                "homepage": "https://llamasearch.ai/packages/llamamath",
                "license": "MIT",
                "latest_version": "0.5.0"
            }
        ],
        "package": {
            "name": "llamatext",
            "description": "Text processing utilities",
            "author": "LlamaSearch.ai",
            "homepage": "https://llamasearch.ai/packages/llamatext",
            "license": "MIT",
            "latest_version": "1.0.0"
        },
        "versions": [
            {
                "version": "0.9.0",
                "release_date": "2023-01-01",
                "description": "Initial release"
            },
            {
                "version": "1.0.0",
                "release_date": "2023-02-01",
                "description": "Stable release"
            }
        ],
        "auth": {
            "token": "test-token-123",
            "user": {
                "username": "test_user",
                "email": "test@example.com"
            }
        }
    }

@pytest.fixture
def mock_package_data():
    """Return mock package data for testing."""
    return {
        "name": "test-package",
        "version": "0.1.0",
        "description": "A test package for integration testing",
        "author": "Test Author",
        "email": "test@example.com",
        "homepage": "https://example.com/test-package",
        "license": "MIT",
        "keywords": ["test", "integration"],
        "dependencies": ["requests>=2.25.0"],
        "python_requires": ">=3.8"
    } 