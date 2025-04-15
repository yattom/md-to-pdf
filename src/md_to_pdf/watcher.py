"""
File system monitoring for Markdown files.
"""

import os
import time
from pathlib import Path
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from md_to_pdf.converter import convert_file


class MarkdownHandler(FileSystemEventHandler):
    """
    Event handler for Markdown file changes.
    
    This handler tracks changes to Markdown files and triggers
    conversion after a specified delay period. If additional changes
    are detected during the delay period, the timer is reset.
    """
    
    def __init__(self, delay=60):
        """
        Initialize the handler.
        
        Args:
            delay (int): Delay in seconds before triggering conversion
        """
        self.delay = delay
        self.timers = {}  # Maps file paths to their conversion timers
    
    def on_modified(self, event):
        """
        Handle file modification events.
        """
        if event.is_directory:
            return
        
        if self._is_markdown_file(event.src_path):
            self._schedule_conversion(event.src_path)
    
    def on_created(self, event):
        """
        Handle file creation events.
        """
        if event.is_directory:
            return
        
        if self._is_markdown_file(event.src_path):
            self._schedule_conversion(event.src_path)
    
    def _is_markdown_file(self, path):
        """
        Check if the file is a Markdown file.
        
        Args:
            path (str): Path to the file
            
        Returns:
            bool: True if the file is a Markdown file, False otherwise
        """
        return path.lower().endswith('.md')
    
    def _schedule_conversion(self, file_path):
        """
        Schedule a conversion for the file after the delay period.
        If a conversion is already scheduled, cancel it and reschedule.
        
        Args:
            file_path (str): Path to the Markdown file
        """
        if file_path in self.timers and self.timers[file_path].is_alive():
            self.timers[file_path].cancel()
        
        timer = Timer(
            self.delay,
            self._convert_file,
            args=[file_path]
        )
        timer.daemon = True
        
        self.timers[file_path] = timer
        timer.start()
        
        print(f"Scheduled conversion for {file_path} in {self.delay} seconds")
    
    def _convert_file(self, file_path):
        """
        Convert the file to PDF.
        
        Args:
            file_path (str): Path to the Markdown file
        """
        try:
            output_path = convert_file(file_path)
            print(f"Converted {file_path} to {output_path}")
        except Exception as e:
            print(f"Error converting {file_path}: {e}")
        
        if file_path in self.timers:
            del self.timers[file_path]


def watch_directory(directory, recursive=False, delay=60):
    """
    Watch a directory for changes to Markdown files.
    
    Args:
        directory (str): Path to the directory to watch
        recursive (bool): Whether to watch subdirectories
        delay (int): Delay in seconds before triggering conversion
    """
    directory = Path(directory).resolve()
    
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")
    
    event_handler = MarkdownHandler(delay=delay)
    observer = Observer()
    observer.schedule(event_handler, str(directory), recursive=recursive)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
