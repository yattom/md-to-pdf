"""
Markdown to PDF conversion functionality using Sphinx.
"""

import os
import shutil
import tempfile
import subprocess
from pathlib import Path


def convert_file(input_path, output_path=None):
    """
    Convert a Markdown file to PDF using Sphinx.
    
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
        
        shutil.copy(input_path, source_dir / 'index.md')
        
        create_sphinx_config(source_dir)
        
        try:
            subprocess.run(
                ['sphinx-build', '-b', 'latex', str(source_dir), str(build_dir)],
                check=True,
                capture_output=True,
                text=True
            )
            
            latex_dir = build_dir
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'index.tex'],
                cwd=latex_dir,
                check=True,
                capture_output=True,
                text=True
            )
            
            pdf_path = latex_dir / 'index.pdf'
            if pdf_path.exists():
                shutil.copy(pdf_path, output_path)
            else:
                raise RuntimeError("PDF generation failed: output file not found")
        
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"PDF conversion failed: {e.stderr}")
    
    return str(output_path)


def create_sphinx_config(source_dir):
    """
    Create a Sphinx configuration file (conf.py) in the source directory.
    
    Args:
        source_dir (Path): Path to the Sphinx source directory
    """
    config_content = """

project = 'md-to-pdf'
copyright = '2025'
author = 'md-to-pdf'

extensions = [
    'myst_parser',
]

latex_elements = {
    'papersize': 'a4paper',
}

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
