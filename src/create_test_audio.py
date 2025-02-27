#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Audio Generator for Chatter Pi

This utility creates test audio files for testing Chatter Pi.
"""

import numpy as np
import wave
import os
import argparse

def create_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """Create a sine wave with the given frequency and duration"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine_wave

def create_speech_like_audio(duration, sample_rate=44100):
    """Create audio that mimics speech patterns"""
    # Create a base carrier frequency
    carrier = create_sine_wave(200, duration, sample_rate, 0.7)
    
    # Add some harmonics
    harmonics = (
        create_sine_wave(400, duration, sample_rate, 0.3) +
        create_sine_wave(600, duration, sample_rate, 0.2) +
        create_sine_wave(800, duration, sample_rate, 0.1)
    )
    
    # Create an amplitude envelope that mimics speech
    # (periods of sound followed by brief pauses)
    envelope = np.ones(int(sample_rate * duration))
    
    # Create pauses at regular intervals
    word_duration = 0.3  # seconds
    pause_duration = 0.1  # seconds
    
    word_samples = int(word_duration * sample_rate)
    pause_samples = int(pause_duration * sample_rate)
    
    position = 0
    while position < len(envelope):
        if position + pause_samples < len(envelope):
            envelope[position:position+pause_samples] = 0.1  # not complete silence
        position += word_samples + pause_samples
    
    # Apply a smoothing filter to the envelope
    window_size = int(0.01 * sample_rate)  # 10ms
    smoothed_envelope = np.zeros_like(envelope)
    for i in range(len(envelope)):
        start = max(0, i - window_size // 2)
        end = min(len(envelope), i + window_size // 2)
        smoothed_envelope[i] = np.mean(envelope[start:end])
    
    # Apply the envelope to the combined signal
    signal = (carrier + harmonics) * smoothed_envelope
    
    # Normalize to 16-bit range
    signal = signal / np.max(np.abs(signal)) * 32767
    
    return signal.astype(np.int16)

def create_ambient_audio(duration, sample_rate=44100):
    """Create ambient background noise"""
    # Create white noise
    noise = np.random.normal(0, 0.1, int(sample_rate * duration))
    
    # Add some low frequency rumble
    rumble = create_sine_wave(30, duration, sample_rate, 0.2)
    
    # Add occasional higher pitched sounds
    high_sounds = np.zeros(int(sample_rate * duration))
    
    # Add random high-pitched sounds
    for _ in range(5):
        start = np.random.randint(0, int(sample_rate * duration) - int(sample_rate * 0.5))
        end = start + int(sample_rate * 0.5)
        freq = np.random.randint(500, 2000)
        high_sounds[start:end] = create_sine_wave(freq, 0.5, sample_rate, 0.3)
    
    # Combine signals
    signal = noise + rumble + high_sounds
    
    # Normalize to 16-bit range
    signal = signal / np.max(np.abs(signal)) * 32767 * 0.7  # make it a bit quieter than speech
    
    return signal.astype(np.int16)

def save_wav(signal, filename, sample_rate=44100):
    """Save the signal as a WAV file"""
    # Create directory if it doesn't exist
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    # Save the file
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(signal.tobytes())
    
    print(f"Created {filename} ({len(signal)/sample_rate:.1f} seconds)")

def main():
    parser = argparse.ArgumentParser(description='Create test audio files for Chatter Pi')
    parser.add_argument('--vocals', type=int, default=3, help='Number of vocal files to create')
    parser.add_argument('--ambient', type=int, default=2, help='Number of ambient files to create')
    
    args = parser.parse_args()
    
    print("Creating test audio files for Chatter Pi...")
    
    # Create vocal files
    for i in range(1, args.vocals + 1):
        # Create a speech-like audio file
        duration = np.random.uniform(3.0, 8.0)  # Random duration between 3 and 8 seconds
        signal = create_speech_like_audio(duration)
        
        # Save the file
        filename = f"vocals/v{i:02d}.wav"
        save_wav(signal, filename)
    
    # Create ambient files
    for i in range(1, args.ambient + 1):
        # Create an ambient audio file
        duration = np.random.uniform(10.0, 20.0)  # Random duration between 10 and 20 seconds
        signal = create_ambient_audio(duration)
        
        # Save the file
        filename = f"ambient/a{i:02d}.wav"
        save_wav(signal, filename)
    
    print("\nTest audio files created successfully!")
    print("\nYou can now run the audio analyzer:")
    print("  python3 analyze_audio.py --all")
    print("\nOr test with a specific file:")
    print("  python3 analyze_audio.py vocals/v01.wav")

if __name__ == "__main__":
    main()
