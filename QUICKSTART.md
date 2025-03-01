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

### Testing Servo Movement
Test servo movement without audio:
```bash
python3 src/test_servo.py --mode sweep
```

### Analyzing Audio
Analyze an audio file for jaw movement settings:
```bash
python3 src/analyze_audio.py path/to/your/file.wav
```

## Configuration

Edit `src/config.ini` to customize settings. Key sections include:

- `[SERVO]`: Servo movement parameters
- `[AUDIO]`: Volume thresholds and filtering
- `[PATHS]`: File locations
- `[TIMING]`: Animation timing

## Advanced Features

### Daemon Mode
Run in daemon mode to watch a directory for new WAV files:
```bash
python3 src/daemon.py /path/to/watch
```

### Backup and Restore
Create a backup of your configuration and audio files:
```bash
python3 src/backup.py create
```

Restore from a backup:
```bash
python3 src/backup.py restore backup_file.zip
```

## Troubleshooting

1. Check dependencies:
   ```bash
   python3 src/check_gui_deps.py
   ```

2. Run diagnostics:
   ```bash
   python3 src/diagnostics.py
   ```

3. Consult the troubleshooting guide in `src/TROUBLESHOOTING.md`

## Next Steps

- Explore the control panel GUI for advanced configuration
- Refer to `src/TECHNICAL.md` for implementation details
- Check `src/PLATFORM_SUPPORT.md` for platform-specific information
