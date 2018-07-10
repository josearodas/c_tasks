# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 18:22:52 2016

@author: Jarp

                                UPDATING TASK
                                
In this task a set of strings of letters will be presented to the participant
and he has to recall the last four items of each string.
"""

import random
import datetime

from psychopy import visual, event, core, gui, data


numb_trials = 4         #must be set to 4 (wich really are 16). Each trials (group of trials) implies one run for each length (5,7,9,11)
numb_practrials = 1     #MUST be three, unless instructions are changed
stim_pres = 1


def typed_resp():
    returned_string = ''
    typed_string = ''
    subj_resp = 0
    win.flip()
    input_instructions.draw()
    win.flip()
    while subj_resp == 0:
        for i in event.getKeys(keyList=['backspace','return','escape',
        'q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j',
        'k','l','z','x','c','v','b','n','m']):
            if i in ['escape']:
                core.quit()
            elif i in ['return']:
                returned_string = typed_string #the returned string
                core.wait(2)
                subj_resp = 1
            elif i in ['backspace']:
                typed_string = typed_string[:-1]
                participant_input.setText(typed_string)
                participant_input.draw()
                input_instructions.draw()
                win.flip()
            else:
                typed_string += i.upper()
                participant_input.setText(typed_string)
                participant_input.draw()
                input_instructions.draw()
                win.flip()
    #if len(returned_string) > 4:
    #    returned_string = returned_string[-4:]

    return returned_string[-4:]


#IMPUT DATA AND FILENAME
my_dlg = gui.Dlg(title='Assessment')
my_dlg.addField('Participant:')
my_dlg.addField('Session:',choices=['pre','post','follow'])
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

date = data.getDateStr()
id_participant = str(my_dlg.data[0])
id_session = str(my_dlg.data[1])

file_name = id_participant+'_updating_'+date+'_'+id_session

#Creating a string with date & time info
i = datetime.datetime.now()
now_date = str(i.day)+str(i.month)+str(i.year)
now_time = str(i.hour)+str(i.minute)
date_time = now_date+now_time


#INITIALISE STIMULI AND CREATE THE WINDOW
#The window will be fullscreen
win = visual.Window(units='pix',fullscr=True, color=(-1,-1,-1))
win.mouseVisible = False


participant_input = visual.TextStim(win,units='pix',color=(1,1,1), height=80)

input_instructions = visual.TextStim(win,units='norm',pos=(0,0.5),color=(1,1,1),
    text="Please type the last four letters and press <enter>")

txt_instructions = visual.TextStim(win,units='pix',height=26,wrapWidth=900,color=(1,1,1))

p_stimulus = visual.TextStim(win,height=80)

clock = core.Clock()

instructions_counter = 0
score = 0


#some practice trials
pract_strings = []
for i in range(3): 
    pract_strings.append({'str_len':random.randint(5,7)})
    
#trialHandler for the practice loops
pract_trials = data.TrialHandler(pract_strings, numb_practrials, method='sequential')

#create the stimuli strings for the real trials
string_sizes = []
for i in range(5,12,2): 
    string_sizes.append({"str_len":i})

#Create a trial handler to mannage the task
trials = data.TrialHandler(
    string_sizes, numb_trials,   #this must be set to (16) 4
    method='random',
    extraInfo = {'participant':id_participant, 'session':id_session})
trials.data.addDataType('CorrAns')


txt_instructions.text = "In the following task a string of letters will be presented at the center of the screen one by one. You won't know how many letters each string will contain, but you will always have to remember the last four. This means that as the string progresses you will have to remember new letters and forget the old ones (e.g. 5th letter). Let's say that the following letters are presented one by one on the screen:\n\nR - T - K - C - P - S\n\nAfter the letter 'S' the string suddenly stops (no more letters appear). Instead, a message will be displayed asking you to type the last four letters presented. You should have to type KCPS (without spaces or hyphens) and press <enter>. If you do not remember all the last four letters you can enter the ones that you remember, but take in mind that order and position matters. You can not alter the order or position of the letters as it will be considered an error.\n\nWe'll have a few practice trials so you can have a look at the task before really starting.\n\nPlease press the <space> bar to start the practice."
txt_instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])


#*******************PRACTICE TRIALS******************************
#Each loop represent a trial
for i_trials in pract_trials:
    
    running_string = [] 
    running_list = ['C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','X','Z']    #B has been omited
        
    
    if instructions_counter == 0:
        txt_instructions.text = "This will be your first practice trial. Remember to always keep in mind ONLY the last four letters from the string.\n\nPress the <space> bar to start."
        txt_instructions.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        #Wait for 1s after the the instructions before presenting the stimuli
        clock.reset()
        while clock.getTime() < 1:   #1s before presenting the first stimulus
            win.flip()
    elif instructions_counter == 1:
        txt_instructions.text = "Let's do another practice trial. Remember to always keep in mind ONLY the last four letters from the string.\n\nPress the <space> bar to start."
        txt_instructions.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        #Wait for 1s after the the instructions before presenting the stimuli
        clock.reset()
        while clock.getTime() < 1:   #1s before presenting the first stimulus
            win.flip()
    else:
        txt_instructions.text = "This is going to be the last practice trial. If you feel the task is not completely clear feel free to ask the examiner any question you have.\n\nPress the <space> bar when ready."
        txt_instructions.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        
        core.wait(1)

    event.clearEvents()
    
    #The stimuli is presented and the string is created
    for i in range(i_trials['str_len']):
        s_stimulus = random.choice(running_list)
        p_stimulus.text = s_stimulus
        running_string.append(s_stimulus)
        
        clock.reset()
        while clock.getTime() < stim_pres:
            p_stimulus.draw()
            win.flip()
        
        while clock.getTime() < (stim_pres+0.5):
            win.flip()
        
        running_list.remove(s_stimulus)
        
    event.clearEvents()
    
    
    returned_string = typed_resp()
    
    
    #Responses must be contrasted with the running_string the resposponse must be evaluated and summed
    lastitems_runningstring = ''.join(running_string[-4:])
    score_counter = 0
    for i in range(len(returned_string)):
        if returned_string[(i+1)*-1] == lastitems_runningstring[(i+1)*-1]:
            score_counter += 1
    if score_counter == 4:
        txt_instructions.text = 'You got four letters right\n\nPress any key to continue'
        txt_instructions.draw()
        win.flip()
        event.waitKeys()
    elif score_counter == 3:
        txt_instructions.text = 'You got three letters right\n\nPress any key to continue'
        txt_instructions.draw()
        win.flip()
        event.waitKeys()
    elif score_counter == 2:
        txt_instructions.text = 'You got two letters right\n\nPress any key to continue'
        txt_instructions.draw()
        win.flip()
        event.waitKeys()
    elif score_counter == 1:
        txt_instructions.text = 'You just got one letter right\n\nPress any key to continue'
        txt_instructions.draw()        
        win.flip()
        event.waitKeys()
    else:
        txt_instructions.text = "Those were not the correct letters.\n\nRemember that the position of each letter is important."
        txt_instructions.draw()
        win.flip()
        event.waitKeys()
        
    instructions_counter += 1
    
    event.clearEvents()


txt_instructions.text = "You have concluded the practice trials so you will begin the task. This is not an easy task, but try to do your best. Press the <space> bar to continue."
txt_instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

event.clearEvents()


#THE TRIALS**************************************************
#Each loop represent a trial
for i_trials in trials:
    #Setting local variables, instructions, and clocks
    running_string = [] #local var to store strings in each trial
    running_list = ['C','D','F','G','H','J','K','L','M','N','P','Q',
               'R','S','T','V','X','Z']    #B has been omited
    returned_string = ''
    typed_string = ''    #stores the participant answer
    txt_instructions.text = "Press the <space> bar to start the trial"
    txt_instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    #Wait for 1s after the the instructions before presenting the stimuli
    clock.reset()
    while clock.getTime() < 1:
        win.flip()
            
    
    event.clearEvents()
    
    
    for i in range(i_trials['str_len']):
        s_stimulus = random.choice(running_list)
        p_stimulus.text = s_stimulus
        running_string.append(s_stimulus)
        
        clock.reset()
        while clock.getTime() < stim_pres:
            p_stimulus.draw()
            win.flip()
        
        while clock.getTime() < (stim_pres+0.5):
            win.flip()
        #Removing the letter from the pool so that it does not appear again in the same trial
        running_list.remove(s_stimulus)
    
    event.clearEvents()
    
    returned_string = typed_resp()
        
    #contrasting responses to be stored
    lastitems_runningstring = ''.join(running_string[-4:])
    score_counter = 0
    for i in range(len(returned_string)):
        if returned_string[(i+1)*-1] == lastitems_runningstring[(i+1)*-1]:
            score_counter += 1
    if returned_string == lastitems_runningstring:
        trials.data.add('CorrAns',4)
        score += 4
        win.flip()
        core.wait(1)
    elif returned_string[-3:] == lastitems_runningstring[-3:]:
        trials.data.add('CorrAns',3)
        score += 3
        core.wait(1)
    elif returned_string[-2:] == lastitems_runningstring[-2:]:
        trials.data.add('CorrAns',2)
        score += 2
        core.wait(1)
    elif returned_string[-1:] == lastitems_runningstring[-1:]:
        trials.data.add('CorrAns',1)
        score += 1
        core.wait(1)
    else:
        trials.data.add('CorrAns',0)
        core.wait(1)
    
    event.clearEvents()

trials.saveAsExcel(file_name,
                   stimOut=['str_len']
                   #dataOut=['CorrAns_raw','Corr_answ_mean']
                   )

txt_instructions.text = "The task has concluded. Thanks for participating.\n\nPlease press any key."
txt_instructions.draw()


win.flip()

event.waitKeys()

win.close()