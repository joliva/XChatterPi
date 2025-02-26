# Chatter Pi Platform Support

Chatter Pi now supports multiple platforms through a hardware abstraction layer. This document explains how platform support works and how to run Chatter Pi on different systems.

## Supported Platforms

### Raspberry Pi
- Full hardware support with GPIO pins for servo control, PIR sensor, and LED eyes
- Uses the gpiozero and pigpio libraries for hardware control
- Recommended for production use

### Linux (Ubuntu, Debian, etc.)
- Software simulation of hardware components
- No physical servo control or GPIO support
- Useful for development and testing

### macOS
- Software simulation of hardware components
- No physical servo control or GPIO support
- Useful for development and testing

## Platform Detection

Chatter Pi automatically detects the platform it's running on and loads the appropriate hardware implementation. The detection logic is as follows:

1. Check if running on Linux with Raspberry Pi hardware
2. If not a Raspberry Pi, check the operating system (Linux, macOS, etc.)
3. Load the appropriate platform module

## Installation

Use the provided `install.sh` script which will detect your platform and install the necessary dependencies:

```bash
sudo bash src/install.sh
```

## Platform-Specific Considerations

### Raspberry Pi
- Requires the pigpio daemon to be running (`sudo systemctl start pigpiod`)
- Needs physical connections to servo, PIR sensor, and LEDs as configured in config.ini
- Supports all features of Chatter Pi

### Linux
- No physical hardware control
- Simulates hardware interactions with console output
- Useful for testing audio processing and configuration

### macOS
- No physical hardware control
- Simulates hardware interactions with console output
- Useful for testing audio processing and configuration

## Developing for New Platforms

To add support for a new platform:

1. Create a new file in the `platforms` directory (e.g., `platforms/windows.py`)
2. Implement the `PlatformHardware` class that inherits from `HardwareBase`
3. Implement all required methods for hardware control
4. Update the platform detection logic in `platforms/__init__.py` if needed

## Troubleshooting

If you encounter platform-specific issues:

1. Run the diagnostics tool: `python3 src/diagnostics.py`
2. Check that the correct platform is detected
3. Verify that all required dependencies are installed
4. For Raspberry Pi, ensure the pigpio daemon is running
