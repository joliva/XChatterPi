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
- Full audio playback functionality
- Useful for development and testing

### macOS
- Software simulation of hardware components
- No physical servo control or GPIO support
- Full audio playback functionality
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
- Supports all features of Chatter Pi including hardware control and audio playback
- GUI control panel works with X11 desktop environment

### Linux
- No physical hardware control
- Simulates hardware interactions with console output
- Full audio playback through system audio device
- Supports microphone/line input for live audio processing
- GUI control panel works with any desktop environment
- Useful for testing audio processing and configuration

### macOS
- No physical hardware control
- Simulates hardware interactions with console output
- Full audio playback through system audio device
- Supports microphone/line input for live audio processing
- GUI control panel works natively
- Useful for testing audio processing and configuration

## Developing for New Platforms

To add support for a new platform:

1. Create a new file in the `platforms` directory (e.g., `platforms/windows.py`)
2. Implement the `PlatformHardware` class that inherits from `HardwareBase`
3. Implement all required methods for hardware control
4. Update the platform detection logic in `platforms/__init__.py` if needed

## GUI Control Panel

Chatter Pi includes a graphical control panel that works on all supported platforms:

1. To launch the control panel with dependency checking:
   ```
   python3 src/run_control_panel.py
   ```

2. Or launch it directly:
   ```
   python3 src/controlPanel.py
   ```

The control panel allows you to:
- Adjust servo settings
- Configure audio thresholds
- Set trigger options
- Maximize audio volume

## Audio Device Support

Chatter Pi supports audio input and output on all platforms. To help with audio device configuration:

1. List all available audio devices:
   ```
   python3 src/audio_devices.py list
   ```

2. Test audio input and output:
   ```
   python3 src/audio_devices.py test
   ```

3. Test input sensitivity and get recommended threshold settings:
   ```
   python3 src/audio_devices.py sensitivity
   ```

4. To use a specific input device, set the `INPUT_DEVICE` parameter in `config.ini` to the device index.

## Troubleshooting

If you encounter platform-specific issues:

1. Run the diagnostics tool: `python3 src/diagnostics.py`
2. Check that the correct platform is detected
3. Verify that all required dependencies are installed
4. For Raspberry Pi, ensure the pigpio daemon is running
5. For audio issues, use the audio device utility: `python3 src/audio_devices.py list`
