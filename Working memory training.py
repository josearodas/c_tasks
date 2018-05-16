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

file_name = id_participant+'_n-back_'+date+'.csv'
data_headings = 'trial;n-level;Details'


#Create the file to insert each trial data
np.savetxt(
    file_name,
    ['trial;n-level;details'],
    fmt = '%s',
    delimiter = ';',
    newline = '\n'
    )

win = visual.Window(
        fullscr = True,
        color=(1,1,1),
        units = 'pix',
        size = (800,600)
        )

txt_menu = visual.TextStim(win = win, color=(-1,-1,-1))
txt_session_t = visual.TextStim(win = win, pos=(0,-250),color = (-1,-1,-1))

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

nback_level_file = open('nback_system','r')

nback_level = int(nback_level_file.read())
nback_level_file.close()
nback_history = []   #this var will store each n-back level within the session to create a mean n-back level for each session in order to present it on a graph


for session_trial in range(20):
    
    order = ['b2']*nback_level
    responses = []    #this var stores participants responses with RT; can be either correct (c), incorrect (i) or miss (m)
    errors = 0    #missess and incorrects are considered errors; this counter control the adaptive n-back

    block = block_creator(nback_level)
    
    txt_menu.text= 'Please choose one of the following options by pressing the given key:\n\n        s => Start a new trial block\n    esc => Quit'
    txt_session_t.text = 'Block %s\nN-back level = %s' % ((session_trial+1), nback_level)
    
    while True:
        txt_menu.draw()
        txt_session_t.draw()
        win.flip()
        k = event.waitKeys()
        if 'escape' in k:
            #insert core for creating the data file
            core.quit()
        elif 's' in k:
            break
    
    grid.draw()
    win.flip()
    nback_history.append(nback_level)
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
    
    data_doc = open(file_name,'a')
    
    data_doc.write(str(session_trial+1))
    data_doc.write(';')
    data_doc.write(str(nback_level))
    data_doc.write(';')
    data_doc.write(str(responses))
    data_doc.write('\n')
    
    data_doc.close()
    
    #adjust the n-back level
    if errors > 5:
        if nback_level > 1:
            nback_level -= 1
    elif errors < 3:
        nback_level += 1
    
    with open('nback_system','w') as nback_level_file:
        nback_level_file.write(str(nback_level))
    
    #reset variables
    del order, responses, block, errors

'''I must create a file for each session to store each block's RTs, responses (infor in var), # of errors, nback_level
'''


#some test prints
print order
print responses

win.close()