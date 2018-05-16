# -*- coding: utf-8 *-*

"""
Created on Thursday 12 April 2018 13:30
@author: JARP

The task is based on the description in Oberauer 2008
For setsize 2 chances are 50% of repetition, for setsize 4 there are 4 repetitions, and for
setsize 6 aproximately 3 repetitions (sometimes 4). This is in order to have a more equitative
number of changes vs no-change in updatings.

Could the difference in the updating process be related to the eye movement and not to the 
updating process itself? I could test this by comparing the task with another one without any 
updating, only with the eye movement. Maybe an eyetraker would be needed.

For the output file the mean storage is the mean time taken for memorizing the displayed set
of numbers in the onset

Only data from correct recall (all boxes) is stored in the summary file

There are 6 runs for n=2 and 4 runs for n=4 and 6. This is mostly because the main purpose of
this task in this study is to assess the focus switching costs, and the n=2 condition is the
one that gives the most information in this respect. The other two conditions are kept for 
other research purposes.

Must add a raw output with: numb_boxes, position, RT, condition (SW or nSW)

"""


from __future__ import division
from psychopy import visual, event, gui, core, data
import numpy as np
import random, copy


def general_runcreator(setsize):
    positions = ['A1','B1','A2','B2','A3','B3']
    
    block_pos = [positions[i] for i in range(setsize)]
    
    order = [random.choice(block_pos) for i in range(9)]
    
    state_of_digits_B = {}
    [state_of_digits_B.update({i:random.randint(1,9)}) for i in block_pos]
    
    state_of_digits_E = copy.deepcopy(state_of_digits_B)
    
    stims = [{'pos':i, 'dig':state_of_digits_E[i],'update':0} for i in block_pos]
    
    #removes unplanned repetitions (this segment still leaves a chance for unplanned repetitions to be created at this moment)
    if setsize >2:
        for order_i in range(len(order)-1):
            pos_pool = copy.copy(block_pos)
            pos_pool.remove(order[order_i])    #remove the item to be avaluated for repetition from the pool of choices to replace it
            if order[order_i] == order[order_i+1]:
                del order[order_i]
                order.insert(order_i,random.choice(pos_pool))
        
        index_pool = [i for i in range(len(order)-1)]    #a list of index to use as possible repetitions
        for i in range(4):
            trial_torep = random.choice(index_pool)
            order.insert(trial_torep+1,order[trial_torep])
            del order[trial_torep+2]
            index_pool.remove(trial_torep)
        
    updatings = [] # this should include a list of dictionaries with the position and the updatings
    
    for stim in order: #this must update the state_of_digits for each step of order_post providing with the stim updating for each stem. This latter value must be included in the stim list of dictionaries
        working_dig = state_of_digits_E[stim]
        possible_values = []
        neg_index = -1
        for i in range(working_dig-1):
            possible_values.append(neg_index)
            neg_index -= 1
        pos_index = 9 - working_dig
        [possible_values.append(i+1) for i in range(pos_index)]
        
        digit_modifier = random.choice(possible_values)
        
        updatings.append({'pos':stim, 'dig':digit_modifier})
        state_of_digits_E[stim] = working_dig + digit_modifier
    
    
    return (state_of_digits_B, state_of_digits_E, updatings)

def box_draw(setsize):
    if setsize == 2:
        box3.draw()
        box4.draw()
    elif setsize == 4:
        box7.draw()
        box8.draw()
        box9.draw()
        box10.draw()
    else:
        box1.draw()
        box2.draw()
        box3.draw()
        box4.draw()
        box5.draw()
        box6.draw()

def dim_box_color():
    box1.lineColor = (-0.5,-0.5,-0.5)
    box2.lineColor = (-0.5,-0.5,-0.5)
    box3.lineColor = (-0.5,-0.5,-0.5)
    box4.lineColor = (-0.5,-0.5,-0.5)
    box5.lineColor = (-0.5,-0.5,-0.5)
    box6.lineColor = (-0.5,-0.5,-0.5)
    box7.lineColor = (-0.5,-0.5,-0.5)
    box8.lineColor = (-0.5,-0.5,-0.5)
    box9.lineColor = (-0.5,-0.5,-0.5)
    box10.lineColor = (-0.5,-0.5,-0.5)

