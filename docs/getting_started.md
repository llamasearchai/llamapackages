# Getting Started with LlamaPackages

This guide will walk you through the basics of using LlamaPackages, from installation to searching, installing, and publishing packages.

## Installation

Install LlamaPackages using pip:

```bash
pip install llamapackages
```

## Authentication

Before you can install or publish packages, you need to authenticate:

```bash
llamapackage login
```

You'll be prompted to enter your LlamaSearch.ai username and password.

## Finding Packages

### Searching for Packages

To search for packages, use the `search` command:

```bash
llamapackage search text-processing
```

This will list all packages related to text processing.

### Listing Package Details

To get more information about a specific package:

```bash
llamapackage info llamatext
```

This will show details like description, author, version history, dependencies, etc.

## Installing Packages

### Installing the Latest Version

To install the latest version of a package:

```bash
llamapackage install llamatext
```

### Installing a Specific Version

To install a specific version:

```bash
llamapackage install llamatext==1.0.0
```

### Listing Installed Packages

To see what packages you have installed:

```bash
llamapackage list
```

## Using Packages

Once installed, you can import and use packages in your Python code:

```python
# Import the package
from llamatext import TextProcessor

# Use the package
processor = TextProcessor()
result = processor.process("Hello, world!")
print(result)
```

## Publishing Your Own Package

### Package Structure

A basic LlamaPackage has the following structure:

```
mypackage/
├── pyproject.toml
├── README.md
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_main.py
```

### Creating a Package Configuration

Your `pyproject.toml` should look something like this:

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

### Publishing Your Package

Once your package is ready, publish it with:

```bash
llamapackage publish /path/to/mypackage
```

## Updating Packages

### Checking for Updates

To check for updates to installed packages:

```bash
llamapackage check-updates
```

### Updating Packages

To update all packages:

```bash
llamapackage update
```

To update a specific package:

```bash
llamapackage update llamatext
```

## Next Steps

Now that you understand the basics, you might want to:

- Explore the [CLI Documentation](./cli_usage.md) for all available commands
- Check out the [API Reference](./api_reference.md) for programmatic usage
- See the [Package Development Guide](./package_development.md) for creating more complex packages
- Look at the [Examples](../examples) for sample code

For any issues or questions, please refer to our [GitHub repository](https://github.com/llamasearch/llamapackages) or the [Contributing Guide](./contributing.md). 