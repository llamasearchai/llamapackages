# Advanced Usage

This guide covers advanced features and usage scenarios for LlamaPackages. It's intended for users who are already familiar with the basic functionality.

## Table of Contents

- [Environment Management](#environment-management)
- [Package Development Workflows](#package-development-workflows)
- [Private Registries](#private-registries)
- [Dependency Management](#dependency-management)
- [CI/CD Integration](#cicd-integration)
- [Security Features](#security-features)
- [Plugins and Extensions](#plugins-and-extensions)
- [Performance Optimization](#performance-optimization)
- [Scripting and Automation](#scripting-and-automation)
- [Working with Multiple Registries](#working-with-multiple-registries)

## Environment Management

### Virtual Environments

LlamaPackages works with virtual environments to isolate dependencies:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install packages in the environment
llamapackage install llamatext
```

### Isolated Environments

You can create isolated environments for different projects:

```bash
# Create a new isolated environment
llamapackage env create myproject

# Use the environment
llamapackage env use myproject

# Install packages in the environment
llamapackage install llamatext

# List packages in the current environment
llamapackage list

# Switch between environments
llamapackage env use anotherproject
```

### Environment Export/Import

Export and import environments to share them across machines:

```bash
# Export the current environment
llamapackage env export > environment.yaml

# Import an environment
llamapackage env import environment.yaml

# Clone an environment
llamapackage env clone myproject myproject_copy
```

## Package Development Workflows

### Local Development

For local package development with other packages:

```bash
# Install a package in development mode
llamapackage develop /path/to/mypackage

# Run tests for the package
llamapackage test /path/to/mypackage

# Validate the package
llamapackage validate /path/to/mypackage

# Build the package
llamapackage build /path/to/mypackage
```

### Linking Packages

Link packages during development to test them together:

```bash
# Link a local package to the environment
llamapackage link /path/to/packageA

# Use the linked package in another package
cd /path/to/packageB
llamapackage install --editable .
```

### Multi-Package Repositories

For repositories with multiple packages:

```bash
# Install dependencies for all packages
llamapackage install-multi /path/to/repo

# Test all packages
llamapackage test-multi /path/to/repo

# Build all packages
llamapackage build-multi /path/to/repo
```

## Private Registries

### Setting Up a Private Registry

You can set up and use a private registry:

```bash
# Set the registry URL
llamapackage config set registry_url https://private-registry.example.com

# Log in to the private registry
llamapackage login

# Install packages from the private registry
llamapackage install private-package

# Publish to the private registry
llamapackage publish /path/to/mypackage
```

### Registry Authentication

Advanced authentication options:

```bash
# Login with a token
llamapackage login --token YOUR_TOKEN

# Use API key authentication
llamapackage config set api_key YOUR_API_KEY

# Use certificate-based authentication
llamapackage config set cert_file /path/to/cert.pem
```

### Registry Mirroring

Set up registry mirrors for faster downloads or fallbacks:

```bash
# Add a mirror
llamapackage config set mirrors '["https://mirror1.example.com", "https://mirror2.example.com"]'

# Use a specific mirror for this operation
llamapackage install llamatext --mirror https://mirror3.example.com
```

## Dependency Management

### Complex Dependency Resolution

Handle complex dependency requirements:

```bash
# Install with specific dependency resolution strategy
llamapackage install llamatext --resolution=conservative

# Resolve conflicts interactively
llamapackage install llamatext llamamath --interactive

# View the dependency graph
llamapackage deps graph llamatext

# Check for dependency conflicts
llamapackage deps check-conflicts llamatext llamamath
```

### Dependency Pinning

Pin dependencies to exact versions:

```bash
# Pin all dependencies
llamapackage pin

# Export pinned dependencies
llamapackage pin --export > pinned.txt

# Install from pinned dependencies
llamapackage install --from-pin pinned.txt
```

### Dependency Scanning

Scan dependencies for security vulnerabilities:

```bash
# Scan all installed packages
llamapackage scan

# Scan a specific package
llamapackage scan llamatext

# Generate a security report
llamapackage scan --report security_report.html
```

## CI/CD Integration

### GitHub Actions

Example GitHub Actions workflow:

```yaml
name: LlamaPackages CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install LlamaPackages
      run: pip install llamapackages
    - name: Validate package
      run: llamapackage validate .
    - name: Run tests
      run: llamapackage test .
    - name: Build package
      run: llamapackage build .
```

### GitLab CI

Example GitLab CI configuration:

```yaml
stages:
  - validate
  - test
  - build
  - publish

validate:
  stage: validate
  script:
    - pip install llamapackages
    - llamapackage validate .

test:
  stage: test
  script:
    - pip install llamapackages
    - llamapackage test .

build:
  stage: build
  script:
    - pip install llamapackages
    - llamapackage build .
  artifacts:
    paths:
      - dist/

publish:
  stage: publish
  script:
    - pip install llamapackages
    - llamapackage login --token $LLAMAPACKAGE_TOKEN
    - llamapackage publish .
  only:
    - tags
```

### Jenkins

Example Jenkins pipeline:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.10'
        }
    }
    stages {
        stage('Setup') {
            steps {
                sh 'pip install llamapackages'
            }
        }
        stage('Validate') {
            steps {
                sh 'llamapackage validate .'
            }
        }
        stage('Test') {
            steps {
                sh 'llamapackage test .'
            }
        }
        stage('Build') {
            steps {
                sh 'llamapackage build .'
            }
        }
        stage('Publish') {
            when {
                tag "*"
            }
            steps {
                sh 'llamapackage login --token $LLAMAPACKAGE_TOKEN'
                sh 'llamapackage publish .'
            }
        }
    }
}
```

## Security Features

### Signature Verification

Verify package signatures:

```bash
# Enable signature verification
llamapackage config set verify_signatures true

# Import a public key
llamapackage key import /path/to/public_key.pem

# Install with explicit signature verification
llamapackage install llamatext --verify
```

### Signed Publishing

Sign packages when publishing:

```bash
# Generate a signing key
llamapackage key generate

# Publish with signing
llamapackage publish /path/to/mypackage --sign
```

### Access Controls

Manage permissions for packages:

```bash
# Set package visibility
llamapackage publish /path/to/mypackage --visibility=private

# Grant access to specific users
llamapackage access grant mypackage user1 user2

# Grant access to an organization
llamapackage access grant mypackage --org=myorg
```

## Plugins and Extensions

### Using Plugins

LlamaPackages supports plugins for additional functionality:

```bash
# List available plugins
llamapackage plugins list

# Install a plugin
llamapackage plugins install llamapackage-s3

# Use plugin functionality
llamapackage s3 upload mypackage
```

### Creating Plugins

Create your own plugins:

```python
# plugin.py
from llamapackage import plugin

@plugin.register('myplugin')
class MyPlugin:
    def initialize(self, api):
        self.api = api
    
    @plugin.command('greet')
    def greet(self, name):
        """Greet someone"""
        print(f"Hello, {name}!")
```

### Extending Commands

Add custom commands to the CLI:

```python
# custom_command.py
from llamapackage.cli import command

@command('mycmd')
def my_command(args):
    """My custom command"""
    print("Executing custom command")
```

## Performance Optimization

### Parallel Downloads

Enable parallel downloads for faster installation:

```bash
# Set the number of parallel downloads
llamapackage config set parallel_downloads 8

# Install with parallel downloads
llamapackage install llamatext llamamath llamagraph
```

### Caching

Manage the package cache:

```bash
# View cache info
llamapackage cache info

# Clean the cache
llamapackage cache clean

# Only cache frequently used packages
llamapackage cache optimize
```

### Binary Packages

Use pre-built binary packages:

```bash
# Prefer binary packages
llamapackage config set prefer_binary true

# Install binary packages
llamapackage install --binary llamatext
```

## Scripting and Automation

### Scripting with the API

Use the Python API for automation:

```python
from llamapackage import LlamaPackageAPI

# Initialize the API
api = LlamaPackageAPI()

# Login
api.login(username="user", password="pass")

# Install a package
api.install_package("llamatext")

# Search for packages
results = api.search("data processing")
for pkg in results:
    print(f"{pkg.name}: {pkg.description}")

# Check for updates
updates = api.check_for_updates()
for pkg_name, pkg_info in updates.items():
    print(f"{pkg_name}: {pkg_info['current']} -> {pkg_info['latest']}")
```

### Batch Operations

Perform batch operations:

```bash
# Install packages from a file
llamapackage install --from-file requirements.txt

# Update all outdated packages
llamapackage update --all

# Remove all packages matching a pattern
llamapackage uninstall --pattern "llama*"
```

### Hooks

Use hooks to trigger actions:

```bash
# Add a post-install hook
llamapackage hooks add post-install /path/to/script.sh

# Add a pre-update hook
llamapackage hooks add pre-update /path/to/another_script.sh

# Remove a hook
llamapackage hooks remove post-install /path/to/script.sh

# List all hooks
llamapackage hooks list
```

## Working with Multiple Registries

### Registry Configuration

Configure multiple registries:

```bash
# Add a registry
llamapackage registry add myregistry https://registry.example.com

# List all configured registries
llamapackage registry list

# Set the default registry
llamapackage registry default myregistry
```

### Registry Selection

Select registries for specific operations:

```bash
# Install from a specific registry
llamapackage install llamatext --registry myregistry

# Search in a specific registry
llamapackage search text --registry myregistry

# Publish to a specific registry
llamapackage publish /path/to/mypackage --registry myregistry
```

### Registry Scopes

Use registry scopes for package namespaces:

```bash
# Configure a scoped registry
llamapackage registry add myscope https://scoped-registry.example.com --scope @myscope

# Install a scoped package
llamapackage install @myscope/mypackage
```

This automatically uses the correct registry for packages with the @myscope prefix.

## Advanced Configuration

### Custom Configurations

Create and use custom configurations:

```bash
# Create a custom configuration profile
llamapackage config create dev

# Use a specific configuration profile
llamapackage --profile dev install llamatext

# Export a configuration profile
llamapackage config export dev > dev_config.json

# Import a configuration profile
llamapackage config import prod < prod_config.json
```

### System Integration

Integrate with system package managers:

```bash
# Install system dependencies
llamapackage system-deps install llamatext

# Check system compatibility
llamapackage system-deps check llamatext

# Generate system requirements
llamapackage system-deps generate llamatext > system_requirements.txt
```

### Advanced Logging

Configure detailed logging:

```bash
# Enable debug logging
llamapackage --log-level debug install llamatext

# Log to a file
llamapackage --log-file llamapackage.log install llamatext

# Format log output as JSON
llamapackage --log-format json install llamatext
```

## Additional Resources

For more advanced usage examples, see:

- [Example Scripts](https://github.com/llamasearch/llamapackages-examples/scripts)
- [API Documentation](./api_reference.md)
- [Plugin Development Guide](./plugin_development.md)
- [Registry Server Setup](./registry_setup.md) 