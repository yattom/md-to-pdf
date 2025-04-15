"""
Example configuration file for md-to-pdf with Japanese font support.

This file shows how to configure rinohtype to use Japanese fonts.
"""

rinoh_documents = [
    {
        'doc': 'index',       # The name of the master document
        'target': 'index',    # The name of the output PDF file
    }
]

rinoh_paper_size = 'A4'
rinoh_font_path = [r'C:/Windows/Fonts']  # Use raw string with forward slashes
rinoh_font_config = {
    'serif': [r'C:/Windows/Fonts/msmincho.ttc', 'DejaVu Serif'],
    'sans': [r'C:/Windows/Fonts/msgothic.ttc', 'DejaVu Sans'],
    'mono': [r'C:/Windows/Fonts/msgothic.ttc', 'DejaVu Sans Mono'],
}

language = 'ja'  # Set to 'ja' for Japanese content

myst_enable_extensions = [
    'colon_fence',
    'deflist',
]
source_suffix = {
    '.md': 'markdown',
}
