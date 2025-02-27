#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dependency Installer for Chatter Pi

This utility checks for and installs required dependencies.
"""

import subprocess
import sys
import importlib.util
import platform
import os

def check_module(module_name):
    """Check if a Python module is installed"""
    return importlib.util.find_spec(module_name) is not None

def install_module(module_name):
    """Attempt to install a Python module"""
    print(f"Installing {module_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing {module_name}: {e}")
        return False

def main():
    print("Chatter Pi Dependency Installer")
    print("==============================\n")
    
    # Check platform
    system = platform.system()
    print(f"Detected platform: {system}\n")
    
    # Required modules
    required_modules = {
        "numpy": "Required for audio processing",
        "matplotlib": "Required for visualization",
        "pyaudio": "Required for audio playback",
        "scipy": "Required for audio filtering (optional)"
    }
    
    # Check which modules are installed
    missing_modules = []
    for module, description in required_modules.items():
        if check_module(module):
            print(f"✓ {module} is already installed")
        else:
            print(f"✗ {module} is not installed - {description}")
            missing_modules.append(module)
    
    # Install missing modules
    if missing_modules:
        print("\nInstalling missing modules...")
        for module in missing_modules:
            success = install_module(module)
            if success:
                print(f"✓ Successfully installed {module}")
            else:
                print(f"✗ Failed to install {module}")
                
                # Special instructions for problematic modules
                if module == "pyaudio":
                    if system == "Darwin":  # macOS
                        print("\nTo install PyAudio on macOS, try:")
                        print("  brew install portaudio")
                        print("  pip install pyaudio")
                    elif system == "Linux":
                        print("\nTo install PyAudio on Linux, try:")
                        print("  sudo apt-get install python3-pyaudio")
                        print("  or")
                        print("  sudo apt-get install portaudio19-dev")
                        print("  pip install pyaudio")
                elif module == "scipy":
                    print("\nTo install SciPy, try:")
                    print("  pip install scipy")
                    print("\nIf that fails, you can use the basic audio analyzer:")
                    print("  python3 analyze_audio_basic.py")
    else:
        print("\nAll required dependencies are installed!")
    
    # Check if we can run the audio analyzer
    if check_module("scipy") and check_module("numpy") and check_module("matplotlib"):
        print("\nYou can now run the audio analyzer:")
        print("  python3 analyze_audio.py vocals/v01.wav")
    elif check_module("numpy") and check_module("matplotlib"):
        print("\nYou can run the basic audio analyzer (no scipy required):")
        print("  python3 analyze_audio_basic.py vocals/v01.wav")

if __name__ == "__main__":
    main()
