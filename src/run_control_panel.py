#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Control Panel Launcher for Chatter Pi

This script checks for dependencies and then launches the control panel.
"""

import os
import sys
import importlib.util
import subprocess
from platforms import get_platform

def check_dependencies():
    """Check if all required dependencies are installed"""
    # First check if we have the dependency checker
    if os.path.exists("check_gui_deps.py"):
        try:
            # Run the dependency checker
            result = subprocess.run(
                [sys.executable, "check_gui_deps.py"],
                capture_output=True,
                text=True,
                check=False
            )
            print(result.stdout)
            
            # If the checker reported success, return True
            if "All GUI dependencies are installed!" in result.stdout:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error running dependency checker: {e}")
            return False
    
    # Fallback: check for tkinter directly
    if not importlib.util.find_spec("tkinter"):
        print("tkinter is not installed. Please install it first.")
        platform_name = get_platform()
        if platform_name == "macos":
            print("On macOS: brew install python-tk")
        elif platform_name in ["linux", "raspberry_pi"]:
            print("On Linux/Raspberry Pi: sudo apt-get install python3-tk")
        return False
    
    return True

def main():
    """Main function to launch the control panel"""
    # Check if we're in the right directory
    if not os.path.exists("controlPanel.py"):
        print("Error: This script must be run from the ChatterPi root directory.")
        print("Please change to the ChatterPi directory and try again.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("Please install the missing dependencies and try again.")
        return
    
    # Launch the control panel
    print("Launching ChatterPi Control Panel...")
    try:
        subprocess.run([sys.executable, "controlPanel.py"])
    except Exception as e:
        print(f"Error launching control panel: {e}")

if __name__ == "__main__":
    main()
