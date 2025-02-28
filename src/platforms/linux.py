"""
Linux specific hardware implementation.
"""

import subprocess
import platform
import logging
from platforms.base import HardwareBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def default_handler(value): 
    logger.info(f"[Linux] Setting servo angle to {value}")

def bottango_handler(value): 
    logger.info(f"[Bottango] Setting servo angle to {value}")

# For Linux, we'll use a software-based approach since we don't have GPIO
class SoftwareServo:
    """Software-based servo implementation for Linux"""
    
    def __init__(self, pin, min_angle, max_angle, **kwargs):
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self._angle = None
        self._angle_handler = default_handler
        #self.set_angle_handler(bottango_handler)
        logger.info(f"[Linux] Created software servo (pin {pin} is virtual)")
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        self._angle = value
        self._angle_handler(value)
    
    def set_angle_handler(self, handler):
        """Set a custom handler for angle changes"""
        self._angle_handler = handler
    
    def close(self):
        logger.info(f"[Linux] Closing software servo")

class SoftwareButton:
    """Software-based button implementation for Linux"""
    
    def __init__(self, pin, pull_up=True):
        self.pin = pin
        self.pull_up = pull_up
        self._pressed = False
        logger.info(f"[Linux] Created software button (pin {pin} is virtual)")
    
    def wait_for_press(self, timeout=None):
        logger.info(f"[Linux] Waiting for button press (virtual)")
        # Simulate button press with random delay between 1-3 seconds
        import time
        import random
        delay = random.uniform(1, 3)
        time.sleep(delay)
        logger.info(f"[Linux] Button pressed (simulated)")
    
    @property
    def is_pressed(self):
        # Randomly return True sometimes to simulate button presses
        import random
        self._pressed = random.random() > 0.7
        return self._pressed
    
    def close(self):
        logger.info(f"[Linux] Closing software button")

class SoftwareOutput:
    """Software-based output implementation for Linux"""
    
    def __init__(self, pin):
        self.pin = pin
        self._state = False
        logger.info(f"[Linux] Created software output (pin {pin} is virtual)")
    
    def on(self):
        self._state = True
        logger.info(f"[Linux] Turning on output (virtual)")
    
    def off(self):
        self._state = False
        logger.info(f"[Linux] Turning off output (virtual)")
    
    def close(self):
        logger.info(f"[Linux] Closing software output")

class PlatformHardware(HardwareBase):
    """Linux specific hardware implementation"""
    
    def setup(self):
        """Initialize Linux hardware components"""
        logger.info("[Linux] Setting up hardware")
        return True
    
    def cleanup(self):
        """Clean up Linux hardware resources"""
        logger.info("[Linux] Cleaning up hardware")
    
    def create_servo(self, pin, min_angle, max_angle, min_pulse_width, max_pulse_width):
        """Create a software servo controller"""
        return SoftwareServo(pin, min_angle, max_angle)
    
    def create_button(self, pin, pull_up=True):
        """Create a software button/input device"""
        return SoftwareButton(pin, pull_up)
    
    def create_output(self, pin):
        """Create a software digital output device"""
        return SoftwareOutput(pin)
    
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
        """Get Linux system information"""
        info = {}
        
        # Get distribution info
        info["distribution"] = platform.freedesktop_os_release().get("PRETTY_NAME", "Unknown Linux")
        
        # Get CPU temperature if available
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = int(f.read().strip()) / 1000
                info["temperature"] = f"{temp}°C"
        except Exception:
            info["temperature"] = "Unknown"
        
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
