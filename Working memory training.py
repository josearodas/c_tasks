#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:31:06 2017
Started on Thu Nov 23
@author: JARP
"""

from __future__ import division
from psychopy import visual, core, data, event, gui
import numpy as np
import random
import os
import pandas as pd
import matplotlib.pyplot as plt


'''Some functions. block_creator creates the blocks with 6 n-back repetitions.
It only asks the n-back level as a paramenter.'''

'''This will create the trials' block with six n-back repetitions'''

#correct (c), incorrect (i) or miss (m)
def block_creator(nback_level):
    
    block = []
    
    for n in range(20+nback_level): #create the basic block (with unwanted random n-back repetitions)
        block.append(random.choice(stim_pool))
    
    block_len = len(block)
    
    for i in range(block_len - nback_level): #this section eliminate any unplanned n-back repetition
        prov_pool = [{'area':'a1','x':-150,'y':150},{'area':'a2','x':0,'y':150},
                    {'area':'a3','x':150,'y':150},{'area':'b1','x':-150,'y':0},{'area':'b3','x':150,'y':0},
                    {'area':'c1','x':-150,'y':-150},{'area':'c2','x':0,'y':-150},{'area':'c3','x':150,'y':-150}]
        if block[i] == block[i+nback_level]:
            prov_pool.remove(block[i]) #the pool without the current position
            del block[i] #the block without the unwanted trial
            block.insert(i, random.choice(prov_pool))
    
    #the following section inserts 6 n-back repetition trials in the already cleaned block
    
    index_pool = []

    for ixpool in range(len(block)-nback_level): #creates a set of possible positions to insert the n-back trials
        index_pool.append(ixpool)

    for ii in range(6):
        trial_torep = random.choice(index_pool) #selects a random position x (a random trial)
        block.insert(trial_torep+nback_level, block[trial_torep]) #create the duplicated trial after x position
        #print trial_torep    #this helps to identify the duplicated trials
        del block[trial_torep+(nback_level+1)]   #delete the previous x+n trial
        
        if trial_torep >= nback_level and (trial_torep-nback_level) in index_pool: #in case tries to eliminate an item out of index
            index_pool.remove(trial_torep-nback_level) #eliminate the trial n-back so they not interfere in future dublications
            index_pool.remove(trial_torep) #eliminate the duplicated trial
        else:
            index_pool.remove(trial_torep)

    del index_pool
    
    return block

def typed_resp():
    returned_string = ''
    typed_string = ''
    subj_resp = 0
    win.flip()
    txt_instr.draw()
    txt_legend.draw()
    win.flip()
    while subj_resp == 0:
        for i in event.getKeys(keyList=['1','2','3','4','5','return']):
            if i in ['return']:
                returned_string = typed_string #the returned string
                win.flip()
                core.wait(0.5)
                subj_resp = 1
            else:
                typed_string = i
                txt_input.setText(typed_string)
                txt_input.draw()
                txt_instr.draw()
                txt_legend.draw()
                win.flip()
    
    return returned_string

'''A function to create a graph depicting the participants progress untill the last session'''
#def progress_graph()

#obtaining participant info
my_dlg = gui.Dlg(title='N-back training')
my_dlg.addText('Please enter your assigned code')
my_dlg.addField('Participant:')
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

id_participant = str(my_dlg.data[0])
date = data.getDateStr()
date_reg = data.getDateStr()[:11]

file_name = id_participant+'_n-back_'+date
data_headings = 'trial;n-level;Details'

win = visual.Window(
        fullscr = True,
        color=(1,1,1),
        units = 'pix'
        )

win.mouseVisible=False

txt_menu = visual.TextStim(win = win, color=(-1,-1,-1), height=24)
txt_session_t = visual.TextStim(win = win, pos=(0,-250),color = (-1,-1,-1))
txt_instr = visual.TextStim(win, pos=(0,180), wrapWidth=800,
    text="In a scale from 1 to 5 how motivated to do the training are you feeling today? Please type a number",
    height=24,color=(-1,-1,-1))
txt_input = visual.TextStim(win, color=(-1,-1,-1), units='norm', pos=(0,-0.4), 
    height=0.1)
txt_legend = visual.TextStim(win, pos=(0,40),height=20, color=(-1,-1,-1),
    text="1=>not at all\n2=>not so much\n3=> can't say\n4=>somehow motivated\n5=>really motivated")

grid = visual.ImageStim(
    win=win, 
    image='frame.png'
    )

square_stim = visual.ImageStim(
    win = win,
    image = 'box.png',
    units = 'pix'
    )

clock = core.Clock()   #general timer

stim_pool = [{'area':'a1','x':-150,'y':150},{'area':'a2','x':0,'y':150},
    {'area':'a3','x':150,'y':150},{'area':'b1','x':-150,'y':0},{'area':'b3','x':150,'y':0},
    {'area':'c1','x':-150,'y':-150},{'area':'c2','x':0,'y':-150},{'area':'c3','x':150,'y':-150}]


motivation = 0

while motivation == '' or motivation == 0:
    txt_instr.draw()
    txt_legend.draw()
    win.flip()

    motivation = typed_resp()


#Create the file to insert each trial data
np.savetxt(
    file_name,
    ['date,motivation,day_session,n-level,details'],
    fmt = '%s',
    delimiter = ',',
    newline = '\n',
    )

with open('nback_system') as nbackfile:
    last_line = nbackfile.readlines()[-1]
    nback_level = int(last_line[17:])
    if last_line[:11] == date_reg:
        day_session = int(last_line[14:16])+1
    else:
        day_session = 1

for session_trial in range(20):
    
    order = ['b2']*nback_level
    responses = []    #this var stores participants responses with RT; can be either correct (c), incorrect (i) or miss (m)
    errors = 0    #missess and incorrects are considered errors; this counter control the adaptive n-back

    block = block_creator(nback_level)
    
    txt_menu.text= 'Please choose one of the following options by pressing the given key:\n\n        s => Start a new trial block\n        p => Show progress\n    esc => Quit\n\n\n\nRemember that <space> bar indicates a match'
    txt_session_t.text = 'Block %s\nN-back level = %s' % (day_session, nback_level)
    
    while True:
        txt_menu.draw()
        txt_session_t.draw()
        win.flip()
        k = event.waitKeys()
        if 'escape' in k:
            #insert core for creating the data file
            core.quit()

        elif 'p' in k:
            data = pd.read_csv('nback_system')
            
            tmp_meanscore = []
            tmp_dayscore = []
            tmp_date_reg = ['xxx_xxx_xx']

            for index, i in data.iterrows():
                tmp_date = i['Date']
                tmp_level = i['n_level']

                if tmp_date == tmp_date_reg[-1]:
                    tmp_meanscore.append(int(tmp_level))
                else:
                    tmp_dayscore.append(np.mean(tmp_meanscore))
                    tmp_meanscore = []
                    tmp_date_reg.append(tmp_date)

            tmp_dayscore.append(np.mean(tmp_meanscore))
            
            plt.plot(tmp_dayscore[1:])
            plt.ylabel('N-level')
            plt.xlabel('Sessions')
            plt.title('Press any key to go back')
            plt.savefig('progress.png')
            fig_progress = visual.ImageStim(win,image='progress.png')
            fig_progress.draw()
            win.flip()
            event.waitKeys()
            os.remove('progress.png')
            del data, tmp_meanscore, tmp_date_reg, tmp_date, tmp_level, tmp_dayscore

        elif 's' in k:
            break
    
    grid.draw()
    win.flip()
    #nback_history.append(nback_level)
    core.wait(2)
    
    #this is the core of the program. It presents the trials and collects responses
    for active_trial in block:
        
        clock.reset()
        event.clearEvents()
        
        square_stim.pos = (active_trial['x'],active_trial['y'])
        order.append(active_trial['area']) #this var stores the order of presentation of the stimuli (square position)
        
        while clock.getTime() < 1: #this should be set to 1s
            grid.draw()
            square_stim.draw()
            win.flip()
        
        while clock.getTime() < 3:   #only the grid (no square) must be shown for 2s
            grid.draw()
            win.flip()
        
        #Colect the correct, missed or incorrect responses and store this responses into a var
        key_pressed = event.getKeys(keyList=['space'], timeStamped = clock)
        if active_trial['area'] == order[len(order)-(nback_level+1)]:
            if len(key_pressed) > 0:
                responses.append(['c',key_pressed[-1][1]])
            else:
                responses.append(['m',0])
                errors += 1
        else:
            if len(key_pressed) > 0:
                responses.append(['i',key_pressed[-1][1]])
                errors += 1
    
    
    #The following section updates the file
    
    with open(file_name,'a') as sendfile:
        sendfile.write(str(date_reg))
        sendfile.write(',')
        sendfile.write(str(motivation))
        sendfile.write(',')
        sendfile.write(str(day_session))
        sendfile.write(',')
        sendfile.write(str(nback_level))
        sendfile.write(',')
        sendfile.write(str(responses))
        sendfile.write('\n')

    
    with open('nback_system','a') as nbackfile:
        nbackfile.write('\n')
        nbackfile.write(str(date_reg))
        nbackfile.write(',')
        nbackfile.write(str(motivation))
        nbackfile.write(',')
        if day_session < 10:
            nbackfile.write('0'+str(day_session))
        nbackfile.write(',')
        if nback_level < 10:
            nbackfile.write('0'+str(nback_level))
    
    #adjust the n-back level
    if errors > 5:
        if nback_level > 1:
            nback_level -= 1
    elif errors < 3:
        nback_level += 1


    #reset variables
    del order, responses, block, errors
    day_session += 1

'''I must create a file for each session to store each block's RTs, responses (infor in var), # of errors, nback_level
'''


#some test prints
print order
print responses

win.close()