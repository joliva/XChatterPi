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

def create_backup(include_audio=True, include_config=True):
    """Create a backup of configuration and optionally audio files"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/backup_{timestamp}"
    
    try:
        # Create backup directory
        os.makedirs(backup_dir)
        
        # Copy configuration files if requested
        if include_config:
            config_paths = ["config.ini", "src/config.ini"]
            config_found = False
            for config_path in config_paths:
                if os.path.exists(config_path):
                    shutil.copy2(config_path, backup_dir)
                    print(f"Backed up: {config_path}")
                    config_found = True
                    break
            
            if not config_found:
                # Create a default config file
                default_config_path = "src/config.ini.default"
                if os.path.exists(default_config_path):
                    shutil.copy2(default_config_path, os.path.join(backup_dir, "config.ini"))
                    print(f"Created default config.ini from template")
                else:
                    print("Warning: No config.ini found and no default template available")
        
        # Copy audio files if requested
        if include_audio:
            # Create audio directories
            os.makedirs(os.path.join(backup_dir, "vocals"), exist_ok=True)
            os.makedirs(os.path.join(backup_dir, "ambient"), exist_ok=True)
            
            # Copy vocal files
            vocal_files = glob.glob("vocals/*.wav")
            if vocal_files:
                for file in vocal_files:
                    shutil.copy2(file, os.path.join(backup_dir, "vocals"))
                    print(f"Backed up: {file}")
            else:
                print("No vocal files found")
            
            # Copy ambient files
            ambient_files = glob.glob("ambient/*.wav")
            if ambient_files:
                for file in ambient_files:
                    shutil.copy2(file, os.path.join(backup_dir, "ambient"))
                    print(f"Backed up: {file}")
            else:
                print("No ambient files found")
        
        # Create zip archive
        zip_filename = f"{backup_dir}.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, 
                              os.path.relpath(file_path, 
                                             os.path.join(backup_dir, '..')))
        
        # Remove temporary directory
        shutil.rmtree(backup_dir)
        
        print(f"Backup created: {zip_filename}")
        return zip_filename
    
    except Exception as e:
        print(f"Error creating backup: {e}")
        # Clean up if there was an error
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        return None

def restore_backup(backup_file, overwrite=False):
    """Restore configuration and audio files from a backup"""
    try:
        # Check if backup file exists
        if not os.path.exists(backup_file):
            print(f"Backup file not found: {backup_file}")
            return False
        
        # Create temporary directory
        temp_dir = "temp_restore"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # Extract backup
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(temp_dir)
        
        # Find the backup directory inside temp_dir
        backup_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))]
        if not backup_dirs:
            # Check if files are directly in temp_dir (no subdirectory)
            if os.path.exists(os.path.join(temp_dir, "config.ini")):
                backup_dir = temp_dir
            else:
                print("Invalid backup format: No configuration files found")
                shutil.rmtree(temp_dir)
                return False
        else:
            backup_dir = os.path.join(temp_dir, backup_dirs[0])
        
        # Restore configuration file
        config_path = os.path.join(backup_dir, "config.ini")
        if os.path.exists(config_path):
            if overwrite or not os.path.exists("config.ini"):
                shutil.copy2(config_path, "config.ini")
                print("Configuration restored")
            else:
                print("Skipped config.ini (use --overwrite to replace)")
        
        # Restore audio files
        vocals_dir = os.path.join(backup_dir, "vocals")
        if os.path.exists(vocals_dir):
            os.makedirs("vocals", exist_ok=True)
            for file in glob.glob(os.path.join(vocals_dir, "*.wav")):
                filename = os.path.basename(file)
                if overwrite or not os.path.exists(os.path.join("vocals", filename)):
                    shutil.copy2(file, os.path.join("vocals", filename))
                    print(f"Restored: vocals/{filename}")
                else:
                    print(f"Skipped: vocals/{filename} (use --overwrite to replace)")
        
        ambient_dir = os.path.join(backup_dir, "ambient")
        if os.path.exists(ambient_dir):
            os.makedirs("ambient", exist_ok=True)
            for file in glob.glob(os.path.join(ambient_dir, "*.wav")):
                filename = os.path.basename(file)
                if overwrite or not os.path.exists(os.path.join("ambient", filename)):
                    shutil.copy2(file, os.path.join("ambient", filename))
                    print(f"Restored: ambient/{filename}")
                else:
                    print(f"Skipped: ambient/{filename} (use --overwrite to replace)")
        
        # Clean up
        shutil.rmtree(temp_dir)
        print("Restore completed successfully")
        return True
    
    except Exception as e:
        print(f"Error restoring backup: {e}")
        # Clean up if there was an error
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return False

def list_backups():
    """List available backup files"""
    backups = glob.glob("backups/backup_*.zip")
    if not backups:
        print("No backup files found")
        return
    
    print("Available backups:")
    for i, backup in enumerate(sorted(backups), 1):
        # Get file size
        size_mb = os.path.getsize(backup) / (1024 * 1024)
        # Get creation date
        timestamp = os.path.getctime(backup)
        date_str = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"{i}. {backup} ({size_mb:.2f} MB, created {date_str})")

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
    subparsers.add_parser('list', help='List available backups')
    
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
