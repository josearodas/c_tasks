# -*- coding: utf-8 -*-

"""
Created on Fry Apr 06 15:15 2018
@author: JARP
The task will be created according to the description provided in Millisecond.com, based on the original
study of Rosvold, et al. (1956).
Should I increase the rate of appearance of A without a following X?
Each run contains 31 items and from those: 8 are targets in the X cond and 6 for the AX cond
For the second modality of the task (AX) three types of commissions are registered: nox, when an 'A' is
presented, a key is pressed after it but the letter is not an 'X'; noa, when the key is pressed on an 'X'
not preceded by an 'A'; and nxna, when a key is pressed but the letter is not an 'X' and is not preceded by
an 'A'.

The no targets are  automatically counted for the output file on the 'AX' modality.
Responses given the first 100ms after stim presentation are not registered, as they are considered to 
belong to previous stimulus (anticipatory). Search for relevant research for more explanations. Studies
related to SART have reported this (mostly because of the nature of the task).
"""

from __future__ import division
from psychopy import visual, core, clock, event, gui, data
import random
import numpy as np


numb_runsx = 15 #must be 15
numb_runsax = 15 # must be 15
numb_practx = 2 # must be 2
numb_practax = 2 # must be 2
rest_period = 90   #this is between the two formats of the task; is in sec; should be 90




def run_creatorX():
    letter_pool = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','C','V','B','N','M']
    run = []
    
    for i in range(23):
        run.append(random.choice(letter_pool))
    
    counter = 0
    while counter < 8:
        rand_indx = random.randint(1,(len(run)-2))
        
        if ('X' is run[rand_indx] or 'X' is run[rand_indx+1] or 'X' is run[rand_indx-1]):
            continue
        else:
            run.insert(rand_indx,'X')
            counter += 1
    
    
    return run

def run_creatorAX():
    letter_pool = ['Q','W','E','R','T','Y','U','I','O','P','S','D','F','G','H','J','K','L','Z','C','V','B','N','M','A','A','A','X','X','X'] #in here the X is included as not target as well
    run = []
    indx_lst = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    
    for i in range(31):
        run.append(random.choice(letter_pool))
    
    counter = 0
    
    while counter < 6:
        rand_indx = random.choice(indx_lst[1:])
        
        del run[rand_indx]
        indx_lst.remove(rand_indx)
        run.insert(rand_indx,'X')
        del run[rand_indx-1]
        if rand_indx-1 in indx_lst:
            indx_lst.remove(rand_indx-1)
        run.insert(rand_indx-1,'A')
        if rand_indx+1 in indx_lst:
            indx_lst.remove(rand_indx+1)
        counter += 1
        
    return run

my_dlg = gui.Dlg(title='Assessment')
my_dlg.addField('Participant:')
my_dlg.addField('Session:',choices=['pre','post','follow'])
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

date = data.getDateStr()
id_participant = str(my_dlg.data[0])
session = str(my_dlg.data[1])

file_name = id_participant+'_CPT_'+date+'_'+session+'.csv'


win = visual.Window(units='pix',color=(-1,-1,-1), fullscr= True)
win.mouseVisible = False
txt_stim = visual.TextStim(win,color=(1,1,1),height=44)
txt_instr = visual.TextStim(win,color=(1,1,1),height=28,wrapWidth=900)
clk_rt = core.Clock()
clk_stim = core.Clock()

correct_x = []
total_x = 0
omissions_x = 0
commissions_x = 0
commissionsls_x = []
correct_ax = []
total_ax = 0
omissions_ax = 0
commissions_nxna = 0    #no x no a
commissions_nox = 0
commissions_noa = 0
commissionsls_nox = []
commissionsls_noa = []
commissionsls_nxna = []
notarg_ax = 0

##############     FIRST PART -- PHASE "X"     ####################
event.clearEvents()
txt_instr.text = "In this task a string of letters will appear on the center of the screen one by one on a fast pace. You will have to press the <space> key each time the letter 'X' appears and to refrain from pressing the key for any other letter.\n\nWe'll do some pracice trials before beginning the real ones.\n\nPlease press any key to start. "
txt_instr.draw()
win.flip()

