import numpy as np
import pandas as pd
from psychopy import core, visual, gui, data, event
from settings import *
from PIL import Image
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
    image_path = 'rspm/' + index + '.png'
    image_pil = Image.open(image_path)
    width, height = image_pil.size

    image_stim = visual.ImageStim(mywin, image=image_path, pos=(0,0))

    ratio = 1.5 # 1.5 ~ 4k/2k
    if options == 6:
        image_stim.size = (1380/ratio, (1380*height)/(width*ratio))
        image_stim.draw()
        for i in range(6):
            click_box = visual.Rect(mywin, pos=pos_6[i], size=click_box_size, lineColor=None, fillColor=bk_color)
            click_text = visual.TextStim(mywin, text=text_6[i], color=tx_color, pos=pos_6[i], height=tx_height)
            click_box.draw()
            click_text.draw()
    else:
        image_stim.size = (1400/ratio, (1400*height)/(width*ratio))
        image_stim.draw()
        for i in range(8):
            click_box = visual.Rect(mywin, pos=pos_8[i], size=click_box_size, lineColor=None, fillColor=bk_color)
            click_text = visual.TextStim(mywin, text=text_8[i], color=tx_color, pos=pos_8[i], height=tx_height)
            click_box.draw()
            click_text.draw()

    mywin.flip()
    event.waitKeys(keyList=['space'])
    answer = 2
    reaction_time = 11.34
    return answer, reaction_time


def draw_6options(mywin):
    

    return True


def draw_8options(mywin):

    # mywin.flip()
    return True


def start(mywin, expInfo):
    # display instructions and wait
    message1 = visual.TextStim(mywin, pos=[0,+100], wrapWidth=1000,
        text="Hello, " + expInfo['Name'] + "!\n Welcome to the experiment.")
    message2 = visual.TextStim(mywin, pos=[0,-100], wrapWidth=1000,
                               text='Please hit the space to start.')
    message1.setSize(text_size)
    message2.setSize(text_size)
    message1.draw()
    message2.draw()
    mywin.flip()
    event.waitKeys(keyList=['space'])


def finish(mywin, expInfo):
    # display end message and quit
    message1 = visual.TextStim(mywin, pos=[0,0], wrapWidth=1000,
        text="Thank you for participating, " + expInfo['Name'] + "!")
    message1.setSize(text_size)
    message1.draw()
    mywin.flip()
    core.wait(2)