def reset_box_color():
    box1.lineColor = (0.5,0.5,0.5)
    box2.lineColor = (0.5,0.5,0.5)
    box3.lineColor = (0.5,0.5,0.5)
    box4.lineColor = (0.5,0.5,0.5)
    box5.lineColor = (0.5,0.5,0.5)
    box6.lineColor = (0.5,0.5,0.5)
    box7.lineColor = (0.5,0.5,0.5)
    box8.lineColor = (0.5,0.5,0.5)
    box9.lineColor = (0.5,0.5,0.5)
    box10.lineColor = (0.5,0.5,0.5)

def collect_response():
    subj_resp = 0
    typed_string = ''
    returned_string = ''
    
    txt_topinstr.draw()
    box_draw(setsize)
    win.flip()
    while subj_resp == 0:
        for i in event.getKeys(keyList=['backspace','return','escape',
        '1','2','3','4','5','6','7','8','9']):
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
                box_draw(setsize)
                win.flip()
            else:
                typed_string += i.upper()
                txt_input.setText(typed_string)
                txt_input.draw()
                txt_topinstr.draw()
                box_draw(setsize)
                win.flip()
    
    if returned_string == '':
        returned_string = '0'
    
    return returned_string

my_dlg = gui.Dlg(title='Assessment')
my_dlg.addField('Participant:')
my_dlg.addField('Session:', choices=['pre','post','follow'])
my_dlg.show()

if my_dlg.OK == False:
    core.quit()

date = data.getDateStr()
id_participant = str(my_dlg.data[0])
session = str(my_dlg.data[1])

file_name = id_participant+'_box_upd_'+date+'_'+session+'.csv'

win = visual.Window(color=(-1,-1,-1), fullscr=True, units='pix', size=(800,600))
win.mouseVisible=False
clock = core.Clock()

txt_instr = visual.TextStim(win,color=(1,1,1), height=26, wrapWidth = 900)
txt_feedback = visual.TextStim(win,color=(1,1,1),height=40)
txt_topinstr = visual.TextStim(win, color=(1,1,1), pos=(0,280), wrapWidth=900)
txt_input = visual.TextStim(win, color=(1,1,1), height=93)
A1 = visual.TextStim(win, color=(1,1,1), height=93)
A2 = visual.TextStim(win, color=(1,1,1), height=93)
A3 = visual.TextStim(win, color=(1,1,1), height=93)
B1 = visual.TextStim(win, color=(1,1,1), height=93)
B2 = visual.TextStim(win, color=(1,1,1), height=93)
B3 = visual.TextStim(win, color=(1,1,1), height=93)

box1 = visual.Rect(win, width=200, height=240, pos=(-230,140), lineWidth=5)
box2 = visual.Rect(win, width=200, height=240, pos=(-230,-140), lineWidth=5)
box3 = visual.Rect(win, width=200, height=240, pos=(0,140), lineWidth=5)
box4 = visual.Rect(win, width=200, height=240, pos=(0,-140), lineWidth=5)
box5 = visual.Rect(win, width=200, height=240, pos=(230,140), lineWidth=5)
box6 = visual.Rect(win, width=200, height=240, pos=(230,-140), lineWidth=5)
#for the setsize four condition
box7 = visual.Rect(win, width=200, height=240, pos=(110,140), lineWidth=5)
box8 = visual.Rect(win, width=200, height=240, pos=(110,-140), lineWidth=5)
box9 = visual.Rect(win, width=200, height=240, pos=(-110,140), lineWidth=5)
box10= visual.Rect(win, width=200, height=240, pos=(-110,-140), lineWidth=5)

out_raw = []

runs_pool = [2,2,2,2,2,2,4,4,4,4,6,6,6,6]
resp_storage2 = []
resp_storage4 = []
resp_storage6 = []
resp_nosw2 = []
resp_nosw4 = []
resp_nosw6 = []
resp_sw2 = []
resp_sw4 = []
resp_sw6 = []

out_resp_storage2 = []
out_resp_storage4 = []
out_resp_storage6 = []
out_resp_nosw2 = []
out_resp_nosw4 = []
out_resp_nosw6 = []
out_resp_sw2 = []
out_resp_sw4 = []
out_resp_sw6 = []

