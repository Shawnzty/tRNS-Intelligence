from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
import os
from settings import *
from funcs import *
import serial
import time


def rs_start(mywin):
    # display instructions and wait
    message1 = visual.TextStim(mywin, pos=[0,0], wrapWidth=1000,
        text="Please hit the space to start resting state.")
    message1.setSize(text_size)
    message1.draw()
    mywin.flip()
    event.waitKeys(keyList=['space'])
    return True


def rs_count_down(mywin):
    numbers = ["5", "4", "3", "2", "1"]
    for i in numbers:
        number = visual.TextStim(mywin, pos=[0,0], wrapWidth=1000, text=i)
        number.setSize(200)
        number.draw()
        mywin.flip()
        core.wait(1)
    return True


def rs_finish(mywin):
    message1 = visual.TextStim(mywin, pos=[0,0], wrapWidth=1000,
        text="Resting state finished.")
    message1.setSize(text_size)
    message1.draw()
    mywin.flip()
    core.wait(3)
    return True


def resting_state(mywin, trigger):
    fixation = visual.ShapeStim(mywin, pos=[0,0], vertices=((0, -50), (0, 50), (0,0), (-50,0), (50, 0)),
                            lineWidth=15, closeShape=False, lineColor='white')
    fixation.draw()
    trigger.write(b'H')
    mywin.flip()
    core.wait(rs_time)
    trigger.write(b'L')
    return True


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
resting_state(mywin, trigger)
rs_finish(mywin)
