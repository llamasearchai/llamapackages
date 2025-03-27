"""
Utility functions for LlamaPackage.

This module provides utility functions used throughout the package.
"""

import os
import sys
import logging
import subprocess
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
import re
import shutil
import platform

logger = logging.getLogger(__name__)


def get_platform_info() -> Dict[str, str]:
    """Get platform information.
    
    Returns:
        Dictionary with platform information
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a file.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use
        
    Returns:
        Hash of the file as a hex string
    """
    hash_alg = hashlib.new(algorithm)
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_alg.update(chunk)
    
    return hash_alg.hexdigest()


def verify_file_integrity(file_path: str, expected_hash: str, algorithm: str = "sha256") -> bool:
    """Verify file integrity by comparing hash.
    
    Args:
        file_path: Path to the file
        expected_hash: Expected hash value
        algorithm: Hash algorithm used
        
    Returns:
        True if the file hash matches the expected hash
    """
    actual_hash = calculate_file_hash(file_path, algorithm)
    return actual_hash == expected_hash


def run_command(
    cmd: List[str],
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    capture_output: bool = True,
) -> Tuple[int, str, str]:
    """Run a command in a subprocess.
    
    Args:
        cmd: Command and arguments as a list
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        
    Returns:
        Tuple of (return code, stdout, stderr)
    """
    try:
        process = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            text=True,
            capture_output=capture_output,
        )
        
        return process.returncode, process.stdout or "", process.stderr or ""
    
    except Exception as e:
        logger.error(f"Error running command {' '.join(cmd)}: {e}")
        return 1, "", str(e)


def save_json(data: Any, file_path: str, pretty: bool = True) -> bool:
    """Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to the file
        pretty: Whether to format the JSON with indentation
        
    Returns:
        True if the file was saved successfully
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        with open(file_path, "w") as f:
            if pretty:
                json.dump(data, f, indent=2)
            else:
                json.dump(data, f)
        
        return True
    
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        return False


def load_json(file_path: str) -> Optional[Any]:
    """Load data from a JSON file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Loaded data, or None if the file couldn't be loaded
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        return None


def ensure_dir(directory: str) -> bool:
    """Ensure that a directory exists.
    
    Args:
        directory: Directory path
        
    Returns:
        True if the directory exists or was created successfully
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False


def is_valid_package_name(name: str) -> bool:
    """Check if a package name is valid.
    
    Args:
        name: Package name to check
        
    Returns:
        True if the name is valid
    """
    # Package names should be lowercase, with words separated by underscores
    # or hyphens, and should not start or end with a hyphen or underscore
    pattern = r"^[a-z][a-z0-9_-]*[a-z0-9]$"
    return bool(re.match(pattern, name))


def is_valid_version(version: str) -> bool:
    """Check if a version string is valid.
    
    Args:
        version: Version string to check
        
    Returns:
        True if the version is valid
    """
    # Semantic versioning: MAJOR.MINOR.PATCH
    pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"
    return bool(re.match(pattern, version))


def find_files(
    directory: str,
    pattern: str = "*",
    recursive: bool = True,
    exclude_dirs: Optional[List[str]] = None,
) -> List[str]:
    """Find files matching a pattern.
    
    Args:
        directory: Directory to search in
        pattern: Glob pattern to match
        recursive: Whether to search recursively
        exclude_dirs: Directories to exclude
        
    Returns:
        List of matching file paths
    """
    exclude_dirs = exclude_dirs or []
    exclude_dirs = [os.path.normpath(d) for d in exclude_dirs]
    
    result = []
    
    for root, dirs, files in os.walk(directory):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in exclude_dirs]
        
        for file in files:
            if Path(file).match(pattern):
                result.append(os.path.join(root, file))
        
        if not recursive:
            break
    
    return result 