# Contributing to LlamaPackages

Thank you for considering contributing to LlamaPackages! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Requests](#pull-requests)
- [Code Reviews](#code-reviews)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)
- [Release Process](#release-process)
- [Community](#community)

## Code of Conduct

Please read and follow our [Code of Conduct](../CODE_OF_CONDUCT.md). We expect all contributors to adhere to this code to ensure a positive and respectful environment for everyone.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip and virtualenv

### Fork and Clone

1. Fork the [LlamaPackages repository](https://github.com/llamasearch/llamapackages) on GitHub.
2. Clone your fork locally:

```bash
git clone https://github.com/yourusername/llamapackages.git
cd llamapackages
```

3. Add the original repository as a remote to keep up with changes:

```bash
git remote add upstream https://github.com/llamasearch/llamapackages.git
```

## Development Setup

### Setting Up a Development Environment

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install the package in development mode with development dependencies:

```bash
pip install -e ".[dev,test,docs]"
```

### Code Style and Linting

We use the following tools for code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

To set up pre-commit hooks that run these tools automatically:

```bash
pre-commit install
```

To run the linters manually:

```bash
# Format your code
black .

# Sort imports
isort .

# Run the linter
flake8

# Run type checking
mypy src
```

## Making Changes

### Branching Strategy

- Create a new branch for each feature or bugfix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

- Keep your branch up to date with the main branch:

```bash
git fetch upstream
git rebase upstream/main
```

### Commits

- Make small, focused commits that address a single concern.
- Use clear and descriptive commit messages.
- Follow the conventional commits format:
  - `feat: add new feature`
  - `fix: resolve issue with X`
  - `docs: update documentation for Y`
  - `test: add tests for Z`
  - `refactor: improve code structure without changing behavior`

## Testing

### Running Tests

We use pytest for testing. To run the tests:

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/unit/
pytest tests/integration/

# Run with coverage report
pytest --cov=llamapackage

# Run integration tests (requires additional setup)
python llamapackage/tests/run_integration_tests.py
```

### Writing Tests

- Write unit tests for all new functionality.
- Ensure your tests are isolated and don't depend on external resources.
- Aim for high code coverage, but prioritize meaningful tests over coverage percentage.
- For complex functionality, add integration tests.

## Documentation

### Updating Documentation

When making changes, be sure to update the relevant documentation:

- Update docstrings for all public functions, classes, and methods.
- Update user-facing documentation in the `docs/` directory if your changes affect user behavior.
- Add examples for new features.

### Building Documentation

To build and preview the documentation locally:

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build the documentation
cd docs
make html

# View the documentation (open _build/html/index.html in your browser)
```

## Pull Requests

### Creating a Pull Request

1. Push your changes to your fork:

```bash
git push origin feature/your-feature-name
```

2. Go to the [LlamaPackages repository](https://github.com/llamasearch/llamapackages) and create a new pull request.

3. Fill out the pull request template with:
   - A clear description of the changes
   - The issue(s) it addresses
   - Any additional context or information

### PR Requirements

For a PR to be accepted, it should:

- Pass all CI checks (tests, linting, type checking)
- Include appropriate tests for new functionality
- Update relevant documentation
- Follow the code style guidelines
- Be focused on a single concern

## Code Reviews

### Review Process

- All PRs require at least one review from a maintainer.
- Address all comments and requested changes.
- If changes are requested, make them in the same branch and push again.

### Reviewing Code

If you're reviewing someone else's code:

- Be respectful and constructive.
- Focus on code quality, correctness, and maintainability.
- Consider performance, security, and edge cases.
- Provide specific suggestions where possible.

## Issue Reporting

### Creating an Issue

If you find a bug or have a suggestion:

1. Check if a similar issue already exists.
2. If not, create a new issue using the appropriate template.
3. Provide as much detail as possible, including:
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots or logs if relevant

### Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working as expected
- `enhancement`: New feature or improvement
- `documentation`: Updates to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed

## Feature Requests

For feature requests:

1. Describe the problem your feature would solve.
2. Explain how your solution would work.
3. Provide examples of how users would use the feature.
4. Consider alternatives and trade-offs.

## Release Process

Our release process follows these steps:

1. We create a release branch from main.
2. We update the version and changelog.
3. We run final tests and checks.
4. We publish the release to PyPI.
5. We create a GitHub release with release notes.

## Community

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and discussions
- **Slack Channel**: For real-time communication (join through our website)
- **Mailing List**: For announcements and broader discussions

### Contributing Beyond Code

There are many ways to contribute beyond writing code:

- Improving documentation
- Testing releases and reporting bugs
- Answering questions in discussions
- Writing tutorials or blog posts
- Giving talks about the project

## Recognition

All contributors are recognized in our [CONTRIBUTORS.md](../CONTRIBUTORS.md) file. We're grateful for all contributions, whether they're code, documentation, issues, or community support.

## License

By contributing to LlamaPackages, you agree that your contributions will be licensed under the project's [MIT License](../LICENSE). 