trials = 0

correct2 = 0
correct4 = 0
correct6 = 0

txt_instr.text = "In the following task you will be presented with two rows of boxes. The number of boxes per row can vary from 1 to 3. Each box will contain a number inside between 1 and 9 and you will be required to remember them, as they will be updated with basic additions and substractions. After a few of these operations you will be asked to type in the final number of each of these boxes. The results will always be numbers between 1 and 9, so you don't have to worry about complex arithmetics. First, you'll do some practice trials so you know how the task works.\n\nPress the <space> bar to start."
txt_instr.draw()
win.flip()

event.waitKeys(keyList=['space'])
win.flip()
core.wait(1)

#some practice trials
practice_pool = [2,4,6]
for trial in practice_pool: 
    setsize = trial
    
    run_details = general_runcreator(setsize)
    core.wait(0.5)
    
    if setsize == 2:
        updates = run_details[2]
        A1.pos = (0,140)
        B1.pos = (0,-140)
        
        A1.text = run_details[0]['A1']
        B1.text = run_details[0]['B1']
        
        reset_box_color()
        box_draw(2)
        A1.draw()
        B1.draw()
        win.flip()
        
        event.clearEvents()
        event.waitKeys(keyList=['space'])
        
        box_draw(2)
        win.flip()
        core.wait(0.5)
        
        stim_track= []
        
        for stim in updates:
            if stim['dig']>0:
                stim_dig = '+'+str(stim['dig'])
            else:
                stim_dig = str(stim['dig'])
            
            exec("%s.text = stim_dig" % stim['pos'])
            exec("%s.draw()" % stim['pos'])
            reset_box_color()
            box_draw(2)
            win.flip()
            
            resp_prestore = event.waitKeys(keyList = ['space','esc','escape'],timeStamped=clock)
            if resp_prestore[0][0] == 'escape':
                core.quit()
            stim_track.append(stim['pos'])
            
            
            reset_box_color()
            box_draw(2)
            win.flip()
            core.wait(0.5)
        
        corr_resp = run_details[1]
        
        prov_correct = 0
        
        for item in corr_resp:
            dim_box_color()
            txt_topinstr.text = 'Please enter the resulting number in the highlighted box'
            if item == 'A1':
                box3.lineColor=(1,1,1) 
            else:
                box4.lineColor=(1,1,1)
            
            box_draw(2)
            txt_topinstr.draw()
            if item == 'A1':
                txt_input.pos = (0,140)
            else:
                txt_input.pos = (0,-140)
            win.flip()
            
            
            answer = int(collect_response())
            
            if answer == corr_resp[item]:
                prov_correct+=1 
            
        win.flip()
        core.wait(1)
        if prov_correct == 2:
            txt_feedback.text = 'You got them right!'
            txt_feedback.draw()
            win.flip()
            core.wait(2)
        else:
            txt_feedback.text = 'Those were not the resulting numbers...'
            txt_feedback.draw()
            win.flip()
            core.wait(2)
    
    elif setsize == 4:
        updates = run_details[2]
        A1.pos = (-110,140)
        B1.pos = (-110,-140)
        A2.pos = (110,140)
        B2.pos = (110,-140)
        
        A1.text = run_details[0]['A1']
        A2.text = run_details[0]['A2']
        B1.text = run_details[0]['B1']
        B2.text = run_details[0]['B2']
        
        reset_box_color()
        box_draw(4)
        A1.draw()
        B1.draw()
        A2.draw()
        B2.draw()
        win.flip()
        
        event.clearEvents()
        event.waitKeys(keyList=['space'])
        
        box_draw(4)
        win.flip()
        core.wait(0.5)
        
        stim_track= []
        
        for stim in updates:
            if stim['dig']>0:
                stim_dig = '+'+str(stim['dig'])
            else:
                stim_dig = str(stim['dig'])
            
            exec("%s.text = stim_dig" % stim['pos'])
            exec("%s.draw()" % stim['pos'])
            reset_box_color()
            box_draw(4)
            win.flip()
            
            resp_prestore = event.waitKeys(keyList = ['space','escape'],timeStamped=clock)
            if resp_prestore[0][0] == 'escape':
                core.quit()
            stim_track.append(stim['pos'])
            
            
            reset_box_color()
            box_draw(4)
            win.flip()
            core.wait(0.5)
        
        corr_resp = run_details[1]
        
        prov_correct = 0
        
        for item in corr_resp:
            dim_box_color()
            txt_topinstr.text = 'Please enter the resulting number in the highlighted box'
            if item == 'A1':
                box9.lineColor=(1,1,1) 
            elif item == 'A2':
                box7.lineColor=(1,1,1)
            elif item == 'B1':
                box10.lineColor=(1,1,1)
            elif item == 'B2':
                box8.lineColor=(1,1,1)
            
            box_draw(4)
            txt_topinstr.draw()
            if item == 'A1':
                txt_input.pos = (-110,135)
            elif item == 'A2':
                txt_input.pos = (110,135)
            elif item == 'B1':
                txt_input.pos = (-110,-135)
            elif item == 'B2':
                txt_input.pos = (110,-135)
            win.flip()
            
            answer = int(collect_response())
            
            if answer == corr_resp[item]:
                prov_correct+=1
        
        if prov_correct == 4:
            txt_feedback.text = 'You got them right!'
            txt_feedback.draw()
            win.flip()
            core.wait(2)
        else:
            txt_feedback.text = 'Those were not the resulting numbers...'
            txt_feedback.draw()
            win.flip()
            core.wait(2)
            
        win.flip()
        core.wait(1)
    
    elif setsize == 6:
        updates = run_details[2]
        A1.pos = (-230,140)
        B1.pos = (-230,-140)
        A2.pos = (0,140)
        B2.pos = (0,-140)
        A3.pos = (230,140)
        B3.pos = (230,-140)
        
        A1.text = run_details[0]['A1']
        A2.text = run_details[0]['A2']
        B1.text = run_details[0]['B1']
        B2.text = run_details[0]['B2']
        A3.text = run_details[0]['A3']
        B3.text = run_details[0]['B3']
        
        reset_box_color()
        box_draw(6)
        A1.draw()
        B1.draw()
        A2.draw()
        B2.draw()
        A3.draw()
        B3.draw()
        win.flip()
        
        event.clearEvents()
        event.waitKeys(keyList=['space'])
        
        box_draw(6)
        win.flip()
        core.wait(0.5)
        
        stim_track= []
        
        for stim in updates:
            if stim['dig']>0:
                stim_dig = '+'+str(stim['dig'])
            else:
                stim_dig = str(stim['dig'])
            
            exec("%s.text = stim_dig" % stim['pos'])
            exec("%s.draw()" % stim['pos'])
            reset_box_color()
            box_draw(6)
            clock.reset()
            win.flip()
            
            resp_prestore = event.waitKeys(keyList = ['space','escape'],timeStamped=clock)
            if resp_prestore[0][0] == 'escape':
                core.quit()
            stim_track.append(stim['pos'])
            
            reset_box_color()
            box_draw(6)
            win.flip()
            core.wait(0.5)
        
        corr_resp = run_details[1]
        
        prov_correct = 0
        
        for item in corr_resp:
            dim_box_color()
            txt_topinstr.text = 'Please enter the resulting number in the highlighted box'
            if item == 'A1':
                box1.lineColor=(1,1,1) 
            elif item == 'A2':
                box3.lineColor=(1,1,1)
            elif item == 'B1':
                box2.lineColor=(1,1,1)
            elif item == 'B2':
                box4.lineColor=(1,1,1)
            elif item == 'A3':
                box5.lineColor=(1,1,1)
            elif item == 'B3':
                box6.lineColor=(1,1,1)
            
            box_draw(6)
            txt_topinstr.draw()
            if item == 'A1':
                txt_input.pos = (-230,140)
            elif item == 'A2':
                txt_input.pos = (0,140)
            elif item == 'A3':
                txt_input.pos = (230,140)
            elif item == 'B1':
                txt_input.pos = (-230,-140)
            elif item == 'B2':
                txt_input.pos = (0,-140)
            elif item == 'B3':
                txt_input.pos = (230,-140)
            win.flip()
            
            #print corr_resp
            answer = int(collect_response())
            
            if answer == corr_resp[item]:
                prov_correct+=1
        
        if prov_correct == 6:
            txt_feedback.text = 'You got them right!'
            txt_feedback.draw()
            win.flip()
            core.wait(2)
        else:
            txt_feedback.text = 'Those were not the resulting numbers...'
            txt_feedback.draw()
            win.flip()
            core.wait(2)
            
        win.flip()
        core.wait(1)
    
    txt_instr.text = 'Press any key to continue'
    txt_instr.draw()
    win.flip()
    
    event.waitKeys()

