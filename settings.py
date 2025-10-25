"""
HardLinker Settings Manager
Handles user preferences and settings
"""

import json
import os
import sys

SETTINGS_FILE = "hardlinker_settings.json"

def get_settings_path():
    """Get the full path to settings file"""
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if getattr(sys, 'frozen', False):
        # Running as compiled exe - save settings next to exe
        app_dir = os.path.dirname(sys.executable)
    else:
        # Running as script - save in script directory
        app_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(app_dir, SETTINGS_FILE)

def load_settings():
    """Load settings from file"""
    try:
        settings_path = get_settings_path()
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {
        "show_welcome": True,
        "show_admin_warning": True
    }

def save_settings(settings):
    """Save settings to file"""
    try:
        settings_path = get_settings_path()
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception:
        pass

def should_show_welcome():
    """Check if welcome dialog should be shown"""
    settings = load_settings()
    return settings.get("show_welcome", True)

def set_show_welcome(show):
    """Set whether to show welcome dialog"""
    settings = load_settings()
    settings["show_welcome"] = show
    save_settings(settings)

def should_show_admin_warning():
    """Check if admin warning should be shown"""
    settings = load_settings()
    return settings.get("show_admin_warning", True)

def set_show_admin_warning(show):
    """Set whether to show admin warning"""
    settings = load_settings()
    settings["show_admin_warning"] = show
    save_settings(settings)
