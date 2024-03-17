from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
import os
from settings import *
from funcs import *
import serial
import time

# create a window
mywin = visual.Window([screen_width, screen_height], 
                      fullscr=True, screen=2, monitor="testMonitor", 
                      color=[-1,-1,-1], units="pix")
print("Window created.")


refresh_rate = mywin.getActualFrameRate()
print("Refresh rate: %.2f", refresh_rate)

trigger = serial.Serial('COM17', 9600) # lab 11, office 3
print("Serial port for Arduino opened.")

rs_start(mywin)
rs_count_down(mywin)
resting_state(mywin, trigger, rs_time)
rs_finish(mywin)
