from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
import os
from settings import *
from funcs import *
import serial
import time

# dilogue box
''' Set: 1,2,3,4
    Test: 0,1 '''
expInfo = {'Name': 'HAL', 'ID': '31', 'Set': '1', 'Test': '0'}
expInfo['dateStr'] = data.getDateStr()  # add the current time
# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Experiment Info', fixed=['dateStr'])
if dlg.OK:
    if expInfo['Test']=='1':
        filename = expInfo['Name'] + "_" + expInfo['ID'] + "_test_" + expInfo['dateStr']
    else:
        filename = expInfo['Name'] + "_" + expInfo['ID'] + "_" + expInfo['Set'] + "_" + expInfo['dateStr']
else:
    core.quit()  # the user hit cancel so exit
dataFile = open('../../behav_data/'+filename+'.csv', 'w')  # a simple text file with 'comma-separated-values'
''' question: A1, A2, ..., B1, B2, ...
    answer: 3, 5, 1 ...
    response: 0 = no response, 1 = has response ?
    reaction time: in second '''
dataFile.write('question,answer,reaction time\n')

# create a window
mywin = visual.Window([screen_width, screen_height], 
                      fullscr=True, screen=2, monitor="testMonitor", 
                      color=[-1,-1,-1], units="pix")
print("Window created.")

# create objects
# trigger_flash = visual.Rect(mywin, pos=((screen_width-trigger_sizex)/2, trigger_ypos),
#                        size=(trigger_sizex,trigger_sizey), lineColor=None, fillColor='white')

# print("Objects created.")

# get questions by set
sets = get_sets(id=int(expInfo['ID']), set_number=int(expInfo['Set']), test=int(expInfo['Test']))
print(sets)
print("Question set generated.")

refresh_rate = mywin.getActualFrameRate()
print("Refresh rate: %.2f", refresh_rate)

trigger = serial.Serial('COM17', 9600) # lab 11, office 3
print("Serial port for Arduino opened.")

start(mywin, expInfo)
for question in sets:
    index, options = question[0], question[1]
    answer, reaction_time = one_question(mywin, index, options, trigger)
    # save data
    dataFile.write('%s,%d,%.3f\n' %(index, answer, reaction_time))

print(dataFile)

finish(mywin, expInfo)

dataFile.close()
