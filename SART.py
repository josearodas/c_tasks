#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 11:38 2017

@author: Jarp

SART
The test is based on the description provided in Cheyne et al. (2009)
This is a test to assess sustained attention.

"""
from __future__ import division
from psychopy import visual, event, core, gui, data
import datetime
import random
import numpy
import pprint


num_trials = 25          #must be 25
num_practrial = 3       #3 is ok


my_dlg = gui.Dlg(title = 'Assessment')
my_dlg.addField('Participant:')
my_dlg.addField('Session:', choices = ['pre', 'post','follow'])
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

id_participant = str(my_dlg.data[0])
date = data.getDateStr()
session = str(my_dlg.data[1])

file_name = id_participant+'_SART_'+date+'_'+session+'.csv'


win = visual.Window(units='pix',fullscr=True,color = (-1,-1,-1))
txt_general = visual.TextStim(win,units='pix',wrapWidth = 800,color=(1,1,1),height = 32)
txt_stim = visual.TextStim(win,units='pix',color=(1,1,1))

#mask stimuli
txt_mask = visual.TextStim(win,color=(1,1,1),height=120,text = u'\u24CD')

#STABLISHING SOME VARIABLES
stimuli_sizes = [48,72,94,100,120]
numbers = [1,2,3,4,5,6,7,8,9]
stimuli = []
#variables to study
commissions = 0   #response in no-go trials
omissions = 0   #no response in go trials
anticipatory = 0   #RT less or equal to 100ms
ambiguous = 0   #RT more than 100ms and less than 200ms
suppressions = 0    #successful no go
correct = 0   #counter for valid and correct go trials
errors = 0   #omissions + commissions
#response times
RT_beforesuccessNOGO = []
RT_beforefailedNOGO = []
RTs = []
RTs_forcalcs = [] #a list of RT to compute speed before GOs and NOGOs
#trials counters
trial_n = 0
go_n = 0
nogo_n = 0

#randomize the stimuli size
for i in numbers:
    #rnd_size = random.choice(stimuli_sizes)
    stimuli.append({'number':i}) #, 'size':rnd_size})

#trial handlers
trials = data.TrialHandler(
    stimuli,
    num_trials,   #amount of trials, must be 25
    method = 'random',
    extraInfo = {'Participant:': id_participant, 'Session:':session,
                 'Date:':date}
)
trials.data.addDataType('RTs_all')

pract_trials = data.TrialHandler(
    stimuli,
    num_practrial,
    method = 'random'
)

k = []
RT = 0

#Clocks
resp_clock = core.Clock()
#trial_clock = core.Clock()
event.Mouse(visible=False)

#first and general instructions
txt_general.text = "In this task a series of digits will appear on the screen (one by one) for a very short period of time each. You will have to press the <space> bar each time any digit different than '3' appears, and supress from pressing any key if the number '3' appears. You will have some practice trials before starting the real task.\n\nPress the <space> bar to start the practice trials."
txt_general.draw()
win.flip()
event.waitKeys(keyList = ['space'])

#some practice trials
for i in pract_trials:
    txt_stim.text = i['number']
    txt_stim.height = random.choice(stimuli_sizes)
    
    #presenting the stimuli; for practice trials I don't need ms precision
    txt_stim.draw()
    win.flip()
    core.wait(0.25)
    txt_mask.draw()
    win.flip()
    core.wait(0.9)
    
    k = event.getKeys(keyList=['space','escape'], timeStamped = resp_clock)[-1:]
    if k == []:
        k=[(0,0)]
    
    if k[0][0] == 'escape':
        core.quit()
    elif k[0][1] != 0 and txt_stim.text == '3':   #a commission
        txt_general.text = "Remember not to press any key when '3' appears"
        txt_general.color = [1,-1,-1]
        txt_general.draw()
        win.flip()
        core.wait(2)
        txt_general.color = [1,1,1]
    elif k[0][1] == 0 and txt_stim.text != '3':
        txt_general.text = "Remember to press the <space> bar for each number different than '3'"
        txt_general.draw()
        win.flip()
        core.wait(3)

txt_general.color = [1,1,1]
txt_general.text = "Now that you have practiced a bit we may begin the recorded trials. If there is something you feel is not sufficiently clear feel free to ask the examiner about it.\n\nPress the <space> bar to start the task."
txt_general.draw()
win.flip()
event.waitKeys(keyList=['space'])


#recorded trials

for i in trials:
    txt_stim.text = i['number']
    txt_stim.height = random.choice(stimuli_sizes)
    resp_clock.reset(newT=0)
    
    while resp_clock.getTime() <= 0.250:
        txt_stim.draw()
        win.flip()
    while resp_clock.getTime() <= 1.150:
        txt_mask.draw()
        win.flip()
    win.flip()   #just to see how long the following calculations takes
    
    k = event.getKeys(keyList = ['space', 'escape'], timeStamped=resp_clock)[-1:]
    if k == []:
        k = [(0,0)]
    
    trials.data.add('RTs_all', k[0][1])
    trial_n += 1
    
    #the calculations for the variables
    if k[0][0] == 'escape':   #close task if esc key is pressed
        core.quit()
    elif k[0][1] > 0 and k[0][1] <= 0.1: #anticimpatory
        anticipatory += 1
        if txt_stim.text == '3':
            nogo_n += 1
        else:
            go_n += 1
    elif k[0][1] != 0 and txt_stim.text == '3': #failed nogo
        commissions += 1
        errors += 1
        nogo_n += 1
        if len(RTs_forcalcs) > 3 and 0 not in RTs_forcalcs[-4:]: #this will copute the mean RT without repeating numbers (no proximate nogos)
            RT_beforefailedNOGO.append(numpy.mean(RTs_forcalcs[-4:]))
        RTs_forcalcs.append(0)
    elif k[0][1] >= 0.2:  #success go
        RTs.append(k[0][1])
        correct += 1
        go_n += 1
        RTs_forcalcs.append(k[0][1])
    elif k[0][1] == 0 and txt_stim.text == '3': #success nogo
        correct += 1
        suppressions += 1
        nogo_n += 1
        if len(RTs_forcalcs) > 3 and 0 not in RTs_forcalcs[-4:]:
            RT_beforesuccessNOGO.append(numpy.mean(RTs_forcalcs[-4:]))
        RTs_forcalcs.append(0)
    elif k[0][1] == 0 and txt_stim.text != '3':  #failed go
        omissions += 1
        errors += 1
        go_n += 1
    elif k[0][1] >0.1 and k[0][1] <0.2:  #ambiguous responce
        ambiguous += 1
        if txt_stim.text == '3':
            nogo_n += 1
        else:
            go_n += 1


#stablishing some percentages and other calcs
anticipatory_percent = round((anticipatory/trial_n) * 100,3)
commissions_percent = round((commissions/nogo_n) * 100,3)
omissions_percent = round((omissions/go_n)*100,3)
errors_percent = round((errors/trial_n)*100,3)
correct_percent = round((correct/trial_n)*100,3)
ambiguous_percent = round((ambiguous/trial_n)*100,3)
RTs_mean = round(numpy.mean(RTs),3)
std_rtGO = round(numpy.std(RTs),3)
CVgo = std_rtGO/RTs_mean
meanRT_GObeforesuccessNOGO = round(numpy.mean(RT_beforesuccessNOGO),3)
meanRT_GObeforefailedNOGO = round(numpy.mean(RT_beforefailedNOGO),3)


#variable with data to store in file
data_file = [('Participant','n_trials','n_commissions','perc_commissions',
    'n_omissions','perc_omissions','n_anticipatory','perc_anticipatory','mean_rtGO',
    'std_rtGO','CV_go','meanRT_GObeforesuccessNOGO','meanRT_GObeforefailedNOGO',
    'n_correct','perc_correct','n_errors','perc_errors','n_ambiguous','perc_amboguous'),
    (id_participant,trial_n,commissions,commissions_percent,omissions,
    omissions_percent,anticipatory,anticipatory_percent,RTs_mean,std_rtGO,CVgo,
    meanRT_GObeforesuccessNOGO,meanRT_GObeforefailedNOGO,correct,correct_percent,errors,
    errors_percent,ambiguous,ambiguous_percent)]
    


numpy.savetxt(
    file_name,
    data_file,
    fmt='%s',
    delimiter=',',
    newline='\n',
    header = 'SART test'
)

txt_general.text = "The task has concluded.\n\nThanks for participating. Please press the <space> bar to close the window."
txt_general.draw()
win.flip()
event.waitKeys(keyList=['space'])

win.close()