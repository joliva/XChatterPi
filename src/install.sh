#!/bin/bash
# Chatter Pi Installation Script

echo "Chatter Pi Installation"
echo "======================="

# Detect platform
PLATFORM="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -f /proc/device-tree/model ] && grep -q "Raspberry Pi" /proc/device-tree/model; then
        PLATFORM="raspberry_pi"
    else
        PLATFORM="linux"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
fi

echo "Detected platform: $PLATFORM"

# Check if running as root on Linux
if [[ "$PLATFORM" == "raspberry_pi" || "$PLATFORM" == "linux" ]]; then
    if [ "$EUID" -ne 0 ]; then
        echo "Please run as root (use sudo)"
        exit 1
    fi
fi

# Install platform-specific dependencies
if [ "$PLATFORM" == "raspberry_pi" ]; then
    echo "Installing Raspberry Pi specific packages..."
    apt-get update
    apt-get install -y python3-pip python3-numpy python3-scipy python3-matplotlib pigpio python3-pigpio portaudio19-dev
    
    echo "Installing Python packages..."
    pip3 install pyaudio gpiozero
    
    echo "Setting up pigpio service..."
    systemctl enable pigpiod
    systemctl start pigpiod
    
    # Set up desktop entry
    echo "Setting up desktop entry..."
    cp chatter.desktop /usr/share/applications/
    chmod +x chatter.sh

elif [ "$PLATFORM" == "linux" ]; then
    echo "Installing Linux packages..."
    apt-get update
    apt-get install -y python3-pip python3-numpy python3-scipy python3-matplotlib portaudio19-dev
    
    echo "Installing Python packages..."
    pip3 install pyaudio

elif [ "$PLATFORM" == "macos" ]; then
    echo "Installing macOS packages..."
    if command -v brew &> /dev/null; then
        brew install python3 numpy scipy portaudio
    else
        echo "Homebrew not found. Please install Homebrew first: https://brew.sh/"
        echo "Then run this script again."
        exit 1
    fi
    
    echo "Installing Python packages..."
    pip3 install pyaudio matplotlib
else
    echo "Unsupported platform. Manual installation required."
    exit 1
fi

# Create directories if they don't exist (common for all platforms)
echo "Setting up directories..."
mkdir -p vocals
mkdir -p ambient

# Make sure chatter.sh is executable
chmod +x chatter.sh

echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Place vocal audio files in the vocals/ directory (v01.wav, v02.wav, etc.)"
echo "2. Place ambient audio files in the ambient/ directory (a01.wav, a02.wav, etc.)"
echo "3. Edit config.ini to customize settings"
echo "4. Run the application with ./chatter.sh or python3 main.py"
echo ""
echo "For more information, see README.md"
