# LlamaPackages

LlamaPackages is a package management system for the LlamaSearch.ai ecosystem. It allows you to discover, install, and publish packages with ease.

## Features

- 📦 **Simple Package Management**: Install, update, and remove packages with a simple CLI
- 🔍 **Package Discovery**: Search for packages by name, keyword, or functionality
- 🚀 **Easy Publishing**: Publish your own packages to share with the community
- 🔄 **Dependency Management**: Automatically handle dependencies between packages
- 🌐 **Web Interface**: Browse and manage packages through a user-friendly web interface
- 🔒 **Secure**: Package validation and verification to ensure security

## Installation

Install LlamaPackages using pip:

```bash
pip install llamapackages
```

For development purposes or to include the web interface:

```bash
# Install with development dependencies
pip install llamapackages[dev]

# Install with web interface dependencies
pip install llamapackages[web]

# Install all dependencies
pip install llamapackages[all]
```

## Quick Start

```bash
# Log in to your account
llamapackage login

# Search for packages
llamapackage search text-processing

# Install a package
llamapackage install llamatext

# List installed packages
llamapackage list

# Update packages
llamapackage update

# Publish your own package
llamapackage publish /path/to/your/package
```

## Documentation

For detailed documentation, see the [docs](./docs/) directory:

- [Getting Started Guide](./docs/getting_started.md) - Quick introduction to LlamaPackages
- [CLI Usage](./docs/cli_usage.md) - Command line interface reference
- [API Reference](./docs/api_reference.md) - Programmatic usage
- [Web Interface](./docs/web_interface.md) - Using the web interface
- [Package Development Guide](./docs/package_development.md) - Creating your own packages
- [Advanced Usage](./docs/advanced_usage.md) - Advanced features and scenarios
- [Contributing Guide](./docs/contributing.md) - How to contribute to LlamaPackages

## Examples

Check out the [examples](./examples/) directory for sample code showing how to use LlamaPackages in different scenarios:

- [Basic Usage](./examples/basic/) - Simple examples for getting started
- [Advanced Usage](./examples/advanced/) - More complex scenarios
- [Integration Examples](./examples/integration/) - Integrating with other systems
- [Publishing Packages](./examples/publishing/) - How to publish your own packages

## Testing

LlamaPackages includes a comprehensive test suite:

```bash
# Install development dependencies
pip install -e ".[dev,test]"

# Run unit tests
pytest llamapackage/tests/unit/

# Run integration tests
python llamapackage/tests/run_integration_tests.py
```

## License

LlamaPackages is licensed under the [MIT License](./LICENSE).

## Community

- GitHub Issues: For bug reports and feature requests
- GitHub Discussions: For questions and general discussions
- Slack Channel: For real-time communication
- Mailing List: For announcements and broader discussions

## Contributing

Contributions are welcome! See the [Contributing Guide](./docs/contributing.md) for details.
