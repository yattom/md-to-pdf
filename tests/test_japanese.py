"""
Tests for Japanese text support in PDF generation.
"""

import os
import pytest
from pathlib import Path

from md_to_pdf.converter import convert_file
from md_to_pdf.fonts import get_system_japanese_fonts


def test_get_system_japanese_fonts():
    """Test that Japanese fonts are detected on the system."""
    fonts = get_system_japanese_fonts()
    assert isinstance(fonts, dict)
    assert len(fonts) > 0


def has_dependencies():
    """Check if the required dependencies are available."""
    try:
        import sphinx
        import rinoh
        return True
    except ImportError:
        return False


@pytest.mark.skipif(not has_dependencies(), reason="Sphinx or rinohtype not installed")
def test_convert_japanese_markdown(tmp_path):
    """Test converting a Japanese Markdown file to PDF."""
    test_dir = Path(__file__).parent
    fixtures_dir = test_dir / 'fixtures'
    japanese_md_file = fixtures_dir / 'japanese_sample.md'
    
    if not japanese_md_file.exists():
        japanese_md_file = tmp_path / "japanese_test.md"
        japanese_md_file.write_text("# 日本語テスト\n\nこれは日本語のテストです。")
    
    pdf_file = convert_file(str(japanese_md_file))
    
    assert os.path.exists(pdf_file)
    assert pdf_file.endswith(".pdf")
