"""
Authentication and authorization for LlamaPackage.

This module provides functionality for user authentication and authorization.
"""

import os
import time
import json
import logging
import hashlib
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
from datetime import datetime, timedelta

import requests
import jwt

from llamapackage.config import Config

logger = logging.getLogger(__name__)


class User:
    """User information for LlamaPackage."""
    
    def __init__(
        self,
        username: str,
        email: Optional[str] = None,
        is_admin: bool = False,
        owned_packages: Optional[Set[str]] = None,
    ):
        """Initialize a user.
        
        Args:
            username: Username
            email: Email address
            is_admin: Whether the user is an admin
            owned_packages: Set of packages owned by the user
        """
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.owned_packages = owned_packages or set()
    
    def add_owned_package(self, package_name: str) -> None:
        """Add a package to the user's owned packages.
        
        Args:
            package_name: Name of the package
        """
        self.owned_packages.add(package_name)
    
    def remove_owned_package(self, package_name: str) -> bool:
        """Remove a package from the user's owned packages.
        
        Args:
            package_name: Name of the package
            
        Returns:
            True if the package was removed, False if it was not owned
        """
        if package_name in self.owned_packages:
            self.owned_packages.remove(package_name)
            return True
        return False
    
    def is_owner(self, package_name: str) -> bool:
        """Check if the user owns a package.
        
        Args:
            package_name: Name of the package
            
        Returns:
            True if the user owns the package
        """
        return package_name in self.owned_packages
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary.
        
        Returns:
            Dictionary representation of the user
        """
        return {
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "owned_packages": list(self.owned_packages),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create a user from a dictionary.
        
        Args:
            data: Dictionary representation of the user
            
        Returns:
            User object
        """
        return cls(
            username=data["username"],
            email=data.get("email"),
            is_admin=data.get("is_admin", False),
            owned_packages=set(data.get("owned_packages", [])),
        )


class Authentication:
    """Authentication provider for LlamaPackage."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize authentication provider.
        
        Args:
            config: Configuration provider
        """
        self.config = config or Config()
        self.users_dir = Path(self.config.get("users_dir", str(Path.home() / ".llamapackage" / "users")))
        self.users_dir.mkdir(parents=True, exist_ok=True)
        self.jwt_secret = self.config.get("jwt_secret")
        
        # Create a secret key if one doesn't exist
        if not self.jwt_secret:
            self.jwt_secret = hashlib.sha256(os.urandom(32)).hexdigest()
            self.config.set("jwt_secret", self.jwt_secret)
            self.config.save()
    
    def login(self, username: str, password: str) -> Optional[str]:
        """Log in a user and return a token.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            JWT token if login successful, None otherwise
        """
        user_file = self.users_dir / f"{username}.json"
        
        if not user_file.exists():
            logger.warning(f"User {username} not found")
            return None
        
        try:
            with open(user_file, "r") as f:
                user_data = json.load(f)
            
            # Check password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash != user_data.get("password_hash"):
                logger.warning(f"Invalid password for user {username}")
                return None
            
            # Create JWT token
            payload = {
                "username": username,
                "exp": datetime.utcnow() + timedelta(days=30),
                "iat": datetime.utcnow(),
            }
            token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
            
            return token
        
        except Exception as e:
            logger.error(f"Error during login for user {username}: {e}")
            return None
    
    def register(self, username: str, password: str, email: Optional[str] = None) -> bool:
        """Register a new user.
        
        Args:
            username: Username
            password: Password
            email: Email address
            
        Returns:
            True if registration successful, False otherwise
        """
        user_file = self.users_dir / f"{username}.json"
        
        if user_file.exists():
            logger.warning(f"User {username} already exists")
            return False
        
        try:
            # Create password hash
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Create user data
            user_data = {
                "username": username,
                "email": email,
                "password_hash": password_hash,
                "is_admin": False,
                "owned_packages": [],
                "created_at": datetime.utcnow().isoformat(),
            }
            
            # Save user data
            with open(user_file, "w") as f:
                json.dump(user_data, f, indent=2)
            
            return True
        
        except Exception as e:
            logger.error(f"Error during registration for user {username}: {e}")
            return False
    
    def verify_token(self, token: Optional[str]) -> bool:
        """Verify a JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            True if token is valid, False otherwise
        """
        if not token:
            return False
        
        try:
            jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return False
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return False
    
    def get_user_from_token(self, token: Optional[str]) -> Optional[User]:
        """Get user from a JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            User object if token is valid, None otherwise
        """
        if not token:
            return None
        
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            username = payload.get("username")
            
            if not username:
                return None
            
            user_file = self.users_dir / f"{username}.json"
            
            if not user_file.exists():
                return None
            
            with open(user_file, "r") as f:
                user_data = json.load(f)
            
            return User(
                username=user_data["username"],
                email=user_data.get("email"),
                is_admin=user_data.get("is_admin", False),
                owned_packages=set(user_data.get("owned_packages", [])),
            )
        
        except Exception as e:
            logger.error(f"Error getting user from token: {e}")
            return None
    
    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username.
        
        Args:
            username: Username
            
        Returns:
            User object if found, None otherwise
        """
        user_file = self.users_dir / f"{username}.json"
        
        if not user_file.exists():
            return None
        
        try:
            with open(user_file, "r") as f:
                user_data = json.load(f)
            
            return User(
                username=user_data["username"],
                email=user_data.get("email"),
                is_admin=user_data.get("is_admin", False),
                owned_packages=set(user_data.get("owned_packages", [])),
            )
        
        except Exception as e:
            logger.error(f"Error getting user {username}: {e}")
            return None
    
    def update_user(self, user: User) -> bool:
        """Update a user.
        
        Args:
            user: User object
            
        Returns:
            True if update successful, False otherwise
        """
        user_file = self.users_dir / f"{user.username}.json"
        
        if not user_file.exists():
            logger.warning(f"User {user.username} not found")
            return False
        
        try:
            # Get existing user data
            with open(user_file, "r") as f:
                user_data = json.load(f)
            
            # Update user data
            user_data["email"] = user.email
            user_data["is_admin"] = user.is_admin
            user_data["owned_packages"] = list(user.owned_packages)
            
            # Save user data
            with open(user_file, "w") as f:
                json.dump(user_data, f, indent=2)
            
            return True
        
        except Exception as e:
            logger.error(f"Error updating user {user.username}: {e}")
            return False


class Authorization:
    """Authorization provider for LlamaPackage."""
    
    def can_publish(self, user: Optional[User], package_name: str) -> bool:
        """Check if a user can publish a package.
        
        Args:
            user: User object
            package_name: Name of the package
            
        Returns:
            True if user can publish the package
        """
        if not user:
            return False
        
        # Admins can publish any package
        if user.is_admin:
            return True
        
        # Users can publish packages they own
        return user.is_owner(package_name)
    
    def can_download(self, user: Optional[User], package_name: str) -> bool:
        """Check if a user can download a package.
        
        Args:
            user: User object
            package_name: Name of the package
            
        Returns:
            True if user can download the package
        """
        # All packages are publicly downloadable for now
        return True 