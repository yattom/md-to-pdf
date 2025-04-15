"""
Command-line interface for md-to-pdf.
"""

import os
import sys
import click

from md_to_pdf.converter import convert_file
from md_to_pdf.watcher import watch_directory


@click.group()
@click.version_option()
def main():
    """
    md-to-pdf: Automatically convert Markdown files to PDF.
    """
    pass


@main.command()
@click.argument('file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--output', '-o', type=click.Path(), help='Output PDF file path')
def convert(file_path, output):
    """
    Convert a single Markdown file to PDF.
    """
    if not file_path.lower().endswith('.md'):
        click.echo(f"Error: {file_path} is not a Markdown file", err=True)
        sys.exit(1)

    output_path = output or os.path.splitext(file_path)[0] + '.pdf'
    click.echo(f"Converting {file_path} to {output_path}...")
    
    try:
        convert_file(file_path, output_path)
        click.echo(f"Successfully converted to {output_path}")
    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--recursive', '-r', is_flag=True, help='Watch subdirectories recursively')
@click.option('--delay', '-d', type=int, default=60, help='Delay in seconds before conversion (default: 60)')
def watch(directory, recursive, delay):
    """
    Watch a directory for changes to Markdown files and convert them to PDF.
    """
    click.echo(f"Watching {directory} for changes to Markdown files...")
    click.echo(f"Conversion will be triggered {delay} seconds after the last change")
    
    try:
        watch_directory(directory, recursive=recursive, delay=delay)
    except KeyboardInterrupt:
        click.echo("\nStopping watcher...")
    except Exception as e:
        click.echo(f"Error during watching: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
