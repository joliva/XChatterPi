#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daemon process that watches a directory for .wav files and processes them through main.py
"""

import time
import os
import sys
import logging
import subprocess
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class WavFileHandler(FileSystemEventHandler):
    """
    Handles file system events, specifically for .wav files.
    """
    def on_created(self, event):
        if event.is_directory:
            return None
        
        filepath = event.src_path
        if filepath.endswith('.wav'):
            logging.info(f"New WAV file detected: {filepath}")
            process_wav_file(filepath)

def process_wav_file(filepath):
    """
    Processes a .wav file using main.py.
    """
    try:
        # Run main.py with the filepath as an argument
        result = subprocess.run([sys.executable, "src/main.py", filepath],
                                capture_output=True, text=True, check=True)
        logging.info(f"Successfully processed {filepath}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {filepath}:\n{e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error processing {filepath}:\n{str(e)}")

def watch_directory(directory):
    """
    Watches the specified directory for new .wav files.
    """
    event_handler = WavFileHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    logging.info(f"Watching directory: {directory}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Get the directory to watch from the configuration
    watch_dir = config.get('DAEMON', 'watch_directory', fallback='.')
    
    # Start watching the directory
    watch_directory(watch_dir)

if __name__ == "__main__":
    main()
