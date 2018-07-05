# -*- coding: utf-8 -*-

"""
Created on Fry Apr 06 15:15 2018
@author: JARP

Stim is presented at 900ms. Register basic vars (commissions, omissions, rates, etc.) and a new one:
delayed responses. These are keypresses one stim after the target (because of a delayed response). 

IMPORTANT: in the summary file omissions do not include delayed responses but the raw file does. In the
latter file delayed responses are registered as omissions. This should be taken into consideration when
analyzing this data.

"""

from __future__ import division
from psychopy import visual, core, clock, event, gui, data, sound
import random
import numpy as np


numb_runsx = 22 #must be 20
numb_practx = 1 # must be 1 or 2

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
delayed_resp = 0
delayed_respls = []
allstim_presented = []


one_ogg = sound.Sound("ogg/one.ogg")
two_ogg = sound.Sound("ogg/two.ogg")
three_ogg = sound.Sound("ogg/three.ogg")
four_ogg = sound.Sound("ogg/four.ogg")
five_ogg = sound.Sound("ogg/five.ogg")
six_ogg = sound.Sound("ogg/six.ogg")
seven_ogg = sound.Sound("ogg/seven.ogg")
eight_ogg = sound.Sound("ogg/eight.ogg")
nine_ogg = sound.Sound("ogg/nine.ogg")


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
        

txt_instr.text = "Now that you have practiced a bit the real trials will begin. Remember to be accurate and not to miss any 'three'. Also keep in mind that if you are too slow to answer your key press might be computed for the next stimulus. This means that if you hear the number three but the key is pressed when the next number is being recited it will be computed as an error.\n\nPress any key to continue when you feel ready to start."
txt_instr.draw()
win.flip()

event.clearEvents()
event.waitKeys()
win.flip()
core.wait(2)

#the recorded trials
for i in range(numb_runsx): 
    curr_run = run_creatorX()
    presented_stim = [0]

    for stim in curr_run:
        
        if stim == one_ogg   : stim_innum = 1
        if stim == two_ogg   : stim_innum = 2
        if stim == three_ogg : stim_innum = 3
        if stim == four_ogg  : stim_innum = 4
        if stim == five_ogg  : stim_innum = 5
        if stim == six_ogg   : stim_innum = 6
        if stim == seven_ogg : stim_innum = 7
        if stim == eight_ogg : stim_innum = 8
        if stim == nine_ogg  : stim_innum = 9

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
        
        if stim_innum == 3 and key_pressed:
            correct_x.append(round(key_pressed[-1][1],3))
            total_x += 1
            allstim_presented.append(['cor',stim_innum,round(key_pressed[-1][1],3)])
        elif stim_innum == 3 and key_pressed == []:
            omissions_x += 1
            total_x += 1
            allstim_presented.append(['omi',stim_innum,0])
        elif stim_innum != 3 and presented_stim[-1] == 3 and key_pressed:
            delayed_resp += 1
            delayed_respls.append(round(key_pressed[-1][1],3))
            allstim_presented.append(['delay',stim_innum,round(key_pressed[-1][1],3)])
        elif stim_innum != 3 and key_pressed:
            commissions_x += 1
            commissionsls_x.append(round(key_pressed[-1][1],3))
            allstim_presented.append(['com',stim_innum,round(key_pressed[-1][1],3)])
        else:
            allstim_presented.append(['none',stim_innum,0])
        
        presented_stim.append(stim_innum)
        

notarg_x = 23*numb_runsx
omissionsrate_xsub = omissions_x-delayed_resp
omissionsrate_x = omissionsrate_xsub / total_x
commissionsrate_x = commissions_x/notarg_x
mean_correctx_RT = np.mean(correct_x)
mean_commissionsx_RT = np.mean(commissionsls_x)
mean_delayed = np.mean(delayed_respls)
delayed_rate = delayed_resp/total_x


np.savetxt(file_name,[('targets','omissions','omissions_rate','notargets','commissions','commissions_rate','delayed',
    'delayed_rate','meanRT_corr','meanRT_comm','delayed_RT'),
    (total_x, omissions_x-delayed_resp, omissionsrate_x, notarg_x, commissions_x, commissionsrate_x, delayed_resp,
    delayed_rate, mean_correctx_RT, mean_commissionsx_RT, mean_delayed)],delimiter=',',fmt='%s')

raw_rtx = 'corrRT_X,'+str(correct_x)[1:-1]
raw_comx = 'Commissions_X,'+str(commissionsls_x)[1:-1]


np.savetxt(file_name[:-4]+'_raw.csv',allstim_presented,fmt='%s',delimiter=',',header='type,stim,RT')

txt_instr.text = 'The task has concluded.\n\nThanks for participating. Please press any key.'
txt_instr.draw()
win.flip()

event.clearEvents()
event.waitKeys()

win.close()
