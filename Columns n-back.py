#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:23 2018
@author: JARP

legend:
    0-> continue key
    1-> correct
    2-> miss
    3-> incorrect

The last n-level stored in files are the ones the participant could not perform 
well enough to progress to next leve. This data in theory should not be considered
for analysis as its performance is not adequate enough. This data is registered just
in case is found usefull for future analyses.

The task automatically increases the n-level if the participant has a mean score of
3 or more within all runs of each level and does not register an incorrect mean score
of 3 or more. Otherwise the task stops.

Different RTs should be observed between the 1back and >1-back. An increase in
the focus of attention should eliminate this difference.
"""

from __future__ import division

from psychopy import visual, core, data, event, gui
import numpy as np
import random
import pprint
import math


'''This will create the trials' block with six n-back repetitions'''
def block_creator(nback_level):
    
    block = []
    
    for n in range(20+nback_level): #create the basic block (with unwanted random n-back repetitions)
        block.append(random.choice(stim_pool).copy())
    
    block_len = len(block)
    
    for i in range(block_len - nback_level): #this section eliminate any unplanned n-back repetition
        prov_pool = [{'item':'1','x':0,'y':0},{'item':'2','x':0,'y':0},{'item':'3','x':0,'y':0},
        {'item':'4','x':0,'y':0},{'item':'5','x':0,'y':0},{'item':'6','x':0,'y':0},{'item':'7','x':0,'y':0},
        {'item':'8','x':0,'y':0},{'item':'9','x':0,'y':0}]
        if block[i] == block[i+nback_level]:
            prov_pool.remove(block[i]) #the pool without the current position
            del block[i] #the block without the unwanted trial
            block.insert(i, random.choice(prov_pool).copy())
    
    #the following section inserts 6 n-back repetition trials in the already cleaned block
    
    index_pool = []

    for ixpool in range(len(block)-nback_level): #creates a set of possible positions to insert the n-back trials
        index_pool.append(ixpool)

    for ii in range(6):
        trial_torep = random.choice(index_pool) #selects a random position x (a random trial)
        block.insert(trial_torep+nback_level, block[trial_torep].copy()) #create the duplicated trial after x position
        #print trial_torep    #this helps to identify the duplicated trials, do not serve any functional purpose
        del block[trial_torep+(nback_level+1)]   #delete the previous x+n trial
        
        if trial_torep >= nback_level and (trial_torep-nback_level) in index_pool: #in case tries to eliminate an item out of index
            index_pool.remove(trial_torep-nback_level) #eliminate the trial n-back so they not interfere in future dublications
            index_pool.remove(trial_torep) #eliminate the duplicated trial
        else:
            index_pool.remove(trial_torep)
            
    
    #the following section inserts the position to each item
    
    n_items = 20+nback_level
    n_rows = math.ceil(n_items/nback_level)
    y_pos = 0.9     #items will always start at the same position at the top of the screen
    
    pool_index = 0      #this var will control the index of items in the block in order to alter their position coordinates
    
    for i_cor in range(n_rows):     #this loop will insert the position coordinates of each item from the block
        x_distance = round((2/(nback_level+1)),2)      #the position of each column is adaptive in relation to the nback_level
        x_pos = -1 + x_distance
        for iii in range(nback_level):
            block[pool_index]['y'] = y_pos
            block[pool_index]['x'] = x_pos
            x_pos += x_distance
            if pool_index == (len(block)-1):    #avoids IndexError with incompleted rows like in n=3
                break
            pool_index += 1
        y_pos -= 0.09
        
    
    del index_pool
    
    return block


my_dlg = gui.Dlg(title='Assessment')
my_dlg.addField('Participant:')
my_dlg.addField('Session:', choices=['pre','post','follow'])
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

id_participant = str(my_dlg.data[0])
phase = str(my_dlg.data[1])

date = data.getDateStr()

file_name = id_participant+'_colnback_'+date+phase+'.csv'


#save trial info into file
np.savetxt(
    file_name,
    ['n_back, resp, RT'],
    fmt = '%s',
    newline = '\n'
    )

win = visual.Window(fullscr=True,color=(-1,-1,-1),units='norm')
win.mouseVisible = False

txt_instr = visual.TextStim(win, color = (1,1,1))
txt_stim = visual.TextStim(win, color = (1,1,1), height = 0.08)
txt_feedback = visual.TextStim(win, color = (1,1,1), alignHoriz = 'center', height = 0.08)
img_ex1a = visual.ImageStim(win,'Cols-example/col-ex1-1.png',units='norm',pos=(0,-0.15))
img_ex1b = visual.ImageStim(win,'Cols-example/col-ex1-2.png',units='norm',pos=(0,-0.15))
img_ex1c = visual.ImageStim(win,'Cols-example/col-ex1-3.png',units='norm',pos=(0,-0.15))
img_ex1d = visual.ImageStim(win,'Cols-example/col-ex1-4.png',units='norm',pos=(0,-0.15))
img_ex1e = visual.ImageStim(win,'Cols-example/col-ex1-5.png',units='norm',pos=(0,-0.15))
img_ex1f = visual.ImageStim(win,'Cols-example/col-ex1-6.png',units='norm',pos=(0,-0.15))
img_ex21a = visual.ImageStim(win,'Cols-example/col-ex2-1a.png',units='norm',pos=(0,-0.5))
img_ex21b = visual.ImageStim(win,'Cols-example/col-ex2-1b.png',units='norm',pos=(0,-0.5))
img_ex22a = visual.ImageStim(win,'Cols-example/col-ex2-2a.png',units='norm',pos=(0,-0.5))
img_ex22b = visual.ImageStim(win,'Cols-example/col-ex2-2b.png',units='norm',pos=(0,-0.5))
img_ex23a = visual.ImageStim(win,'Cols-example/col-ex2-3a.png',units='norm',pos=(0,-0.5))
img_ex23b = visual.ImageStim(win,'Cols-example/col-ex2-3b.png',units='norm',pos=(0,-0.5))
img_ex24a = visual.ImageStim(win,'Cols-example/col-ex2-4a.png',units='norm',pos=(0,-0.5))
img_ex24b = visual.ImageStim(win,'Cols-example/col-ex2-4b.png',units='norm',pos=(0,-0.5))
img_ex25a = visual.ImageStim(win,'Cols-example/col-ex2-5a.png',units='norm',pos=(0,-0.5))
img_ex25b = visual.ImageStim(win,'Cols-example/col-ex2-5b.png',units='norm',pos=(0,-0.5))
img_ex26a = visual.ImageStim(win,'Cols-example/col-ex2-6a.png',units='norm',pos=(0,-0.5))
img_ex26b = visual.ImageStim(win,'Cols-example/col-ex2-6b.png',units='norm',pos=(0,-0.5))
img_ex27a = visual.ImageStim(win,'Cols-example/col-ex2-7a.png',units='norm',pos=(0,-0.5))
img_ex27b = visual.ImageStim(win,'Cols-example/col-ex2-7b.png',units='norm',pos=(0,-0.5))
img_ex28a = visual.ImageStim(win,'Cols-example/col-ex2-8a.png',units='norm',pos=(0,-0.5))
img_ex28b = visual.ImageStim(win,'Cols-example/col-ex2-8b.png',units='norm',pos=(0,-0.5))
img_ex29a = visual.ImageStim(win,'Cols-example/col-ex2-9a.png',units='norm',pos=(0,-0.5))
img_ex29b = visual.ImageStim(win,'Cols-example/col-ex2-9b.png',units='norm',pos=(0,-0.5))

img_examples1 = [img_ex1a,img_ex1b,img_ex1c,img_ex1d,img_ex1e,img_ex1f]
img_examples2 = [{'img':img_ex21a,'dur':55},{'img':img_ex21b,'dur':15},{'img':img_ex22a,'dur':55},{'img':img_ex22b,'dur':15},
    {'img':img_ex23a,'dur':55},{'img':img_ex23b,'dur':15},{'img':img_ex24a,'dur':55},{'img':img_ex24b,'dur':15},
    {'img':img_ex25a,'dur':55},{'img':img_ex25b,'dur':15},{'img':img_ex26a,'dur':55},{'img':img_ex26b,'dur':15},
    {'img':img_ex27a,'dur':55},{'img':img_ex27b,'dur':15},{'img':img_ex28a,'dur':55},{'img':img_ex28b,'dur':15},
    {'img':img_ex29a,'dur':55},{'img':img_ex29b,'dur':15}]

out_corr = []
clock = core.Clock()

main_output = []

#Instructions
part_resp = 0
txt_instr.text = "In the following task you will be presented with single digit numbers appearing in a reading order within an imaginary grid (with columns which are vertical and rows which are horizontal). Each digit will appear only one at a time and you will have to remember its horizontal position (column).\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nPlease press the <space> bar to continue with the instructions."
txt_instr.wrapWidth = 1.5
txt_instr.height = 0.07
txt_instr.pos = (0,0)
while part_resp == 0:
    for curr_img in img_examples1:
        if part_resp == 0:
            for i in range(50):
                txt_instr.draw()
                curr_img.draw()
                if event.getKeys(keyList=['space']): part_resp=1
                win.flip()
        else: break
win.flip()

event.clearEvents()

txt_instr.text = "If the same digit appears in the same column during the next row you will have to indicate that a match has occurred by pressing the <m> key. This will also make the next digit to appear. If there is no match between digits you press the <z> key to make the next digit appear (new digits will not be presented unless you press either the <z> or the <m> key).\n\n     m --> match\n     z  --> no match.\n\nPress the <space> bar to see an example (you will also be able to practice before starting the task)."
txt_instr.wrapWidth = 1.5
txt_instr.height = 0.07
txt_instr.pos = (0,0)
txt_instr.draw()
win.flip()
event.waitKeys(keyList=['space'])


txt_instr.text = "Look closely at the animation. Each number is presented after a key has been pressed. Notice that during the second number of the last row the key <m> is pressed. This is because this number (8) is the same that the one just one row above (8 as well).\n\nDon't worry if it is not very clear yet. We'll do some practice before starting.\n\nPress the <space> bar to start the practice trial. We'll begin with just one column."
txt_instr.wrapWidth = 1.5
txt_instr.height = 0.07
txt_instr.pos = (0,0.5)

event.clearEvents()

part_resp = 0
while part_resp == 0:
    for curr_img in img_examples2:
        if part_resp == 0:
            for i in range(curr_img['dur']):
                curr_img['img'].draw()
                txt_instr.draw()
                if event.getKeys(keyList=['space']): part_resp=1
                win.flip()
        else: break
win.flip()


stim_pool = [{'item':'1','x':0,'y':0},{'item':'2','x':0,'y':0},{'item':'3','x':0,'y':0},
            {'item':'4','x':0,'y':0},{'item':'5','x':0,'y':0},{'item':'6','x':0,'y':0},{'item':'7','x':0,'y':0},
            {'item':'8','x':0,'y':0},{'item':'9','x':0,'y':0}]

pract_quit = 0

nback_level = 1

while pract_quit == 0:
    block_prac = block_creator(nback_level)
    order = ['empty']*nback_level
    for i in block_prac:
        order.append(i['item'])
        txt_stim.text = i['item']
        txt_stim.pos = (i['x'],i['y'])
        txt_stim.draw()
        clock.reset()
        win.flip()
        
        key_pressed = event.waitKeys(keyList=['z','m'],timeStamped = clock)    #<m> stands for repeat and <z> for continue
        
        if len(order) >= nback_level:    #1-> correct; 2-> miss; 3-> incorrect
            if order[-1] == order[-2] and key_pressed[-1][0] == 'm':
                txt_feedback.text = 'That was right! This digit appeared just above a few moments ago.'
                txt_feedback.draw()
                win.flip()
                core.wait(3)
            elif order[-1] == order[-2] and key_pressed[-1][0] == 'z':
                txt_feedback.text = 'You just missed a match.'
                txt_feedback.draw()
                win.flip()
                core.wait(2)
            elif order[-1] != order[-2] and key_pressed[-1][0] == 'm':
                txt_feedback.text = 'There was no match on that one'
                txt_feedback.draw()
                win.flip()
                core.wait(2)
    
    txt_instr.text = 'Would you like to practice with two columns?\n\n    a--> yes\n    k-->no\n\n\nIf you feel the task is not clear yet, please do not hesitate to ask the researcher.'
    txt_instr.pos=(0,0)
    txt_instr.draw()
    win.flip()
    
    repeat_pract = event.waitKeys(keyList=['a','k'])
    if 'k' in repeat_pract: break
    
    del order
    
    #practice trial with n=2; this just appears if the participant decides to
    nback_level = 2
    order = ['empty']*nback_level
    block_prac = block_creator(nback_level)
    for i in block_prac:
        order.append(i['item'])
        txt_stim.text = i['item']
        txt_stim.pos = (i['x'],i['y'])
        txt_stim.draw()
        clock.reset()
        win.flip()
        
        key_pressed = event.waitKeys(keyList=['z','m'],timeStamped = clock)    #<m> stands for repeat and <z> for continue
        
        if len(order) >= nback_level:    #1-> correct; 2-> miss; 3-> incorrect
            if order[-1] == order[-3] and key_pressed[-1][0] == 'm':
                txt_feedback.text = 'That was right! This digit appeared just above a few moments ago.'
                txt_feedback.draw()
                win.flip()
                core.wait(3)
            elif order[-1] == order[-3] and key_pressed[-1][0] == 'z':
                txt_feedback.text = 'You just missed a match.'
                txt_feedback.draw()
                win.flip()
                core.wait(2)
            elif order[-1] != order[-3] and key_pressed[-1][0] == 'm':
                txt_feedback.text = 'There was no match on that one'
                txt_feedback.draw()
                win.flip()
                core.wait(2)
    pract_quit = 1

del order

txt_instr.text = 'On the practice trials you did before only one or two columns were presented, but bear in mind that the trials will start with just one column and progress with even more than two.\n\nPress the <space> bar in order to start the task. Try to be fast when responding. From now on there will not be any feedback.\n\nIf you feel tired during the task you will be able to have some rests between the blocks of trials.'
txt_instr.draw()
win.flip()

event.waitKeys(keyList=['space'])

nback_level = 1

#Main program
while True:
    stim_pool = [{'item':'1','x':0,'y':0},{'item':'2','x':0,'y':0},{'item':'3','x':0,'y':0},
            {'item':'4','x':0,'y':0},{'item':'5','x':0,'y':0},{'item':'6','x':0,'y':0},{'item':'7','x':0,'y':0},
            {'item':'8','x':0,'y':0},{'item':'9','x':0,'y':0}]
    
    prov_correct = [nback_level]
    prov_error = []
    
    for i in range(5):
        block = block_creator(nback_level)
        
        order = ['empty']*nback_level
        local_output = []
        
        corr_counter = 0
        err_counter = 0
        
        for i in block:
            order.append(i['item'])
            txt_stim.text = i['item']
            txt_stim.pos = (i['x'],i['y'])
            txt_stim.draw()
            clock.reset()
            win.flip()
            
            key_pressed = event.waitKeys(keyList=['z','m'],timeStamped = clock)    #<m> stands for repeat and <z> for continue
            
            if len(order) >= nback_level:    #1-> correct; 2-> miss; 3-> incorrect
                if order[-1] == order[(nback_level+1)*-1] and key_pressed[-1][0] == 'm':
                    corr_counter += 1
                    local_output.append([nback_level,1,key_pressed[-1][1]])
                elif order[-1] == order[(nback_level+1)*-1] and key_pressed[-1][0] == 'z':
                    local_output.append([nback_level,2,key_pressed[-1][1]])
                elif order[-1] != order[(nback_level+1)*-1] and key_pressed[-1][0] == 'm':
                    err_counter += 1
                    local_output.append([nback_level,3,key_pressed[-1][1]])
                else:
                    local_output.append([nback_level,0,key_pressed[-1][1]])
        
        prov_correct.append(corr_counter)
        
        #update file data
        data_doc = open(file_name, 'a')
        
        for item in local_output:
            str_item = str(item)
            data_doc.write(str_item[1:-1])
            data_doc.write('\n')
        
        data_doc.close()
        
        
        txt_instr.text = "Please press the <space> bar in order to continue.\n\n\nRemember:\nm --> match\nz--> continue."
        txt_instr.draw()
        win.flip()
        
        event.waitKeys(keyList = ('space'))
        
        main_output.append(local_output)
        
        del order, local_output, block
    
    out_corr.append(prov_correct)
    
    if np.mean(prov_correct) < 3: break
    if np.mean(prov_error) > 3: break
    
    
    nback_level += 1

np.savetxt(file_name[:-4]+'_means.csv',out_corr, fmt='%i', delimiter=',',header='n-level,run1,run2,run3,run4,run5')

txt_instr.alignHoriz = 'center'
txt_instr.text = "The task has concluded. Thanks for participating\n\nPlease press the <space bar> to exit."
txt_instr.draw()
win.flip()

event.waitKeys(keyList = ['space'])

win.close()