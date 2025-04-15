"""
Utility functions for md-to-pdf.
"""

import os
import sys
import shutil
from pathlib import Path


def check_dependencies():
    """
    Check if all required external dependencies are installed.
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    dependencies = {
        'sphinx-build': 'Sphinx',
    }
    
    missing = []
    
    for cmd, name in dependencies.items():
        if not shutil.which(cmd):
            missing.append(name)
    
    try:
        import rinoh
    except ImportError:
        missing.append('rinohtype')
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Please install the missing dependencies and try again.")
        return False
    
    return True


def find_markdown_files(directory, recursive=False):
    """
    Find all Markdown files in a directory.
    
    Args:
        directory (str): Path to the directory to search
        recursive (bool): Whether to search subdirectories
        
    Returns:
        list: List of paths to Markdown files
    """
    directory = Path(directory)
    
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")
    
    pattern = '**/*.md' if recursive else '*.md'
    return list(directory.glob(pattern))


def ensure_directory_exists(path):
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        path (str): Path to the directory
        
    Returns:
        Path: Path object for the directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
