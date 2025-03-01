# XChatterPi
A flexible Audio Servo Controller for talking props (skulls, animals, etc.)

Originally developed as XChatterPi by Mike McGurrin (https://github.com/ViennaMike/ChatterPi)
Enhanced with cross-platform support by John Oliva

XChatterPi now runs on:
- Raspberry Pi (with full hardware support)
- Linux (with simulated hardware)
- macOS (with simulated hardware)

On Linux and macOS, the hardware interfaces (servos, buttons, LEDs) are simulated in software, allowing you to develop and test your audio-controlled animations on any platform. For actual prop control, use a Raspberry Pi where real hardware is supported.

Originally developed and tested on Raspberry Pi Model 3 A+, Pi 4, and Pi Zero W.

# Installation Options

1. Source Code Installation (All Platforms):
   - Download the source code
   - Install dependencies using the installation script
   - Configure and run

2. Pre-built Raspberry Pi Image (Raspberry Pi Only):
   - Download chat.img.gz from [Google Drive](https://drive.google.com/drive/folders/1njfqegJImeXq-ZoW_yuY0TCJ0bTiwWCA?usp=sharing)
   - Flash to SD card
   - Boot and run

Note: The pre-built image is only for Raspberry Pi. For Linux and macOS, use the source code installation.

## Quick Installation

For a quick installation of dependencies, run:
```bash
sudo bash src/install.sh
```

# Introduction

XChatterPi is a software package that turns a Raspberry Pi into an audio servo controller. In other words, the Pi outputs commands to control a servo based on the volume of the audio input. The input can be either stored audio files (in either mono or stereo .wav format) or from an external source, such as a microphone or line level input. One of the uses is to drive animatronic props, such as a skull or a talking bird.

See the documentation for additional information.

# Background: A Brief History of Talking Skull Control

A common prop that still makes a good impact is a talking object, whether a skull or animal. Some lower cost commercial props use a motor and spring. Another approach is to pre-program a complete sequence to match the vocals, but this is very time consuming and if you want to change the vocals, or even just edit them slightly, you need to reprogram the entire sequence. For that reason, the use of an audio servo controller to drive a servomotor controlling the jaw is a very popular approach. There are several variations. One of the earliest use hardware to detect when the audio exceeded a threshold, and then began moving the jaw towards a fully open position, and when the audio went below the threshold, it would begin closing the jaw. &quot;Scary Terry&quot; Simmons may have been the first to develop an [electronic hardware board](http://www.scary-terry.com/audioservo/audioservo.htm) to do this, and [Cowlacious Designs](https://www.cowlacious.com/categories/Scary-Terry-Audio-Servo-Driver/) has continued to improve and sell commercial versions, with many added features such as a built in audio player, various triggering options, and the ability to control LEDs as eyes.

Later, someone named Mike (no relation) combined an Arduino with a hardware volume level board to produce the [Jawduino](http://buttonbanger.com/?page_id=137). This went from having just 2 levels to 4. The original project just took audio in and controlled the servo, but others added extensions to play stored mp3 files and/or randomly move additional servos (for example, [http://batbuddy.org/resources/Halloweenstuff/TalkingSkull.php](http://batbuddy.org/resources/Halloweenstuff/TalkingSkull.php)).

A few years ago, Steve Bjork from Haunt Hackers combined dedicated hardware with a propeller microcontroller to increase the number of levels to almost 256 and also to filter out low and high frequencies that don&#39;t tend to result in jaw movement for spoken sound. The result is the [Wee Little Talker](http://www.haunthackers.com/weelittletalker/index.shtml). This commercial board also has an onboard mp3 player, can be triggered externally, control LED &#39;eyes,&quot; and adds a wide array of features including a voice feedback menu system.

It occurred to me that with current single board computer capabilities and powerful software libraries, it should be possible to incorporate most of the best features of all of these into a single, software-based system running on a Raspberry Pi. The result is XChatterPi. XChatterPi was based on ChatterPi (https://github.com/ViennaMike/ChatterPi) and developed using the Python language, but ideas for capabilities and features were freely borrowed from previous audio servo controller projects.

# Features
XChatterPi includes the following features

- Audio signal volume controls servo
- Can be started by an external trigger, such as a PIR motion detector
- Can be set to start periodically via an internal timer
- Audio can be from wav files or external input
- Can send an output trigger to start another device when it is triggered
- Output to light LED "eyes" (e.g., for a skull)
- Optionally can play ambient sound tracis between triggering events
- GUI control panel for modifying the configuration parameters
- Utility (via control panel) to maximize the volume of the audio files

## Utilities

XChatterPi now includes several utilities to help with setup and configuration:

### Audio Analysis Tool
Analyzes audio files to recommend threshold settings for jaw movement in XChatterPi:
```bash
python3 src/analyze_audio.py vocals/v01.wav
python3 src/analyze_audio.py --filtered ambient/a01.wav
python3 src/analyze_audio.py --all  # Analyze all audio files
```

If you don't have scipy installed, you can use the basic version:
```bash
python3 src/analyze_audio_basic.py vocals/v01.wav
python3 src/analyze_audio_basic.py --all
```

### Servo Test Utility
Test and calibrate servo movement in XChatterPi without playing audio:
```bash
python3 src/test_servo.py --mode sweep
python3 src/test_servo.py --mode steps --speed 2.0
python3 src/test_servo.py --mode position --min-angle 0 --max-angle 90
```

### Backup Utility
Create and restore backups of your XChatterPi configuration and audio files:
```bash
python3 src/backup.py create        # Create a full backup
python3 src/backup.py list          # List available backups
python3 src/backup.py restore backup_20250226_123456.zip
```

### Audio Processing Daemon
Monitor a directory for wav files and automatically process them with XChatterPi:
```bash
python3 src/daemon.py /path/to/watch/directory
```

The daemon will:
- Watch the specified directory for new .wav files
- Process any found files through XChatterPi
- Delete each file after successful processing
- Continue watching for new files
- Handle graceful shutdown with Ctrl+C

This is useful for:
- Integration with other audio generation systems
- Processing files from network shares
- Batch processing multiple audio files
- Automated testing and development

## Documentation

For more detailed information, see:
- `src/README.md` - General documentation
- `src/TECHNICAL.md` - Technical details about the code
- `src/QUICKSTART.md` - Quick start guide

If you use XChatterPi, I'd love to hear about it. Post a comment on my blog: https://www.mcgurrin.info/robots/690/ and consider giving this package a star here on GitHub. Thanks!

Special thanks to Mike McGurrin for the original XChatterPi project that XChatterPi is based on.
