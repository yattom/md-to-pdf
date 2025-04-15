"""
Markdown to PDF conversion functionality using Sphinx with rinohtype.
"""

import os
import shutil
import tempfile
import subprocess
import platform
from pathlib import Path

from md_to_pdf.fonts import create_rinoh_stylesheet


def convert_file(input_path, output_path=None):
    """
    Convert a Markdown file to PDF using Sphinx with rinohtype.
    
    Args:
        input_path (str): Path to the Markdown file to convert
        output_path (str, optional): Path where the PDF should be saved.
            If not provided, the PDF will be saved in the same directory
            as the input file with the same name but .pdf extension.
            
    Returns:
        str: Path to the generated PDF file
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        RuntimeError: If the conversion process fails
    """
    input_path = Path(input_path).resolve()
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if not output_path:
        output_path = input_path.with_suffix('.pdf')
    else:
        output_path = Path(output_path).resolve()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        source_dir = temp_dir_path / 'source'
        build_dir = temp_dir_path / 'build'
        source_dir.mkdir()
        build_dir.mkdir()
        
        stylesheet_path = temp_dir_path / 'japanese_style.rts'
        create_rinoh_stylesheet(stylesheet_path)
        
        # Copy the input file to the source directory
        shutil.copy(input_path, source_dir / 'index.md')
        
        create_sphinx_config(source_dir, stylesheet_path)
        
        try:
            subprocess.run(
                ['sphinx-build', '-b', 'rinoh', str(source_dir), str(build_dir)],
                check=True,
                capture_output=True,
                text=True
            )
            
            pdf_path = build_dir / 'index.pdf'
            if pdf_path.exists():
                shutil.copy(pdf_path, output_path)
            else:
                raise RuntimeError("PDF generation failed: output file not found")
        
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"PDF conversion failed: {e.stderr}")
    
    return str(output_path)


def create_sphinx_config(source_dir, stylesheet_path=None):
    """
    Create a Sphinx configuration file (conf.py) in the source directory.
    
    Args:
        source_dir (Path): Path to the Sphinx source directory
        stylesheet_path (Path, optional): Path to a custom rinohtype stylesheet
    """
    from md_to_pdf.fonts import get_system_japanese_fonts
    jp_fonts = get_system_japanese_fonts()
    
    font_paths = {}
    for key, path in jp_fonts.items():
        if path:
            font_paths[key] = path.replace("\\", "/")
    
    config_content = """
project = 'md-to-pdf'
copyright = '2025'
author = 'md-to-pdf'

extensions = [
    'myst_parser',
    'rinoh.frontend.sphinx',  # Add rinohtype Sphinx extension
]

import os
from pathlib import Path
from rinoh.font import Typeface
from rinoh.font.opentype import OpenTypeFont

"""

    for font_type, font_path in font_paths.items():
        if font_path and (font_path.endswith('.ttc') or font_path.endswith('.ttf') or font_path.endswith('.otf')):
            config_content += f"""
try:
    {font_type}_jp_path = r"{font_path}"
    if os.path.exists({font_type}_jp_path):
        {font_type}_jp_typeface = Typeface('{font_type.capitalize()} JP', OpenTypeFont({font_type}_jp_path))
except Exception as e:
    print(f"Warning: Could not register {font_type} Japanese font: {{e}}")
"""

    config_content += """
rinoh_documents = [
    {
        'doc': 'index',       # The name of the master document
        'target': 'index',    # The name of the output PDF file
"""

    if stylesheet_path:
        stylesheet_path_str = str(stylesheet_path).replace("\\", "/")
        config_content += f"""        'stylesheet': r"{stylesheet_path_str}",  # Custom stylesheet with Japanese font support
"""

    config_content += """    }
]

language = 'ja'

myst_enable_extensions = [
    'colon_fence',
    'deflist',
]
source_suffix = {
    '.md': 'markdown',
}
"""
    
    with open(source_dir / 'conf.py', 'w') as f:
        f.write(config_content)
