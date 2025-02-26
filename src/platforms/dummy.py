"""
Dummy hardware implementation for unsupported platforms.
"""

from platforms.base import HardwareBase

class DummyServo:
    """Dummy servo implementation that logs actions instead of controlling hardware"""
    
    def __init__(self, pin, min_angle, max_angle, **kwargs):
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self._angle = None
        print(f"[DUMMY] Created servo on pin {pin}")
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        self._angle = value
        print(f"[DUMMY] Setting servo angle to {value}")
    
    def close(self):
        print(f"[DUMMY] Closing servo on pin {self.pin}")

class DummyButton:
    """Dummy button implementation"""
    
    def __init__(self, pin, pull_up=True):
        self.pin = pin
        self.pull_up = pull_up
        print(f"[DUMMY] Created button on pin {pin}")
    
    def wait_for_press(self, timeout=None):
        print(f"[DUMMY] Waiting for button press on pin {self.pin}")
        # In dummy mode, simulate a button press after 2 seconds
        import time
        time.sleep(2)
        print(f"[DUMMY] Button pressed on pin {self.pin}")
    
    @property
    def is_pressed(self):
        # Randomly return True sometimes to simulate button presses
        import random
        pressed = random.random() > 0.7
        if pressed:
            print(f"[DUMMY] Button on pin {self.pin} is pressed")
        return pressed
    
    def close(self):
        print(f"[DUMMY] Closing button on pin {self.pin}")

class DummyOutput:
    """Dummy output implementation"""
    
    def __init__(self, pin):
        self.pin = pin
        self._state = False
        print(f"[DUMMY] Created output on pin {pin}")
    
    def on(self):
        self._state = True
        print(f"[DUMMY] Turning on output on pin {self.pin}")
    
    def off(self):
        self._state = False
        print(f"[DUMMY] Turning off output on pin {self.pin}")
    
    def close(self):
        print(f"[DUMMY] Closing output on pin {self.pin}")

class PlatformHardware(HardwareBase):
    """Dummy hardware implementation for unsupported platforms"""
    
    def setup(self):
        """Initialize dummy hardware components"""
        print("[DUMMY] Setting up hardware")
        return True
    
    def cleanup(self):
        """Clean up dummy hardware resources"""
        print("[DUMMY] Cleaning up hardware")
    
    def create_servo(self, pin, min_angle, max_angle, min_pulse_width, max_pulse_width):
        """Create a dummy servo controller"""
        return DummyServo(pin, min_angle, max_angle)
    
    def create_button(self, pin, pull_up=True):
        """Create a dummy button/input device"""
        return DummyButton(pin, pull_up)
    
    def create_output(self, pin):
        """Create a dummy digital output device"""
        return DummyOutput(pin)
    
    def is_service_running(self, service_name):
        """Check if a system service is running (always returns True in dummy mode)"""
        print(f"[DUMMY] Checking if service {service_name} is running")
        return True
    
    def get_system_info(self):
        """Get dummy system information"""
        return {
            "model": "Dummy Platform",
            "temperature": "25.0'C"
        }
    
    def get_audio_devices(self):
        """Get dummy audio devices"""
        return "card 0: Dummy [Dummy Audio], device 0: Dummy Output [Dummy Output]"
