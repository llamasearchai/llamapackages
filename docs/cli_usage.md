# Command Line Interface (CLI) Usage

LlamaPackages provides a powerful command-line interface (CLI) for managing packages. This document outlines all available commands and their options.

## Global Options

The following options are available for all commands:

| Option | Description |
|--------|-------------|
| `--debug` | Enable debug output |
| `--config-dir PATH` | Specify a custom configuration directory |
| `--help`, `-h` | Show help message |
| `--version` | Show version information |

## Available Commands

### Authentication Commands

#### `login`

Authenticate with the LlamaPackages registry.

```bash
llamapackage login
```

You'll be prompted to enter your username and password.

Options:
- `--token TOKEN` - Use an existing auth token instead of username/password

#### `logout`

Log out from the LlamaPackages registry.

```bash
llamapackage login
```

### Package Discovery Commands

#### `search`

Search for packages in the registry.

```bash
llamapackage search QUERY
```

Options:
- `--limit N` - Limit the number of results (default: 10)
- `--json` - Output results in JSON format

Example:
```bash
llamapackage search text-processing
```

#### `info`

Show detailed information about a package.

```bash
llamapackage info PACKAGE_NAME
```

Options:
- `--version VERSION` - Show information for a specific version
- `--json` - Output results in JSON format

Example:
```bash
llamapackage info llamatext
```

### Package Management Commands

#### `install`

Install a package from the registry.

```bash
llamapackage install PACKAGE_NAME[==VERSION]
```

Options:
- `--upgrade`, `-U` - Upgrade the package if already installed
- `--no-deps` - Don't install dependencies
- `--dev` - Install development dependencies as well

Examples:
```bash
# Install latest version
llamapackage install llamatext

# Install specific version
llamapackage install llamatext==1.0.0

# Install multiple packages
llamapackage install llamatext llamamath
```

#### `uninstall`

Uninstall a package.

```bash
llamapackage uninstall PACKAGE_NAME
```

Options:
- `--yes`, `-y` - Skip confirmation
- `--no-deps` - Don't uninstall dependencies

Example:
```bash
llamapackage uninstall llamatext
```

#### `list`

List installed packages.

```bash
llamapackage list
```

Options:
- `--outdated` - Only show outdated packages
- `--json` - Output results in JSON format

#### `update`

Update installed packages.

```bash
llamapackage update [PACKAGE_NAME]
```

If no package name is specified, all packages will be updated.

Options:
- `--yes`, `-y` - Skip confirmation
- `--no-deps` - Don't update dependencies

#### `check-updates`

Check for available updates to installed packages.

```bash
llamapackage check-updates
```

Options:
- `--json` - Output results in JSON format

### Publishing Commands

#### `publish`

Publish a package to the registry.

```bash
llamapackage publish [PACKAGE_DIR]
```

If no directory is specified, the current directory is used.

Options:
- `--skip-validation` - Skip validation checks
- `--yes`, `-y` - Skip confirmation

#### `validate`

Validate a package without publishing it.

```bash
llamapackage validate [PACKAGE_DIR]
```

If no directory is specified, the current directory is used.

### Configuration Commands

#### `config`

Manage configuration.

```bash
llamapackage config get KEY
llamapackage config set KEY VALUE
llamapackage config list
```

Examples:
```bash
# Get the registry URL
llamapackage config get registry_url

# Set the registry URL
llamapackage config set registry_url https://registry.llamasearch.ai

# List all config values
llamapackage config list
```

### Web Interface Commands

#### `web`

Start the web interface.

```bash
llamapackage web
```

Options:
- `--host HOST` - Host to bind to (default: 127.0.0.1)
- `--port PORT` - Port to bind to (default: 5000)
- `--no-browser` - Don't open a browser window

### Advanced Commands

#### `export`

Export installed packages to a requirements file.

```bash
llamapackage export [FILE]
```

If no file is specified, the output is written to stdout.

Options:
- `--format FORMAT` - Output format (requirements, poetry, pipenv)

#### `import`

Import packages from a requirements file.

```bash
llamapackage import FILE
```

Options:
- `--upgrade`, `-U` - Upgrade already installed packages
- `--no-deps` - Don't install dependencies

#### `run`

Run a command in the context of the installed packages.

```bash
llamapackage run COMMAND [ARGS...]
```

Example:
```bash
llamapackage run python -c "from llamatext import TextProcessor; print(TextProcessor().process('Hello'))"
```

#### `shell`

Start a shell with the environment set up for the installed packages.

```bash
llamapackage shell
```

## Environment Variables

The following environment variables can be used to configure the CLI behavior:

| Variable | Description |
|----------|-------------|
| `LLAMAPACKAGE_CONFIG_DIR` | Path to the configuration directory |
| `LLAMAPACKAGE_REGISTRY_URL` | URL of the package registry |
| `LLAMAPACKAGE_AUTH_TOKEN` | Authentication token |
| `LLAMAPACKAGE_DEBUG` | Enable debug output when set to 1 |

## Exit Codes

The CLI uses the following exit codes:

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Command-line usage error |
| 3 | Authentication error |
| 4 | Network error |
| 5 | Package not found |

## Bash Completion

To enable Bash completion, add the following to your `.bashrc` or `.bash_profile`:

```bash
eval "$(llamapackage completion)"
```

## Examples

### Basic Package Management Workflow

```bash
# Login to the registry
llamapackage login

# Search for text processing packages
llamapackage search text

# Install a package
llamapackage install llamatext

# Check for updates
llamapackage check-updates

# Update all packages
llamapackage update

# List installed packages
llamapackage list
```

### Publishing Workflow

```bash
# Create a new package (interactively)
llamapackage new mypackage

# Validate the package
llamapackage validate ./mypackage

# Publish the package
llamapackage publish ./mypackage
```

For more examples, see the [Examples](../examples) directory. 