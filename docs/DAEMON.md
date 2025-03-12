# Daemon.py - Directory Monitoring Utility

This Python script functions as a daemon process that monitors a specified directory for new `.wav` files and automatically processes them through a separate `main.py` script.

## Functionality

The daemon works by:

1. Watching a user-specified directory for file system events
2. Detecting when new `.wav` files are created in the monitored directory
3. Processing each new `.wav` file by passing it to a `main.py` script located in the `../src/` directory

The script uses the `watchdog` library to efficiently monitor directory changes without constantly polling the file system.

## Key Components

**WavFileHandler Class**
- Extends `FileSystemEventHandler` from the watchdog library
- Implements the `on_created` method to detect new file creation events
- Filters for `.wav` files specifically

**Process Function**
- Calls the `main.py` script with the absolute path to the detected `.wav` file
- Captures and logs the output or errors from the processing

**Monitoring Function**
- Sets up the observer to watch the specified directory
- Runs continuously until interrupted by keyboard (Ctrl+C)

## Usage Guide

### Prerequisites
- Python 3
- The `watchdog` library installed (`pip install watchdog`)

### Basic Usage

Run the script from the command line, providing the directory to monitor as an argument:

```bash
python daemon.py /path/to/watch/directory
```

### Example

```bash
python daemon.py ~/audio_files
```

This will start monitoring the `~/audio_files` directory for new `.wav` files.

### Notes

- The script expects `main.py` to be located in a `../src/` directory relative to where the daemon is run
- Only `.wav` files will trigger processing
- The daemon will continue running until manually stopped with Ctrl+C
- Processing results are logged with timestamps
- Subdirectories within the watched directory are not monitored (recursive=False)

### Logging

The daemon logs all activities with timestamps, including:
- When it starts watching a directory
- When new `.wav` files are detected
- Processing results (success or failure)

Logs are output to the console in the format: `YYYY-MM-DD HH:MM:SS - message`

