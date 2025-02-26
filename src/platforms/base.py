"""
Base class for platform-specific hardware implementations.
"""

from abc import ABC, abstractmethod

class HardwareBase(ABC):
    """Abstract base class for platform-specific hardware implementations"""
    
    @abstractmethod
    def setup(self):
        """Initialize hardware components"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """Clean up hardware resources"""
        pass
    
    @abstractmethod
    def create_servo(self, pin, min_angle, max_angle, min_pulse_width, max_pulse_width):
        """Create a servo controller"""
        pass
    
    @abstractmethod
    def create_button(self, pin, pull_up=True):
        """Create a button/input device"""
        pass
    
    @abstractmethod
    def create_output(self, pin):
        """Create a digital output device"""
        pass
    
    @abstractmethod
    def is_service_running(self, service_name):
        """Check if a system service is running"""
        pass
    
    @abstractmethod
    def get_system_info(self):
        """Get system information (temperature, etc.)"""
        pass
    
    @abstractmethod
    def get_audio_devices(self):
        """Get available audio devices"""
        pass
