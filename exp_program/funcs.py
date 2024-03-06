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

    show_one_question(mywin, options, image_stim, width, height)

    mouse = event.Mouse(mywin)

    # trigger.write(b'H')
    mywin.flip()
    answer = 0
    reaction_time = 0
    rt_clock = core.Clock()
    while rt_clock.getTime() < wait_for_answer:
        buttons, _ = mouse.getPressed(getTime=True)
        if buttons[0] == 1: # left click
            pos = mouse.getPos()
            # print(f"Left click detected at position: {pos}")
            answer = pos_to_answer(pos, options)
            # print(answer)
            if answer != 0:
                reaction_time = rt_clock.getTime()
                # trigger.write(b'L')
                show_one_question(mywin, options, image_stim, width, height)
                clicked_box(mywin, options, answer)
                mywin.flip()
                core.wait(0.5)
                break
            else:
                continue
    
    return answer, reaction_time


def show_one_question(mywin, options, image_stim, width, height):
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
    
    return True

def pos_to_answer(pos, options):
    if options == 6:
        if (pos[0] > col1_6 - 0.5*click_box_w) and (pos[0] < col1_6 + 0.5*click_box_w):
            if (pos[1] > row1_6 - 0.5*click_box_h) and (pos[1] < row1_6 + 0.5*click_box_h):
                return 1
            elif (pos[1] > row2_6 - 0.5*click_box_h) and (pos[1] < row2_6 + 0.5*click_box_h):
                return 4
            else:
                return 0
        elif (pos[0] > col2_6 - 0.5*click_box_w) and (pos[0] < col2_6 + 0.5*click_box_w):
            if (pos[1] > row1_6 - 0.5*click_box_h) and (pos[1] < row1_6 + 0.5*click_box_h):
                return 2
            elif (pos[1] > row2_6 - 0.5*click_box_h) and (pos[1] < row2_6 + 0.5*click_box_h):
                return 5
            else:
                return 0
        elif (pos[0] > col3_6 - 0.5*click_box_w) and (pos[0] < col3_6 + 0.5*click_box_w):
            if (pos[1] > row1_6 - 0.5*click_box_h) and (pos[1] < row1_6 + 0.5*click_box_h):
                return 3
            elif (pos[1] > row2_6 - 0.5*click_box_h) and (pos[1] < row2_6 + 0.5*click_box_h):
                return 6
            else:
                return 0
        else:
            return 0
    
    else:
        if (pos[0] > col1_8 - 0.5*click_box_w) and (pos[0] < col1_8 + 0.5*click_box_w):
            if (pos[1] > row1_8 - 0.5*click_box_h) and (pos[1] < row1_8 + 0.5*click_box_h):
                return 1
            elif (pos[1] > row2_8 - 0.5*click_box_h) and (pos[1] < row2_8 + 0.5*click_box_h):
                return 5
            else:
                return 0
        elif (pos[0] > col2_8 - 0.5*click_box_w) and (pos[0] < col2_8 + 0.5*click_box_w):
            if (pos[1] > row1_8 - 0.5*click_box_h) and (pos[1] < row1_8 + 0.5*click_box_h):
                return 2
            elif (pos[1] > row2_8 - 0.5*click_box_h) and (pos[1] < row2_8 + 0.5*click_box_h):
                return 6
            else:
                return 0
        elif (pos[0] > col3_8 - 0.5*click_box_w) and (pos[0] < col3_8 + 0.5*click_box_w):
            if (pos[1] > row1_8 - 0.5*click_box_h) and (pos[1] < row1_8 + 0.5*click_box_h):
                return 3
            elif (pos[1] > row2_8 - 0.5*click_box_h) and (pos[1] < row2_8 + 0.5*click_box_h):
                return 7
            else:
                return 0
        elif (pos[0] > col4_8 - 0.5*click_box_w) and (pos[0] < col4_8 + 0.5*click_box_w):
            if (pos[1] > row1_8 - 0.5*click_box_h) and (pos[1] < row1_8 + 0.5*click_box_h):
                return 4
            elif (pos[1] > row2_8 - 0.5*click_box_h) and (pos[1] < row2_8 + 0.5*click_box_h):
                return 8
            else:
                return 0
        else:
            return 0


def clicked_box(mywin, options, answer):
    answer = answer - 1 # 0-based index
    if options == 6:
        click_box = visual.Rect(mywin, pos=pos_6[answer], size=click_box_size, lineColor=None, fillColor=tx_color)
        click_text = visual.TextStim(mywin, text=text_6[answer], color=bk_color, pos=pos_6[answer], height=tx_height)
        click_box.draw()
        click_text.draw()
    else:
        click_box = visual.Rect(mywin, pos=pos_8[answer], size=click_box_size, lineColor=None, fillColor=tx_color)
        click_text = visual.TextStim(mywin, text=text_8[answer], color=bk_color, pos=pos_8[answer], height=tx_height)
        click_box.draw()
        click_text.draw()
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