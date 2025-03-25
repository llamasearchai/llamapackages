"""
Storage management for LlamaPackage.

This module provides functionality for storing and retrieving package files.
"""

import os
import logging
import shutil
import zipfile
import tempfile
from typing import List, Optional, Tuple, Dict, Any, IO, Union
from pathlib import Path

import requests

from llamapackage.config import Config

logger = logging.getLogger(__name__)


class StorageError(Exception):
    """Exception raised for storage-related errors."""
    pass


class Storage:
    """Storage manager for package files."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the storage manager.
        
        Args:
            config: Configuration provider
        """
        self.config = config or Config()
        self.base_dir = Path(self.config.get("storage_dir", str(Path.home() / ".llamapackage" / "packages")))
        self.index_file = self.base_dir / "index.json"
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self) -> None:
        """Ensure that the storage directory exists."""
        os.makedirs(self.base_dir, exist_ok=True)
    
    def package_dir(self, package_name: str) -> Path:
        """Get the directory path for a package.
        
        Args:
            package_name: Name of the package
            
        Returns:
            Path object for the package directory
        """
        return self.base_dir / package_name
    
    def version_dir(self, package_name: str, version: str) -> Path:
        """Get the directory path for a package version.
        
        Args:
            package_name: Name of the package
            version: Version string
            
        Returns:
            Path object for the package version directory
        """
        return self.package_dir(package_name) / version
    
    def get_index(self) -> Optional[Dict[str, Any]]:
        """Get the package index.
        
        Returns:
            Package index dictionary, or None if it doesn't exist
        """
        if not self.index_file.exists():
            return {}
        
        try:
            import json
            with open(self.index_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading package index: {e}")
            return {}
    
    def save_index(self, index: Dict[str, Any]) -> bool:
        """Save the package index.
        
        Args:
            index: Package index dictionary
            
        Returns:
            True if the index was saved successfully
        """
        try:
            import json
            with open(self.index_file, "w") as f:
                json.dump(index, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving package index: {e}")
            return False
    
    def upload_package(
        self,
        package_name: str,
        version: str,
        package_file: Union[str, Path, bytes],
    ) -> str:
        """Upload a package file and return the download URL.
        
        Args:
            package_name: Name of the package
            version: Version string
            package_file: Path to package file or file content
            
        Returns:
            Download URL for the package
            
        Raises:
            StorageError: If the package could not be uploaded
        """
        try:
            # Create target directory
            target_dir = self.version_dir(package_name, version)
            os.makedirs(target_dir, exist_ok=True)
            
            # Save package file
            if isinstance(package_file, (str, Path)):
                # Copy file to storage
                package_path = Path(package_file)
                target_path = target_dir / package_path.name
                shutil.copy2(package_path, target_path)
            else:
                # Save bytes to file
                target_path = target_dir / f"{package_name}-{version}.zip"
                with open(target_path, "wb") as f:
                    f.write(package_file)
            
            # Return download URL (local file:// URL for now)
            return f"file://{target_path}"
        
        except Exception as e:
            logger.error(f"Error uploading package {package_name} {version}: {e}")
            raise StorageError(f"Failed to upload package {package_name} {version}: {e}")
    
    def save_package(
        self,
        package_name: str,
        version: str,
        package_file: IO[bytes],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Path:
        """Save a package file to storage.
        
        Args:
            package_name: Name of the package
            version: Version string
            package_file: File-like object containing the package data
            metadata: Optional package metadata to store
            
        Returns:
            Path to the saved package directory
            
        Raises:
            StorageError: If the package could not be saved
        """
        target_dir = self.version_dir(package_name, version)
        
        # Create the target directory
        os.makedirs(target_dir, exist_ok=True)
        
        try:
            # Create a temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save the package file
                package_path = Path(temp_dir) / f"{package_name}-{version}.zip"
                with open(package_path, "wb") as f:
                    f.write(package_file.read())
                
                # Extract the package
                with zipfile.ZipFile(package_path, "r") as zip_ref:
                    zip_ref.extractall(target_dir)
                
                # Save metadata if provided
                if metadata:
                    import json
                    with open(target_dir / "metadata.json", "w") as f:
                        json.dump(metadata, f, indent=2)
            
            return target_dir
        
        except Exception as e:
            # Clean up on failure
            if target_dir.exists():
                shutil.rmtree(target_dir)
            
            logger.error(f"Error saving package {package_name} {version}: {e}")
            raise StorageError(f"Failed to save package {package_name} {version}: {e}")
    
    def download_package(
        self,
        package_name: str,
        version: str,
        url: str,
        destination: Optional[Union[str, Path]] = None,
        api_token: Optional[str] = None,
    ) -> Path:
        """Download a package from a URL and save it to a destination.
        
        Args:
            package_name: Name of the package
            version: Version string
            url: URL to download the package from
            destination: Destination directory or path
            api_token: Optional API token for authentication
            
        Returns:
            Path to the downloaded package
            
        Raises:
            StorageError: If the package could not be downloaded
        """
        headers = {}
        if api_token:
            headers["Authorization"] = f"Bearer {api_token}"
        
        # Handle file:// URLs (local files)
        if url.startswith("file://"):
            file_path = url[7:]  # Remove file:// prefix
            
            if destination:
                dest_path = Path(destination)
                if dest_path.is_dir():
                    dest_file = dest_path / os.path.basename(file_path)
                else:
                    dest_file = dest_path
                
                # Copy file
                try:
                    shutil.copy2(file_path, dest_file)
                    return dest_file
                except Exception as e:
                    logger.error(f"Error copying file {file_path} to {dest_file}: {e}")
                    raise StorageError(f"Failed to copy file: {e}")
            else:
                return Path(file_path)
        
        try:
            # Create destination directory if needed
            if destination:
                dest_path = Path(destination)
                if dest_path.is_dir():
                    dest_file = dest_path / f"{package_name}-{version}.zip"
                else:
                    dest_file = dest_path
            else:
                # Save to current directory
                dest_file = Path.cwd() / f"{package_name}-{version}.zip"
            
            # Download file
            with requests.get(url, headers=headers, stream=True) as response:
                response.raise_for_status()
                with open(dest_file, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            return dest_file
        
        except Exception as e:
            logger.error(f"Error downloading package {package_name} {version} from {url}: {e}")
            raise StorageError(f"Failed to download package {package_name} {version}: {e}")
    
    def get_package_path(self, package_name: str, version: str) -> Optional[Path]:
        """Get the path to a package version if it exists.
        
        Args:
            package_name: Name of the package
            version: Version string
            
        Returns:
            Path to the package version directory, or None if it doesn't exist
        """
        path = self.version_dir(package_name, version)
        return path if path.exists() else None
    
    def get_package_metadata(self, package_name: str, version: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a package version.
        
        Args:
            package_name: Name of the package
            version: Version string
            
        Returns:
            Dictionary of metadata, or None if not found
        """
        path = self.version_dir(package_name, version)
        metadata_path = path / "metadata.json"
        
        if metadata_path.exists():
            try:
                import json
                with open(metadata_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading metadata for {package_name} {version}: {e}")
        
        return None
    
    def get_installed_versions(self, package_name: str) -> List[str]:
        """Get installed versions of a package.
        
        Args:
            package_name: Name of the package
            
        Returns:
            List of installed version strings
        """
        package_path = self.package_dir(package_name)
        if not package_path.exists():
            return []
        
        return [
            d.name for d in package_path.iterdir()
            if d.is_dir() and (d / "metadata.json").exists()
        ]
    
    def get_all_packages(self) -> Dict[str, List[str]]:
        """Get all installed packages and their versions.
        
        Returns:
            Dictionary of package name -> list of installed versions
        """
        result = {}
        
        if not self.base_dir.exists():
            return result
        
        for package_dir in self.base_dir.iterdir():
            if package_dir.is_dir():
                versions = self.get_installed_versions(package_dir.name)
                if versions:
                    result[package_dir.name] = versions
        
        return result
    
    def remove_package(self, package_name: str, version: Optional[str] = None) -> bool:
        """Remove a package from storage.
        
        Args:
            package_name: Name of the package
            version: Optional version string. If None, all versions are removed.
            
        Returns:
            True if the package was removed, False otherwise
        """
        if version:
            # Remove specific version
            path = self.version_dir(package_name, version)
            if path.exists():
                try:
                    shutil.rmtree(path)
                    return True
                except Exception as e:
                    logger.error(f"Error removing {package_name} {version}: {e}")
                    return False
            return False
        else:
            # Remove all versions
            path = self.package_dir(package_name)
            if path.exists():
                try:
                    shutil.rmtree(path)
                    return True
                except Exception as e:
                    logger.error(f"Error removing all versions of {package_name}: {e}")
                    return False
            return False
    
    def create_package_archive(
        self,
        source_dir: str,
        package_name: str,
        version: str,
        exclude: Optional[List[str]] = None,
    ) -> Tuple[str, Path]:
        """Create a package archive from a directory.
        
        Args:
            source_dir: Source directory to archive
            package_name: Name of the package
            version: Version string
            exclude: List of patterns to exclude
            
        Returns:
            Tuple of (archive path, temporary directory that contains the archive)
            
        Raises:
            StorageError: If the archive could not be created
        """
        temp_dir = tempfile.mkdtemp()
        archive_path = os.path.join(temp_dir, f"{package_name}-{version}.zip")
        
        try:
            source_path = Path(source_dir)
            
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    # Skip excluded directories
                    if exclude:
                        dirs[:] = [d for d in dirs if not any(
                            Path(os.path.join(root, d)).match(pattern)
                            for pattern in exclude
                        )]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # Skip excluded files
                        if exclude and any(
                            Path(file_path).match(pattern)
                            for pattern in exclude
                        ):
                            continue
                        
                        # Add file to archive with relative path
                        rel_path = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, rel_path)
            
            return archive_path, Path(temp_dir)
        
        except Exception as e:
            # Clean up on failure
            shutil.rmtree(temp_dir)
            
            logger.error(f"Error creating package archive for {package_name} {version}: {e}")
            raise StorageError(f"Failed to create package archive: {e}")
    
    def install_from_path(
        self,
        package_path: str,
        dest_dir: str,
        package_name: Optional[str] = None,
        version: Optional[str] = None,
    ) -> Path:
        """Install a package from a path (directory or archive) to a destination directory.
        
        Args:
            package_path: Path to package directory or archive
            dest_dir: Destination directory to install to
            package_name: Optional package name for logging
            version: Optional version for logging
            
        Returns:
            Path to the installed package directory
            
        Raises:
            StorageError: If the package could not be installed
        """
        try:
            pkg_name = package_name or os.path.basename(package_path)
            ver = version or "unknown"
            dest_path = Path(dest_dir)
            os.makedirs(dest_path, exist_ok=True)
            
            if os.path.isdir(package_path):
                # Copy directory
                for item in os.listdir(package_path):
                    src_item = os.path.join(package_path, item)
                    dst_item = dest_path / item
                    
                    if os.path.isdir(src_item):
                        shutil.copytree(src_item, dst_item)
                    else:
                        shutil.copy2(src_item, dst_item)
            
            elif package_path.endswith(".zip"):
                # Extract archive
                with zipfile.ZipFile(package_path, "r") as zip_ref:
                    zip_ref.extractall(dest_path)
            
            else:
                raise StorageError(f"Unsupported package format: {package_path}")
            
            logger.info(f"Installed {pkg_name} {ver} to {dest_dir}")
            return dest_path
        
        except Exception as e:
            logger.error(f"Error installing package from {package_path}: {e}")
            raise StorageError(f"Failed to install package: {e}")
    
    def install(
        self,
        package_name: str,
        version: str,
        dest_dir: str,
    ) -> Path:
        """Install a package from storage to a destination directory.
        
        Args:
            package_name: Name of the package
            version: Version string
            dest_dir: Destination directory to install to
            
        Returns:
            Path to the installed package directory
            
        Raises:
            StorageError: If the package could not be installed
        """
        package_path = self.get_package_path(package_name, version)
        if not package_path:
            raise StorageError(f"Package {package_name} {version} not found in storage")
        
        return self.install_from_path(
            str(package_path),
            dest_dir,
            package_name,
            version,
        ) 