event.waitKeys()
win.flip()
core.wait(2)

#practice trials
for i in range(numb_practx): 
    curr_run = run_creatorX()
    for stim in curr_run:
        txt_stim.text = stim
        clk_stim.reset()
        clk_rt.reset()
        
        event.clearEvents()
        
        while clk_stim.getTime() < 0.690:
            txt_stim.draw()
            win.flip()
        
        key_pressed = event.getKeys(keyList='space',timeStamped=clk_rt)
        
        if stim == 'X' and key_pressed == []:
            txt_instr.text = "That's a miss..."
            txt_instr.draw()
            win.flip()
            core.wait(1)
        elif stim != 'X' and key_pressed:
            txt_instr.text = "That was not an 'X'"
            txt_instr.draw()
            win.flip()
            core.wait(1)
        
        while clk_stim.getTime() < 0.92:
            win.flip()

txt_instr.text = "Now that you have practiced a bit the real trials will begin. Remember to be accurate and not to miss any 'X'.\n\nPress any key to continue."
txt_instr.draw()
win.flip()

event.clearEvents()
event.waitKeys()
win.flip()
core.wait(2)

#the recorded trials
for i in range(numb_runsx): #10 for a short version and 20 for a long one; I'll use an in-between so should be set to 15
    curr_run = run_creatorX()
    for stim in curr_run:
        txt_stim.text = stim
        clk_stim.reset()
        clk_rt.reset()
        
        event.clearEvents()
        
        while clk_stim.getTime() < 0.1:
            txt_stim.draw()
            win.flip()
        event.clearEvents()
        while clk_stim.getTime() < 0.690:
            txt_stim.draw()
            win.flip()
        
        key_pressed = event.getKeys(keyList='space',timeStamped=clk_rt)
        
        if stim == 'X' and key_pressed:
            correct_x.append(round(key_pressed[-1][1],3))
            total_x += 1
        elif stim == 'X' and key_pressed == []:
            omissions_x += 1
            total_x += 1
        elif stim != 'X' and key_pressed:
            commissions_x += 1
            commissionsls_x.append(round(key_pressed[-1][1],3))
        
        while clk_stim.getTime() < 0.92:
            win.flip()
        
event.clearEvents()
txt_instr.text = "You have concluded the first part of the task. Please give yourself a two minutes break in order to start the second part. After two minutes the new instructions will appear automatically."
txt_instr.draw()
win.flip()

core.wait(rest_period)

event.clearEvents()
txt_instr.text = "In the following section the task is very similiar, although you will only have to press the <space> key when the 'X' is preceded by an 'A'. This means you will have to pay more attention to the letters on the screen. We'll do some practice before starting.\n\nPlease press any key to continue."
txt_instr.draw()
win.flip()

event.waitKeys()
win.flip()
core.wait(2)


##############     SECOND PART -- PHASE "AX"     ################
#practice trials
for i in range(numb_practax):
    curr_run = run_creatorAX()
    indx_counter = 0
    previous_letter= []
    
    for stim in curr_run:
        txt_stim.text = stim
        clk_stim.reset()
        clk_rt.reset()
        
        event.clearEvents()
        
        while clk_stim.getTime() < 0.690:
            txt_stim.draw()
            win.flip()
        
        key_pressed = event.getKeys(keyList='space',timeStamped=clk_rt)
        
        if indx_counter > 0:
            if stim == 'X' and key_pressed == [] and previous_letter[-1] == 'A':
                txt_instr.text = "That's a miss..."
                txt_instr.draw()
                win.flip()
                core.wait(1)
            elif stim != 'X' and key_pressed:
                txt_instr.text = "That was not an 'X'"
                txt_instr.draw()
                win.flip()
                core.wait(1)
            elif stim == 'X' and key_pressed and previous_letter[-1] != 'A':
                txt_instr.text = "No 'A' before this 'X'"
                txt_instr.draw()
                win.flip()
                core.wait(1)
        
        indx_counter += 1
        previous_letter.append(stim)
        
        while clk_stim.getTime() < 0.92:
            win.flip()

event.clearEvents()
txt_instr.text = "Now that you have some practice we'll begin the real task.\n\nPlease press any key to start whenever you feel ready."
txt_instr.draw()
win.flip()

