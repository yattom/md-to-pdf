"""
Tests for the watcher module.
"""

import os
import time
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from md_to_pdf.watcher import MarkdownHandler, watch_directory


def test_markdown_handler_init():
    """Test MarkdownHandler initialization."""
    handler = MarkdownHandler(delay=30)
    assert handler.delay == 30
    assert handler.timers == {}


def test_is_markdown_file():
    """Test _is_markdown_file method."""
    handler = MarkdownHandler()
    
    assert handler._is_markdown_file("test.md") is True
    assert handler._is_markdown_file("test.MD") is True
    assert handler._is_markdown_file("test.Md") is True
    assert handler._is_markdown_file("test.txt") is False
    assert handler._is_markdown_file("test") is False


@patch('md_to_pdf.watcher.Timer')
def test_schedule_conversion(mock_timer):
    """Test _schedule_conversion method."""
    mock_timer_instance = MagicMock()
    mock_timer.return_value = mock_timer_instance
    
    handler = MarkdownHandler(delay=10)
    handler._schedule_conversion("test.md")
    
    mock_timer.assert_called_once_with(
        10,
        handler._convert_file,
        args=["test.md"]
    )
    
    mock_timer_instance.start.assert_called_once()
    
    assert "test.md" in handler.timers
    assert handler.timers["test.md"] == mock_timer_instance


@patch('md_to_pdf.watcher.Timer')
def test_schedule_conversion_reschedule(mock_timer):
    """Test _schedule_conversion method with rescheduling."""
    mock_timer_instance1 = MagicMock()
    mock_timer_instance2 = MagicMock()
    mock_timer.side_effect = [mock_timer_instance1, mock_timer_instance2]
    
    handler = MarkdownHandler(delay=10)
    handler._schedule_conversion("test.md")
    
    assert mock_timer_instance1.start.call_count == 1
    
    mock_timer_instance1.is_alive.return_value = True
    
    handler._schedule_conversion("test.md")
    
    mock_timer_instance1.cancel.assert_called_once()
    
    assert mock_timer_instance2.start.call_count == 1
    
    assert handler.timers["test.md"] == mock_timer_instance2


@patch('md_to_pdf.watcher.convert_file')
def test_convert_file(mock_convert_file):
    """Test _convert_file method."""
    mock_convert_file.return_value = "test.pdf"
    
    handler = MarkdownHandler()
    handler.timers = {"test.md": MagicMock()}
    handler._convert_file("test.md")
    
    mock_convert_file.assert_called_once_with("test.md")
    
    assert "test.md" not in handler.timers


@patch('md_to_pdf.watcher.convert_file')
def test_convert_file_error(mock_convert_file):
    """Test _convert_file method with an error."""
    mock_convert_file.side_effect = Exception("Test error")
    
    handler = MarkdownHandler()
    handler.timers = {"test.md": MagicMock()}
    handler._convert_file("test.md")
    
    mock_convert_file.assert_called_once_with("test.md")
    
    assert "test.md" not in handler.timers


def test_on_modified():
    """Test on_modified method."""
    event = MagicMock()
    event.is_directory = False
    event.src_path = "test.md"
    
    handler = MarkdownHandler()
    handler._schedule_conversion = MagicMock()
    
    handler.on_modified(event)
    
    handler._schedule_conversion.assert_called_once_with("test.md")


def test_on_modified_directory():
    """Test on_modified method with a directory event."""
    event = MagicMock()
    event.is_directory = True
    
    handler = MarkdownHandler()
    handler._schedule_conversion = MagicMock()
    
    handler.on_modified(event)
    
    handler._schedule_conversion.assert_not_called()


def test_on_modified_non_markdown():
    """Test on_modified method with a non-Markdown file."""
    event = MagicMock()
    event.is_directory = False
    event.src_path = "test.txt"
    
    handler = MarkdownHandler()
    handler._schedule_conversion = MagicMock()
    
    handler.on_modified(event)
    
    handler._schedule_conversion.assert_not_called()


@patch('md_to_pdf.watcher.Observer')
@patch('pathlib.Path.is_dir')
def test_watch_directory(mock_is_dir, mock_observer):
    """Test watch_directory function."""
    mock_is_dir.return_value = True
    
    mock_observer_instance = MagicMock()
    mock_observer.return_value = mock_observer_instance
    
    with patch('md_to_pdf.watcher.time.sleep', side_effect=KeyboardInterrupt) as mock_sleep:
        try:
            watch_directory("test_dir", recursive=True, delay=30)
        except KeyboardInterrupt:
            pass  # Expected exception
    
    mock_observer.assert_called_once()
    mock_observer_instance.start.assert_called_once()
    
    mock_observer_instance.schedule.assert_called_once()
    args, kwargs = mock_observer_instance.schedule.call_args
    assert isinstance(args[0], MarkdownHandler)
    assert args[0].delay == 30
    assert args[1] == str(Path("test_dir").resolve())
    assert kwargs.get('recursive') is True
