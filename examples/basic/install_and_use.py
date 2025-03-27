#!/usr/bin/env python3
"""
Package Installation and Usage Example

This example demonstrates how to install a package and use it in your code.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to make the llamapackage module importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from llamapackage import PackageRegistry, Config, DependencyResolver

def main():
    """Demonstrate package installation and usage."""
    print("LlamaPackages Installation and Usage Example")
    print("===========================================\n")

    # Initialize the configuration
    config = Config()
    config.registry_url = "https://registry.llamasearch.ai"
    config.auth_token = os.environ.get("LLAMA_AUTH_TOKEN", "")
    
    # Initialize the package registry and dependency resolver
    registry = PackageRegistry(config)
    resolver = DependencyResolver(config)
    
    # Package to install
    package_name = "llamatext"
    package_version = "1.0.0"  # Specify a version or omit for latest
    
    print(f"Installing {package_name} (v{package_version})...")
    
    try:
        # Resolve dependencies
        dependencies = resolver.resolve_dependencies(package_name, package_version)
        print(f"Resolved dependencies: {', '.join(f'{d.name}@{d.version}' for d in dependencies)}")
        
        # Install the package and its dependencies
        registry.install_package(package_name, package_version)
        
        print(f"\nSuccessfully installed {package_name} (v{package_version})")
        
        # Now use the installed package (in a real scenario, you would import it)
        print("\nSimulating usage of the installed package:")
        print("-------------------------------------------")
        
        # In a real scenario, you would do:
        # from llamatext import TextProcessor
        # processor = TextProcessor()
        # result = processor.process("Sample text")
        
        # For this example, we'll just simulate the usage
        simulate_package_usage(package_name)
        
    except Exception as e:
        print(f"Error installing or using package: {e}")
    
    print("\nInstallation and usage example completed.")

def simulate_package_usage(package_name):
    """Simulate using an installed package."""
    if package_name == "llamatext":
        print("from llamatext import TextProcessor")
        print("processor = TextProcessor()")
        print("result = processor.process('Hello, LlamaPackages!')")
        print("print(result)")
        print("\nOutput: {'sentiment': 'positive', 'tokens': ['Hello', ',', 'LlamaPackages', '!']}")
    else:
        print(f"Import and use {package_name} here")

if __name__ == "__main__":
    main() 