txt_instr.text = "Now that you have done some practice we can start the real trials. Don't worry if you found the task hard, specially the ones with more boxes, that's normal.\n\nIf you fell you still don't quite underestand how the task works do not hesitate to ask the examiner. It is very important that you feel confident regarding what you are expected to do.\n\nIf you fell ready to start just press the <space> bar. You are allowed to take short rests between trials (after entering the response and before the next set of boxes appear)."
txt_instr.draw()
win.flip()
event.waitKeys(keyList=['space'])

#the real task
for trial in range(14): #in original study was 16, I may use 14. I could test with 15
    setsize = runs_pool.pop(random.randint(0,len(runs_pool)-1))
    
    run_details = general_runcreator(setsize)
    core.wait(0.5)
    
    if setsize == 2:
        updates = run_details[2]
        A1.pos = (0,140)
        B1.pos = (0,-140)
        
        A1.text = run_details[0]['A1']
        B1.text = run_details[0]['B1']
        
        reset_box_color()
        box_draw(2)
        A1.draw()
        B1.draw()
        clock.reset()
        win.flip()
        
        event.clearEvents()
        resp_storage2.append(round(event.waitKeys(keyList=['space'],timeStamped=clock)[-1][1],4))
        
        box_draw(2)
        win.flip()
        core.wait(0.5)
        
        stim_track= []
        
        for stim in updates:
            if stim['dig']>0:
                stim_dig = '+'+str(stim['dig'])
            else:
                stim_dig = str(stim['dig'])
            
            exec("%s.text = stim_dig" % stim['pos'])
            exec("%s.draw()" % stim['pos'])
            reset_box_color()
            box_draw(2)
            clock.reset()
            win.flip()
            
            resp_prestore = event.waitKeys(keyList = ['space','esc','escape'],timeStamped=clock)
            if resp_prestore[0][0] == 'escape':
                core.quit()
            stim_track.append(stim['pos'])
            
            if len(stim_track) > 1:
                if stim['pos'] == stim_track[-2]:
                    resp_nosw2.append(round(resp_prestore[-1][1],4))
                else:
                    resp_sw2.append(round(resp_prestore[-1][1],4))
            
            reset_box_color()
            box_draw(2)
            win.flip()
            core.wait(0.5)
        
        corr_resp = run_details[1]
        
        prov_correct = 0
        
        for item in corr_resp:
            dim_box_color()
            txt_topinstr.text = 'Please enter the resulting number in the highlighted box'
            if item == 'A1':
                box3.lineColor=(1,1,1) 
            else:
                box4.lineColor=(1,1,1)
            
            box_draw(2)
            txt_topinstr.draw()
            if item == 'A1':
                txt_input.pos = (0,140)
            else:
                txt_input.pos = (0,-140)
            win.flip()
            
            
            answer = int(collect_response())
            
            if answer == corr_resp[item]:
                prov_correct+=1 
            
        win.flip()
        core.wait(1)
        if prov_correct == 2:
            [out_resp_nosw2.append(i) for i in resp_nosw2]
            [out_resp_storage2.append(i) for i in resp_storage2]
            [out_resp_sw2.append(i) for i in resp_sw2]
            correct2 += 1
        
        trials += 1
    
    elif setsize == 4:
        updates = run_details[2]
        A1.pos = (-110,140)
        B1.pos = (-110,-140)
        A2.pos = (110,140)
        B2.pos = (110,-140)
        
        A1.text = run_details[0]['A1']
        A2.text = run_details[0]['A2']
        B1.text = run_details[0]['B1']
        B2.text = run_details[0]['B2']
        
        reset_box_color()
        box_draw(4)
        A1.draw()
        B1.draw()
        A2.draw()
        B2.draw()
        clock.reset()
        win.flip()
        
        event.clearEvents()
        resp_storage4.append(round(event.waitKeys(keyList=['space'],timeStamped=clock)[-1][1],4))
        
        box_draw(4)
        win.flip()
        core.wait(0.5)
        
        stim_track= []
        
        for stim in updates:
            if stim['dig']>0:
                stim_dig = '+'+str(stim['dig'])
            else:
                stim_dig = str(stim['dig'])
            
            exec("%s.text = stim_dig" % stim['pos'])
            exec("%s.draw()" % stim['pos'])
            reset_box_color()
            box_draw(4)
            clock.reset()
            win.flip()
            
            resp_prestore = event.waitKeys(keyList = ['space','escape'],timeStamped=clock)
            if resp_prestore[0][0] == 'escape':
                core.quit()
            stim_track.append(stim['pos'])
            
            if len(stim_track) > 1:
                if stim['pos'] == stim_track[-2]:
                    resp_nosw4.append(round(resp_prestore[-1][1],4))
                    print 'nosw', resp_nosw4
                else:
                    resp_sw4.append(round(resp_prestore[-1][1],4))
                    print 'sw', resp_sw4
            
            reset_box_color()
            box_draw(4)
            win.flip()
            core.wait(0.5)
        
        corr_resp = run_details[1]
        
        prov_correct = 0
        
        for item in corr_resp:
            dim_box_color()
            txt_topinstr.text = 'Please enter the resulting number in the highlighted box'
            if item == 'A1':
                box9.lineColor=(1,1,1) 
            elif item == 'A2':
                box7.lineColor=(1,1,1)
            elif item == 'B1':
                box10.lineColor=(1,1,1)
            elif item == 'B2':
                box8.lineColor=(1,1,1)
            
            box_draw(4)
            txt_topinstr.draw()
            if item == 'A1':
                txt_input.pos = (-110,135)
            elif item == 'A2':
                txt_input.pos = (110,135)
            elif item == 'B1':
                txt_input.pos = (-110,-135)
            elif item == 'B2':
                txt_input.pos = (110,-135)
            win.flip()
            
            answer = int(collect_response())
            
            if answer == corr_resp[item]:
                prov_correct+=1
        
        if prov_correct == 4:
            [out_resp_nosw4.append(i) for i in resp_nosw4]
            [out_resp_storage4.append(i) for i in resp_storage4]
            [out_resp_sw4.append(i) for i in resp_sw4]
            correct4 += 1
            
        trials += 1
        win.flip()
        core.wait(1)
    
    elif setsize == 6:
        updates = run_details[2]
        A1.pos = (-230,140)
        B1.pos = (-230,-140)
        A2.pos = (0,140)
        B2.pos = (0,-140)
        A3.pos = (230,140)
        B3.pos = (230,-140)
        
        A1.text = run_details[0]['A1']
        A2.text = run_details[0]['A2']
        B1.text = run_details[0]['B1']
        B2.text = run_details[0]['B2']
        A3.text = run_details[0]['A3']
        B3.text = run_details[0]['B3']
        
        reset_box_color()
        box_draw(6)
        A1.draw()
        B1.draw()
        A2.draw()
        B2.draw()
        A3.draw()
        B3.draw()
        clock.reset()
        win.flip()
        
        event.clearEvents()
        resp_storage6.append(round(event.waitKeys(keyList=['space'],timeStamped=clock)[-1][1],4))
        
        box_draw(6)
        win.flip()
        core.wait(0.5)
        
        stim_track= []
        
        for stim in updates:
            if stim['dig']>0:
                stim_dig = '+'+str(stim['dig'])
            else:
                stim_dig = str(stim['dig'])
            
            exec("%s.text = stim_dig" % stim['pos'])
            exec("%s.draw()" % stim['pos'])
            reset_box_color()
            box_draw(6)
            clock.reset()
            win.flip()
            
            resp_prestore = event.waitKeys(keyList = ['space','escape'],timeStamped=clock)
            if resp_prestore[0][0] == 'escape':
                core.quit()
            stim_track.append(stim['pos'])
            
            if len(stim_track) > 1:
                if stim['pos'] == stim_track[-2]:
                    resp_nosw6.append(round(resp_prestore[-1][1],4))
                else:
                    resp_sw6.append(round(resp_prestore[-1][1],4))
            
            reset_box_color()
            box_draw(6)
            win.flip()
            core.wait(0.5)
        
        corr_resp = run_details[1]
        
        prov_correct = 0
        
        for item in corr_resp:
            dim_box_color()
            txt_topinstr.text = 'Please enter the resulting number in the highlighted box'
            if item == 'A1':
                box1.lineColor=(1,1,1) 
            elif item == 'A2':
                box3.lineColor=(1,1,1)
            elif item == 'B1':
                box2.lineColor=(1,1,1)
            elif item == 'B2':
                box4.lineColor=(1,1,1)
            elif item == 'A3':
                box5.lineColor=(1,1,1)
            elif item == 'B3':
                box6.lineColor=(1,1,1)
            
            box_draw(6)
            txt_topinstr.draw()
            if item == 'A1':
                txt_input.pos = (-230,140)
            elif item == 'A2':
                txt_input.pos = (0,140)
            elif item == 'A3':
                txt_input.pos = (230,140)
            elif item == 'B1':
                txt_input.pos = (-230,-140)
            elif item == 'B2':
                txt_input.pos = (0,-140)
            elif item == 'B3':
                txt_input.pos = (230,-140)
            win.flip()
            
            #print corr_resp
            answer = int(collect_response())
            
            if answer == corr_resp[item]:
                prov_correct+=1
        
        if prov_correct == 6:
            [out_resp_nosw6.append(i) for i in resp_nosw6]
            [out_resp_storage6.append(i) for i in resp_storage6]
            [out_resp_sw6.append(i) for i in resp_sw6]
            correct6 += 1
            
        trials += 1
        win.flip()
        core.wait(1)
    
    txt_instr.text = 'Press any key to continue'
    txt_instr.draw()
    win.flip()
    
    event.waitKeys()

