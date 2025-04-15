"""
Tests for the converter module.
"""

import os
import pytest
from pathlib import Path

from md_to_pdf.converter import convert_file


def test_convert_file_not_found():
    """Test that FileNotFoundError is raised when the input file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        convert_file("nonexistent_file.md")


def has_dependencies():
    """Check if the required dependencies are available."""
    try:
        import sphinx
        import subprocess
        
        result = subprocess.run(
            ["pdflatex", "--version"], 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0
    except (ImportError, FileNotFoundError):
        return False


@pytest.mark.skipif(not has_dependencies(), reason="Sphinx or LaTeX not installed")
def test_convert_simple_markdown(tmp_path):
    """Test converting a simple Markdown file to PDF."""
    md_file = tmp_path / "test.md"
    md_file.write_text("# Test Heading\n\nThis is a test.")
    
    pdf_file = convert_file(str(md_file))
    
    assert os.path.exists(pdf_file)
    assert pdf_file.endswith(".pdf")
