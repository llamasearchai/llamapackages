# API Reference

LlamaPackages provides a Python API for programmatic access to the package registry and management functionality. This document outlines the available classes and methods.

## Table of Contents

- [Main API](#main-api)
- [Authentication](#authentication)
- [Package Registry](#package-registry)
- [Package Management](#package-management)
- [Dependency Resolution](#dependency-resolution)
- [Configuration](#configuration)
- [Exceptions](#exceptions)

## Main API

The main entry point to the API is the `LlamaPackageAPI` class:

```python
from llamapackage import LlamaPackageAPI

# Create API instance
api = LlamaPackageAPI()

# Login
api.login(username="your_username", password="your_password")

# Search for packages
results = api.search("text processing")
```

### `LlamaPackageAPI`

The main API class that provides access to all functionality.

#### Constructor

```python
LlamaPackageAPI(config=None)
```

Parameters:
- `config` (optional): A `Config` instance. If not provided, a default config will be created.

#### Methods

##### Authentication

```python
login(username=None, password=None, token=None)
```
Authenticate with the registry.

Parameters:
- `username` (optional): Username for authentication.
- `password` (optional): Password for authentication.
- `token` (optional): Use existing token instead of username/password.

Returns:
- `bool`: True if login was successful.

```python
logout()
```
Log out from the registry.

Returns:
- `bool`: True if logout was successful.

```python
is_authenticated()
```
Check if the user is authenticated.

Returns:
- `bool`: True if authenticated.

##### Package Discovery

```python
search(query)
```
Search for packages.

Parameters:
- `query`: Search query string.

Returns:
- `list`: List of `Package` objects.

```python
get_package(name)
```
Get information about a package.

Parameters:
- `name`: Package name.

Returns:
- `Package`: Package object.

```python
get_package_versions(name)
```
Get versions of a package.

Parameters:
- `name`: Package name.

Returns:
- `list`: List of `PackageVersion` objects.

##### Package Management

```python
install_package(name, version=None)
```
Install a package.

Parameters:
- `name`: Package name.
- `version` (optional): Specific version to install. If not provided, the latest version will be installed.

Returns:
- `bool`: True if installation was successful.

```python
uninstall_package(name)
```
Uninstall a package.

Parameters:
- `name`: Package name.

Returns:
- `bool`: True if uninstallation was successful.

```python
list_installed_packages()
```
List installed packages.

Returns:
- `list`: List of `Package` objects.

```python
is_package_installed(name)
```
Check if a package is installed.

Parameters:
- `name`: Package name.

Returns:
- `bool`: True if the package is installed.

```python
check_for_updates()
```
Check for updates to installed packages.

Returns:
- `dict`: Dictionary mapping package names to update information.

```python
update_package(name=None)
```
Update a package or all packages.

Parameters:
- `name` (optional): Package name. If not provided, all packages will be updated.

Returns:
- `dict`: Dictionary mapping package names to update results.

##### Publishing

```python
publish_package(path)
```
Publish a package.

Parameters:
- `path`: Path to the package directory.

Returns:
- `Package`: The published package.

```python
validate_package(path)
```
Validate a package without publishing.

Parameters:
- `path`: Path to the package directory.

Returns:
- `dict`: Validation results.

##### Configuration

```python
get_config(key)
```
Get a configuration value.

Parameters:
- `key`: Configuration key.

Returns:
- Configuration value.

```python
set_config(key, value)
```
Set a configuration value.

Parameters:
- `key`: Configuration key.
- `value`: Configuration value.

```python
save_config()
```
Save the configuration.

## Authentication

The `Authentication` class handles authentication with the package registry.

```python
from llamapackage import Authentication, Config

config = Config()
auth = Authentication(config)
auth.login(username="your_username", password="your_password")
```

### `Authentication`

#### Constructor

```python
Authentication(config)
```

Parameters:
- `config`: A `Config` instance.

#### Methods

```python
login(username=None, password=None, token=None)
```
Authenticate with the registry.

Parameters:
- `username` (optional): Username for authentication.
- `password` (optional): Password for authentication.
- `token` (optional): Use existing token instead of username/password.

Returns:
- `bool`: True if login was successful.

```python
logout()
```
Log out from the registry.

Returns:
- `bool`: True if logout was successful.

```python
is_authenticated()
```
Check if the user is authenticated.

Returns:
- `bool`: True if authenticated.

```python
validate_token()
```
Validate the current authentication token.

Returns:
- `bool`: True if the token is valid.

## Package Registry

The `PackageRegistry` class provides access to the package registry.

```python
from llamapackage import PackageRegistry, Config

config = Config()
registry = PackageRegistry(config)
results = registry.search("text processing")
```

### `PackageRegistry`

#### Constructor

```python
PackageRegistry(config)
```

Parameters:
- `config`: A `Config` instance.

#### Methods

```python
search(query)
```
Search for packages.

Parameters:
- `query`: Search query string.

Returns:
- `list`: List of `Package` objects.

```python
get_package(name)
```
Get information about a package.

Parameters:
- `name`: Package name.

Returns:
- `Package`: Package object.

```python
get_package_versions(name)
```
Get versions of a package.

Parameters:
- `name`: Package name.

Returns:
- `list`: List of `PackageVersion` objects.

```python
install_package(name, version=None)
```
Install a package.

Parameters:
- `name`: Package name.
- `version` (optional): Specific version to install. If not provided, the latest version will be installed.

Returns:
- `bool`: True if installation was successful.

```python
uninstall_package(name)
```
Uninstall a package.

Parameters:
- `name`: Package name.

Returns:
- `bool`: True if uninstallation was successful.

```python
list_installed_packages()
```
List installed packages.

Returns:
- `list`: List of `Package` objects.

```python
is_package_installed(name)
```
Check if a package is installed.

Parameters:
- `name`: Package name.

Returns:
- `bool`: True if the package is installed.

```python
publish_package(path)
```
Publish a package.

Parameters:
- `path`: Path to the package directory.

Returns:
- `Package`: The published package.

```python
check_for_updates()
```
Check for updates to installed packages.

Returns:
- `dict`: Dictionary mapping package names to update information.

## Package Management

### `Package`

Represents a package in the registry.

#### Constructor

```python
Package(name, description=None, author=None, homepage=None, license=None, latest_version=None, version=None)
```

Parameters:
- `name`: Package name.
- `description` (optional): Package description.
- `author` (optional): Package author.
- `homepage` (optional): Package homepage.
- `license` (optional): Package license.
- `latest_version` (optional): Latest version of the package.
- `version` (optional): Current version of the package.

#### Properties

- `name`: Package name.
- `description`: Package description.
- `author`: Package author.
- `homepage`: Package homepage.
- `license`: Package license.
- `latest_version`: Latest version of the package.
- `version`: Current version of the package.

#### Methods

```python
from_dict(data)
```
Create a package from a dictionary.

Parameters:
- `data`: Dictionary containing package data.

Returns:
- `Package`: A new Package instance.

```python
to_dict()
```
Convert the package to a dictionary.

Returns:
- `dict`: Dictionary representation of the package.

### `PackageVersion`

Represents a specific version of a package.

#### Constructor

```python
PackageVersion(version, package_name, release_date=None, description=None, download_url=None)
```

Parameters:
- `version`: Version string.
- `package_name`: Name of the package.
- `release_date` (optional): Release date of the version.
- `description` (optional): Description of the version.
- `download_url` (optional): URL to download the version.

#### Properties

- `version`: Version string.
- `package_name`: Name of the package.
- `release_date`: Release date of the version.
- `description`: Description of the version.
- `download_url`: URL to download the version.

#### Methods

```python
from_dict(data)
```
Create a package version from a dictionary.

Parameters:
- `data`: Dictionary containing version data.

Returns:
- `PackageVersion`: A new PackageVersion instance.

```python
to_dict()
```
Convert the package version to a dictionary.

Returns:
- `dict`: Dictionary representation of the package version.

## Dependency Resolution

### `DependencyResolver`

Handles dependency resolution for packages.

#### Constructor

```python
DependencyResolver(config)
```

Parameters:
- `config`: A `Config` instance.

#### Methods

```python
resolve_dependencies(package_name, version=None)
```
Resolve dependencies for a package.

Parameters:
- `package_name`: Name of the package.
- `version` (optional): Specific version to resolve dependencies for.

Returns:
- `list`: List of `Package` objects representing dependencies.

```python
check_conflicts(dependencies1, dependencies2)
```
Check for conflicts between two sets of dependencies.

Parameters:
- `dependencies1`: First set of dependencies.
- `dependencies2`: Second set of dependencies.

Returns:
- `list`: List of conflicts.

## Configuration

### `Config`

Manages configuration.

#### Constructor

```python
Config(config_dir=None)
```

Parameters:
- `config_dir` (optional): Path to the configuration directory.

#### Properties

- `config_dir`: Path to the configuration directory.
- `registry_url`: URL of the package registry.
- `auth_token`: Authentication token.

#### Methods

```python
get(key, default=None)
```
Get a configuration value.

Parameters:
- `key`: Configuration key.
- `default` (optional): Default value if the key doesn't exist.

Returns:
- Configuration value.

```python
set(key, value)
```
Set a configuration value.

Parameters:
- `key`: Configuration key.
- `value`: Configuration value.

```python
save()
```
Save the configuration.

```python
load()
```
Load the configuration.

## Exceptions

LlamaPackages defines several exception classes:

### `LlamaPackageError`

Base class for all LlamaPackages exceptions.

### `AuthenticationError`

Raised when authentication fails.

### `PackageNotFoundError`

Raised when a package is not found.

### `VersionNotFoundError`

Raised when a specific version of a package is not found.

### `DependencyError`

Raised when there's an issue with dependencies.

### `ConfigError`

Raised when there's an issue with configuration.

### `NetworkError`

Raised when there's a network issue.

## Usage Examples

### Search and Install Packages

```python
from llamapackage import LlamaPackageAPI

# Create API instance
api = LlamaPackageAPI()

# Login
api.login(username="your_username", password="your_password")

# Search for packages
results = api.search("text processing")

# Print results
for package in results:
    print(f"{package.name} - {package.description}")

# Install a package
api.install_package("llamatext")

# List installed packages
installed = api.list_installed_packages()
for package in installed:
    print(f"{package.name} {package.version}")
```

### Publishing a Package

```python
from llamapackage import LlamaPackageAPI

# Create API instance
api = LlamaPackageAPI()

# Login
api.login(username="your_username", password="your_password")

# Validate the package
validation = api.validate_package("./mypackage")
if validation["valid"]:
    # Publish the package
    package = api.publish_package("./mypackage")
    print(f"Published {package.name} {package.version}")
else:
    print("Validation failed:")
    for error in validation["errors"]:
        print(f"- {error}")
```

### Managing Configuration

```python
from llamapackage import LlamaPackageAPI

# Create API instance
api = LlamaPackageAPI()

# Get configuration
registry_url = api.get_config("registry_url")
print(f"Current registry URL: {registry_url}")

# Set configuration
api.set_config("registry_url", "https://custom-registry.example.com")
api.save_config()
```

For more examples, see the [Examples](../examples) directory. 