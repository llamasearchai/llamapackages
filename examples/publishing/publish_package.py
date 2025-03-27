#!/usr/bin/env python3
"""
Package Publishing Example

This example demonstrates how to publish a package to the LlamaPackages registry.
"""

import os
import sys
from pathlib import Path
import tempfile
import shutil

# Add the parent directory to sys.path to make the llamapackage module importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from llamapackage import PackageRegistry, Config, Authentication

def main():
    """Demonstrate how to publish a package to the registry."""
    print("LlamaPackages Publishing Example")
    print("===============================\n")

    # Check for authentication token
    auth_token = os.environ.get("LLAMA_AUTH_TOKEN")
    if not auth_token:
        print("Error: LLAMA_AUTH_TOKEN environment variable not set")
        print("Please set your authentication token to publish packages.")
        return
    
    # Initialize the configuration
    config = Config()
    config.registry_url = "https://registry.llamasearch.ai"
    config.auth_token = auth_token
    
    # Initialize the authentication and package registry
    auth = Authentication(config)
    registry = PackageRegistry(config)
    
    # Check if the user is authenticated
    if not auth.is_authenticated():
        print("Authenticating with the registry...")
        try:
            auth.login()
            print("Authentication successful.")
        except Exception as e:
            print(f"Authentication failed: {e}")
            return
    
    # Create a temporary package for demonstration
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\nCreating a sample package in: {temp_dir}")
        package_path = create_sample_package(temp_dir)
        
        # Publish the package
        print(f"\nPublishing package from: {package_path}")
        try:
            result = registry.publish_package(package_path)
            print("\nPackage published successfully!")
            print(f"Name: {result.name}")
            print(f"Version: {result.version}")
            print(f"Description: {result.description}")
            print(f"URL: {config.registry_url}/packages/{result.name}")
        except Exception as e:
            print(f"Failed to publish package: {e}")
    
    print("\nPublishing example completed.")

def create_sample_package(base_path):
    """Create a sample package structure for demonstration."""
    package_name = "sample-llamapackage"
    package_dir = Path(base_path) / package_name
    
    # Create package directory structure
    src_dir = package_dir / "src" / package_name.replace("-", "_")
    tests_dir = package_dir / "tests"
    
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)
    
    # Create package files
    write_file(src_dir / "__init__.py", """
\"\"\"Sample LlamaPackage for demonstration.\"\"\"

__version__ = "0.1.0"
    """)
    
    write_file(src_dir / "main.py", """
\"\"\"Main module for the sample package.\"\"\"

def hello():
    \"\"\"Return a greeting message.\"\"\"
    return "Hello from Sample LlamaPackage!"
    """)
    
    write_file(package_dir / "pyproject.toml", f"""
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{package_name}"
version = "0.1.0"
description = "A sample package for LlamaPackages demonstration"
readme = "README.md"
authors = [
    {{name = "Sample Author", email = "author@example.com"}}
]
license = {{text = "MIT"}}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
]
keywords = ["sample", "llama", "package"]
dependencies = [
    "requests>=2.25.0",
]
requires-python = ">=3.8"

[project.urls]
"Homepage" = "https://github.com/sample/sample-llamapackage"
"Bug Tracker" = "https://github.com/sample/sample-llamapackage/issues"
    """)
    
    write_file(package_dir / "README.md", f"""
# {package_name}

A sample package for LlamaPackages demonstration.

## Installation

```bash
pip install {package_name}
```

## Usage

```python
from {package_name.replace("-", "_")} import main

print(main.hello())
```
    """)
    
    write_file(tests_dir / "test_main.py", """
\"\"\"Tests for the main module.\"\"\"

from sample_llamapackage import main

def test_hello():
    \"\"\"Test the hello function.\"\"\"
    assert main.hello() == "Hello from Sample LlamaPackage!"
    """)
    
    print(f"Created sample package structure in {package_dir}")
    return str(package_dir)

def write_file(path, content):
    """Write content to a file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")

if __name__ == "__main__":
    main() 