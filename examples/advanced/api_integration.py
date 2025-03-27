#!/usr/bin/env python3
"""
API Integration Example

This example demonstrates how to use the LlamaPackages API programmatically
for advanced use cases such as integrating with CI/CD pipelines or custom tooling.
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to sys.path to make the llamapackage module importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from llamapackage import PackageRegistry, Config, Authentication, DependencyResolver, Storage

class LlamaPackagesAPI:
    """Class for working with LlamaPackages programmatically."""
    
    def __init__(self, registry_url=None, auth_token=None):
        """Initialize the API client."""
        self.config = Config()
        self.config.registry_url = registry_url or "https://registry.llamasearch.ai"
        self.config.auth_token = auth_token or os.environ.get("LLAMA_AUTH_TOKEN", "")
        
        # Initialize components
        self.auth = Authentication(self.config)
        self.registry = PackageRegistry(self.config)
        self.resolver = DependencyResolver(self.config)
        self.storage = Storage(self.config)
        
        # Authenticate if token is provided
        if self.config.auth_token and not self.auth.is_authenticated():
            self.auth.login()
    
    def search_packages(self, query, limit=10):
        """Search for packages based on a query string."""
        results = self.registry.search(query)
        return results[:limit] if limit else results
    
    def get_package_info(self, package_name):
        """Get detailed information about a package."""
        package = self.registry.get_package(package_name)
        versions = self.registry.get_package_versions(package_name)
        
        # Add versions to the package info
        package_info = package.dict()
        package_info['versions'] = [str(v) for v in versions]
        
        return package_info
    
    def install_package(self, package_name, version=None, install_deps=True):
        """Install a package and optionally its dependencies."""
        # Resolve dependencies if needed
        if install_deps:
            dependencies = self.resolver.resolve_dependencies(package_name, version)
            # Install dependencies first
            for dep in dependencies:
                if dep.name != package_name:  # Skip the main package
                    self.registry.install_package(dep.name, dep.version)
        
        # Install the main package
        self.registry.install_package(package_name, version)
        return True
    
    def publish_package(self, package_path):
        """Publish a package to the registry."""
        result = self.registry.publish_package(package_path)
        return result
    
    def export_packages_manifest(self, output_path):
        """Export a manifest of installed packages."""
        installed = self.registry.list_installed_packages()
        manifest = {
            "packages": [
                {
                    "name": pkg.name,
                    "version": str(pkg.version),
                    "install_time": pkg.install_time.isoformat() if pkg.install_time else None
                }
                for pkg in installed
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return manifest
    
    def import_packages_from_manifest(self, manifest_path):
        """Install packages from a manifest file."""
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        results = []
        for pkg in manifest.get("packages", []):
            try:
                self.install_package(pkg["name"], pkg.get("version"))
                results.append({"name": pkg["name"], "success": True})
            except Exception as e:
                results.append({"name": pkg["name"], "success": False, "error": str(e)})
        
        return results

def main():
    """Demonstrate advanced API usage."""
    print("LlamaPackages API Integration Example")
    print("====================================\n")
    
    # Initialize API client
    api = LlamaPackagesAPI()
    print(f"Using registry: {api.config.registry_url}\n")
    
    # Example 1: Search for packages
    query = "data"
    print(f"Searching for packages matching '{query}'...")
    packages = api.search_packages(query, limit=5)
    print(f"Found {len(packages)} packages:")
    for pkg in packages:
        print(f"- {pkg.name} (v{pkg.latest_version}): {pkg.description}")
    print()
    
    # Example 2: Get detailed package info
    package_name = packages[0].name if packages else "llamatext"
    print(f"Getting detailed info for '{package_name}'...")
    try:
        info = api.get_package_info(package_name)
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    # Example 3: Export manifest
    manifest_path = "installed_packages.json"
    print(f"Exporting package manifest to {manifest_path}...")
    try:
        manifest = api.export_packages_manifest(manifest_path)
        print(f"Exported {len(manifest['packages'])} packages to manifest file")
    except Exception as e:
        print(f"Error exporting manifest: {e}")
    
    print("\nAPI Integration example completed.")

if __name__ == "__main__":
    main() 