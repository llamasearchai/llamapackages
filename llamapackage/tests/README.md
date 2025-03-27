# LlamaPackages Tests

This directory contains tests for the LlamaPackages Python package. The tests are organized into unit tests and integration tests.

## Test Structure

- `unit/`: Unit tests for individual components
- `integration/`: Integration tests that test multiple components together
- `conftest.py`: Shared fixtures and configuration for tests
- `run_integration_tests.py`: Script to run integration tests with proper setup

## Running Tests

### Unit Tests

Run all unit tests:

```bash
pytest -m unit
```

Run a specific unit test file:

```bash
pytest llamapackage/tests/unit/test_registry.py
```

### Integration Tests

Integration tests require more setup and are disabled by default. There are two ways to run them:

1. Using the provided script (recommended):

```bash
python llamapackage/tests/run_integration_tests.py
```

This script sets up the environment, starts a mock registry server, and runs the tests.

Options:
- `--registry URL`: URL of an existing registry to use (default: uses mock registry)
- `--debug`: Enable debug output
- `--no-mock`: Don't start a mock registry (you must provide a registry URL)
- `--test-path PATH`: Path to a specific test file or directory
- `--verbose`, `-v`: Enable verbose output

2. Manually setting the environment variable:

```bash
export LLAMA_RUN_INTEGRATION_TESTS=1
pytest -m integration
```

## Adding New Tests

When adding new tests:

1. Unit tests should be placed in the `unit/` directory and marked with `@pytest.mark.unit`
2. Integration tests should be placed in the `integration/` directory and marked with `@pytest.mark.integration`
3. Tests requiring authentication should be marked with `@pytest.mark.requires_auth`
4. Tests requiring internet connection should be marked with `@pytest.mark.requires_internet`
5. Slow-running tests should be marked with `@pytest.mark.slow`

## Mock Registry

The integration tests use a mock registry server that mimics the behavior of the LlamaPackages registry. The server is started automatically by the `run_integration_tests.py` script.

The mock registry provides endpoints for:
- Authentication (login, validate token)
- Package operations (search, get, install, uninstall, publish)

The mock registry contains sample packages for testing, including:
- `llamatext`: A text processing package
- `llamamath`: A mathematics package
- `test-package`: A test package
- `package-a` and `package-b`: Packages with conflicting dependencies

## Test Fixtures

Common test fixtures are defined in `conftest.py` and include:

- `temp_config_dir`: Creates a temporary configuration directory for tests
- `mock_registry_response`: Sample response data for mocking registry API calls
- `mock_package_data`: Sample package data for testing

## Best Practices

1. Keep tests isolated and independent
2. Mock external dependencies when possible
3. Use fixtures for shared setup
4. Clean up any resources created during tests
5. Keep tests deterministic and repeatable
6. Write assertions that provide clear error messages

## Debugging Tests

To see more detailed output when tests fail:

```bash
pytest -v --tb=long llamapackage/tests/unit/test_auth.py
```

To drop into a debugger on test failure:

```bash
pytest --pdb llamapackage/tests/unit/test_auth.py
``` 