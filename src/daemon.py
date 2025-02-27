#!/usr/bin/env python3
"""
Daemon process that watches a directory for .wav files and processes them through main.py
"""

import os
import sys
import time
import subprocess
import signal

def process_wav_file(filepath):
    """Process a wav file through main.py and delete it afterwards"""
    try:
        # Run main.py with the wav file
        result = subprocess.run(['python3', 'main.py', filepath], check=True)
        
        # If main.py completed successfully, delete the file
        if result.returncode == 0:
            os.remove(filepath)
            print(f"Processed and removed: {filepath}")
        else:
            print(f"Error processing file: {filepath}")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running main.py: {e}")
    except Exception as e:
        print(f"Error: {e}")

def watch_directory(directory):
    """Watch a directory for .wav files and process them"""
    print(f"Watching directory: {directory}")
    
    # Handle graceful shutdown
    def signal_handler(signum, frame):
        print("\nShutting down daemon...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    while True:
        try:
            # Look for .wav files in the directory
            for filename in os.listdir(directory):
                if filename.endswith('.wav'):
                    filepath = os.path.join(directory, filename)
                    print(f"Found wav file: {filepath}")
                    process_wav_file(filepath)
            
            # Wait before checking again
            time.sleep(1)
            
        except Exception as e:
            print(f"Error scanning directory: {e}")
            sys.exit(1)

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 daemon.py <watch_directory>")
        sys.exit(1)
    
    watch_dir = sys.argv[1]
    
    # Verify directory exists
    if not os.path.isdir(watch_dir):
        print(f"Error: Directory does not exist: {watch_dir}")
        sys.exit(1)
    
    # Start watching the directory
    watch_directory(watch_dir)

if __name__ == "__main__":
    main()
