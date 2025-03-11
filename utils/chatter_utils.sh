#!/bin/bash
# Utility launcher for Chatter Pi

# Determine the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Function to display help
show_help() {
    echo "Chatter Pi Utilities"
    echo "===================="
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Available commands:"
    echo "  analyze [file]     - Analyze audio file(s)"
    echo "  analyze-basic      - Analyze audio without scipy"
    echo "  test-servo         - Test servo movement"
    echo "  backup             - Create a backup"
    echo "  restore [file]     - Restore from backup"
    echo "  list-backups       - List available backups"
    echo "  audio-devices      - List audio devices"
    echo "  test-audio         - Test audio recording/playback"
    echo "  help               - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 analyze ../src/vocals/v01.wav"
    echo "  $0 analyze --all"
    echo "  $0 test-servo --mode steps"
    echo "  $0 backup"
    echo "  $0 restore backup_20250226_123456.zip"
}

# Check if a command was provided
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

# Process commands
case "$1" in
    analyze)
        shift
        if [ $# -eq 0 ]; then
            python3 "$SCRIPT_DIR/analyze_audio.py" --all
        else
            python3 "$SCRIPT_DIR/analyze_audio.py" "$@"
        fi
        ;;
    analyze-basic)
        shift
        if [ $# -eq 0 ]; then
            python3 "$SCRIPT_DIR/analyze_audio_basic.py" --all
        else
            python3 "$SCRIPT_DIR/analyze_audio_basic.py" "$@"
        fi
        ;;
    test-servo)
        shift
        python3 "$SCRIPT_DIR/test_servo.py" "$@"
        ;;
    backup)
        shift
        python3 "$SCRIPT_DIR/backup.py" create "$@"
        ;;
    restore)
        shift
        if [ $# -eq 0 ]; then
            echo "Error: Backup file required"
            echo "Usage: $0 restore backup_file.zip [--overwrite]"
            exit 1
        fi
        python3 "$SCRIPT_DIR/backup.py" restore "$@"
        ;;
    list-backups)
        python3 "$SCRIPT_DIR/backup.py" list
        ;;
    audio-devices)
        shift
        python3 "$SCRIPT_DIR/../src/audio_devices.py" list "$@"
        ;;
    test-audio)
        shift
        python3 "$SCRIPT_DIR/../src/audio_devices.py" test "$@"
        ;;
    help)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
