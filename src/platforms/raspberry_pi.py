"""
Raspberry Pi specific hardware implementation with simulation support.
"""

import subprocess
import time
import config as c
import logging
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, AngularServo, Button, DigitalOutputDevice
from platforms.base import HardwareBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def default_handler(value): 
    logger.info(f"[Raspberry Pi] Setting servo angle to {value}")

def bottango_handler(value): 
    logger.info(f"[Bottango] Setting servo angle to {value}")

class SoftwareServo:
    """Software-based servo implementation for Raspberry Pi simulation"""
    
    def __init__(self):
        self._angle = None
        self._angle_setter = self._default_angle_setter
        logger.info(f"[Raspberry Pi] Created simulated servo")
        
    @property
    def angle(self):
        return self._angle
        
    @angle.setter
    def angle(self, value):
        self._angle_setter(value)
            
    def _default_angle_setter(self, value):
        self._angle = value
        if value is not None:
            logger.info(f"[Raspberry Pi] Servo moved to angle: {value}")
            
    def set_angle_handler(self, handler):
        """Set a custom handler for angle changes"""
        self._angle_setter = handler
            
    def close(self):
        logger.info(f"[Raspberry Pi] Closing simulated servo")

class SoftwareButton:
    """Software-based button implementation for Raspberry Pi simulation"""
    
    def __init__(self):
        self._pressed = False
        logger.info(f"[Raspberry Pi] Created simulated button")
        
    def wait_for_press(self, timeout=None):
        logger.info(f"[Raspberry Pi] Waiting for simulated button press...")
        # Simulate button press with random delay between 1-3 seconds
        import random
        delay = random.uniform(1, 3)
        time.sleep(delay)
        logger.info(f"[Raspberry Pi] Button pressed (simulated)")
    
    @property
    def is_pressed(self):
        # Toggle state each time to simulate button presses
        self._pressed = not self._pressed
        return self._pressed
        
    def close(self):
        logger.info(f"[Raspberry Pi] Closing simulated button")

class SoftwareOutput:
    """Software-based output implementation for Raspberry Pi simulation"""
    
    def __init__(self):
        self._state = False
        logger.info(f"[Raspberry Pi] Created simulated output")
        
    def on(self):
        self._state = True
        logger.info(f"[Raspberry Pi] Output turned ON")
        
    def off(self):
        self._state = False
        logger.info(f"[Raspberry Pi] Output turned OFF")
        
    def close(self):
        logger.info(f"[Raspberry Pi] Closing simulated output")

class PlatformHardware(HardwareBase):
    """Raspberry Pi specific hardware implementation"""
    
    def __init__(self):
        """Initialize Raspberry Pi hardware"""
        self.pin_factory = None
        self.simulation_mode = c.RPI_HW_SIMULATION
        
    def setup(self):
        """Initialize hardware components"""
        if not self.simulation_mode:
            try:
                self.pin_factory = PiGPIOFactory()
                Device.pin_factory = self.pin_factory
            except Exception as e:
                logger.warning(f"Failed to initialize Pi hardware ({e}), falling back to simulation mode")
                self.simulation_mode = True
        if self.simulation_mode:
            logger.info(f"[Raspberry Pi] Running in simulation mode")
        return True
    
    def cleanup(self):
        """Clean up hardware resources"""
        # gpiozero handles cleanup automatically
        pass
    
    def create_servo(self, pin, min_angle, max_angle, min_pulse_width, max_pulse_width):
        """Create a servo controller using gpiozero or software implementation"""
        if self.simulation_mode:
            return SoftwareServo()
        return AngularServo(
            pin, 
            min_angle=min_angle, 
            max_angle=max_angle, 
            initial_angle=None, 
            min_pulse_width=min_pulse_width,
            max_pulse_width=max_pulse_width
        )
    
    def create_button(self, pin, pull_up=True):
        """Create a button/input device using gpiozero or software implementation"""
        if self.simulation_mode:
            return SoftwareButton()
        return Button(pin, pull_up=pull_up)
    
    def create_output(self, pin):
        """Create a digital output device using gpiozero or software implementation"""
        if self.simulation_mode:
            return SoftwareOutput()
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
