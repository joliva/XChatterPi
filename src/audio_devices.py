#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Device Utility for Chatter Pi

This utility helps list and test audio input/output devices.
"""

import pyaudio
import wave
import numpy as np
import time
import argparse
import os
import matplotlib.pyplot as plt
from platforms import get_platform

def list_devices():
    """List all available audio devices"""
    p = pyaudio.PyAudio()
    
    print("\nAudio Device Information:")
    print("========================\n")
    
    # Get host API info
    print("Host APIs:")
    for i in range(p.get_host_api_count()):
        info = p.get_host_api_info_by_index(i)
        print(f"  {i}: {info['name']}")
    
    print("\nInput Devices:")
    input_devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            input_devices.append(i)
            print(f"  {i}: {info['name']}")
            print(f"     Input Channels: {info['maxInputChannels']}")
            print(f"     Default Sample Rate: {info['defaultSampleRate']} Hz")
    
    print("\nOutput Devices:")
    output_devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxOutputChannels'] > 0:
            output_devices.append(i)
            print(f"  {i}: {info['name']}")
            print(f"     Output Channels: {info['maxOutputChannels']}")
            print(f"     Default Sample Rate: {info['defaultSampleRate']} Hz")
    
    # Get default devices
    print("\nDefault Devices:")
    try:
        default_input = p.get_default_input_device_info()
        print(f"  Default Input: {default_input['index']} - {default_input['name']}")
    except IOError:
        print("  No default input device found")
    
    try:
        default_output = p.get_default_output_device_info()
        print(f"  Default Output: {default_output['index']} - {default_output['name']}")
    except IOError:
        print("  No default output device found")
    
    p.terminate()
    
    return input_devices, output_devices

def record_and_play(input_device=None, output_device=None, duration=5, sample_rate=44100, visualize=False):
    """Record from input device and play back on output device"""
    p = pyaudio.PyAudio()
    
    # Use default devices if not specified
    if input_device is None:
        try:
            input_device = p.get_default_input_device_info()['index']
        except IOError:
            print("No default input device available")
            p.terminate()
            return
    
    if output_device is None:
        try:
            output_device = p.get_default_output_device_info()['index']
        except IOError:
            print("No default output device available")
            p.terminate()
            return
    
    # Get device info
    try:
        input_info = p.get_device_info_by_index(input_device)
        output_info = p.get_device_info_by_index(output_device)
    except ValueError:
        print(f"Invalid device index")
        p.terminate()
        return
    
    # Use device's preferred sample rate if available
    if sample_rate is None:
        sample_rate = int(input_info['defaultSampleRate'])
    
    print(f"\nRecording from: {input_info['name']} (Device {input_device})")
    print(f"Playing back on: {output_info['name']} (Device {output_device})")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Duration: {duration} seconds")
    print("Recording will start in 3 seconds...")
    
    time.sleep(3)
    print("Recording... (speak into your microphone)")
    
    # Set up recording stream
    frames = []
    
    def callback(in_data, frame_count, time_info, status):
        frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    input_device_index=input_device,
                    output_device_index=output_device,
                    frames_per_buffer=1024,
                    stream_callback=callback)
    
    stream.start_stream()
    
    # Record for specified duration
    time.sleep(duration)
    
    stream.stop_stream()
    stream.close()
    
    print("Recording finished")
    
    # Save recording to file
    filename = "test_recording.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    p.terminate()
    
    print(f"Recording saved to {filename}")
    
    # Visualize the recording if requested
    if visualize:
        visualize_audio(filename)
    
    return filename

def visualize_audio(filename):
    """Visualize the recorded audio"""
    wf = wave.open(filename, 'rb')
    sample_rate = wf.getframerate()
    n_frames = wf.getnframes()
    data = wf.readframes(n_frames)
    wf.close()
    
    # Convert to numpy array
    samples = np.frombuffer(data, dtype=np.int16)
    duration = n_frames / sample_rate
    time_axis = np.linspace(0, duration, num=len(samples))
    
    # Calculate volume envelope
    window_size = int(sample_rate * 0.05)  # 50ms window
    if window_size > 0:
        abs_samples = np.abs(samples)
        envelope = np.zeros(len(abs_samples) - window_size + 1)
        for i in range(len(envelope)):
            envelope[i] = np.mean(abs_samples[i:i+window_size])
        envelope_time = np.linspace(0, duration, num=len(envelope))
    
    # Plot waveform and envelope
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, samples)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(envelope_time, envelope)
    plt.title('Volume Envelope')
    plt.xlabel('Time (s)')
    plt.ylabel('Volume')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("test_recording_analysis.png")
    print("Audio visualization saved to test_recording_analysis.png")
    plt.show()

def test_input_sensitivity(input_device=None, duration=10, sample_rate=44100):
    """Test input sensitivity and recommend threshold settings"""
    p = pyaudio.PyAudio()
    
    # Use default input device if not specified
    if input_device is None:
        try:
            input_device = p.get_default_input_device_info()['index']
        except IOError:
            print("No default input device available")
            p.terminate()
            return
    
    # Get device info
    try:
        input_info = p.get_device_info_by_index(input_device)
    except ValueError:
        print(f"Invalid device index")
        p.terminate()
        return
    
    # Use device's preferred sample rate if available
    if sample_rate is None:
        sample_rate = int(input_info['defaultSampleRate'])
    
    print(f"\nTesting input sensitivity on: {input_info['name']} (Device {input_device})")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Duration: {duration} seconds")
    print("Test will start in 3 seconds...")
    print("Please speak at normal volume during the test")
    
    time.sleep(3)
    print("Testing... (speak into your microphone)")
    
    # Set up recording stream
    volume_levels = []
    
    def callback(in_data, frame_count, time_info, status):
        # Calculate volume level
        samples = np.frombuffer(in_data, dtype=np.int16)
        volume = np.mean(np.abs(samples))
        volume_levels.append(volume)
        return (None, pyaudio.paContinue)
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    input_device_index=input_device,
                    frames_per_buffer=1024,
                    stream_callback=callback)
    
    stream.start_stream()
    
    # Record for specified duration
    for i in range(duration):
        time.sleep(1)
        current_volume = volume_levels[-1] if volume_levels else 0
        print(f"Current volume level: {current_volume:.0f}", end="\r")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print("\nTest finished")
    
    # Calculate statistics
    if volume_levels:
        max_volume = max(volume_levels)
        avg_volume = sum(volume_levels) / len(volume_levels)
        p25 = np.percentile(volume_levels, 25)
        p50 = np.percentile(volume_levels, 50)
        p75 = np.percentile(volume_levels, 75)
        p90 = np.percentile(volume_levels, 90)
        
        print("\nResults:")
        print(f"Maximum volume: {max_volume:.0f}")
        print(f"Average volume: {avg_volume:.0f}")
        
        print("\nRecommended threshold settings:")
        print("For STYLE=0 (Threshold):")
        print(f"THRESHOLD: {int(p50)}")
        print("\nFor STYLE=1 (Multi-level):")
        print(f"LEVEL1: {int(p25)}")
        print(f"LEVEL2: {int(p75)}")
        print(f"LEVEL3: {int(p90)}")
        
        # Plot volume levels
        plt.figure(figsize=(10, 6))
        plt.plot(volume_levels)
        plt.axhline(y=p25, color='g', linestyle='--', label=f'25% ({int(p25)})')
        plt.axhline(y=p50, color='y', linestyle='--', label=f'50% ({int(p50)})')
        plt.axhline(y=p75, color='orange', linestyle='--', label=f'75% ({int(p75)})')
        plt.axhline(y=p90, color='r', linestyle='--', label=f'90% ({int(p90)})')
        plt.title('Input Volume Levels')
        plt.xlabel('Time (frames)')
        plt.ylabel('Volume')
        plt.legend()
        plt.grid(True)
        plt.savefig("input_sensitivity_test.png")
        print("\nVolume level graph saved to input_sensitivity_test.png")
        plt.show()
    else:
        print("No volume data recorded")

def main():
    parser = argparse.ArgumentParser(description='Audio Device Utility for Chatter Pi')
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # List devices command
    subparsers.add_parser('list', help='List all audio devices')
    
    # Test devices command
    test_parser = subparsers.add_parser('test', help='Test audio input/output')
    test_parser.add_argument('--input', type=int, help='Input device index')
    test_parser.add_argument('--output', type=int, help='Output device index')
    test_parser.add_argument('--duration', type=int, default=5, help='Recording duration in seconds')
    test_parser.add_argument('--rate', type=int, help='Sample rate')
    test_parser.add_argument('--visualize', action='store_true', help='Visualize the recording')
    
    # Sensitivity test command
    sensitivity_parser = subparsers.add_parser('sensitivity', help='Test input sensitivity')
    sensitivity_parser.add_argument('--input', type=int, help='Input device index')
    sensitivity_parser.add_argument('--duration', type=int, default=10, help='Test duration in seconds')
    sensitivity_parser.add_argument('--rate', type=int, help='Sample rate')
    
    args = parser.parse_args()
    
    print(f"Platform: {get_platform()}")
    
    if args.command == 'list':
        list_devices()
    elif args.command == 'test':
        record_and_play(
            input_device=args.input,
            output_device=args.output,
            duration=args.duration,
            sample_rate=args.rate,
            visualize=args.visualize
        )
    elif args.command == 'sensitivity':
        test_input_sensitivity(
            input_device=args.input,
            duration=args.duration,
            sample_rate=args.rate
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
