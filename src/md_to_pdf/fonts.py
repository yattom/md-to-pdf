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
    
    sans_jp = fonts.get("sans", "").replace("\\", "/")
    serif_jp = fonts.get("serif", "").replace("\\", "/")
    mono_jp = fonts.get("monospace", "").replace("\\", "/")
    
    output_path_str = str(output_path).replace("\\", "/")
    
    stylesheet_content = f"""
from rinoh.font import Typeface
from rinoh.font.opentype import OpenTypeFont
from rinoh.style import StyleSheet, StyledMatcher
from rinoh.stylesheets import sphinx
from rinoh.text import StyledText
from rinoh.document import DocumentTree, Document, Page, PORTRAIT
from rinoh.dimension import PT, CM, INCH
from rinoh.structure import SectionTitles
from rinoh.stylesheets import sphinx_base14

try:
    sans_jp_path = r"{sans_jp}"
    serif_jp_path = r"{serif_jp}"
    mono_jp_path = r"{mono_jp}"
    
    if sans_jp_path and sans_jp_path.endswith(('.ttc', '.ttf', '.otf')):
        sans_jp_typeface = Typeface('Sans JP', OpenTypeFont(sans_jp_path))
    else:
        sans_jp_typeface = None
        
    if serif_jp_path and serif_jp_path.endswith(('.ttc', '.ttf', '.otf')):
        serif_jp_typeface = Typeface('Serif JP', OpenTypeFont(serif_jp_path))
    else:
        serif_jp_typeface = None
        
    if mono_jp_path and mono_jp_path.endswith(('.ttc', '.ttf', '.otf')):
        mono_jp_typeface = Typeface('Mono JP', OpenTypeFont(mono_jp_path))
    else:
        mono_jp_typeface = None
        
    # Create a new stylesheet based on sphinx_base14
    stylesheet = sphinx_base14.copy()
    
    # Set the typefaces in the stylesheet
    if sans_jp_typeface:
        stylesheet.variables['sans_typeface'] = sans_jp_typeface
    if serif_jp_typeface:
        stylesheet.variables['serif_typeface'] = serif_jp_typeface
    if mono_jp_typeface:
        stylesheet.variables['mono_typeface'] = mono_jp_typeface
except Exception as e:
    print(f"Warning: Could not configure Japanese fonts: {{e}}")
    stylesheet = sphinx_base14.copy()

# Export the stylesheet
stylesheet.write(r"{output_path_str}")
"""
    
    with open(output_path, 'w') as f:
        f.write(stylesheet_content)
    
    return str(output_path)
