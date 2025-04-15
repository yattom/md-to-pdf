
project = 'md-to-pdf'
copyright = '2025'
author = 'md-to-pdf'
version = '0.1.0'
release = '0.1.0'

extensions = [
    'myst_parser',
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

myst_enable_extensions = [
    'colon_fence',
    'deflist',
]
source_suffix = {
    '.md': 'markdown',
}