mean_storage2 = np.mean(out_resp_storage2) if len(out_resp_storage2)>0 else 0
mean_storage4 = np.mean(out_resp_storage4) if len(out_resp_storage4)>0 else 0
mean_storage6 = np.mean(out_resp_storage6) if len(out_resp_storage6)>0 else 0
mean_nosw2 = np.mean(out_resp_nosw2) if len(out_resp_nosw2)>0 else 0
mean_nosw4 = np.mean(out_resp_nosw4) if len(out_resp_nosw4)>0 else 0
mean_nosw6 = np.mean(out_resp_nosw6) if len(out_resp_nosw6)>0 else 0
mean_sw2 = np.mean(out_resp_sw2) if len(out_resp_sw2)>0 else 0
mean_sw4 = np.mean(out_resp_sw4) if len(out_resp_sw4)>0 else 0
mean_sw6 = np.mean(out_resp_sw6) if len(out_resp_sw6)>0 else 0

np.savetxt(file_name, [('#trials','correct2','correct4','correct6','mean_storage2','mean_storage4',
    'mean_storage6','mean_nosw2','mean_nosw4','mean_nosw6','mean_sw2','mean_sw4','mean_sw6','raw_storage2',
    'raw_storage4','raw_storage6','raw_nosw2','raw_nosw4','raw_nosw6','raw_sw2','raw_sw4','raw_sw6'),
    (trials,correct2,correct4,correct6,mean_storage2,mean_storage4,mean_storage6,mean_nosw2,mean_nosw4,
    mean_nosw6,mean_sw2,mean_sw4,mean_sw6,str(out_resp_storage2),str(out_resp_storage4),
    str(out_resp_storage6),str(out_resp_nosw2),str(out_resp_nosw4),str(out_resp_nosw6),str(out_resp_sw2),
    str(out_resp_sw4),str(out_resp_sw6))],fmt='%s',delimiter=',')

txt_instr.text = 'The task has concluded.\n\nPress any key.'
txt_instr.draw()
win.flip()

event.waitKeys()

win.close()