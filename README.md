# 🦙 LlamaPackages

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-orange)](https://llamasearch.ai

A comprehensive package management and distribution system for the LlamaSearch.ai ecosystem. LlamaPackages provides a unified way to discover, install, and manage packages across all Llama-related projects.

## 📋 Overview

LlamaPackages serves as the central package management system for the LlamaSearch.ai ecosystem. It enables developers to easily publish their packages to the repository, and users to discover and install these packages with minimal effort.

### Key Features

- **Unified Package Registry**: Central repository for all Llama-related packages
- **Dependency Management**: Automatic resolution of package dependencies
- **Version Control**: Track and manage package versions
- **Package Discovery**: Search and browse available packages
- **Integration with Common Tools**: Seamless integration with pip, conda, and other package managers
- **Authentication & Authorization**: Secure access control for package publishing
- **Package Verification**: Automated testing and verification of packages
- **Usage Analytics**: Tracking of package downloads and usage statistics

## 🚀 Quick Start

### Installation

```bash
# Install the LlamaPackages client
pip install llamapackage

# Set up the client
llamapackage setup
```

### Usage

```bash
# Search for packages
llamapackage search "summarize"

# Install a package
llamapackage install llamasummarize

# List installed packages
llamapackage list

# Update a package
llamapackage update llamasummarize

# Publish a package (requires authentication)
llamapackage publish ./my-package
```

## 📦 Package Structure

LlamaPackages follows a standardized structure for all packages:

```
package_name/
├── src/                  # Source code
│   └── package_name/     # Main package code
├── tests/                # Test files
├── docs/                 # Documentation
├── examples/             # Usage examples
├── scripts/              # Utility scripts
├── pyproject.toml        # Modern Python project configuration
├── setup.py              # Traditional setup (for backward compatibility)
├── requirements.txt      # Dependencies
└── README.md             # Package documentation
```

## 🧪 Testing

We use pytest for testing:

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=llamapackage
```

## 📖 Documentation

Comprehensive documentation is available at [https://llamasearch.ai

### API Reference

- `llamapackage.registry`: Package registry management
- `llamapackage.dependency`: Dependency resolution
- `llamapackage.auth`: Authentication and authorization
- `llamapackage.cli`: Command-line interface tools
- `llamapackage.storage`: Package storage utilities

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://llamasearch.ai
cd llamapackages

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running the Registry Server

```bash
# Start the registry server
llamapackage server start
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to submit contributions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
# Updated in commit 1 - 2025-04-04 17:44:39

# Updated in commit 9 - 2025-04-04 17:44:39

# Updated in commit 17 - 2025-04-04 17:44:40

# Updated in commit 25 - 2025-04-04 17:44:40

# Updated in commit 1 - 2025-04-05 14:44:01

# Updated in commit 9 - 2025-04-05 14:44:01

# Updated in commit 17 - 2025-04-05 14:44:02

# Updated in commit 25 - 2025-04-05 14:44:02

# Updated in commit 1 - 2025-04-05 15:30:13

# Updated in commit 9 - 2025-04-05 15:30:13

# Updated in commit 17 - 2025-04-05 15:30:13

# Updated in commit 25 - 2025-04-05 15:30:14
