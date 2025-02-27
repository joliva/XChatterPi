#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:19:49 2020

@author: Mike McGurrin
"""
import sys
import os
import config as c
c.update()

# Check for optional wavfile argument
fullpath_wavfile = sys.argv[1] if len(sys.argv) > 1 else None
if fullpath_wavfile and not os.path.exists(fullpath_wavfile):
    print(f"Error: Audio file not found: {fullpath_wavfile}")
    sys.exit(1)

# check for invalid config (can't have SOURCE == FILES and PROP_TRIGGER == START
if c.SOURCE == "FILES" and c.PROP_TRIGGER == 'START':
    print("Invalid settings. SOURCE must be MICROPHONE if PROP_TRIGGER is START\n"
    "Please edit the configuration and try again.")
    raise SystemExit(1)

import control
# Run control loop (it will handle the wav file if provided)
control.controls(fullpath_wavfile)
