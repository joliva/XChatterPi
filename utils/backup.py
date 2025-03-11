#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backup Utility for Chatter Pi

This utility creates and restores backups of configuration and audio files.
"""

import os
import shutil
import argparse
import datetime
import zipfile
import glob
import sys

BACKUP_DIR = "backups"
VOCALS_DIR = "src/vocals"
AMBIENT_DIR = "src/ambient"

def create_backup(include_audio=True, include_config=True):
    """Create a backup of configuration and optionally audio files"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    # Ensure the backup directory exists
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # Create temporary directory for backup files
    temp_dir = os.path.join(BACKUP_DIR, f"temp_backup_{timestamp}")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Copy configuration files if requested
        if include_config:
            config_paths = ["config.ini"]
            config_found = False
            for config_path in config_paths:
                if os.path.exists(config_path):
                    shutil.copy2(config_path, temp_dir)
                    print(f"Backed up: {config_path}")
                    config_found = True
                    break
            
            if not config_found:
                # Create a default config file
                default_config_path = "src/config.ini.default"
                if os.path.exists(default_config_path):
                    shutil.copy2(default_config_path, os.path.join(temp_dir, "config.ini"))
                    print(f"Created default config.ini from template")
                else:
                    print("Warning: No config.ini found and no default template available")
        
        # Copy audio files if requested
        if include_audio:
            # Create audio directories in the temporary directory
            os.makedirs(os.path.join(temp_dir, "vocals"), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, "ambient"), exist_ok=True)
            
            # Copy vocal files
            vocal_files = glob.glob(os.path.join(VOCALS_DIR, "*.wav"))
            if vocal_files:
                for file in vocal_files:
                    shutil.copy2(file, os.path.join(temp_dir, "vocals"))
                    print(f"Backed up: {file}")
            else:
                print("No vocal files found")
            
            # Copy ambient files
            ambient_files = glob.glob(os.path.join(AMBIENT_DIR, "*.wav"))
            if ambient_files:
                for file in ambient_files:
                    shutil.copy2(file, os.path.join(temp_dir, "ambient"))
                    print(f"Backed up: {file}")
            else:
                print("No ambient files found")
        
        # Create zip archive
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, 
                              os.path.relpath(file_path, temp_dir))
        
        print(f"Backup created: {backup_path}")
        return backup_path
    
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None
    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def restore_backup(backup_file, overwrite=False):
    """Restore configuration and audio files from a backup"""
    # Check if backup file exists
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    if not os.path.exists(backup_path):
        print(f"Backup file not found: {backup_path}")
        return False
    
    # Create temporary directory
    temp_dir = "temp_restore"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Extract backup
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall(temp_dir)
        
        # Restore configuration file
        config_path = os.path.join(temp_dir, "config.ini")
        if os.path.exists(config_path):
            if overwrite or not os.path.exists("config.ini"):
                shutil.copy2(config_path, "config.ini")
                print("Configuration restored")
            else:
                print("Skipped config.ini (use --overwrite to replace)")
        
        # Restore audio files
        vocals_dir = os.path.join(temp_dir, "vocals")
        if os.path.exists(vocals_dir):
            os.makedirs(VOCALS_DIR, exist_ok=True)
            for file in glob.glob(os.path.join(vocals_dir, "*.wav")):
                filename = os.path.basename(file)
                dest_path = os.path.join(VOCALS_DIR, filename)
                if overwrite or not os.path.exists(dest_path):
                    shutil.copy2(file, dest_path)
                    print(f"Restored: vocals/{filename}")
                else:
                    print(f"Skipped: vocals/{filename} (use --overwrite to replace)")
        
        ambient_dir = os.path.join(temp_dir, "ambient")
        if os.path.exists(ambient_dir):
            os.makedirs(AMBIENT_DIR, exist_ok=True)
            for file in glob.glob(os.path.join(ambient_dir, "*.wav")):
                filename = os.path.basename(file)
                dest_path = os.path.join(AMBIENT_DIR, filename)
                if overwrite or not os.path.exists(dest_path):
                    shutil.copy2(file, dest_path)
                    print(f"Restored: ambient/{filename}")
                else:
                    print(f"Skipped: ambient/{filename} (use --overwrite to replace)")
        
        print("Restore completed successfully")
        return True
    
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

def list_backups():
    """List available backup files"""
    backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith("backup_") and f.endswith(".zip")]
    if not backups:
        print("No backup files found")
        return
    
    print("Available backups:")
    for backup in backups:
        print(f"- {backup}")

def main():
    parser = argparse.ArgumentParser(description='Backup utility for Chatter Pi')
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Create backup command
    create_parser = subparsers.add_parser('create', help='Create a backup')
    create_parser.add_argument('--no-audio', action='store_true', 
                              help='Exclude audio files from backup')
    create_parser.add_argument('--no-config', action='store_true',
                              help='Exclude configuration from backup')
    
    # Restore backup command
    restore_parser = subparsers.add_parser('restore', help='Restore from a backup')
    restore_parser.add_argument('file', help='Backup file to restore from')
    restore_parser.add_argument('--overwrite', action='store_true', 
                               help='Overwrite existing files')
    
    # List backups command
    list_parser = subparsers.add_parser('list', help='List available backups')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_backup(not args.no_audio, not args.no_config)
    elif args.command == 'restore':
        restore_backup(args.file, args.overwrite)
    elif args.command == 'list':
        list_backups()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
