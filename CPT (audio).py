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
belong to previous stimulus (anticipatory). 

This version has been modified to an audio format. The number three represents the X and the seven the A.
The AX condition has been removed as apparently it is too easy. An extra measure has been included to count
delayed responses (when a key is pressed one number delayed; not sure what this means yet...)
"""

from __future__ import division
from psychopy import visual, core, clock, event, gui, data, sound
import random
import numpy as np


numb_runsx = 2 #must be 15
numb_runsax = 10 # must be 15
numb_practx = 1 # must be 2
numb_practax = 1 # must be 2
rest_period = 60   #this is between the two formats of the task; is in sec; should be 60


def run_creatorX(): #create the x run (string of letters with X targets)
    stim_pool = [one_ogg,two_ogg,four_ogg,five_ogg,six_ogg,seven_ogg,eight_ogg,nine_ogg]
    run = []
    
    for i in range(23):
        run.append(random.choice(stim_pool)) #create a basic no-target string
    
    counter = 0
    while counter < 8: #insert eight targets in the no-target string (string length=31)
        rand_indx = random.randint(1,(len(run)-2)) #select random positions in the no-target string
        
        if (three_ogg is run[rand_indx] or three_ogg is run[rand_indx+1] or three_ogg is run[rand_indx-1]):
            continue
        else:
            run.insert(rand_indx,three_ogg)
            counter += 1
    
    
    return run

def run_creatorAX():
    stim_pool = [one_ogg,two_ogg,three_ogg,four_ogg,five_ogg,six_ogg,seven_ogg,eight_ogg,nine_ogg] #in here the X is included as no-target as well
    run = []
    indx_lst = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    
    for i in range(31):
        run.append(random.choice(stim_pool))
    
    counter = 0
    
    while counter < 6:
        rand_indx = random.choice(indx_lst[1:])
        
        del run[rand_indx] #delete a random item
        indx_lst.remove(rand_indx) #delete the corresponding index
        run.insert(rand_indx,three_ogg)
        del run[rand_indx-1] #del previous item
        if rand_indx-1 in indx_lst: #to prevent and error from deleting an item that does not exist
            indx_lst.remove(rand_indx-1)
        run.insert(rand_indx-1,seven_ogg)
        if rand_indx+1 in indx_lst: #the deletion of indx+1 will prevent overlaping between target stim insertion in list
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
txt_stim = visual.TextStim(win,color=(1,1,1),height=84)
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


one_ogg = sound.Sound("ogg/one.ogg")
two_ogg = sound.Sound("ogg/two.ogg")
three_ogg = sound.Sound("ogg/three.ogg")
four_ogg = sound.Sound("ogg/four.ogg")
five_ogg = sound.Sound("ogg/five.ogg")
six_ogg = sound.Sound("ogg/six.ogg")
seven_ogg = sound.Sound("ogg/seven.ogg")
eight_ogg = sound.Sound("ogg/eight.ogg")
nine_ogg = sound.Sound("ogg/nine.ogg")


##############     FIRST PART -- PHASE "X"     ####################
event.clearEvents()
txt_instr.text = "In this task you will hear a string of numbers one by one. You will have to press the <space> key each time you hear the number 'three' and to refrain from pressing the key for any other number.\n\nWe'll do some pracice trials before beginning the real ones.\n\nPlease press any key to start. "
txt_instr.draw()
win.flip()

event.waitKeys()
win.flip()
core.wait(2)

#practice trials
for i in range(numb_practx): 
    curr_run = run_creatorX()
    for stim in curr_run:
        clk_stim.reset()
        clk_rt.reset()
        
        event.clearEvents()
        stim.play()
        while clk_stim.getTime() < 0.9:
            win.flip()
        
        key_pressed = event.getKeys(keyList='space',timeStamped=clk_rt)
        
        if stim == three_ogg and key_pressed == []:
            txt_instr.text = "That's a miss..."
            txt_instr.draw()
            win.flip()
            core.wait(1)
        elif stim != three_ogg and key_pressed:
            txt_instr.text = "That was not a 'three'"
            txt_instr.draw()
            win.flip()
            core.wait(1)
        

txt_instr.text = "Now that you have practiced a bit the real trials will begin. Remember to be accurate and not to miss any 'three'.\n\nPress any key to continue."
txt_instr.draw()
win.flip()

event.clearEvents()
event.waitKeys()
win.flip()
core.wait(2)

#the recorded trials
for i in range(numb_runsx): 
    curr_run = run_creatorX()
    for stim in curr_run:
        clk_stim.reset()
        clk_rt.reset()
        
        event.clearEvents()
        stim.play()

        while clk_stim.getTime() < 0.1: #this prevent to record delayed answers (from previous trial)
            win.flip()
        event.clearEvents()
        while clk_stim.getTime() < 0.9:
            win.flip()
        
        key_pressed = event.getKeys(keyList='space',timeStamped=clk_rt)
        
        if stim == three_ogg and key_pressed:
            correct_x.append(round(key_pressed[-1][1],3))
            total_x += 1
        elif stim == three_ogg and key_pressed == []:
            omissions_x += 1
            total_x += 1
        elif stim != three_ogg and key_pressed:
            commissions_x += 1
            commissionsls_x.append(round(key_pressed[-1][1],3))
        
'''
event.clearEvents()
txt_instr.text = "You have concluded the first part of the task. Please give yourself a one minute break in order to start the second part. After this the new instructions will appear automatically."
txt_instr.draw()
win.flip()

core.wait(rest_period)

event.clearEvents()
txt_instr.text = "In the following section the task is very similiar, although you will only have to press the <space> key when the 'three' is preceded by a 'seven'. This means you will have to pay more attention to the numbers. We'll do some practice before starting.\n\nPlease press any key to continue."
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
    previous_number= []
    
    for stim in curr_run:
        clk_stim.reset()
        clk_rt.reset()
        
        event.clearEvents()
        stim.play()
        while clk_stim.getTime() < 0.90:
            win.flip()
        
        key_pressed = event.getKeys(keyList='space',timeStamped=clk_rt)
        
        if indx_counter > 0:
            if stim == three_ogg and key_pressed == [] and previous_number[-1] == seven_ogg:
                txt_instr.text = "That's a miss..."
                txt_instr.draw()
                win.flip()
                core.wait(1)
            elif stim != three_ogg and key_pressed:
                txt_instr.text = "That was not a 'three'"
                txt_instr.draw()
                win.flip()
                core.wait(1)
            elif stim == three_ogg and key_pressed and previous_number[-1] != seven_ogg:
                txt_instr.text = "No 'seven' before this 'three'"
                txt_instr.draw()
                win.flip()
                core.wait(1)
        
        indx_counter += 1
        previous_number.append(stim)


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
    previous_number= []
    
    for stim in curr_run:
        clk_stim.reset()
        clk_rt.reset()
        
        event.clearEvents()
        stim.play()

        while clk_stim.getTime() < 0.1:
            win.flip()
        event.clearEvents()
        while clk_stim.getTime() < 0.9:
            win.flip()
        
        key_pressed = event.getKeys(keyList='space',timeStamped=clk_rt)
        
        if indx_counter > 0:
            if stim == three_ogg and key_pressed and previous_number[-1] == seven_ogg:
                correct_ax.append(round(key_pressed[-1][1],3))
                total_ax += 1
            elif stim == three_ogg and key_pressed == [] and previous_number[-1] == seven_ogg:
                omissions_ax += 1
                total_ax += 1
            elif stim == three_ogg and key_pressed and previous_number[-1] != seven_ogg:
                commissions_noa += 1
                notarg_ax += 1
                commissionsls_noa.append(round(key_pressed[-1][1],3))
            elif key_pressed and previous_number[-1] == seven_ogg and stim != three_ogg:
                commissions_nox += 1
                notarg_ax += 1
                commissionsls_nox.append(round(key_pressed[-1][1],3))
            elif stim != three_ogg and key_pressed:
                commissions_nxna += 1
                notarg_ax += 1
                commissionsls_nxna.append(round(key_pressed[-1][1],3))
            else:
                notarg_ax += 1
        
        indx_counter += 1
        previous_number.append(stim)
'''
notarg_x = 23*numb_runsx
omissionsrate_x = omissions_x/total_x
commissionsrate_x = commissions_x/notarg_x
#omissionsrate_ax = omissions_ax/total_ax
#commissionsrate_ax = (commissions_nox+commissions_noa+commissions_nxna)/notarg_ax
mean_correctx_RT = np.mean(correct_x)
#mean_correctax_RT = np.mean(correct_ax)
#mean_commissionsna_RT = np.mean(commissionsls_noa)
#mean_commissionsnx_RT = np.mean(commissionsls_nox)
mean_commissionsx_RT = np.mean(commissionsls_x)


np.savetxt(file_name,[('targets_x','omissions_x','omissionsrate_x','notargets_x','commissions_x','commissionsrate_x',
    'meanRT_corrX','meanRT_commX'),
    (total_x,omissions_x,omissionsrate_x,notarg_x,commissions_x,commissionsrate_x,mean_correctx_RT,
    mean_commissionsx_RT)],delimiter=',',fmt='%s')

raw_rtx = 'corrRT_X,'+str(correct_x)[1:-1]
#raw_rtax = 'corrRT_AX,'+str(correct_ax)[1:-1]
raw_comx = 'Commissions_X,'+str(commissionsls_x)[1:-1]
#raw_comna = 'Commissions_noa,'+str(commissionsls_noa)[1:-1]
#raw_comnx = 'Commissions_nox,'+str(commissionsls_nox)[1:-1]
#raw_comnanx = 'Commissions_nxna,'+str(commissionsls_nxna)[1:-1]

np.savetxt(file_name[:-4]+'_raw.csv',[raw_rtx,raw_comx],fmt='%s',delimiter=',')

txt_instr.text = 'The task has concluded.\n\nThanks for participating. Please press any key.'
txt_instr.draw()
win.flip()

event.clearEvents()
event.waitKeys()

win.close()
