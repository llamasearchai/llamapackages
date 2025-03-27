# Package Development Guide

This guide will walk you through the process of creating and publishing packages for LlamaPackages.

## Table of Contents

- [Package Structure](#package-structure)
- [Project Configuration](#project-configuration)
- [Metadata](#metadata)
- [Dependencies](#dependencies)
- [Creating Your First Package](#creating-your-first-package)
- [Testing](#testing)
- [Documentation](#documentation)
- [Publishing](#publishing)
- [Versioning](#versioning)
- [Best Practices](#best-practices)
- [Advanced Features](#advanced-features)

## Package Structure

A typical LlamaPackage has the following structure:

```
mypackage/
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
└── tests/
    ├── __init__.py
    ├── test_main.py
    └── test_utils.py
```

### Key Components

- `LICENSE`: Contains the package's license.
- `README.md`: Documentation for your package.
- `pyproject.toml`: Package configuration file.
- `src/`: Source code directory.
- `tests/`: Test files.

## Project Configuration

LlamaPackages uses the standard Python packaging format with `pyproject.toml`.

### Basic Configuration

Here's a minimal `pyproject.toml` file:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
description = "My awesome package"
readme = "README.md"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
license = {text = "MIT"}
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    "requests>=2.25.0",
]
requires-python = ">=3.8"
```

### Additional Fields

You can add additional fields to provide more information:

```toml
[project]
# ... (basic fields)
keywords = ["example", "llamapackage"]
urls = {Homepage = "https://github.com/yourusername/mypackage"}

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
]
doc = [
    "sphinx>=4.0.0",
]

[project.scripts]
mypackage-cli = "mypackage.cli:main"
```

## Metadata

LlamaPackages uses standard Python packaging metadata, plus some additional fields for enhanced functionality.

### Required Metadata

- `name`: The name of your package (must be unique).
- `version`: The version of your package.
- `description`: A short description.
- `authors`: At least one author with name and email.
- `license`: The license for your package.

### Optional Metadata

- `keywords`: List of keywords for search.
- `urls`: URLs for project homepage, documentation, etc.
- `classifiers`: Standard Python classifiers.

### LlamaPackages-specific Metadata

You can add LlamaPackages-specific metadata under the `[tool.llamapackage]` section:

```toml
[tool.llamapackage]
category = "ai"
tags = ["machine-learning", "nlp"]
compatibility = ["llamatext>=1.0.0"]
```

## Dependencies

LlamaPackages uses standard Python dependency specification.

### Basic Dependencies

```toml
[project]
dependencies = [
    "requests>=2.25.0",
    "numpy~=1.20",
    "pandas==1.3.0",
]
```

### Optional Dependencies

Optional dependencies are grouped by feature:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
]
full = [
    "scikit-learn>=1.0.0",
    "matplotlib>=3.4.0",
]
```

### LlamaPackages Dependencies

To specify dependencies on other LlamaPackages, use the normal Python dependency syntax:

```toml
[project]
dependencies = [
    "llamatext>=1.0.0",
    "llamamath~=0.5.0",
]
```

## Creating Your First Package

### Step 1: Initialize the Package

You can use the LlamaPackages CLI to create a new package:

```bash
llamapackage new mypackage
```

This will create a basic package structure with the necessary files.

### Step 2: Implement Your Code

Edit the Python files in the `src/mypackage/` directory to implement your package functionality.

Here's a simple example:

```python
# src/mypackage/__init__.py
from .main import MyClass

__version__ = "0.1.0"
```

```python
# src/mypackage/main.py
class MyClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"
```

### Step 3: Write Tests

Add tests to ensure your package works correctly:

```python
# tests/test_main.py
from mypackage import MyClass

def test_greet():
    obj = MyClass("World")
    assert obj.greet() == "Hello, World!"
```

### Step 4: Update Documentation

Edit the README.md file to provide documentation for your package:

```markdown
# MyPackage

A simple example package for LlamaPackages.

## Installation

```bash
llamapackage install mypackage
```

## Usage

```python
from mypackage import MyClass

obj = MyClass("World")
print(obj.greet())  # Output: Hello, World!
```
```

### Step 5: Configure Package Metadata

Edit the `pyproject.toml` file to set your package metadata:

```toml
[project]
name = "mypackage"
version = "0.1.0"
description = "A simple example package"
readme = "README.md"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
license = {text = "MIT"}
```

## Testing

### Running Tests

LlamaPackages recommends using pytest for testing:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Test Coverage

To check test coverage:

```bash
pytest --cov=mypackage
```

### CI Integration

Consider setting up continuous integration to run tests automatically. LlamaPackages works with GitHub Actions, Travis CI, and other CI systems.

## Documentation

### README

Your README.md should include:

1. Package name and description
2. Installation instructions
3. Basic usage examples
4. Features
5. License information

### API Documentation

For larger packages, consider creating API documentation using Sphinx or MkDocs.

### Example Code

Include example code in your documentation to show how to use your package.

## Publishing

### Preparing for Publication

Before publishing, validate your package:

```bash
llamapackage validate /path/to/mypackage
```

This will check for common issues like missing metadata, malformed files, etc.

### Publishing Process

To publish your package to the LlamaPackages registry:

```bash
# Log in to your account
llamapackage login

# Publish the package
llamapackage publish /path/to/mypackage
```

### Publication Checks

The publication process includes several checks:

1. Metadata validation
2. License check
3. Code safety analysis
4. Dependency resolution
5. Package building

## Versioning

LlamaPackages follows semantic versioning (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for added functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

Example versions: `1.0.0`, `1.2.3`, `2.0.0-beta.1`

### Updating Versions

When updating your package, update the version in `pyproject.toml`:

```toml
[project]
version = "1.1.0"  # Increment appropriately
```

## Best Practices

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints for better code readability
- Document your functions and classes with docstrings

### Package Design

- Keep the public API simple and intuitive
- Use meaningful names for modules, classes, and functions
- Separate concerns into different modules

### Dependencies

- Minimize dependencies to reduce installation issues
- Specify version ranges to avoid compatibility problems
- Consider making heavy dependencies optional

### Testing

- Write tests for all public functions and classes
- Include integration tests for critical functionality
- Test with different Python versions

### Documentation

- Keep documentation up to date
- Provide examples for common use cases
- Include troubleshooting information

## Advanced Features

### Entry Points

To create command-line tools, use entry points:

```toml
[project.scripts]
mypackage-cli = "mypackage.cli:main"
```

### Plugins

LlamaPackages supports a plugin system. To create a plugin for another package:

```toml
[project.entry_points."llamatext.plugins"]
myplugin = "mypackage.plugin:LlamaTextPlugin"
```

### Data Files

To include data files with your package:

```toml
[tool.setuptools]
package-data = {"mypackage" = ["data/*.json", "templates/*.html"]}
```

### Extension Modules

If your package includes C extensions, use `build_ext`:

```toml
[build-system]
requires = ["setuptools>=42", "wheel", "Cython>=0.29.0"]
build-backend = "setuptools.build_meta"
```

### Development Mode

During development, install your package in editable mode:

```bash
pip install -e /path/to/mypackage
```

## Example Projects

For complete examples, see the [example packages](https://github.com/llamasearch/llamapackages-examples) repository.

These examples show how to create different types of packages, including:

- Basic library packages
- Command-line tools
- Web applications
- Machine learning models
- Data visualization packages

## Additional Resources

- [Python Packaging Guide](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
- [Semantic Versioning](https://semver.org/)
- [Choose a License](https://choosealicense.com/) 