"""
Command-line interface for LlamaPackage.

This module provides the command-line interface (CLI) for interacting
with the LlamaPackage system.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from llamapackage.registry import PackageRegistry
from llamapackage.auth import Authentication
from llamapackage.config import Config

console = Console()
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration.
    
    Args:
        verbose: Whether to enable verbose logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@click.group()
@click.version_option()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """LlamaPackage CLI - Package management for the LlamaSearch.ai ecosystem."""
    setup_logging(verbose)
    
    # Initialize context with shared objects
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config()
    ctx.obj["registry"] = PackageRegistry()
    ctx.obj["auth"] = Authentication()
    ctx.obj["verbose"] = verbose


@cli.command()
@click.pass_context
def setup(ctx: click.Context) -> None:
    """Set up LlamaPackage client configuration."""
    config = ctx.obj["config"]
    
    console.print("[bold]Setting up LlamaPackage client[/bold]")
    
    # Get registry URL
    registry_url = click.prompt(
        "Registry URL",
        default=config.get("registry_url", "https://packages.llamasearch.ai"),
    )
    
    # Get API token if available
    api_token = click.prompt(
        "API token (optional, leave empty if none)",
        default=config.get("api_token", ""),
        hide_input=True,
        show_default=False,
    )
    
    # Save configuration
    config.set("registry_url", registry_url)
    if api_token:
        config.set("api_token", api_token)
    config.save()
    
    console.print("[green]Configuration saved successfully![/green]")


@cli.command()
@click.argument("query")
@click.pass_context
def search(ctx: click.Context, query: str) -> None:
    """Search for packages matching QUERY."""
    registry = ctx.obj["registry"]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Searching for packages matching '{query}'...", total=None)
        packages = registry.search_packages(query)
    
    if not packages:
        console.print(f"[yellow]No packages found matching '{query}'[/yellow]")
        return
    
    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Description")
    
    for package in packages:
        latest = package.get_latest_version()
        version = latest.version if latest else "N/A"
        table.add_row(package.name, version, package.description or "")
    
    console.print(table)


@cli.command()
@click.argument("package_name")
@click.option("--version", "-v", help="Specific version to install")
@click.option("--directory", "-d", help="Directory to install package to")
@click.pass_context
def install(ctx: click.Context, package_name: str, version: Optional[str] = None, directory: Optional[str] = None) -> None:
    """Install PACKAGE_NAME from the registry."""
    registry = ctx.obj["registry"]
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description=f"Installing package {package_name}{f' version {version}' if version else ''}...",
                total=None,
            )
            
            # Download package
            dest_path = Path(directory) if directory else None
            output_path = registry.download_package(package_name, version, dest_path)
            
            # Install package using pip
            if output_path.suffix in (".whl", ".tar.gz"):
                import subprocess
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", str(output_path)],
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    console.print(f"[red]Error installing {package_name}:[/red] {result.stderr}")
                    return
        
        console.print(f"[green]Successfully installed {package_name}{f' version {version}' if version else ''}![/green]")
    
    except Exception as e:
        console.print(f"[red]Error installing {package_name}:[/red] {str(e)}")


@cli.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List all available packages in the registry."""
    registry = ctx.obj["registry"]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching package list...", total=None)
        registry.load()
        packages = list(registry.packages.values())
    
    if not packages:
        console.print("[yellow]No packages found in the registry[/yellow]")
        return
    
    table = Table(title="Available Packages")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Description")
    
    for package in packages:
        latest = package.get_latest_version()
        version = latest.version if latest else "N/A"
        table.add_row(package.name, version, package.description or "")
    
    console.print(table)


