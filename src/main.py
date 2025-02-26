#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:19:49 2020

@author: Mike McGurrin
"""
import os
import config as c
c.update()

# Check if running in simulation mode
if os.environ.get('CHATTERPI_SIMULATION') == '1':
    print("Running in simulation mode - hardware actions will be simulated")

# check for invalid config (can't have SOURCE == FILES and PROP_TRIGGER == START
if c.SOURCE == "FILES" and c.PROP_TRIGGER == 'START':
    print("Invalid settings. SOURCE must be MICROPHONE if PROP_TRIGGER is START\n"
    "Please edit the configuration and try again.")
    raise SystemExit(1)

import control
# run control, which handles the triggers and event handling
control.controls()
    
    
        


    
        
