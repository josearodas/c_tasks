#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 02 12:51 2018
@author: JARP

What type of digit patterns are easier to remember? Does the rythm helps to remember the
strings? If this is true, musicians may perform better.
"""

from __future__ import division

from psychopy import visual, core, data, event, gui, sound
import numpy as np
import random

my_dlg = gui.Dlg(title = 'Assessment')
my_dlg.addField('Participant:')
my_dlg.addField('Session:', choices = ['pre', 'post','follow'])
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

id_participant = str(my_dlg.data[0])
date = data.getDateStr()
session = str(my_dlg.data[1])

file_name = id_participant+'_RSpan_'+date+'_'+session+'.csv'
file_nameraw = id_participant+'_RSpan_'+'raw_'+date+'_'+session+'.csv'



#post-test - still have to create audio
list_12b = [[2, 3, 5, 7, 8, 4, 3, 9, 5, 2, 4, 2],
    [7, 8, 2, 6, 3, 3, 6, 2, 8, 9, 2, 9],
    [8, 5, 6, 8, 6, 4, 7, 5, 9, 1, 9, 9],
    [9, 3, 9, 5, 6, 9, 9, 8, 1, 1, 1, 1],
    [9, 5, 8, 4, 6, 6, 7, 3, 8, 9, 2, 6],
    [4, 7, 9, 3, 6, 6, 1, 8, 7, 5, 6, 6],
    [4, 6, 4, 4, 4, 9, 4, 6, 2, 7, 7, 6],
    [8, 9, 4, 3, 4, 6, 4, 3, 6, 6, 6, 2]]

#followup - still have to create audio
list_12c = [[3, 1, 9, 2, 2, 2, 8, 1, 4, 5, 5, 4],
    [1, 6, 8, 9, 6, 6, 9, 7, 5, 1, 6, 7],
    [1, 8, 2, 4, 1, 3, 4, 2, 5, 8, 5, 8],
    [4, 5, 9, 7, 5, 8, 6, 4, 1, 4, 4, 7],
    [3, 3, 2, 2, 7, 6, 7, 6, 5, 2, 3, 2],
    [6, 7, 9, 2, 6, 5, 5, 8, 9, 4, 6, 8],
    [2, 2, 8, 9, 6, 2, 6, 6, 8, 2, 5, 3],
    [3, 8, 3, 2, 4, 5, 5, 3, 9, 9, 5, 5]]

#no audio
list_14b= [[1, 8, 1, 5, 4, 4, 8, 3, 8, 7, 2, 9, 4, 7],
    [5, 1, 9, 6, 1, 7, 5, 6, 2, 9, 7, 8, 4, 7],
    [4, 8, 5, 1, 7, 3, 1, 2, 6, 7, 6, 7, 3, 9],
    [9, 2, 2, 5, 7, 4, 2, 2, 2, 7, 5, 4, 7, 3],
    [2, 3, 5, 6, 8, 9, 5, 5, 7, 2, 4, 2, 6, 8],
    [3, 1, 9, 1, 2, 6, 6, 6, 8, 8, 3, 6, 3, 5],
    [2, 1, 8, 8, 9, 9, 7, 2, 9, 7, 5, 4, 5, 8],
    [6, 5, 9, 3, 5, 8, 5, 6, 2, 9, 2, 5, 6, 6]]

#no audio
list_14c = [[4, 7, 4, 5, 6, 1, 3, 9, 4, 1, 3, 8, 2, 7],
    [7, 1, 5, 7, 5, 2, 1, 5, 2, 6, 9, 4, 5, 4],
    [8, 5, 7, 1, 9, 9, 3, 2, 2, 5, 6, 1, 6, 6],
    [9, 2, 7, 5, 2, 4, 1, 8, 8, 6, 9, 2, 7, 8],
    [5, 2, 5, 6, 8, 2, 3, 4, 7, 5, 3, 9, 6, 9],
    [3, 2, 2, 5, 7, 9, 7, 8, 7, 3, 7, 8, 5, 3],
    [1, 7, 2, 1, 9, 6, 9, 1, 7, 1, 1, 5, 1, 1],
    [4, 9, 8, 4, 9, 5, 5, 4, 9, 5, 5, 2, 2, 7]]

#no audio
list_16b = [[2, 4, 2, 9, 3, 3, 9, 2, 2, 4, 9, 6, 2, 6, 5, 8],
    [1, 9, 5, 9, 2, 3, 7, 1, 5, 7, 9, 4, 9, 8, 5, 5],
    [2, 9, 4, 5, 5, 1, 9, 4, 7, 8, 7, 3, 8, 1, 6, 8],
    [5, 3, 2, 3, 3, 8, 3, 2, 9, 9, 7, 1, 2, 1, 3, 2],
    [2, 3, 8, 3, 6, 8, 5, 2, 8, 5, 2, 1, 6, 9, 5, 2],
    [3, 8, 2, 2, 6, 4, 7, 1, 3, 4, 9, 7, 4, 6, 6, 7],
    [6, 1, 7, 1, 6, 9, 7, 8, 1, 4, 4, 4, 2, 8, 3, 4],
    [7, 3, 1, 6, 2, 3, 8, 3, 9, 1, 1, 9, 4, 3, 8, 3]]

#no audio
list_16c = [[4, 7, 9, 1, 8, 7, 8, 7, 5, 7, 4, 2, 3, 5, 8, 9],
    [7, 7, 7, 9, 6, 9, 2, 3, 3, 4, 9, 3, 9, 4, 9, 4],
    [1, 9, 7, 5, 5, 6, 4, 3, 7, 3, 9, 1, 6, 3, 9, 4],
    [2, 6, 4, 8, 7, 8, 6, 9, 2, 2, 5, 3, 5, 6, 9, 7],
    [9, 4, 7, 8, 7, 5, 5, 8, 8, 6, 4, 5, 5, 7, 5, 3],
    [1, 4, 6, 1, 3, 7, 9, 9, 9, 3, 6, 1, 7, 6, 2, 4],
    [1, 3, 3, 2, 4, 2, 9, 4, 2, 2, 5, 3, 5, 5, 8, 8],
    [2, 1, 2, 2, 7, 3, 2, 3, 7, 2, 4, 8, 1, 2, 7, 7]]

#no audio
list_18b = [[7, 1, 4, 6, 6, 1, 4, 5, 7, 4, 1, 1, 7, 1, 4, 4, 3, 8],
    [9, 9, 6, 1, 2, 4, 1, 8, 8, 3, 5, 7, 7, 4, 5, 1, 6, 5],
    [1, 4, 7, 9, 8, 5, 4, 8, 5, 9, 2, 7, 4, 7, 5, 2, 7, 7],
    [9, 2, 1, 3, 4, 2, 6, 9, 5, 7, 1, 8, 6, 3, 8, 4, 5, 9],
    [9, 6, 4, 3, 3, 7, 1, 5, 4, 7, 1, 9, 2, 4, 8, 2, 7, 2],
    [6, 3, 3, 1, 1, 8, 8, 9, 8, 5, 7, 8, 4, 9, 2, 8, 4, 8],
    [1, 6, 1, 5, 4, 5, 4, 2, 1, 7, 3, 1, 9, 9, 4, 1, 5, 9],
    [3, 6, 5, 6, 5, 1, 3, 8, 2, 2, 1, 4, 1, 3, 4, 1, 8, 2]]

#no audio
list_18c = [[6, 3, 4, 2, 7, 4, 5, 5, 7, 2, 9, 1, 2, 8, 8, 3, 3, 9],
    [4, 5, 2, 4, 8, 9, 9, 2, 8, 4, 7, 1, 8, 5, 9, 7, 3, 9],
    [2, 3, 8, 4, 4, 9, 2, 4, 1, 7, 5, 5, 5, 2, 4, 8, 8, 9],
    [9, 3, 3, 6, 9, 6, 1, 7, 3, 4, 9, 6, 7, 5, 8, 5, 3, 2],
    [5, 8, 4, 4, 4, 8, 6, 3, 9, 7, 1, 8, 3, 5, 3, 6, 5, 3],
    [7, 4, 3, 3, 6, 3, 7, 9, 8, 1, 2, 9, 3, 4, 9, 2, 2, 1],
    [1, 6, 2, 4, 3, 6, 4, 2, 3, 9, 1, 5, 6, 4, 2, 1, 3, 5],
    [9, 2, 1, 7, 1, 8, 4, 6, 3, 2, 2, 3, 1, 9, 1, 9, 3, 2]]

#no audio
list_20b = [[3, 3, 6, 9, 4, 3, 3, 3, 9, 6, 7, 4, 1, 8, 4, 6, 3, 5, 1, 2],
    [1, 1, 8, 1, 4, 5, 8, 4, 9, 6, 2, 5, 6, 5, 4, 4, 5, 3, 9, 1],
    [7, 3, 7, 3, 6, 1, 6, 9, 8, 7, 8, 4, 8, 3, 7, 2, 1, 7, 7, 6],
    [3, 8, 5, 4, 4, 4, 4, 3, 6, 4, 2, 3, 9, 2, 2, 1, 8, 2, 8, 4],
    [2, 9, 8, 3, 1, 8, 8, 4, 5, 4, 5, 2, 8, 5, 6, 7, 3, 6, 6, 4],
    [7, 1, 9, 2, 7, 4, 9, 2, 6, 7, 9, 8, 6, 5, 8, 2, 3, 8, 7, 3],
    [7, 7, 1, 5, 3, 5, 8, 1, 2, 7, 2, 4, 8, 3, 6, 8, 7, 2, 8, 2],
    [2, 6, 6, 5, 8, 9, 5, 2, 6, 6, 6, 8, 7, 1, 6, 2, 3, 5, 2, 4]]

#no audio
list_20c = [[5, 5, 4, 8, 1, 5, 5, 1, 3, 3, 5, 9, 9, 5, 1, 5, 3, 2, 4, 2],
    [9, 1, 6, 9, 7, 4, 6, 2, 5, 6, 5, 1, 2, 3, 8, 7, 1, 6, 4, 2],
    [4, 8, 5, 1, 8, 9, 8, 7, 7, 1, 7, 2, 3, 9, 5, 1, 2, 2, 8, 5],
    [7, 1, 9, 5, 7, 8, 1, 6, 2, 8, 3, 2, 4, 1, 7, 8, 6, 7, 6, 8],
    [6, 8, 9, 2, 7, 1, 3, 7, 1, 9, 7, 6, 6, 1, 4, 5, 6, 2, 4, 9],
    [2, 3, 1, 5, 8, 6, 2, 2, 4, 8, 1, 9, 1, 2, 9, 8, 8, 9, 6, 1],
    [3, 5, 9, 3, 6, 7, 1, 4, 6, 4, 1, 9, 6, 6, 2, 5, 9, 6, 5, 3],
    [5, 8, 9, 3, 2, 7, 7, 2, 6, 2, 6, 1, 3, 6, 3, 3, 6, 6, 5, 2]]


practStimList = [{'dig':'48142594847563','aud':'ogg/test1.ogg'},{'dig':'6532739546','aud':'ogg/test2.ogg'},{'dig':'6464459781373245','aud':'ogg/test3.ogg'}]

stimlist = [{'dig': '678888179735', 'aud': 'ogg/12-1.ogg'}, {'dig': '662245527642', 'aud': 'ogg/12-2.ogg'}, 
    {'dig': '965371944176', 'aud': 'ogg/12-3.ogg'}, {'dig': '928142952589', 'aud': 'ogg/12-4.ogg'},
    {'dig': '452574982521', 'aud': 'ogg/12-5.ogg'}, {'dig': '559984682263', 'aud': 'ogg/12-6.ogg'}, 
    {'dig': '798122317395', 'aud': 'ogg/12-7.ogg'}, {'dig': '527198964244', 'aud': 'ogg/12-8.ogg'},
    {'dig': '65544296555467', 'aud': 'ogg/14-1.ogg'}, {'dig': '17419421892344', 'aud': 'ogg/14-2.ogg'}, 
    {'dig': '64413396165489', 'aud': 'ogg/14-3.ogg'}, {'dig': '67864675842122', 'aud': 'ogg/14-4.ogg'}, 
    {'dig': '73164188627842', 'aud': 'ogg/14-5.ogg'}, {'dig': '16211551417959', 'aud': 'ogg/14-6.ogg'}, 
    {'dig': '47648878856195', 'aud': 'ogg/14-7.ogg'}, {'dig': '87718977549927', 'aud': 'ogg/14-8.ogg'},
    {'dig': '7138411924375812', 'aud': 'ogg/16-1.ogg'}, {'dig': '9785674186773779', 'aud': 'ogg/16-2.ogg'}, 
    {'dig': '9232469464131772', 'aud': 'ogg/16-3.ogg'}, {'dig': '6633912278449689', 'aud': 'ogg/16-4.ogg'}, 
    {'dig': '8477316986383865', 'aud': 'ogg/16-5.ogg'}, {'dig': '2679842482518537', 'aud': 'ogg/16-6.ogg'}, 
    {'dig': '4849416292882186', 'aud': 'ogg/16-7.ogg'}, {'dig': '3829668964311422', 'aud': 'ogg/16-8.ogg'},
    {'dig': '449951513448554161', 'aud': 'ogg/18-1.ogg'}, {'dig': '983145958679569231', 'aud': 'ogg/18-2.ogg'},
    {'dig': '261316152752592126', 'aud': 'ogg/18-3.ogg'}, {'dig': '458961653598249894', 'aud': 'ogg/18-4.ogg'}, 
    {'dig': '695587865237695199', 'aud': 'ogg/18-5.ogg'}, {'dig': '689856736699433292', 'aud': 'ogg/18-6.ogg'}, 
    {'dig': '115235945877333156', 'aud': 'ogg/18-7.ogg'}, {'dig': '513934714936737386', 'aud': 'ogg/18-8.ogg'},
    {'dig': '59367143946956662948', 'aud': 'ogg/20-1.ogg'}, {'dig': '69931222894869774274', 'aud': 'ogg/20-2.ogg'},
    {'dig': '76113597228775858912', 'aud': 'ogg/20-3.ogg'}, {'dig': '14233656172351726881', 'aud': 'ogg/20-4.ogg'},
    {'dig': '41189577836117552984', 'aud': 'ogg/20-5.ogg'}, {'dig': '99277997637614331823', 'aud': 'ogg/20-6.ogg'},
    {'dig': '57364898875324124469', 'aud': 'ogg/20-7.ogg'}, {'dig': '25427982855623519844', 'aud': 'ogg/20-8.ogg'}]


trials = data.TrialHandler(stimlist,1, extraInfo = {'participant':id_participant,'session':session})
trials.data.addDataType('score')
trials.data.addDataType('response')
prac_trials = data.TrialHandler(practStimList,1)

win = visual.Window(units='pix',fullscr=True,color=(-1,-1,-1))
win.mouseVisible=False

txt_stim = visual.TextStim(win, height = 45)
txt_instr = visual.TextStim(win, height=28,wrapWidth=900)
txt_topinstr = visual.TextStim(win, text = 'Please type the digits that you remember without spaces or hyphens. Use <b> as place holder. You can delete by using the <backspace> key.', pos=(0,150),
    height=28,wrapWidth=900)

score_12 = []
score_14 = []
score_16 = []
score_18 = []
score_20 = []
score_global = []

txt_instr.text = "In the following task you will hear groups of digits recited very fast. After this you will be asked to recall all the last digits of the group that you can remember. You will be asked to type them in the correct order. If you cannot remember a particular item you will be able to use the <b> key as a placeholder.\n\nLet's say for example that you hear:\n\n       3-8-2-6-4-3-9-8-1-6-8-3-6-2\n\nbut you can only remember the last 5 digits. In this case when you are asked to type the digits you can remember you would type\n\n68362\n\nNotice that these digits were the last ones to be recited and are in the correct order. This is important.\n\nLet's have another example before having some practice. Please press the <space> bar."
txt_instr.draw()
win.flip()
event.waitKeys(keyList = ['space'])
win.flip()

txt_instr.text = "Let's say that you hear the numbers:\n\n         8-2-6-4-1-7-5-3-9-7-4-5\n\nand you can only remember the last 6, but you are not sure about the forth one. In this case you would give as an answer:\n\n      539b45\n\nNotice that in this case the letter <b> has been used as a placeholder for a digit you didn't remember. This is perfectly valid.\n\nYou will have a few practice trials so you can try for yourself how this works. If you feel the task is not sufficiently clear yet please do not hesitate to ask the researcher any doubt you have.\n\nPlease press the <space-bar> key to continue."
txt_instr.draw()
win.flip()
event.waitKeys(keyList = ['space'])
win.flip()

#some practice trials
for pracTrial in prac_trials:
    
    aud_stim = sound.Sound(pracTrial['aud'])
    aud_stim.play()
    
    #This will add 1s of wait time after the string presentation
    if len(pracTrial['dig']) == 10:
        core.wait(3.5)
    elif len(pracTrial['dig']) == 14:
        core.wait(4.5)
    elif len(pracTrial['dig']) == 16:
        core.wait(5)
    
    
    #get participant's responses
    subj_resp = 0
    typed_string = ''
    returned_string = ''
    
    txt_topinstr.draw()
    win.flip()
    event.clearEvents()
    while subj_resp == 0:
        for i in event.getKeys(keyList=['backspace','return','escape',
        '1','2','3','4','5','6','7','8','9','b']):
            if i in ['escape']:
                core.quit()
            elif i in ['return']:
                returned_string = typed_string
                core.wait(2)
                subj_resp = 1
            elif i in ['backspace']:
                typed_string = typed_string[:-1]
                txt_stim.setText(typed_string)
                txt_stim.draw()
                txt_topinstr.draw()
                win.flip()
            else:
                typed_string += i
                txt_stim.setText(typed_string)
                txt_stim.draw()
                txt_topinstr.draw()
                win.flip()
    
    win.flip()
    
    #give feedback
    score_counter = 0
    
    digit_index = -1
    for i in range(len(returned_string)):
        if returned_string[digit_index] == pracTrial['dig'][digit_index]:
            score_counter += 1
        digit_index -= 1
    
    event.clearEvents()
    
    txt_instr.text = 'You have correctly recalled %s digits.\n\nTry to recall as many digits as you can from the end of the string. If there is a digit that you cannot remember you can use the <b> key as a place holder, as the position of each digit is important.\n\nPress any key to continue.' %score_counter
    txt_instr.draw()
    win.flip()
    
    event.waitKeys()
    
    win.flip()
    
    core.wait(1)

txt_instr.text = "Now that you have practiced let's start the task.\n\nPlease press the <space-bar> whenever you feel ready to start.\nFeel free to take small rests between the trials if you feel you need them."
txt_instr.draw()
win.flip()

event.waitKeys(keyList = ['space'])
win.flip()

#the real deal
for thisTrial in trials:
    
    aud_stim = sound.Sound(thisTrial['aud'])
    aud_stim.play()
    
    #This will add 1s of wait time after the string presentation
    if len(thisTrial['dig']) == 12:
        core.wait(4)
    elif len(thisTrial['dig']) == 14:
        core.wait(4.5)
    elif len(thisTrial['dig']) == 16:
        core.wait(5)
    elif len(thisTrial['dig']) == 18:
        core.wait(5.5)
    elif len(thisTrial['dig']) == 20:
        core.wait(6)
    
    
    #get participant's responses
    subj_resp = 0
    typed_string = ''
    returned_string = ''
    
    txt_topinstr.draw()
    win.flip()
    event.clearEvents()
    while subj_resp == 0:
        for i in event.getKeys(keyList=['backspace','return','escape',
        '1','2','3','4','5','6','7','8','9','b']):
            if i in ['escape']:
                core.quit()
            elif i in ['return']:
                returned_string = typed_string
                core.wait(2)
                subj_resp = 1
            elif i in ['backspace']:
                typed_string = typed_string[:-1]
                txt_stim.setText(typed_string)
                txt_stim.draw()
                txt_topinstr.draw()
                win.flip()
            else:
                typed_string += i
                txt_stim.setText(typed_string)
                txt_stim.draw()
                txt_topinstr.draw()
                win.flip()
    
    win.flip()
    
    trials.data.add('response',returned_string)
    
    #store scores
    score_counter = 0
    
    digit_index = -1
    for i in range(len(returned_string)):
        if returned_string[digit_index] == thisTrial['dig'][digit_index]:
            score_counter += 1
        digit_index -= 1
    score_global.append(score_counter)
    trials.data.add('score',score_counter)
    
    if len(thisTrial['dig']) == 12:
        score_12.append(score_counter)
        trials.data.add('Score12',score_counter)
    elif len(thisTrial['dig']) == 14:
        score_14.append(score_counter)
        trials.data.add('Score14',score_counter)
    elif len(thisTrial['dig']) == 16:
        score_16.append(score_counter)
        trials.data.add('Score16',score_counter)
    elif len(thisTrial['dig']) == 18:
        score_18.append(score_counter)
        trials.data.add('Score18',score_counter)
    elif len(thisTrial['dig']) == 20:
        score_20.append(score_counter)
        trials.data.add('Score20',score_counter)
    
    event.clearEvents()
    txt_instr.text = 'Press any key to continue'
    txt_instr.draw()
    win.flip()
    
    event.waitKeys()
    
    win.flip()
    
    core.wait(1)

mean_globalScore = round(np.mean(score_global),2)
mean_12score = round(np.mean(score_12),2)
mean_14score = round(np.mean(score_14),2)
mean_16score = round(np.mean(score_16),2)
mean_18score = round(np.mean(score_18),2)
mean_20score = round(np.mean(score_20),2)

score_means = [mean_globalScore, mean_12score, mean_14score, mean_16score, mean_18score, mean_20score]
score_raw = score_12+score_14+score_16+score_18+score_20

#creates a file with the means
np.savetxt(
    file_name,
    [('mean_globalScore','mean_12score','mean_14score','mean_16score','mean_18score','mean_20score'),
    (mean_globalScore,mean_12score,mean_14score,mean_16score,mean_18score,mean_20score)],
    fmt = '%s',
    delimiter = ','
    )

trials.saveAsExcel(fileName=file_nameraw[:-4],stimOut=['dig'])
'''
#creates a file with raw data
np.savetxt(
    file_nameraw,
    [('12-1','12-2','12-3','12-4','12-5','12-6','12-7','12-8','14-1','14-2','14-3','14-4','14-5','14-6',
    '14-7','14-8','16-1','16-2','16-3','16-4','16-5','16-6','16-7','16-8','18-1','18-2','18-3','18-4','18-5'
    ,'18-6','18-7','18-8','20-1','20-2','20-3','20-4','20-5','20-6','20-7','20-8'),(score_12[0],score_12[1],score_12[2],score_12[3],
    score_12[4],score_12[5],score_12[6],score_12[7],score_14[0],score_14[1],score_14[2],score_14[3],score_14[4],
    score_14[5],score_14[6],score_14[7],score_16[0],score_16[1],score_16[2],score_16[3],score_16[4],score_16[5],
    score_16[6],score_16[7],score_18[0],score_18[1],score_18[2],score_18[3],score_18[4],score_18[5],score_18[6],
    score_18[7],score_20[0],score_20[1],score_20[2],score_20[3],score_20[4],score_20[5],score_20[6],score_20[7],)],
    fmt = '%s',
    delimiter = ','
    )
'''

txt_instr.text = "The task has concluded. Thanks for your time. \n\nPlease press any key."
txt_instr.draw()
win.flip()
event.waitKeys()

win.close()