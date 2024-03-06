# All parameters for experiment is defined here
# Author: Tianyi Zheng
import math
import numpy as np

# display settings
# 1512 982 for mbp14
# 3840 2160 for dell
# 5120 1440 for Philips
screen_width = 2560
# screen_width_mm = 596.74
# mm_pix = screen_width / screen_width_mm
screen_height = 1440

# visual settings
distance = 580 # distance between screen and participant in unit of mm
FoV_degree = 60 # field of view in unit of degree
rf_FoV = 10 # field of sharp view

# text settings for opening and closing
text_size = 50
textbox_size = [None, None]

# trigger_flash
trigger_sizex = 30
trigger_sizey = 60
trigger_ypos = -1*(screen_height/2 - trigger_sizey/2 - 100)


# click box
click_box_size = (100,50)
bk_color = '#333333'
tx_color = '#f2f2f2'
tx_height = 40

col1_6 = -400
col2_6 = 0
col3_6 = 400
row1_6 = -100
row2_6 = -400
pos_6 = [(col1_6, row1_6), (col2_6, row1_6), (col3_6, row1_6), (col1_6, row2_6), (col2_6, row2_6), (col3_6, row2_6)]
text_6 = ['1', '2', '3', '4', '5', '6']


col1_8 = -500
col2_8 = -200
col3_8 = 200
col4_8 = 500
row1_8 = -100
row2_8 = -400
pos_8 = [(col1_8, row1_8), (col2_8, row1_8), (col3_8, row1_8), (col4_8, row1_8), (col1_8, row2_8), (col2_8, row2_8), (col3_8, row2_8), (col4_8, row2_8)]
text_8 = ['1', '2', '3', '4', '5', '6', '7', '8']