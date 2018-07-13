from psychopy import visual, event

win = visual.Window()

figure = visual.ImageStim(win, 'frame(2).png')
figure.draw()
win.flip()

event.waitKeys()

win.close()