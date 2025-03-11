#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI Dependency Checker for Chatter Pi

This utility checks if the required dependencies for the GUI are installed.
"""

import importlib.util
import sys
import subprocess
import platform
from src.platforms import get_platform

def check_module(module_name):
    """Check if a Python module is installed"""
    return importlib.util.find_spec(module_name) is not None

def install_module(module_name):
    """Attempt to install a Python module"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("Checking GUI dependencies for Chatter Pi...")
    
    # Check for tkinter
    if not check_module("tkinter"):
        print("❌ tkinter is not installed")
        
        platform_name = get_platform()
        if platform_name == "macos":
            print("\nTo install tkinter on macOS, you can use:")
            print("  brew install python-tk")
        elif platform_name == "linux":
            print("\nTo install tkinter on Linux, you can use:")
            print("  sudo apt-get install python3-tk")
        elif platform_name == "raspberry_pi":
            print("\nTo install tkinter on Raspberry Pi, you can use:")
            print("  sudo apt-get install python3-tk")
        
        print("\nAfter installing, try running the control panel again.")
        return False
    else:
        print("✓ tkinter is installed")
    
    # Check for other required modules
    required_modules = ["numpy", "matplotlib"]
    missing_modules = []
    
    for module in required_modules:
        if not check_module(module):
            print(f"❌ {module} is not installed")
            missing_modules.append(module)
        else:
            print(f"✓ {module} is installed")
    
    # Try to install missing modules
    if missing_modules:
        print("\nAttempting to install missing modules...")
        for module in missing_modules:
            print(f"Installing {module}...")
            if install_module(module):
                print(f"✓ {module} installed successfully")
            else:
                print(f"❌ Failed to install {module}")
                print(f"Please install {module} manually with: pip install {module}")
    
    if not missing_modules or all(check_module(module) for module in missing_modules):
        print("\nAll GUI dependencies are installed!")
        return True
    else:
        print("\nSome dependencies are missing. Please install them and try again.")
        return False

if __name__ == "__main__":
    main()
