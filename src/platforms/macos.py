"""
macOS specific hardware implementation.
"""

import subprocess
import platform
import logging
from platforms.base import HardwareBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def default_handler(value): 
    logger.info(f"[macOS] Setting servo angle to {value}")

def bottango_handler(value): 
    logger.info(f"[Bottango] Setting servo angle to {value}")

# For macOS, we'll use a software-based approach since we don't have GPIO
class SoftwareServo:
    """Software-based servo implementation for macOS"""
    
    def __init__(self, pin, min_angle, max_angle, **kwargs):
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self._angle = None
        self._angle_handler = default_handler
        #self.set_angle_handler(bottango_handler)
        logger.info(f"[macOS] Created software servo (pin {pin} is virtual)")
    
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
        logger.info(f"[macOS] Closing software servo")

class SoftwareButton:
    """Software-based button implementation for macOS"""
    
    def __init__(self, pin, pull_up=True):
        self.pin = pin
        self.pull_up = pull_up
        self._pressed = False
        logger.info(f"[macOS] Created software button (pin {pin} is virtual)")
    
    def wait_for_press(self, timeout=None):
        logger.info(f"[macOS] Waiting for button press (virtual)")
        # Simulate button press with random delay between 1-3 seconds
        import time
        import random
        delay = random.uniform(1, 3)
        time.sleep(delay)
        logger.info(f"[macOS] Button pressed (simulated)")
    
    @property
    def is_pressed(self):
        # Randomly return True sometimes to simulate button presses
        import random
        self._pressed = random.random() > 0.7
        return self._pressed
    
    def close(self):
        logger.info(f"[macOS] Closing software button")

class SoftwareOutput:
    """Software-based output implementation for macOS"""
    
    def __init__(self, pin):
        self.pin = pin
        self._state = False
        logger.info(f"[macOS] Created software output (pin {pin} is virtual)")
    
    def on(self):
        self._state = True
        logger.info(f"[macOS] Turning on output (virtual)")
    
    def off(self):
        self._state = False
        logger.info(f"[macOS] Turning off output (virtual)")
    
    def close(self):
        logger.info(f"[macOS] Closing software output")

class PlatformHardware(HardwareBase):
    """macOS specific hardware implementation"""
    
    def setup(self):
        """Initialize macOS hardware components"""
        logger.info("[macOS] Setting up hardware")
        return True
    
    def cleanup(self):
        """Clean up macOS hardware resources"""
        logger.info("[macOS] Cleaning up hardware")
    
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
        """Check if a system service is running (macOS uses launchd)"""
        try:
            result = subprocess.run(
                ["launchctl", "list", service_name],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_system_info(self):
        """Get macOS system information"""
        info = {}
        
        # Get macOS version
        info["version"] = platform.mac_ver()
        
        # Get model
        try:
            result = subprocess.run(
                ["sysctl", "-n", "hw.model"],
                capture_output=True,
                text=True,
                check=False
            )
            info["model"] = result.stdout.strip()
        except Exception:
            info["model"] = "Unknown Mac"
        
        # Get temperature if possible (requires third-party tools)
        info["temperature"] = "Temperature monitoring requires additional tools on macOS"
        
        return info
    
    def get_audio_devices(self):
        """Get available audio devices"""
        try:
            result = subprocess.run(
                ["system_profiler", "SPAudioDataType"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout.strip()
        except Exception:
            return "No audio devices detected"
