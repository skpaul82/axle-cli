#!/usr/bin/env python3
"""Configuration management for Axle CLI."""

import json
import os
from pathlib import Path


# Config file location
CONFIG_DIR = Path.home() / ".axle"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_config_dir() -> Path:
    """Get the configuration directory."""
    return CONFIG_DIR


def get_config_file() -> Path:
    """Get the configuration file path."""
    return CONFIG_FILE


def ensure_config_dir() -> None:
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load configuration from file.

    Returns:
        Configuration dictionary
    """
    if not CONFIG_FILE.exists():
        return {}

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_config(config: dict) -> None:
    """Save configuration to file.

    Args:
        config: Configuration dictionary to save
    """
    ensure_config_dir()

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_security_setting() -> str:
    """Get the security setting from config.

    Returns:
        'enabled', 'disabled', or None if not set
    """
    config = load_config()
    return config.get("security", None)


def set_security_setting(enabled: bool) -> None:
    """Set the security setting in config.

    Args:
        enabled: True to enable, False to disable
    """
    config = load_config()
    config["security"] = "enabled" if enabled else "disabled"
    save_config(config)


def get_code_review_setting() -> str:
    """Get the code review setting from config.

    Returns:
        'enabled', 'disabled', or None if not set
    """
    config = load_config()
    return config.get("code_review", None)


def set_code_review_setting(enabled: bool) -> None:
    """Set the code review setting in config.

    Args:
        enabled: True to enable, False to disable
    """
    config = load_config()
    config["code_review"] = "enabled" if enabled else "disabled"
    save_config(config)


def is_security_enabled() -> bool:
    """Check if security validation is enabled.

    Returns:
        True if enabled, False otherwise
    """
    setting = get_security_setting()
    if setting is None:
        # Default to disabled
        return False
    return setting == "enabled"


def is_code_review_enabled() -> bool:
    """Check if code review is enabled.

    Returns:
        True if enabled, False otherwise
    """
    setting = get_code_review_setting()
    if setting is None:
        # Default to disabled
        return False
    return setting == "enabled"


def clear_config() -> None:
    """Clear all configuration settings."""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()


def show_config() -> dict:
    """Show current configuration.

    Returns:
        Configuration dictionary
    """
    return load_config()
