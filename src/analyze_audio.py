#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Analysis Tool for Chatter Pi

This utility analyzes audio files to help with configuring
threshold levels for jaw movement.
"""

import wave
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from bandpassFilter import BPFilter

def analyze_audio(filename, filtered=False):
    """Analyze an audio file and display statistics and visualization"""
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found")
        return
    
    try:
        # Open the wave file
        wf = wave.open(filename, 'rb')
        
        # Get basic info
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        n_frames = wf.getnframes()
        duration = n_frames / frame_rate
        
        # Read all frames
        frames = wf.readframes(n_frames)
        wf.close()
        
        # Convert to numpy array
        samples = np.frombuffer(frames, dtype=np.int16)
        
        # If stereo, use right channel for analysis (same as in audio.py)
        if channels == 2:
            samples = samples[1::2]
        
        # Apply bandpass filter if requested
        if filtered:
            bp = BPFilter()
            samples = bp.filter_data(samples)
        
        # Calculate statistics
        abs_samples = np.abs(samples)
        max_volume = np.max(abs_samples)
        avg_volume = np.mean(abs_samples)
        
        # Calculate percentiles for threshold recommendations
        p25 = np.percentile(abs_samples, 25)
        p50 = np.percentile(abs_samples, 50)
        p75 = np.percentile(abs_samples, 75)
        p90 = np.percentile(abs_samples, 90)
        
        # Print analysis
        print(f"\nAudio Analysis for: {filename}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Channels: {channels}")
        print(f"Sample Rate: {frame_rate} Hz")
        print(f"Sample Width: {sample_width * 8} bits")
        print(f"\nVolume Statistics:")
        print(f"Maximum Volume: {max_volume}")
        print(f"Average Volume: {avg_volume:.2f}")
        print(f"\nRecommended Threshold Levels:")
        
        if filtered:
            print("For STYLE=2 (Filtered Multi-level):")
            print(f"FILTERED_LEVEL1: {int(p25)}")
            print(f"FILTERED_LEVEL2: {int(p75)}")
            print(f"FILTERED_LEVEL3: {int(p90)}")
        else:
            print("For STYLE=0 (Threshold):")
            print(f"THRESHOLD: {int(p50)}")
            print("\nFor STYLE=1 (Multi-level):")
            print(f"LEVEL1: {int(p25)}")
            print(f"LEVEL2: {int(p75)}")
            print(f"LEVEL3: {int(p90)}")
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Plot waveform
        plt.subplot(2, 1, 1)
        plt.plot(np.arange(len(samples)) / frame_rate, samples)
        plt.title('Waveform')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        # Plot volume envelope
        plt.subplot(2, 1, 2)
        
        # Calculate envelope (using rolling window)
        window_size = int(frame_rate * 0.05)  # 50ms window
        if window_size > 0:
            envelope = np.zeros(len(abs_samples) - window_size + 1)
            for i in range(len(envelope)):
                envelope[i] = np.mean(abs_samples[i:i+window_size])
            
            plt.plot(np.arange(len(envelope)) / frame_rate, envelope)
            
            # Add threshold lines
            plt.axhline(y=p25, color='g', linestyle='--', label=f'25% ({int(p25)})')
            plt.axhline(y=p50, color='y', linestyle='--', label=f'50% ({int(p50)})')
            plt.axhline(y=p75, color='orange', linestyle='--', label=f'75% ({int(p75)})')
            plt.axhline(y=p90, color='r', linestyle='--', label=f'90% ({int(p90)})')
            
            plt.title('Volume Envelope')
            plt.xlabel('Time (s)')
            plt.ylabel('Volume')
            plt.legend()
            plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(f"{os.path.splitext(filename)[0]}_analysis.png")
        print(f"\nAnalysis image saved as: {os.path.splitext(filename)[0]}_analysis.png")
        plt.show()
        
    except Exception as e:
        print(f"Error analyzing file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Analyze audio files for Chatter Pi')
    parser.add_argument('filename', help='Audio file to analyze')
    parser.add_argument('-f', '--filtered', action='store_true', 
                        help='Apply bandpass filter before analysis')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Analyze all audio files in vocals and ambient directories')
    
    args = parser.parse_args()
    
    if args.all:
        # Analyze all audio files in vocals and ambient directories
        for directory in ['vocals', 'ambient']:
            if os.path.exists(directory):
                print(f"\nAnalyzing files in {directory} directory:")
                for file in os.listdir(directory):
                    if file.endswith('.wav'):
                        filepath = os.path.join(directory, file)
                        analyze_audio(filepath, args.filtered)
    else:
        # Analyze single file
        analyze_audio(args.filename, args.filtered)

if __name__ == "__main__":
    main()
