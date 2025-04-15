"""
Example configuration file for md-to-pdf with Japanese font support.

This file shows how to configure rinohtype to use Japanese fonts.
Place this file in the same directory as your Markdown files or specify
the path to this file using the --config option.
"""

japanese_fonts = {
    'sans': r'C:/Windows/Fonts/msgothic.ttc',  # Windows: MS Gothic
    
    'serif': r'C:/Windows/Fonts/msmincho.ttc',  # Windows: MS Mincho
    
    'monospace': r'C:/Windows/Fonts/msgothic.ttc',  # Windows: MS Gothic as fallback
}

pdf_settings = {
    'paper_size': 'A4',
    'orientation': 'portrait',
    'language': 'ja',  # Set to 'ja' for Japanese content
}

markdown_extensions = [
    'colon_fence',
    'deflist',
    'tables',
    'footnotes',
]

watch_settings = {
    'delay': 60,  # Delay in seconds before conversion after changes
    'recursive': True,  # Whether to watch subdirectories
}
