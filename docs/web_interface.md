# Web Interface

LlamaPackages includes a web interface for easy package management. This document outlines how to use the web interface.

## Starting the Web Interface

To use the web interface, you must first install LlamaPackages with the web dependencies:

```bash
pip install llamapackages[web]
```

Then start the web server:

```bash
llamapackage web
```

By default, the web interface will be available at http://127.0.0.1:5000

### Command-line Options

You can customize the web server using the following options:

```bash
llamapackage web --host 0.0.0.0 --port 8080 --no-browser
```

Options:
- `--host`: The host to bind to (default: 127.0.0.1)
- `--port`: The port to bind to (default: 5000)
- `--no-browser`: Don't open a browser window

### Using Docker

You can also run the web interface using Docker:

```bash
docker run -p 5000:5000 -v ~/.llamapackage:/app/config llamasearch/llamapackages:latest web
```

## Logging In

When you first access the web interface, you'll need to log in with your LlamaSearch.ai credentials.

![Login Screen](/docs/images/login_screen.png)

Enter your username and password, then click "Login".

## Dashboard

After logging in, you'll see the dashboard showing an overview of your installed packages.

![Dashboard](/docs/images/dashboard.png)

The dashboard includes:
- Total number of installed packages
- Recently updated packages
- Packages with available updates
- Quick navigation links

## Searching Packages

The search bar at the top of every page allows you to search for packages in the registry.

![Search Results](/docs/images/search_results.png)

Search results show:
- Package name
- Description
- Author
- Latest version
- Install button

## Package Details

Click on a package name to see detailed information about the package.

![Package Details](/docs/images/package_details.png)

The details page includes:
- Description
- Author information
- License
- Homepage link
- Dependencies
- Version history
- Installation instructions
- README content

## Managing Packages

### Installing Packages

To install a package:
1. Search for the package
2. Click the "Install" button on the search results or package details page

You'll see a progress indicator during installation, and a success message when complete.

### Viewing Installed Packages

Click on "Installed Packages" in the navigation menu to see all your installed packages.

![Installed Packages](/docs/images/installed_packages.png)

### Updating Packages

For packages with available updates:
1. Go to the "Installed Packages" page
2. Click the "Update" button next to the package

You can also update all packages at once by clicking the "Update All" button.

### Uninstalling Packages

To uninstall a package:
1. Go to the "Installed Packages" page
2. Click the "Uninstall" button next to the package
3. Confirm the uninstallation

## Publishing Packages

The web interface also allows you to publish packages.

### Package Validation

To validate a package before publishing:
1. Click on "Publish" in the navigation menu
2. Select the package directory or drag and drop the files
3. Click "Validate"

The validation results will show any issues that need to be fixed before publishing.

### Publishing Process

To publish a package:
1. Click on "Publish" in the navigation menu
2. Select the package directory or drag and drop the files
3. Click "Validate" to check for issues
4. If validation passes, click "Publish"

## Configuration

The web interface allows you to manage your LlamaPackages configuration.

![Configuration](/docs/images/configuration.png)

To access the configuration page, click on "Configuration" in the navigation menu.

You can set the following options:
- Registry URL
- Default package installation directory
- Auto-update settings
- Interface theme

## API Explorer

The web interface includes an API explorer that allows you to try out the LlamaPackages API.

![API Explorer](/docs/images/api_explorer.png)

To access the API explorer, click on "API Explorer" in the navigation menu.

The API explorer includes:
- Documentation for all API endpoints
- Interactive request builder
- Response viewer

## Security Considerations

### Session Management

The web interface uses secure session management. Sessions expire after 30 minutes of inactivity for security.

### HTTPS

For production use, it's recommended to run the web interface behind a secure HTTPS proxy such as Nginx or Apache with SSL/TLS.

### Authentication

All sensitive operations require authentication. Your credentials are never stored in the browser.

## Customizing the Web Interface

### Themes

The web interface supports different themes. To change the theme:
1. Go to the Configuration page
2. Select a theme from the dropdown
3. Click "Save"

### Custom Templates

Advanced users can create custom templates for the web interface. See the [Customization Guide](./customization.md) for details.

## Environment Variables

The web interface can be configured using the following environment variables:

| Variable | Description |
|----------|-------------|
| `LLAMAPACKAGE_WEB_HOST` | Host to bind to |
| `LLAMAPACKAGE_WEB_PORT` | Port to bind to |
| `LLAMAPACKAGE_WEB_DEBUG` | Enable debug mode |
| `LLAMAPACKAGE_WEB_SECRET_KEY` | Secret key for sessions |

Example:
```bash
LLAMAPACKAGE_WEB_PORT=8080 LLAMAPACKAGE_WEB_DEBUG=1 llamapackage web
```

## Troubleshooting

### Common Issues

#### "Cannot connect to server"

If you see this error, check that:
- The web server is running
- You're using the correct URL
- No firewall is blocking the connection

#### "Authentication failed"

This usually means:
- Your username or password is incorrect
- Your session has expired
- The registry is down

#### Slow Performance

If the web interface is slow:
- Check your internet connection
- Reduce the number of installed packages
- Increase the server resources (if self-hosting)

### Getting Help

If you encounter issues with the web interface, you can:
- Check the logs (shown in the console where you started the server)
- Visit our [GitHub repository](https://github.com/llamasearch/llamapackages) for support
- Ask for help in our community forum

## Next Steps

Now that you know how to use the web interface, you might want to:

- Learn about the [CLI](./cli_usage.md) for command-line operations
- Explore the [API Reference](./api_reference.md) for programmatic access
- See how to [create your own packages](./package_development.md) 