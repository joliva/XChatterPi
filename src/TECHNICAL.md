# XChatterPi Technical Documentation

This document provides technical details about XChatterPi's implementation and architecture.

## Code Architecture

### Platform Abstraction Layer
XChatterPi uses a platform abstraction layer to support multiple operating systems:
- `platforms/base.py`: Abstract base class defining the hardware interface
- `platforms/raspberry_pi.py`: Raspberry Pi implementation using GPIO
- `platforms/linux.py`: Linux implementation with simulated hardware
- `platforms/macos.py`: macOS implementation with simulated hardware

### Core Components
- `audio.py`: Audio processing and servo control
- `control.py`: Main control loop and event handling
- `config.py`: Configuration management
- `tracks.py`: Audio file management and playback

### Utilities
- `backup.py`: Configuration and audio file backup/restore
- `daemon.py`: Directory monitoring for automated file processing
- `analyze_audio.py`: Audio analysis for threshold calibration
- `test_servo.py`: Servo testing and calibration

## Hardware Simulation
On non-Raspberry Pi platforms, hardware is simulated in software:
- Servos print angle changes instead of moving physical hardware
- Buttons simulate presses using random intervals
- LEDs and outputs log state changes
- Platform-specific system info is gathered using OS-appropriate commands

## Configuration System
- Uses INI format for easy editing
- Sections organize related settings
- Case-sensitive parameter names (all uppercase)
- Boolean values use "true"/"false"
- Hardware simulation controlled via RPI_HW_SIMULATION parameter

## Audio Processing
- Uses PyAudio for playback and recording
- Supports both WAV files and microphone input
- Bandpass filtering available for improved jaw movement
- Volume analysis determines servo angles
- Multiple control styles (threshold or multi-level)

## Event Handling
- Timer-based triggering
- PIR sensor support
- Ambient sound playback
- LED eye control
- External trigger output

## Error Handling
- Graceful cleanup of hardware resources
- Fallback to simulation mode on hardware errors
- Input validation for configuration
- Meaningful error messages

## Development Guidelines
1. Use platform abstraction for hardware access
2. Keep configuration in INI file, not hardcoded
3. Clean up resources in finally blocks
4. Log meaningful status messages
5. Support both real and simulated hardware
6. Handle errors gracefully
7. Use consistent naming conventions
8. Document public interfaces

## Testing
Test on all supported platforms:
- Raspberry Pi (with real hardware)
- Raspberry Pi (with simulated hardware)
- Linux (simulated)
- macOS (simulated)

## Future Development
Potential areas for enhancement:
1. Additional platform support
2. More audio formats
3. Network control interface
4. Additional trigger types
5. More sophisticated jaw movement algorithms
6. Visual feedback for simulation mode
