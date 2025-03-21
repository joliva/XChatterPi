#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic Tool for Chatter Pi

This utility checks the system configuration and identifies potential issues.
"""

import os
import sys
import subprocess
import platform
import shutil
import importlib.util
import configparser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/src")
from platforms import get_platform, hardware

def check_command(command):
    """Check if a command is available"""
    return shutil.which(command) is not None

def run_command(command):
    """Run a command and return its output"""
    try:
        result = subprocess.run(command, shell=True, check=False, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def check_module(module_name):
    """Check if a Python module is installed"""
    return importlib.util.find_spec(module_name) is not None

def check_file(file_path):
    """Check if a file exists and is readable"""
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)

def check_directory(dir_path):
    """Check if a directory exists and is readable"""
    return os.path.isdir(dir_path) and os.access(dir_path, os.R_OK)

def count_files(dir_path, extension=".wav"):
    """Count files with a specific extension in a directory"""
    if not check_directory(dir_path):
        return 0
    return len([f for f in os.listdir(dir_path) if f.endswith(extension)])

def check_config():
    """Check the configuration file for potential issues"""
    issues = []
    
    if not check_file("../src/config.ini"):
        issues.append("config.ini file not found")
        return issues
    
    try:
        config = configparser.ConfigParser()
        config.read("../src/config.ini")
        
        # Check for invalid combinations
        if config.get("AUDIO", "SOURCE") == "FILES" and config.get("PROP", "PROP_TRIGGER") == "START":
            issues.append("Invalid configuration: SOURCE=FILES cannot be used with PROP_TRIGGER=START")
        
        # Check for missing directories
        if config.get("AUDIO", "SOURCE") == "FILES" and not check_directory("vocals"):
            issues.append("vocals directory not found but SOURCE=FILES")
        
        if config.get("AUDIO", "AMBIENT") == "ON" and not check_directory("ambient"):
            issues.append("ambient directory not found but AMBIENT=ON")
        
        # Check for reasonable values
        try:
            buffer_size = int(config.get("AUDIO", "BUFFER_SIZE"))
            if buffer_size < 1024 or buffer_size > 16384:
                issues.append(f"BUFFER_SIZE={buffer_size} is outside recommended range (1024-16384)")
        except ValueError:
            issues.append("BUFFER_SIZE is not a valid integer")
        
        try:
            delay = int(config.get("PROP", "DELAY"))
            if delay < 1:
                issues.append(f"DELAY={delay} is too small (should be >= 1)")
        except ValueError:
            issues.append("DELAY is not a valid integer")
        
    except Exception as e:
        issues.append(f"Error parsing config.ini: {e}")
    
    return issues

def main():
    print("Chatter Pi Diagnostic Tool")
    print("=========================\n")
    
    # System information
    print("System Information:")
    print(f"  Platform: {platform.platform()}")
    print(f"  Python: {platform.python_version()}")
    print(f"  Architecture: {platform.machine()}")
    
    # Get platform information
    platform_name = get_platform()
    system_info = hardware.get_system_info()
    
    print(f"  Platform: {platform_name}")
    for key, value in system_info.items():
        print(f"  {key.title()}: {value}")
    print("")
    
    # Check required Python modules
    print("Python Modules:")
    modules = ["numpy", "scipy", "pyaudio", "gpiozero", "pigpio", "matplotlib", "tkinter"]
    for module in modules:
        status = "Installed" if check_module(module) else "Missing"
        print(f"  {module}: {status}")
    print("")
    
    # Check required commands
    print("System Commands:")
    commands = ["aplay", "pigpiod", "gpio"]
    for command in commands:
        status = "Available" if check_command(command) else "Missing"
        print(f"  {command}: {status}")
    print("")
    
    # Check required services
    print("Services:")
    if platform_name == "raspberry_pi":
        pigpio_status = "active" if hardware.is_service_running("pigpiod") else "inactive"
        print(f"  pigpiod: {pigpio_status}")
    else:
        print(f"  No hardware services required for {platform_name}")
    print("")
    
    # Check audio devices
    print("Audio Devices:")
    print(hardware.get_audio_devices())
    print("")
    
    # Check files and directories
    print("Files and Directories:")
    print(f"  config.ini: {'Found' if check_file('../src/config.ini') else 'Missing'}")
    print(f"  vocals directory: {'Found' if check_directory('../src/vocals') else 'Missing'}")
    print(f"  ambient directory: {'Found' if check_directory('../src/ambient') else 'Missing'}")
    print(f"  Vocal files: {count_files('../src/vocals')}")
    print(f"  Ambient files: {count_files('../src/ambient')}")
    print("")
    
    # Check configuration
    print("Configuration Check:")
    config_issues = check_config()
    if config_issues:
        print("✗ Configuration issues found:")
        for issue in config_issues:
            print(f"  - {issue}")
    else:
        print("✓ No configuration issues found")
    print("")
    
    # Check hardware simulation setting
    print("Checking hardware simulation setting:")
    config = configparser.ConfigParser()
    config.read('../src/config.ini')
    try:
        rpi_hw_simulation = config.getboolean("HARDWARE", "RPI_HW_SIMULATION", fallback=False)
        print(f"✓ RPI_HW_SIMULATION is set to {rpi_hw_simulation}")
    except configparser.NoSectionError:
        print("✗ HARDWARE section is missing in config.ini")
    except configparser.NoOptionError:
        print("✗ RPI_HW_SIMULATION option is missing in config.ini")
    
    # Overall assessment
    print("Overall Assessment:")
    all_issues = []
    
    # Check for critical dependencies
    if not check_module("pyaudio"):
        all_issues.append("Missing critical dependency: pyaudio")
    if not check_module("gpiozero"):
        all_issues.append("Missing critical dependency: gpiozero")
    if not check_module("numpy"):
        all_issues.append("Missing critical dependency: numpy")
    
    # Check for pigpiod
    #if pigpio_status != "active":
    #    all_issues.append("pigpiod service is not running")
    
    # Check for audio
    if not run_command("aplay -l | grep -v 'List of'"):
        all_issues.append("No audio devices detected")
    
    # Add config issues
    all_issues.extend(config_issues)
    
    if all_issues:
        print("⚠️ Issues detected that may affect functionality:")
        for issue in all_issues:
            print(f"  - {issue}")
        print("\nRecommendations:")
        print("  - Run 'sudo bash install.sh' to install dependencies")
        print("  - Run 'sudo systemctl start pigpiod' to start the pigpio daemon")
        print("  - Check your audio configuration with 'aplay -l' and 'alsamixer'")
        print("  - Verify your config.ini settings")
        print("  - Test your servo with 'python3 test_servo.py'")
    else:
        print("✓ All checks passed! Your system appears to be properly configured.")

if __name__ == "__main__":
    main()
