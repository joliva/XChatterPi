# XChatterPi Quick Start Guide

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/XChatterPi.git
   cd XChatterPi
   ```

2. Install dependencies:
   ```bash
   sudo bash src/install.sh
   ```
   *Note: This script attempts to install all necessary dependencies for your platform. See `src/PLATFORM_SUPPORT.md` for details on supported platforms and any platform-specific instructions. You may encounter errors during this step related to missing packages. Refer to `src/TROUBLESHOOTING.md` for solutions.*

3. Copy the default configuration:
   ```bash
   cp src/config.ini.default src/config.ini
   ```

## Basic Usage

### Running the Control Panel
Start the GUI control panel to configure settings:
```bash
python3 src/run_control_panel.py
```

### Playing Audio Files
To play a specific audio file:
```bash
python3 src/main.py --file path/to/your/file.wav
```
*Note: The path to the audio file can be a relative or absolute path. Ensure the file exists and is a valid WAV file.*

### Testing Servo Movement
Test servo movement without audio:
```bash
python3 src/test_servo.py --mode sweep
```
*Note: This will test the servo using the settings in `src/config.ini`.  See `src/test_servo.py --help` for command-line options to override settings.*

### Analyzing Audio
Analyze an audio file for jaw movement settings:
```bash
python3 src/analyze_audio.py path/to/your/file.wav
```
*Note: This tool provides recommendations for the `THRESHOLD` and `LEVEL` settings in `src/config.ini`.*

## Configuration

Edit `src/config.ini` to customize settings. Key sections include:

- `[SERVO]`: Servo movement parameters (MIN_ANGLE, MAX_ANGLE, SERVO_MIN, SERVO_MAX)
- `[CONTROLLER]`: Audio thresholds and filtering (THRESHOLD, LEVEL1, LEVEL2, LEVEL3, STYLE)
- `[AUDIO]`: Audio source and output settings (SOURCE, OUTPUT_CHANNELS, INPUT_DEVICE)
- `[PROP]`: Prop trigger settings (PROP_TRIGGER, DELAY, EYES, TRIGGER_OUT)
- `[PINS]`: GPIO pin assignments (JAW_PIN, PIR_PIN, EYES_PIN, TRIGGER_OUT_PIN)
- `[HARDWARE]`: Hardware simulation settings (RPI_HW_SIMULATION)

*Note: Ensure the audio device settings (`INPUT_DEVICE`, `OUTPUT_CHANNELS`) in `config.ini` are correct for your system. Use `python3 src/audio_devices.py list` to list available devices. You can also use `python3 src/audio_devices.py test` to test your audio input and output.*

## Advanced Features

### Daemon Mode
Run in daemon mode to watch a directory for new WAV files:
```bash
python3 src/daemon.py /path/to/watch
```
*Note: This will automatically process any new WAV files placed in the specified directory.*

### Backup and Restore
Create a backup of your configuration and audio files:
```bash
python3 src/backup.py create
```

Restore from a backup:
```bash
python3 src/backup.py restore backup_file.zip
```

### Diagnostics
Run the diagnostics tool to check your system configuration:
```bash
python3 src/diagnostics.py
```

## Troubleshooting

1. Check GUI dependencies (if using the control panel):
   ```bash
   python3 src/check_gui_deps.py
   ```
   *Note: This step is only required if you are using the GUI control panel.*

2. Consult the troubleshooting guide in `src/TROUBLESHOOTING.md` for common issues and solutions.

## Next Steps

- Explore the control panel GUI for advanced configuration.
- Refer to `src/TECHNICAL.md` for implementation details.
- Check `src/PLATFORM_SUPPORT.md` for platform-specific information.
