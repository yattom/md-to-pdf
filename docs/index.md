# md-to-pdf Documentation

Welcome to the md-to-pdf documentation. This tool automatically converts Markdown files to PDF using Sphinx.

## Installation

```bash
pip install md-to-pdf
```

## Usage

### Converting a Single File

To convert a single Markdown file to PDF:

```bash
md-to-pdf convert path/to/file.md
```

You can specify an output path:

```bash
md-to-pdf convert path/to/file.md --output path/to/output.pdf
```

### Watching a Directory

To watch a directory for changes to Markdown files:

```bash
md-to-pdf watch path/to/directory
```

Options:

- `--recursive` or `-r`: Watch subdirectories recursively
- `--delay` or `-d`: Set the delay in seconds before conversion (default: 60)

```bash
md-to-pdf watch path/to/directory --recursive --delay 30
```

## How It Works

md-to-pdf uses Sphinx with the MyST parser to convert Markdown to PDF. When watching a directory, it monitors for changes to Markdown files and triggers conversion after a specified delay period. If additional changes are detected during the delay period, the timer is reset.
