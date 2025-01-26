
from setuptools import setup, find_packages

"""
Setup module for llamapackages.

This module provides functionality for the llamapackages project.
"""

setup(
    name="llamapackages-llamasearch",
    version="0.1.0rc350",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "tqdm>=4.60.0",
        "pyyaml>=6.0.0",
    ],
    author="LlamaSearch AI",
    author_email="nikjois@llamasearch.ai",
    description="🦙 LlamaPackages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://llamasearch.ai",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)

# Updated in commit 5 - 2025-04-04 17:44:39

# Updated in commit 13 - 2025-04-04 17:44:39

# Updated in commit 21 - 2025-04-04 17:44:40

# Updated in commit 29 - 2025-04-04 17:44:41

# Updated in commit 5 - 2025-04-05 14:44:01

# Updated in commit 13 - 2025-04-05 14:44:01

# Updated in commit 21 - 2025-04-05 14:44:02

# Updated in commit 29 - 2025-04-05 14:44:02

# Updated in commit 5 - 2025-04-05 15:30:13

# Updated in commit 13 - 2025-04-05 15:30:13

# Updated in commit 21 - 2025-04-05 15:30:13

# Updated in commit 29 - 2025-04-05 15:30:14

# Updated in commit 5 - 2025-04-05 16:10:17

# Updated in commit 13 - 2025-04-05 16:10:17
