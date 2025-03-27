#!/usr/bin/env python3
"""
Unit tests for the Authentication module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

# Add the parent directories to sys.path to make the llamapackage module importable
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from llamapackage.auth import Authentication, Authorization, User
from llamapackage.config import Config

class TestAuthentication:
    """Test cases for the Authentication class."""
    
    @pytest.fixture
    def auth_config(self):
        """Create a test configuration."""
        config = Config()
        config.registry_url = "https://test-registry.llamasearch.ai"
        config.auth_token = "test-token"
        return config
    
    @pytest.fixture
    def auth(self, auth_config):
        """Create an Authentication instance for testing."""
        return Authentication(auth_config)
    
    def test_init(self, auth, auth_config):
        """Test initialization of Authentication."""
        assert auth.config == auth_config
        assert auth._is_authenticated is False
    
    @patch('llamapackage.auth.requests.post')
    def test_login_success(self, mock_post, auth):
        """Test successful login."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "token": "new-token",
            "expires_at": "2023-12-31T23:59:59Z"
        }
        mock_post.return_value = mock_response
        
        # Call login
        result = auth.login()
        
        # Assertions
        assert result is True
        assert auth._is_authenticated is True
        assert auth.config.auth_token == "new-token"
        mock_post.assert_called_once_with(
            f"{auth.config.registry_url}/auth/token",
            json={"token": "test-token"},
            headers={"Content-Type": "application/json"}
        )
    
    @patch('llamapackage.auth.requests.post')
    def test_login_failure(self, mock_post, auth):
        """Test failed login."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid token"}
        mock_post.return_value = mock_response
        
        # Call login and expect exception
        with pytest.raises(Exception) as excinfo:
            auth.login()
        
        # Assertions
        assert "Authentication failed" in str(excinfo.value)
        assert auth._is_authenticated is False
    
    def test_is_authenticated(self, auth):
        """Test is_authenticated method."""
        # Initially not authenticated
        assert auth.is_authenticated() is False
        
        # Set authenticated flag and test again
        auth._is_authenticated = True
        assert auth.is_authenticated() is True
    
    @patch('llamapackage.auth.requests.get')
    def test_validate_token_success(self, mock_get, auth):
        """Test successful token validation."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"valid": True}
        mock_get.return_value = mock_response
        
        # Call validate_token
        result = auth.validate_token()
        
        # Assertions
        assert result is True
        assert auth._is_authenticated is True
        mock_get.assert_called_once_with(
            f"{auth.config.registry_url}/auth/validate",
            headers={"Authorization": f"Bearer {auth.config.auth_token}"}
        )
    
    @patch('llamapackage.auth.requests.get')
    def test_validate_token_failure(self, mock_get, auth):
        """Test failed token validation."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"valid": False, "error": "Token expired"}
        mock_get.return_value = mock_response
        
        # Call validate_token
        result = auth.validate_token()
        
        # Assertions
        assert result is False
        assert auth._is_authenticated is False
    
    @patch('llamapackage.auth.requests.post')
    def test_logout(self, mock_post, auth):
        """Test logout."""
        # Set authenticated flag
        auth._is_authenticated = True
        
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Call logout
        auth.logout()
        
        # Assertions
        assert auth._is_authenticated is False
        mock_post.assert_called_once_with(
            f"{auth.config.registry_url}/auth/logout",
            headers={"Authorization": f"Bearer {auth.config.auth_token}"}
        )

class TestUser:
    """Test cases for the User class."""
    
    def test_user_creation(self):
        """Test User class initialization."""
        user = User(
            id="user123",
            username="testuser",
            email="test@example.com",
            is_admin=False
        )
        
        assert user.id == "user123"
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_admin is False
    
    def test_user_from_dict(self):
        """Test creating a User from a dictionary."""
        user_dict = {
            "id": "user456",
            "username": "dictuser",
            "email": "dict@example.com",
            "is_admin": True,
            "extra_field": "should be ignored"
        }
        
        user = User.from_dict(user_dict)
        
        assert user.id == "user456"
        assert user.username == "dictuser"
        assert user.email == "dict@example.com"
        assert user.is_admin is True
        assert not hasattr(user, "extra_field")
    
    def test_user_to_dict(self):
        """Test converting User to dictionary."""
        user = User(
            id="user789",
            username="tester",
            email="tester@example.com",
            is_admin=False
        )
        
        user_dict = user.to_dict()
        
        assert user_dict == {
            "id": "user789",
            "username": "tester",
            "email": "tester@example.com",
            "is_admin": False
        }

class TestAuthorization:
    """Test cases for the Authorization class."""
    
    @pytest.fixture
    def auth_config(self):
        """Create a test configuration."""
        config = Config()
        config.registry_url = "https://test-registry.llamasearch.ai"
        config.auth_token = "test-token"
        return config
    
    @pytest.fixture
    def authorization(self, auth_config):
        """Create an Authorization instance for testing."""
        return Authorization(auth_config)
    
    @patch('llamapackage.auth.requests.get')
    def test_has_permission_success(self, mock_get, authorization):
        """Test successful permission check."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"has_permission": True}
        mock_get.return_value = mock_response
        
        # Call has_permission
        result = authorization.has_permission("publish", resource="package:testpackage")
        
        # Assertions
        assert result is True
        mock_get.assert_called_once_with(
            f"{authorization.config.registry_url}/auth/check-permission",
            params={"action": "publish", "resource": "package:testpackage"},
            headers={"Authorization": f"Bearer {authorization.config.auth_token}"}
        )
    
    @patch('llamapackage.auth.requests.get')
    def test_has_permission_failure(self, mock_get, authorization):
        """Test failed permission check."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"has_permission": False, "error": "Permission denied"}
        mock_get.return_value = mock_response
        
        # Call has_permission
        result = authorization.has_permission("admin", resource="system:config")
        
        # Assertions
        assert result is False
    
    @patch('llamapackage.auth.requests.get')
    def test_get_current_user_success(self, mock_get, authorization):
        """Test successful current user retrieval."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "is_admin": False
        }
        mock_get.return_value = mock_response
        
        # Call get_current_user
        user = authorization.get_current_user()
        
        # Assertions
        assert isinstance(user, User)
        assert user.id == "user123"
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_admin is False
        mock_get.assert_called_once_with(
            f"{authorization.config.registry_url}/auth/me",
            headers={"Authorization": f"Bearer {authorization.config.auth_token}"}
        )
    
    @patch('llamapackage.auth.requests.get')
    def test_get_current_user_failure(self, mock_get, authorization):
        """Test failed current user retrieval."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_get.return_value = mock_response
        
        # Call get_current_user and expect exception
        with pytest.raises(Exception) as excinfo:
            authorization.get_current_user()
        
        # Assertions
        assert "Failed to get current user" in str(excinfo.value) 