@cli.command()
@click.argument("package_path")
@click.option("--token", "-t", help="API token for authentication")
@click.pass_context
def publish(ctx: click.Context, package_path: str, token: Optional[str] = None) -> None:
    """Publish a package to the registry."""
    registry = ctx.obj["registry"]
    config = ctx.obj["config"]
    
    # Use token from config if not provided
    if not token:
        token = config.get("api_token")
        if not token:
            console.print("[red]Error:[/red] No API token provided. Use --token or configure with 'llamapackage setup'")
            return
    
    try:
        package_path = Path(package_path)
        if not package_path.exists():
            console.print(f"[red]Error:[/red] Package path '{package_path}' does not exist")
            return
        
        # Check if package is a directory (source dist) or file (wheel/tarball)
        if package_path.is_dir():
            # Source distribution - build package first
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Building package...", total=None)
                
                # Check for pyproject.toml or setup.py
                if (package_path / "pyproject.toml").exists() or (package_path / "setup.py").exists():
                    import subprocess
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "wheel", "--no-deps", "-w", str(package_path.parent), str(package_path)],
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode != 0:
                        console.print(f"[red]Error building package:[/red] {result.stderr}")
                        return
                    
                    # Find built wheel
                    wheels = list(package_path.parent.glob("*.whl"))
                    if not wheels:
                        console.print("[red]Error:[/red] Failed to build package wheel")
                        return
                    
                    package_file = wheels[0]
                else:
                    console.print("[red]Error:[/red] Package directory must contain pyproject.toml or setup.py")
                    return
        else:
            # Pre-built wheel or tarball
            package_file = package_path
        
        # Extract metadata from package
        import zipfile
        import tarfile
        import json
        from email.parser import Parser
        
        metadata = {}
        
        if package_file.suffix == ".whl":
            with zipfile.ZipFile(package_file) as wheel:
                # Find metadata file
                meta_files = [f for f in wheel.namelist() if f.endswith(".dist-info/METADATA")]
                if not meta_files:
                    console.print("[red]Error:[/red] Could not find METADATA in wheel")
                    return
                
                # Parse metadata
                with wheel.open(meta_files[0]) as meta_file:
                    meta_content = meta_file.read().decode("utf-8")
                    parser = Parser()
                    message = parser.parsestr(meta_content)
                    
                    metadata["name"] = message.get("Name")
                    metadata["version"] = message.get("Version")
                    metadata["summary"] = message.get("Summary")
                    metadata["author"] = message.get("Author")
                    metadata["author_email"] = message.get("Author-email")
                    metadata["license"] = message.get("License")
        elif package_file.suffix in (".tar.gz", ".tgz"):
            with tarfile.open(package_file) as tar:
                # Find metadata file (PKG-INFO)
                meta_files = [f for f in tar.getnames() if f.endswith("PKG-INFO")]
                if not meta_files:
                    console.print("[red]Error:[/red] Could not find PKG-INFO in tarball")
                    return
                
                # Parse metadata
                meta_file = tar.extractfile(meta_files[0])
                if meta_file:
                    meta_content = meta_file.read().decode("utf-8")
                    parser = Parser()
                    message = parser.parsestr(meta_content)
                    
                    metadata["name"] = message.get("Name")
                    metadata["version"] = message.get("Version")
                    metadata["summary"] = message.get("Summary")
                    metadata["author"] = message.get("Author")
                    metadata["author_email"] = message.get("Author-email")
                    metadata["license"] = message.get("License")
        else:
            console.print(f"[red]Error:[/red] Unsupported package format: {package_file.suffix}")
            return
        
        if not metadata.get("name") or not metadata.get("version"):
            console.print("[red]Error:[/red] Could not extract name and version from package")
            return
        
        # Publish package
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description=f"Publishing {metadata['name']} version {metadata['version']}...",
                total=None,
            )
            
            package_version = registry.publish_package(
                name=metadata["name"],
                version=metadata["version"],
                package_file=package_file,
                metadata=metadata,
                token=token,
            )
        
        console.print(f"[green]Successfully published {metadata['name']} version {metadata['version']}![/green]")
    
    except Exception as e:
        console.print(f"[red]Error publishing package:[/red] {str(e)}")


@cli.command()
@click.argument("package_name")
@click.option("--version", "-v", help="Specific version to update to")
@click.pass_context
def update(ctx: click.Context, package_name: str, version: Optional[str] = None) -> None:
    """Update PACKAGE_NAME to the latest version."""
    # Re-use install command logic
    ctx.invoke(install, package_name=package_name, version=version)


def main() -> None:
    """Run the CLI application."""
    try:
        cli(obj={})
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 