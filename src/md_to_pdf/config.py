"""
Configuration handling for md-to-pdf.
"""

import os
import json
from pathlib import Path


DEFAULT_CONFIG = {
    "delay": 60,  # Delay in seconds before conversion
    "recursive": False,  # Whether to watch subdirectories
    "extensions": [".md"],  # File extensions to watch
}


def get_config_path():
    """
    Get the path to the configuration file.
    
    Returns:
        Path: Path to the configuration file
    """
    config_dir = os.environ.get(
        "XDG_CONFIG_HOME", 
        os.path.join(os.path.expanduser("~"), ".config")
    )
    
    return Path(config_dir) / "md-to-pdf" / "config.json"


def load_config():
    """
    Load the configuration from the config file.
    If the file doesn't exist, create it with default values.
    
    Returns:
        dict: Configuration values
    """
    config_path = get_config_path()
    
    if not config_path.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
        
        return config
    
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading config: {e}")
        print("Using default configuration")
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """
    Save the configuration to the config file.
    
    Args:
        config (dict): Configuration values to save
    """
    config_path = get_config_path()
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    
    except IOError as e:
        print(f"Error saving config: {e}")


def update_config(key, value):
    """
    Update a configuration value.
    
    Args:
        key (str): Configuration key to update
        value: New value for the key
    """
    config = load_config()
    config[key] = value
    save_config(config)
