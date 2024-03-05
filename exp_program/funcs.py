import numpy as np
import pandas as pd
from psychopy import core, visual, gui, data, event
from settings import *
import serial
import time


def get_sets(id, set_number, test):

    filename = 'rspm_info.csv'
    df = pd.read_csv(filename)
    if test == 0:
        id_column = "id" + str(id)
        filtered_df = df[df[id_column] == set_number]
        sets = filtered_df.iloc[:,[0,1]]
    else:
        sets = df.iloc[-3:,[0,1]]
    return_sets = sets.to_numpy()

    return return_sets


def one_question(mywin, index, options):
    answer = 2
    reaction_time = 11.34
    return answer, reaction_time

def start(mywin, expInfo):
    # display instructions and wait
    message1 = visual.TextStim(mywin, pos=[0,+100],
        text="Hello, " + expInfo['Name'] + "!\n Welcome to the experiment.")
    message2 = visual.TextStim(mywin, pos=[0,-100],
                               text='Please hit the space to start.')
    message1.size = [None, 35]
    message2.setSize(text_size)
    message1.draw()
    message2.draw()
    mywin.flip()
    event.waitKeys(keyList=['space'])


def finish(mywin, expInfo):
    # display end message and quit
    message1 = visual.TextStim(mywin, pos=[0,0],
        text="Thank you for participating, " + expInfo['Name'] + "!")
    message1.setSize(text_size)
    message1.draw()
    mywin.flip()
    core.wait(2)
