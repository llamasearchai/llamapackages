#!/usr/bin/env python3
"""
Basic Usage Example for LlamaPackages

This example demonstrates the basic functionality of LlamaPackages,
including searching, installing, and listing packages.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to make the llamapackage module importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from llamapackage import PackageRegistry, Config

def main():
    """Demonstrate basic LlamaPackages functionality."""
    print("LlamaPackages Basic Usage Example")
    print("=================================\n")

    # Initialize the configuration
    config = Config()
    config.registry_url = "https://registry.llamasearch.ai"
    config.auth_token = os.environ.get("LLAMA_AUTH_TOKEN", "")
    
    print(f"Using registry: {config.registry_url}\n")

    # Initialize the package registry
    registry = PackageRegistry(config)
    
    # Search for packages
    print("Searching for packages related to 'text'...")
    search_results = registry.search("text")
    
    print(f"Found {len(search_results)} packages:\n")
    for package in search_results:
        print(f"- {package.name} (v{package.latest_version}): {package.description}")
    
    print("\n")
    
    # Get information about a specific package
    package_name = "llamatext"
    print(f"Getting information about '{package_name}'...")
    
    try:
        package_info = registry.get_package(package_name)
        print(f"Package: {package_info.name} (v{package_info.latest_version})")
        print(f"Description: {package_info.description}")
        print(f"Author: {package_info.author}")
        print(f"Homepage: {package_info.homepage}")
        print(f"License: {package_info.license}")
        
        # List available versions
        versions = registry.get_package_versions(package_name)
        print(f"Available versions: {', '.join(str(v) for v in versions)}")
        
    except Exception as e:
        print(f"Error getting package information: {e}")
    
    print("\n")
    
    # List installed packages
    print("Listing installed packages...")
    installed_packages = registry.list_installed_packages()
    
    if installed_packages:
        print("Installed packages:")
        for package in installed_packages:
            print(f"- {package.name} (v{package.version})")
    else:
        print("No packages installed.")
        
    print("\nBasic usage example completed.")


if __name__ == "__main__":
    main() 