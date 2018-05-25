4#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 16:17 2018
Started on Thu Nov 23
@author: JARP

Based on certain descriptions from Hilbert (2015)

file legend:
    first number is the number of digits
    second digit can be either 1(correct) or 0 (incorrect)
"""
from __future__ import division
from psychopy import visual, core, event, gui, data
import numpy as np
import random


def type_input():
    
    subj_resp = 0
    typed_string = ''
    returned_string = ''
    
    txt_topinstr.draw()
    win.flip()
    
    event.clearEvents()
    
    #shows participant's input in the screen and lets them erase, type and quit the program
    while subj_resp == 0:
        for i in event.getKeys(keyList=['backspace','return','escape',
        '1','2','3','4','5','6','7','8','9']):
            if i in ['escape']:
                core.quit()
            elif i in ['return']:
                returned_string = typed_string #the returned string
                subj_resp = 1
            elif i in ['backspace']:
                typed_string = typed_string[:-1]
                txt_stim.setText(typed_string)
                txt_stim.draw()
                txt_topinstr.draw()
                win.flip()
            else:
                typed_string = i
                txt_stim.setText(typed_string)
                txt_stim.draw()
                txt_topinstr.draw()
                win.flip()
    
    return returned_string

my_dlg = gui.Dlg(title = 'Assessment')
my_dlg.addField('Participant:')
my_dlg.addField('Session:', choices = ['pre','post','follow'])
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

id_participant = str(my_dlg.data[0])
phase = str(my_dlg.data[1])
date = data.getDateStr()

file_name = id_participant+'_backwDS_'+date+'_'+phase+'.csv'

win = visual.Window(fullscr = True,color = [-1,-1,-1],units = 'pix')
win.mouseVisible = False

txt_instr = visual.TextStim(win,color = [1,1,1],height = 28,wrapWidth = 900)
txt_topinstr = visual.TextStim(win,color = [1,1,1],height = 28,pos = (0,200),wrapWidth = 900)
txt_stim = visual.TextStim(win,color = [1,1,1],height = 68)

level = 2
local_output = []

txt_instr.text = 'A series of numbers will be presented on the screen one by one. After the presentation of the numbers you will have to recall them in reversed order and type your answer with the keyboard.\n\nFor example, if the numbers 9-1-2 have been presented you will have to recall 2-1-9.\n\nThe amount of numbers that you will have to recall will increase as you progress in the task.\n\nYou will have two trials to practice before starting the actual task.\n\nPress the <space> bar to begin the practice trials.'
txt_instr.draw()
win.flip()

event.waitKeys(keyList = ['space'])

win.flip()
core.wait(2)

#some practice trials
for rep in range(2):
    digits = []
    digits_str = ''
    pool =[1,2,3,4,5,6,7,8,9]
    
    for i in range(level):
        selected_digit = random.choice(pool)
        digits.append(selected_digit)
        pool.remove(selected_digit)
    
    for digit in digits:
        digits_str += str(digit)
        txt_stim.text = str(digit)
        txt_stim.draw()
        win.flip()
        core.wait(1)
        win.flip()
        core.wait(1)
    
    prereturned_string = []
    
    for i in range(level):
        if i == 0:
            txt_topinstr.text = "Please type the last digit presented and press <enter>"
        else:
            txt_topinstr.text = "Please type the first digit presented and press <enter>"
        prereturned_string.append(type_input())
    
    returned_string = ''.join(prereturned_string)
    
    win.flip()
    rev_digits = digits_str[::-1]   #this should reverse the order of the presented digits
    
    if returned_string != rev_digits:
        txt_instr.text = "That was not right. Remember, you have to type the number in reversed order.\n\nPress any key to continue."
        txt_instr.draw()
        win.flip()
        event.waitKeys()
    else:
        #print 'right'
        txt_instr.text = "That's right."
        txt_instr.draw()
        win.flip()
        core.wait(2)

txt_instr.text = 'Those were the practice trials, now you may begin the real task.\n\nPress the <space> bar to start.'
txt_instr.draw()
win.flip()

event.waitKeys(keyList = ['space'])
win.flip()
core.wait(2)

while level <= 9:
    errors = 0
    for rep in range(2):
        digits = []
        digits_str = ''
        pool =[1,2,3,4,5,6,7,8,9]
        
        for i in range(level):
            selected_digit = random.choice(pool)
            digits.append(selected_digit)
            pool.remove(selected_digit)
        
        for digit in digits:
            digits_str += str(digit)
            txt_stim.text = str(digit)
            txt_stim.draw()
            win.flip()
            core.wait(1)
            win.flip()
            core.wait(1)
        
        prereturned_string = []
        
        txt_topinstr.text = 'Type each digit (in reversed order) followed by an <enter>'
        
        for i in range(level):
            prereturned_string.append(type_input())
        
        returned_string = ''.join(prereturned_string)
        
        win.flip()
        rev_digits = digits_str[::-1]   #this should reverse the order of the presented digits
        
        if returned_string != rev_digits:
            errors += 1
            #print 'wrong'
            local_output.append([level,0])
            win.flip()
            core.wait(2)
        else:
            #print 'right'
            local_output.append([level,1])
            win.flip()
            core.wait(2)
    
    
    if errors == 2:
        break
    
    
    level += 1
    
    del digits

#print local_output

np.savetxt(
    file_name,
    local_output,
    fmt = '%i',
    delimiter = ',',
    header = 'digits,answer'
    )

txt_instr.text = "You have concluded the task. Thanks for participating.\n\nPlease press the <space> bar."
txt_instr.draw()
win.flip()

event.waitKeys(keyList = ['space'])

win.close()