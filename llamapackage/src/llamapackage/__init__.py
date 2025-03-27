"""
LlamaPackage - Package management and distribution system for the LlamaSearch.ai ecosystem.

This package provides tools for managing, distributing, and discovering
packages within the LlamaSearch.ai ecosystem.
"""

from importlib.metadata import version, PackageNotFoundError

from llamapackage.auth import Authentication, Authorization, User
from llamapackage.cli import cli
from llamapackage.registry import PackageRegistry, Package, PackageVersion
from llamapackage.dependency import DependencyResolver, DependencyConflict
from llamapackage.storage import Storage, StorageError
from llamapackage.config import Config

try:
    __version__ = version("llamapackage")
except PackageNotFoundError:
    try:
        from llamapackage._version import version as __version__
    except ImportError:
        __version__ = "0.1.0.dev0"

__all__ = [
    "Authentication",
    "Authorization",
    "User",
    "cli",
    "PackageRegistry",
    "Package",
    "PackageVersion",
    "DependencyResolver",
    "DependencyConflict",
    "Storage",
    "StorageError",
    "Config",
    "__version__",
] 