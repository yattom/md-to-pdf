"""
Font configuration for md-to-pdf.

This module provides font configuration for rinohtype to support
various languages including Japanese.
"""

import os
import sys
import platform
from pathlib import Path


def get_system_japanese_fonts():
    """
    Get Japanese font paths based on the operating system.
    
    Returns:
        dict: Dictionary with font family names as keys and font paths as values
    """
    system = platform.system()
    fonts = {}
    
    if system == 'Windows':
        font_dir = Path('C:/Windows/Fonts')
        fonts = {
            'sans': str(font_dir / 'msgothic.ttc'),  # MS Gothic
            'serif': str(font_dir / 'msmincho.ttc'),  # MS Mincho
            'monospace': str(font_dir / 'msmincho.ttc'),  # MS Mincho as fallback
        }
    elif system == 'Darwin':  # macOS
        font_dir = Path('/System/Library/Fonts')
        fonts = {
            'sans': str(font_dir / 'Hiragino Sans GB.ttc'),
            'serif': str(font_dir / 'Hiragino Mincho ProN.ttc'),
            'monospace': str(font_dir / 'Osaka.ttf'),
        }
    else:  # Linux and others
        font_dirs = [
            Path('/usr/share/fonts/truetype/noto'),
            Path('/usr/share/fonts/opentype/noto'),
            Path('/usr/share/fonts/truetype'),
            Path('/usr/share/fonts/opentype'),
        ]
        
        for font_dir in font_dirs:
            sans_jp = font_dir / 'NotoSansCJK-Regular.ttc'
            serif_jp = font_dir / 'NotoSerifCJK-Regular.ttc'
            
            if sans_jp.exists():
                fonts['sans'] = str(sans_jp)
            if serif_jp.exists():
                fonts['serif'] = str(serif_jp)
                
        if 'sans' not in fonts:
            fonts['sans'] = 'Noto Sans CJK JP'
        if 'serif' not in fonts:
            fonts['serif'] = 'Noto Serif CJK JP'
        if 'monospace' not in fonts:
            fonts['monospace'] = 'Noto Sans Mono CJK JP'
    
    return fonts


def create_rinoh_stylesheet(output_path):
    """
    Create a rinohtype stylesheet with Japanese font support.
    
    Args:
        output_path (Path): Path where the stylesheet should be saved
        
    Returns:
        str: Path to the created stylesheet
    """
    fonts = get_system_japanese_fonts()
    
    stylesheet_content = f"""
from rinoh.font import TypeFace
from rinoh.font.opentype import OpenTypeFont
from rinoh.style import StyleSheet, StyledMatcher
from rinoh.stylesheets import sphinx
from rinoh.text import StyledText
from rinoh.document import DocumentTree, Document, Page, PORTRAIT
from rinoh.dimension import PT, CM, INCH
from rinoh.structure import SectionTitles
from rinoh.stylesheets import sphinx_base14

stylesheet = sphinx_base14.copy()

try:
    sans_jp = '{fonts.get("sans", "")}'
    serif_jp = '{fonts.get("serif", "")}'
    mono_jp = '{fonts.get("monospace", "")}'
    
    if sans_jp:
        stylesheet.variables['sans_typeface'] = sans_jp
    if serif_jp:
        stylesheet.variables['serif_typeface'] = serif_jp
    if mono_jp:
        stylesheet.variables['mono_typeface'] = mono_jp
except Exception as e:
    print(f"Warning: Could not configure Japanese fonts: {{e}}")

stylesheet.write('{output_path}')
"""
    
    with open(output_path, 'w') as f:
        f.write(stylesheet_content)
    
    return str(output_path)
