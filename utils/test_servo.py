#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servo Test Utility for Chatter Pi

This utility helps test and calibrate the servo for jaw movement.
"""

import time
import argparse
import os
import sys
import importlib.util
import configparser

# Add the src directory to the path to find the config and platforms modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/src")

import src.config as c
from src.platforms import hardware

def test_servo(mode="sweep", speed=1.0, min_angle=None, max_angle=None, servo_min=None, servo_max=None, pin=None):
    """Test the servo with different patterns"""
    # Check if config.ini exists, if not create it from default
    config_path = '../src/config.ini'
    default_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src/config.ini.default')
    
    if not os.path.exists(config_path) and os.path.exists(default_config_path):
        print(f"config.ini not found, creating from default template")
        import shutil
        shutil.copy2(default_config_path, config_path)
    
    # Load config
    try:
        c.update()
    except (KeyError, configparser.DuplicateSectionError) as e:
        print(f"Error loading config.ini: {e}")
        print("Using default values")
        # Set default values
        c.SERVO_MIN = 1050
        c.SERVO_MAX = 1250
        c.MIN_ANGLE = 0
        c.MAX_ANGLE = 90
        c.JAW_PIN = 18
    
    # Override config with command line arguments if provided
    if min_angle is not None:
        c.MIN_ANGLE = min_angle
    if max_angle is not None:
        c.MAX_ANGLE = max_angle
    if servo_min is not None:
        c.SERVO_MIN = servo_min
    if servo_max is not None:
        c.SERVO_MAX = servo_max
    if pin is not None:
        c.JAW_PIN = pin
    
    print(f"Testing servo on pin {c.JAW_PIN}")
    print(f"Servo settings: MIN_ANGLE={c.MIN_ANGLE}, MAX_ANGLE={c.MAX_ANGLE}")
    print(f"Pulse width: SERVO_MIN={c.SERVO_MIN}, SERVO_MAX={c.SERVO_MAX}")
    
    # Initialize hardware
    hardware.setup()
    
    # Create servo object
    jaw = hardware.create_servo(
        c.JAW_PIN, 
        min_angle=c.MIN_ANGLE, 
        max_angle=c.MAX_ANGLE, 
        min_pulse_width=c.SERVO_MIN/(1*10**6),
        max_pulse_width=c.SERVO_MAX/(1*10**6)
    )
    
    try:
        if mode == "sweep":
            print("Running sweep test (Ctrl+C to stop)")
            while True:
                # Determine sweep direction based on angle settings
                if c.MIN_ANGLE < c.MAX_ANGLE:
                    start_angle, end_angle, step = c.MIN_ANGLE, c.MAX_ANGLE, 1
                else:
                    start_angle, end_angle, step = c.MIN_ANGLE, c.MAX_ANGLE, -1
                
                # Sweep from min to max
                for angle in range(start_angle, end_angle + step, step):
                    jaw.angle = angle
                    time.sleep(0.01 / speed)
                
                # Sweep from max to min
                for angle in range(end_angle, start_angle - step, -step):
                    jaw.angle = angle
                    time.sleep(0.01 / speed)
        
        elif mode == "steps":
            print("Running step test (Ctrl+C to stop)")
            while True:
                # Calculate step positions (closed, 1/3 open, 2/3 open, fully open)
                if c.MIN_ANGLE < c.MAX_ANGLE:
                    step_size = (c.MAX_ANGLE - c.MIN_ANGLE) / 3
                    positions = [
                        c.MIN_ANGLE,
                        c.MIN_ANGLE + step_size,
                        c.MIN_ANGLE + 2 * step_size,
                        c.MAX_ANGLE
                    ]
                else:
                    step_size = (c.MIN_ANGLE - c.MAX_ANGLE) / 3
                    positions = [
                        c.MIN_ANGLE,
                        c.MIN_ANGLE - step_size,
                        c.MIN_ANGLE - 2 * step_size,
                        c.MAX_ANGLE
                    ]
                
                # Move through positions
                for pos in positions:
                    jaw.angle = pos
                    print(f"Position: {pos}")
                    time.sleep(0.5 / speed)
                
                # And back down
                for pos in reversed(positions[:-1]):
                    jaw.angle = pos
                    print(f"Position: {pos}")
                    time.sleep(0.5 / speed)
        
        elif mode == "random":
            import random
            print("Running random movement test (Ctrl+C to stop)")
            while True:
                # Random position
                if c.MIN_ANGLE < c.MAX_ANGLE:
                    angle = random.uniform(c.MIN_ANGLE, c.MAX_ANGLE)
                else:
                    angle = random.uniform(c.MAX_ANGLE, c.MIN_ANGLE)
                jaw.angle = angle
                print(f"Position: {angle:.1f}")
                time.sleep(random.uniform(0.1, 0.3) / speed)
        
        elif mode == "position":
            # Test specific positions
            print("Testing min and max positions")
            print(f"MIN_ANGLE: {c.MIN_ANGLE}")
            jaw.angle = c.MIN_ANGLE
            time.sleep(2)
            
            print(f"MAX_ANGLE: {c.MAX_ANGLE}")
            jaw.angle = c.MAX_ANGLE
            time.sleep(2)
            
            print("Returning to rest position")
            jaw.angle = None
    
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    finally:
        # Clean up
        print("Cleaning up...")
        jaw.angle = None
        jaw.close()

def main():
    parser = argparse.ArgumentParser(description='Test servo for Chatter Pi')
    parser.add_argument('--mode', choices=['sweep', 'steps', 'random', 'position'], 
                        default='sweep', help='Test mode')
    parser.add_argument('--speed', type=float, default=1.0,
                        help='Movement speed multiplier')
    parser.add_argument('--min-angle', type=int, help='Override MIN_ANGLE')
    parser.add_argument('--max-angle', type=int, help='Override MAX_ANGLE')
    parser.add_argument('--servo-min', type=int, help='Override SERVO_MIN')
    parser.add_argument('--servo-max', type=int, help='Override SERVO_MAX')
    parser.add_argument('--pin', type=int, help='Override JAW_PIN')
    
    args = parser.parse_args()
    
    test_servo(
        mode=args.mode,
        speed=args.speed,
        min_angle=args.min_angle,
        max_angle=args.max_angle,
        servo_min=args.servo_min,
        servo_max=args.servo_max,
        pin=args.pin
    )

if __name__ == "__main__":
    main()