event.waitKeys()
win.flip()
core.wait(2)

for i in range(numb_runsax): 
    curr_run = run_creatorAX()
    indx_counter = 0
    previous_letter= []
    
    for stim in curr_run:
        txt_stim.text = stim
        clk_stim.reset()
        clk_rt.reset()
        
        event.clearEvents()
        
        while clk_stim.getTime() < 0.1:
            txt_stim.draw()
            win.flip()
        event.clearEvents()
        while clk_stim.getTime() < 0.690:
            txt_stim.draw()
            win.flip()
        
        key_pressed = event.getKeys(keyList='space',timeStamped=clk_rt)
        
        if indx_counter > 0:
            if stim == 'X' and key_pressed and previous_letter[-1] == 'A':
                correct_ax.append(round(key_pressed[-1][1],3))
                total_ax += 1
            elif stim == 'X' and key_pressed == [] and previous_letter[-1] == 'A':
                omissions_ax += 1
                total_ax += 1
            elif stim == 'X' and key_pressed and previous_letter[-1] != 'A':
                commissions_noa += 1
                notarg_ax += 1
                commissionsls_noa.append(round(key_pressed[-1][1],3))
            elif key_pressed and previous_letter[-1] == 'A' and stim != 'X':
                commissions_nox += 1
                notarg_ax += 1
                commissionsls_nox.append(round(key_pressed[-1][1],3))
            elif stim != 'X' and key_pressed:
                commissions_nxna += 1
                notarg_ax += 1
                commissionsls_nxna.append(round(key_pressed[-1][1],3))
            else:
                notarg_ax += 1
        
        indx_counter += 1
        previous_letter.append(stim)
        
        while clk_stim.getTime() < 0.92:
            win.flip()

omissionsrate_x = omissions_x/total_x
commissionsrate_x = commissions_x/23
omissionsrate_ax = omissions_ax/total_ax
commissionsrate_ax = (commissions_nox+commissions_noa+commissions_nxna)/25
mean_correctx_RT = np.mean(correct_x)
mean_correctax_RT = np.mean(correct_ax)
mean_commissionsna_RT = np.mean(commissionsls_noa)
mean_commissionsnx_RT = np.mean(commissionsls_nox)
mean_commissionsx_RT = np.mean(commissionsls_x)
notarg_x = 23*numb_runsx

np.savetxt(file_name,[('targets_x','omissions_x','omissionsrate_x','notargets_x','commissions_x','commissionsrate_x',
    'targets_ax','omissions_ax','omissionsrate_ax','notargets_ax','commissions_nox','commissions_noa','commissions_nxna',
    'commissionsrate_nxna','meanRT_corrX','meanRT_corrAX','meanRT_commX','meanRT_commNoX','meanRT_commNoA'),
    (total_x,omissions_x,omissionsrate_x,notarg_x,commissions_x,commissionsrate_x,total_ax,omissions_ax,omissionsrate_ax,
    notarg_ax,commissions_nox,commissions_noa,commissions_nxna,commissionsrate_ax,mean_correctx_RT,mean_correctax_RT,
    mean_commissionsx_RT,mean_commissionsnx_RT,mean_commissionsna_RT)],delimiter=',',fmt='%s')

raw_rtx = 'RT_X,'+str(correct_x)[1:-1]
raw_rtax = 'RT_AX,'+str(correct_ax)[1:-1]
raw_comx = 'Commissions_X,'+str(commissionsls_x)[1:-1]
raw_comna = 'Commissions_noa,'+str(commissionsls_noa)[1:-1]
raw_comnx = 'Commissions_nox,'+str(commissionsls_nox)[1:-1]
raw_comnanx = 'Commissions_nxna,'+str(commissionsls_nxna)[1:-1]

np.savetxt(file_name[:-4]+'_raw.csv',[raw_rtx,raw_rtax,raw_comx,raw_comna,raw_comnx,raw_comnanx],fmt='%s',delimiter=',')

txt_instr.text = 'The task has concluded.\n\nThanks for participating. Please press any key.'
txt_instr.draw()
win.flip()

event.clearEvents()
event.waitKeys()

win.close()