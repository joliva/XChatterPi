"""
Platform abstraction layer for Chatter Pi.
This module provides platform-specific implementations for hardware control.
"""

import platform
import importlib
import os

# Platform detection
def get_platform():
    """Detect the current platform and return the appropriate platform module"""
    system = platform.system()
    
    # Check for Raspberry Pi
    if system == "Linux" and os.path.exists("/proc/device-tree/model"):
        try:
            with open("/proc/device-tree/model") as f:
                model = f.read()
                if "raspberry pi" in model.lower():
                    return "raspberry_pi"
        except:
            pass
    
    # Other platforms
    if system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    elif system == "Windows":
        return "windows"
    else:
        return "unknown"

# Platform module loading
def load_platform():
    """Load the appropriate platform module based on the detected platform"""
    platform_name = get_platform()
    
    try:
        # Try to import the specific platform module
        module_name = f"platforms.{platform_name}"
        platform_module = importlib.import_module(module_name, package="src")
        return platform_module.PlatformHardware()
    except (ImportError, AttributeError):
        # Fall back to dummy implementation if specific platform not available
        from platforms.dummy import PlatformHardware
        return PlatformHardware()

# Create a global instance of the platform hardware
hardware = load_platform()
