# Chatter Pi Troubleshooting Guide

## Common Issues and Solutions

### Audio Issues

#### No Audio Output
- Check that your audio output device is properly connected
- Run `python3 src/audio_devices.py list` to list all audio devices
- Check volume levels with `alsamixer` (Linux/Raspberry Pi) or system volume controls
- Test your audio devices with `python3 src/audio_devices.py test`

#### Audio Quality Issues
- Try increasing BUFFER_SIZE in config.ini
- Check for ground loops or interference in your audio connections
- Use the audio analysis tool to check your audio files:
  ```
  python3 src/analyze_audio.py vocals/v01.wav
  ```
- Test your microphone/line input sensitivity:
  ```
  python3 src/audio_devices.py sensitivity
  ```

#### Audio Files Not Found
- Ensure your audio files are in the correct directories (vocals/ and ambient/)
- Verify file naming: vocal files should be v01.wav, v02.wav, etc.
- Check file permissions: `chmod 644 vocals/*.wav ambient/*.wav`

#### Microphone/Line Input Issues
- Verify your input device is properly connected and recognized
- List available audio devices: `python3 src/audio_devices.py list`
- Test your input device: `python3 src/audio_devices.py test --input X` (replace X with device index)
- Set the INPUT_DEVICE parameter in config.ini to your device index

### Servo Issues

#### Servo Not Moving
- Check physical connections to the GPIO pin
- Verify the pigpio daemon is running: `sudo systemctl status pigpiod`
- Test the servo directly:
  ```
  python3 src/test_servo.py --mode position
  ```
- Check servo power supply (servos need adequate current)

#### Erratic Servo Movement
- Try adjusting SERVO_MIN and SERVO_MAX in config.ini
- Increase BUFFER_SIZE to reduce CPU load
- Check for interference on the servo control line
- Test with different movement patterns:
  ```
  python3 src/test_servo.py --mode steps --speed 0.5
  ```

#### Jaw Movement Not Matching Audio
- Adjust threshold levels (THRESHOLD, LEVEL1, LEVEL2, LEVEL3)
- Try different STYLE settings (0, 1, or 2)
- Use the audio analysis tool to recommend threshold settings:
  ```
  python3 src/analyze_audio.py --filtered vocals/v01.wav
  ```

### Trigger Issues

#### PIR Sensor Not Triggering
- Check PIR sensor connections
- Verify PIR_PIN setting in config.ini
- Test PIR sensor with a simple script:
  ```python
  from gpiozero import MotionSensor
  pir = MotionSensor(23)  # Use your PIR_PIN value
  print("Waiting for motion...")
  pir.wait_for_motion()
  print("Motion detected!")
  ```

#### Timer Not Working
- Check DELAY setting in config.ini
- Verify PROP_TRIGGER is set to TIMER
- Look for error messages in the console output

#### Eyes Not Lighting
- Check LED connections
- Verify EYES_PIN setting in config.ini
- Ensure EYES is set to ON in config.ini

## Diagnostic Tools

### System Information
Get system information to help with troubleshooting:
```
cat /proc/cpuinfo
vcgencmd measure_temp
free -h
```

### Audio Diagnostics
```
aplay -l
amixer
```

### GPIO Diagnostics
```
gpio readall
```

### Log Files
Check system logs for errors:
```
dmesg | grep -i error
journalctl -xe
```

## Getting Help

If you're still experiencing issues:
1. Check the documentation in src/README.md, src/TECHNICAL.md, and src/QUICKSTART.md
2. Create a backup of your configuration: `python3 src/backup.py create`
3. Try restoring default settings by copying config.ini.default to config.ini
4. Post an issue on GitHub with:
   - Description of the problem
   - Steps to reproduce
   - Relevant error messages
   - Output from diagnostic commands
