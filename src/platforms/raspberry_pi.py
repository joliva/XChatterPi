"""
Raspberry Pi specific hardware implementation.
"""

import subprocess
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, AngularServo, Button, DigitalOutputDevice
from platforms.base import HardwareBase

class PlatformHardware(HardwareBase):
    """Raspberry Pi specific hardware implementation"""
    
    def __init__(self):
        """Initialize Raspberry Pi hardware"""
        self.pin_factory = None
        
    def setup(self):
        """Initialize hardware components"""
        self.pin_factory = PiGPIOFactory()
        Device.pin_factory = self.pin_factory
        return True
    
    def cleanup(self):
        """Clean up hardware resources"""
        # gpiozero handles cleanup automatically
        pass
    
    def create_servo(self, pin, min_angle, max_angle, min_pulse_width, max_pulse_width):
        """Create a servo controller using gpiozero"""
        return AngularServo(
            pin, 
            min_angle=min_angle, 
            max_angle=max_angle, 
            initial_angle=None, 
            min_pulse_width=min_pulse_width,
            max_pulse_width=max_pulse_width
        )
    
    def create_button(self, pin, pull_up=True):
        """Create a button/input device using gpiozero"""
        return Button(pin, pull_up=pull_up)
    
    def create_output(self, pin):
        """Create a digital output device using gpiozero"""
        return DigitalOutputDevice(pin)
    
    def is_service_running(self, service_name):
        """Check if a system service is running using systemctl"""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout.strip() == "active"
        except Exception:
            return False
    
    def get_system_info(self):
        """Get Raspberry Pi system information"""
        info = {}
        
        # Get temperature
        try:
            result = subprocess.run(
                ["vcgencmd", "measure_temp"],
                capture_output=True,
                text=True,
                check=False
            )
            info["temperature"] = result.stdout.strip()
        except Exception:
            info["temperature"] = "Unknown"
        
        # Get model
        try:
            with open("/proc/device-tree/model", "r") as f:
                info["model"] = f.read().strip()
        except Exception:
            info["model"] = "Unknown Raspberry Pi"
        
        return info
    
    def get_audio_devices(self):
        """Get available audio devices using aplay"""
        try:
            result = subprocess.run(
                ["aplay", "-l"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout.strip()
        except Exception:
            return "No audio devices detected"
