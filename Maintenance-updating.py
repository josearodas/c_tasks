#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 19 15:45 2018
@author: JARP

In order to modify the number of trials and runs the conditions counter and the runs_trials must be changed:
The runs_trials include 36 runs with 9 runs for all conditions.
Each condition will be presented 8 times (reflected in the 'rep_counter') except for UUUU and URUR which will be
presented 11 and 14 times to increase the number of trials for UP4 and SW4.
"""
from __future__ import division

from psychopy import visual, core, event, gui, clock, data
import random, copy
import numpy as np

#If any of these values have to be changed the content some vars should also be changed (see above for a description)
#these values can be decreased for testing purposes only but not increased more than the recommended value
num_runs = 36       #must be set to 36
num_pract = 3      #must be set to 5


def trial_run(cond, runs):
    
    t_run = []
    initial_trial = []
    
    letters_trial = ['Q','W','R','T','P','S','D','F','G','H','J','K','L','Z','X','C','B','N']
    
    for i in range(4):
        initial_trial.append(random.choice(letters_trial))
        letters_trial.remove(initial_trial[-1])
    
    t_run.append({'stim':initial_trial,'answer':copy.copy(initial_trial),'condition':'XXXX'})
    
    current_numbTrials = random.choice(runs)
    for trial in range(current_numbTrials):
        t_run.append(copy.deepcopy(t_run[-1]))
        
        while True:
            present_cond = random.choice(cond)
            if present_cond['rep_counter'] > 0:
                present_cond['rep_counter'] -= 1
                break
        counter = 0
        t_run[-1]['condition'] = present_cond['condition']
        for stim_index in present_cond['replace']:
            letter_replace = random.choice(letters_trial)
            letters_trial.remove(letter_replace)
            t_run[-1]['stim'][stim_index] = letter_replace
            t_run[-1]['answer'][stim_index] = letter_replace
            counter += 1
        
        if counter < 4:
            for asterisk_index in present_cond['asterisk']:
                t_run[-1]['stim'][asterisk_index] = '*'
    
    runs.remove(current_numbTrials)
    
    return t_run

def collect_response():
    subj_resp = 0
    typed_string = ''
    returned_string = ''
    
    txt_topinstr.draw()
    win.flip()
    event.clearEvents()
    while subj_resp == 0:
        for i in event.getKeys(keyList=['backspace','return','escape',
        'q','w','r','t','p','s','d','f','g','h','j','k','l','z','x','c','m','b','n']):
            if i in ['escape']:
                core.quit()
            elif i in ['return']:
                returned_string = typed_string
                core.wait(1)
                subj_resp = 1
            elif i in ['backspace']:
                typed_string = typed_string[:-1]
                txt_input.setText(typed_string)
                txt_input.draw()
                txt_topinstr.draw()
                win.flip()
            else:
                typed_string += i.upper()
                txt_input.setText(typed_string)
                txt_input.draw()
                txt_topinstr.draw()
                win.flip()
    
    if returned_string == '':
        returned_string = 'XXXX'
    
    return returned_string
    
    win.flip()

my_dlg = gui.Dlg(title = 'Assessment')
my_dlg.addField('Participant:')
my_dlg.addField('Session:', choices=['pre','post','follow'])
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

id_participant = str(my_dlg.data[0])
date = data.getDateStr()
session = str(my_dlg.data[1])

file_name = id_participant+'_astbox_'+date+'_'+session+'.csv'
file_name_raw = id_participant+'_astbox_'+'raw_'+date+'_'+session+'.csv'

win = visual.Window(fullscr=True, units='pix',color=(-1,-1,-1))
win.mouseVisible=False

letters = ['Q','W','R','T','P','S','D','F','G','H','J','K','L','Z','X','C','B','N']

#36 runs (two runs added to increase the number of trials for conditions UUUU, and URUR); each run will contain 
runs_trials = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4]

#conditions with a counter to control the number of times each will appear
conditions = [{'replace':[1,2,3],'asterisk':[0],'rep_counter':8,'condition':'RUUU'},{'replace':[2,3],'asterisk':[0,1],'rep_counter':8,'condition':'RRUU'},
        {'replace':[3],'asterisk':[0,1,2],'rep_counter':8,'condition':'RRRU'},{'replace':[0,1,2],'asterisk':[3],'rep_counter':8,'condition':'UUUR'},
        {'replace':[0,1],'asterisk':[2,3],'rep_counter':8,'condition':'UURR'},{'replace':[0],'asterisk':[1,2,3],'rep_counter':8,'condition':'URRR'},
        {'replace':[1,3],'asterisk':[0,2],'rep_counter':8,'condition':'RURU'},{'replace':[0,2],'asterisk':[1,3],'rep_counter':11,'condition':'URUR'},
        {'replace':[0,3],'asterisk':[1,2],'rep_counter':8,'condition':'URRU'},{'replace':[0,1,2,3],'asterisk':[],'rep_counter':14,'condition':'UUUU'}]

#practice trials
pract_runs = [1,2,3,3,4]
pract_cond = [{'replace':[1,2,3],'asterisk':[0],'rep_counter':1,'condition':'RUUU'},{'replace':[2,3],'asterisk':[0,1],'rep_counter':1,'condition':'RRUU'},
        {'replace':[3],'asterisk':[0,1,2],'rep_counter':2,'condition':'RRRU'},{'replace':[0,1,2],'asterisk':[3],'rep_counter':1,'condition':'UUUR'},
        {'replace':[0,1],'asterisk':[2,3],'rep_counter':1,'condition':'UURR'},{'replace':[0],'asterisk':[1,2,3],'rep_counter':2,'condition':'URRR'},
        {'replace':[1,3],'asterisk':[0,2],'rep_counter':1,'condition':'RURU'},{'replace':[0,2],'asterisk':[1,3],'rep_counter':1,'condition':'URUR'},
        {'replace':[0,3],'asterisk':[1,2],'rep_counter':2,'condition':'URRU'},{'replace':[0,1,2,3],'asterisk':[],'rep_counter':1,'condition':'UUUU'}]
'''
#for 65 runs (the full task)
runs_trials = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
conditions_full = [{'replace':[1,2,3],'asterisk':[0],'rep_counter':16,'condition':'RUUU'},{'replace':[2,3],'asterisk':[0,1],'rep_counter':16,'condition':'RRUU'},
        {'replace':[3],'asterisk':[0,1,2],'rep_counter':16,'condition':'RRRU'},{'replace':[0,1,2],'asterisk':[3],'rep_counter':16,'condition':'UUUR'},
        {'replace':[0,1],'asterisk':[2,3],'rep_counter':16,'condition':'UURR'},{'replace':[0],'asterisk':[1,2,3],'rep_counter':16,'condition':'URRR'},
        {'replace':[1,3],'asterisk':[0,2],'rep_counter':16,'condition':'RURU'},{'replace':[0,2],'asterisk':[1,3],'rep_counter':16,'condition':'URUR'},
        {'replace':[0,3],'asterisk':[1,2],'rep_counter':17,'condition':'URRU'},{'replace':[0,1,2,3],'asterisk':[],'rep_counter':16,'condition':'UUUU'}]
'''

#txt_box1 = visual.TextBox(window=win, font_color=(1,1,1), font_size = 40, units = 'norm', 
#        background_color=[-1,-1,-1], border_color=[1,1,1],textgrid_shape=[1,1],
#        grid_vert_justification='center', grid_horz_justification = 'center')

txt_stim = visual.TextStim(win=win, color=(1,1,1), height=45, font = 'consolas')
txt_input = visual.TextStim(win=win, color=(1,1,1), height=45, font = 'consolas')
txt_instr = visual.TextStim(win=win, color=(1,1,1), height = 28,wrapWidth=900)
txt_topinstr = visual.TextStim(win=win, color=(1,1,1),height=28, pos=(0,200), text='Please type the last digits of each box and press enter')

box1 = visual.Rect(win, width = 50, height = 50, lineColor = (1,1,1), lineWidth = 3,
                        pos = (-188,-4))
box2 = visual.Rect(win, width = 50, height = 50, lineColor = (1,1,1), lineWidth = 3,
                        pos = (-63,-4))
box3 = visual.Rect(win, width = 50, height = 50, lineColor = (1,1,1), lineWidth = 3,
                        pos = (63,-4))
box4 = visual.Rect(win, width = 50, height = 50, lineColor = (1,1,1), lineWidth = 3,
                        pos = (188,-4))

rt_clock = clock.Clock()
rt_stim_output= []
errors = 0

txt_instr.text = 'In the following task you will be presented with four boxes containing one letter each. Your objective is to always remember the content of each of these boxes as they may be updated. Once you have memorized the letter contained in each box a keypress (the <space> bar) will make a new set of characters to appear. These can be either new letters or asterisks. If a letter is presented in a box, you will have to update in your memory the content of that box, and if an asterisk appears the content of the box remains the same.\n\n    -New letter -> update the content of the box\n    -Asterisk (*) -> box content remains the same\n\nYou will do a few practice trials before starting the task. Please press the <space> bar when ready.'
txt_instr.draw()
win.flip()

event.waitKeys(keyList=['space'])
win.flip()
core.wait(1)

#Practice trials
for run in range(num_pract):  #this should be set to 5
    
    event.clearEvents()
    
    current_run = trial_run(pract_cond,pract_runs)
    rt_stim_partial = []
    
    for trial in current_run:
        txt_stim.text = '    '.join(trial['stim'])
        txt_stim.draw()
        box1.draw()
        box2.draw()
        box3.draw()
        box4.draw()
        
        win.flip()
        
        event.waitKeys(keyList=['space'])
        
        box1.draw()
        box2.draw()
        box3.draw()
        box4.draw()
        win.flip()
        core.wait(1)
    
    #print current_run[-1]['answer']             #THIS SHOULD BE DELETED OR COMMENTED!!!
    
    returned_string = collect_response()
    
    answer_contrast = ''.join(current_run[-1]['answer'])
    
    
    if returned_string == answer_contrast:
        txt_instr.text = 'You were right! Those were the last letters presented in each box\n\nPlease press any key to continue.'
        txt_instr.draw()
        win.flip()
        event.waitKeys()
    else:
        txt_instr.text = 'Those were not the last letter contained in the boxes. Remember that each time a new letter appears in a box you have to remember THAT new letter replacing it with the previous one presented in the same box. If an asterisk is presented in the box the last letter presented remains the same.\n\n Please press any key to continue.'
        txt_instr.draw()
        win.flip()
        event.waitKeys()

event.clearEvents()
txt_instr.text = 'Now that you have practiced a few runs you can start the task. If you feel tired during the task you are allowed to take short rests between runs.\n\nPlease press the <space bar> when ready.'
txt_instr.draw()
win.flip()

event.waitKeys(keyList=['space'])
win.flip()
core.wait(1)

#the real deal!
for run in range(num_runs):  #this should be set to 42
    
    event.clearEvents()
    
    current_run = trial_run(conditions,runs_trials)
    rt_stim_partial = []
    
    for trial in current_run:
        txt_stim.text = '    '.join(trial['stim'])
        txt_stim.draw()
        box1.draw()
        box2.draw()
        box3.draw()
        box4.draw()
        
        rt_clock.reset()
        
        win.flip()
        
        response_rt = event.waitKeys(timeStamped=rt_clock, keyList=['space'])
        rt_stim_partial.append([round(response_rt[-1][1],4),trial['condition']])
        
        box1.draw()
        box2.draw()
        box3.draw()
        box4.draw()
        win.flip()
        core.wait(1)
    
    #print current_run[-1]['answer']             #THIS SHOULD BE DELETED OR COMMENTED!!!
    
    returned_string = collect_response()
    
    answer_contrast = ''.join(current_run[-1]['answer'])
    
    
    if returned_string == answer_contrast:
        rt_stim_output += copy.deepcopy(rt_stim_partial)
    else:
        errors += 1
    
    txt_instr.text = 'Press any key to continue'
    txt_instr.draw()
    win.flip()
    event.waitKeys()
    win.flip()
    core.wait(1)


output_RUUU = []
output_RRUU = []
output_RRRU = []
output_UUUR = []
output_UURR = []
output_URRR = []
output_RURU = []
output_URUR = []
output_URRU = []
output_UUUU = []
output_UP1 = []
output_UP2 = []
output_UP3 = []
output_UP4 = []
output_SW1 = []
output_SW2 = []
output_SW3 = []
output_SW4 = []

for i in rt_stim_output:
    if i[1] == 'RUUU':
        output_RUUU.append(i[0])
        output_UP3.append(i[0])
        output_SW1.append(i[0])
    elif i[1] == 'RRUU':
        output_RRUU.append(i[0])
        output_UP2.append(i[0])
        output_SW1.append(i[0])
    elif i[1] == 'RRRU':
        output_RRRU.append(i[0])
        output_UP1.append(i[0])
        output_SW1.append(i[0])
    elif i[1] == 'UUUR':
        output_UUUR.append(i[0])
        output_UP3.append(i[0])
        output_SW2.append(i[0])
    elif i[1] == 'UURR':
        output_UURR.append(i[0])
        output_UP2.append(i[0])
        output_SW2.append(i[0])
    elif i[1] == 'URRR':
        output_URRR.append(i[0])
        output_UP1.append(i[0])
        output_SW2.append(i[0])
    elif i[1] == 'RURU':
        output_RURU.append(i[0])
        output_UP2.append(i[0])
        output_SW3.append(i[0])
    elif i[1] == 'URUR':
        output_URUR.append(i[0])
        output_UP2.append(i[0])
        output_SW4.append(i[0])
    elif i[1] == 'URRU':
        output_URRU.append(i[0])
        output_UP2.append(i[0])
        output_SW3.append(i[0])
    elif i[1] == 'UUUU':
        output_UUUU.append(i[0])
        output_UP4.append(i[0])
        output_SW1.append(i[0])

if len(output_RUUU) > 0:
    mean_output_RUUU = np.mean(output_RUUU)
else:
    mean_output_RUUU = 0
if len(output_RRUU) > 0:
    mean_output_RRUU = np.mean(output_RRUU)
else:
    mean_output_RRUU = 0
if len(output_RRRU) > 0:
    mean_output_RRRU = np.mean(output_RRRU)
else:
    mean_output_RRRU = 0
if len(output_UUUR) > 0:
    mean_output_UUUR = np.mean(output_UUUR)
else:
    mean_output_UUUR = 0
if len(output_UURR) > 0:
    mean_output_UURR = np.mean(output_UURR)
else:
    mean_output_UURR = 0
if len(output_URRR) > 0:
    mean_output_URRR = np.mean(output_URRR)
else:
    mean_output_URRR = 0
if len(output_RURU) > 0:
    mean_output_RURU = np.mean(output_RURU)
else:
    mean_output_RURU = 0
if len(output_URUR) > 0:
    mean_output_URUR = np.mean(output_URUR)
else:
    mean_output_URUR = 0
if len(output_URRU) > 0:
    mean_output_URRU = np.mean(output_URRU)
else:
    mean_output_URRU = 0
if len(output_UUUU) > 0:
    mean_output_UUUU = np.mean(output_UUUU)
else:
    mean_output_UUUU = 0

if len(output_UP1) > 0:
    mean_output_UP1 = np.mean(output_UP1)
else:
    mean_output_UP1 = 0
if len(output_UP2) > 0:
    mean_output_UP2 = np.mean(output_UP2)
else:
    mean_output_UP2 = 0
if len(output_UP3) > 0:
    mean_output_UP3 = np.mean(output_UP3)
else:
    mean_output_UP3 = 0
if len(output_UP4) > 0:
    mean_output_UP4 = np.mean(output_UP4)
else:
    mean_output_UP4 = 0
if len(output_SW1) > 0:
    mean_output_SW1 = np.mean(output_SW1)
else:
    mean_output_SW1 = 0
if len(output_SW2) > 0:
    mean_output_SW2 = np.mean(output_SW2)
else:
    mean_output_SW2 = 0
if len(output_SW3) > 0:
    mean_output_SW3 = np.mean(output_SW3)
else:
    mean_output_SW3 = 0
if len(output_SW4) > 0:
    mean_output_SW4 = np.mean(output_SW4)
else:
    mean_output_SW4 = 0

str_output_RUUU = str(output_RUUU)
str_output_RRUU = str(output_RRUU)
str_output_RRRU = str(output_RRRU)
str_output_UUUR = str(output_UUUR)
str_output_UURR = str(output_UURR)
str_output_URRR = str(output_URRR)
str_output_RURU = str(output_RURU)
str_output_URUR = str(output_URUR)
str_output_URRU = str(output_URRU)
str_output_UUUU = str(output_UUUU)
str_output_UP1 = str(output_UP1)
str_output_UP2 = str(output_UP2)
str_output_UP3 = str(output_UP3)
str_output_UP4 = str(output_UP4)
str_output_SW1 = str(output_SW1)
str_output_SW2 = str(output_SW2)
str_output_SW3 = str(output_SW3)
str_output_SW4 = str(output_SW4)


np.savetxt(file_name, [('RUUU','RRUU','RRRU','UUUR','UURR','URRR','RURU','URUR','URRU','UUUU',
    'UP1','UP2','UP3','UP4','SW1','SW2','SW3','SW4', 'errors'),(mean_output_RUUU,mean_output_RRUU,mean_output_RRRU,
    mean_output_UUUR,mean_output_UURR,mean_output_URRR,mean_output_RURU,mean_output_URUR,mean_output_URRU,
    mean_output_UUUU,mean_output_UP1,mean_output_UP2,mean_output_UP3,mean_output_UP4,mean_output_SW1,
    mean_output_SW2,mean_output_SW3,mean_output_SW4,errors)], fmt = '%s', delimiter = ',')

np.savetxt(file_name_raw,['RUUU,'+str_output_RUUU[1:-1],'RRUU,'+str_output_RRUU[1:-1],'RRRU,'+str_output_RRRU[1:-1],'UUUR,'+str_output_UUUR[1:-1],
    'UURR,'+str_output_UURR[1:-1],'URRR,'+str_output_URRR[1:-1],'RURU,'+str_output_RURU[1:-1],'URUR,'+str_output_URUR[1:-1],'URRU,'+str_output_URRU[1:-1],
    'UUUU,'+str_output_UUUU[1:-1],'UP1,'+str_output_UP1[1:-1],'UP2,'+str_output_UP2[1:-1],'UP3,'+str_output_UP3[1:-1],'UP4,'+str_output_UP4[1:-1],
    'SW1,'+str_output_SW1[1:-1],'SW2,'+str_output_SW2[1:-1],'SW3,'+str_output_SW3[1:-1],'SW4,'+str_output_SW4[1:-1]], fmt = '%s', delimiter = ',')

txt_instr.text = 'The task has concluded. Thanks for participating.\n\nPlease press any key.'
txt_instr.draw()
win.flip()
event.waitKeys()

win.close()
