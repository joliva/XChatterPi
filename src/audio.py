# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:19:49 2020
@author: Mike McGurrin
Updated to improve speed and run on Pi Zero 7/13/2020
"""
import pyaudio
import wave
import time
import atexit
import numpy as np
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, AngularServo
from bandpassFilter import BPFilter
import config as c

Device.pin_factory = PiGPIOFactory()

class AUDIO:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.jaw = AngularServo(c.JAW_PIN, min_angle=c.MIN_ANGLE, 
                    max_angle=c.MAX_ANGLE, initial_angle=None, 
                    min_pulse_width=c.SERVO_MIN/(1*10**6),
                    max_pulse_width=c.SERVO_MAX/(1*10**6))
        self.bp = BPFilter()
        
    def stop(self):
        self.streamAlias.stop_stream()  
        self.jaw.close()
    
    def play_audio(self, filename=None):
        # Used for both threshold (Scary Terry style) and multi-level (jawduino style)
        def get_avg(data, channels):
            """Gets and returns the average volume for the frame (chunk).
            for stereo channels, only looks at the right channel (channel 1)"""
            levels = abs(np.frombuffer(data, dtype='<i2'))
            # Apply bandpass filter if STYLE=2
            if c.STYLE == 2:
                levels = self.bp.filter_data(levels)
            levels = np.absolute(levels)
            if channels == 1:
                avg_volume = sum(levels)//len(levels)
            elif channels == 2:
                rightLevels = levels[1::2]
                avg_volume = sum(rightLevels)//len(rightLevels)
            return(avg_volume)
            
        def get_target(data, channels):
            volume = get_avg(data, channels)
            jawStep = (self.jaw.max_angle - self.jaw.min_angle) / 3
            if c.STYLE == 0:      # Scary Terry style single threshold
                if volume > c.THRESHOLD: 
                    jawTarget = self.jaw.min_angle
                else: 
                    jawTarget = self.jaw.max_angle
            elif c.STYLE == 1:     # Jawduino style multi-level or Wee Talker bandpss multi-level   
                if volume > c.LEVEL3:
                    jawTarget = self.jaw.min_angle
                elif volume > c.LEVEL2:
                    jawTarget = self.jaw.min_angle + jawStep
                elif volume > c.LEVEL1:
                    jawTarget = self.jaw.min_angle + 2 * jawStep
                else:
                    jawTarget = self.jaw.max_angle
            else:     # Jawduino style multi-level or Wee Talker bandpss multi-level   
                if volume > c.FIlTERED_LEVEL3:
                    jawTarget = self.jaw.min_angle
                elif volume > c.FIlTERED_LEVEL2:
                    jawTarget = self.jaw.min_angle + jawStep
                elif volume > c.FIlTERED_LEVEL1:
                    jawTarget = self.jaw.min_angle + 2 * jawStep
                else:
                    jawTarget = self.jaw.max_angle   
            return jawTarget      
        
        def overwrite(data, channels):
            """ overwrites left channel onto right channel for playback"""
            if channels != 2:
                raise ValueError("channels must equal 2")
            levels = np.frombuffer(data, dtype='<i2')
            levels[1::2] = levels[::2]
            data = levels.tolist()
            return data
        
        def filesCallback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            channels = wf.getnchannels()
            jawTarget = get_target(data, channels)
            self.jaw.angle = jawTarget
            # If only want left channel of input, duplicate left channel on right
            if (channels == 2) and (c.OUTPUT_CHANNELS == 'LEFT'):
                data = overwrite(data, channels)
            return (data, pyaudio.paContinue)  
        
        def micCallback(in_data, frame_count, time_info, status):
            channels = 1 # Microphone input is always monaural
            jawTarget = get_target(in_data, channels)
            self.jaw.angle = jawTarget
            # If only want left channel of input, duplicate left channel on right
            if (channels == 2) and (c.OUTPUT_CHANNELS == 'LEFT'):
                in_data = overwrite(in_data, channels)
            return (in_data, pyaudio.paContinue)          
        
        def normalEnd():
            self.streamAlias.stop_stream()
            self.streamAlias.close()
            if c.SOURCE == 'FILES':
                wf.close()
            self.jaw.angle = None  
            
        def cleanup():
            normalEnd()
            self.p.terminate()
            self.jaw.close()
            
        try:
            atexit.register(cleanup)           
            # open stream using callback
            #Playing from wave file
            if c.SOURCE == 'FILES':
                wf = wave.open(filename, 'rb')
                file_sw = wf.getsampwidth()                    
                stream = self.p.open(format=self.p.get_format_from_width(file_sw),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True,
                            stream_callback=filesCallback)  
                self.streamAlias = stream
                while stream.is_active():
                    time.sleep(0.1)
            # Playing from microphone
            elif c.SOURCE == 'MICROPHONE':
                stream = self.p.open(format=pyaudio.paInt16, channels=1,
                            rate=48000, frames_per_buffer=1024,
                            input=True, output=True,
                            stream_callback=micCallback)  
                self.streamAlias = stream
                if c.PROP_TRIGGER != 'START':
                    time.sleep(c.MIC_TIME)
                    stream.close()   
                else:
                    while stream.is_active():
                        time.sleep(1.)
            normalEnd()            
        except (KeyboardInterrupt, SystemExit):
            cleanup()

            
