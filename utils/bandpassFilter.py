#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:19:49 2020

@author: Mike McGurrin
"""

from scipy.signal import butter, lfilter

class BPFilter: 
    def __init__(self):
        fs = 44100.0
        lowcut = 500.0
        highcut = 2500.0
        order = 6 
    
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        self.b, self.a = butter(order, [low, high], btype='band')
        
    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y
    
    def filter_data(self, data):
        y = lfilter(self.b, self.a, data)
        return y
