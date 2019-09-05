from psychopy import visual, core, data, gui, event, data, logging
from itertools import cycle
import numpy as N
import time

info = {}
monSize = [800, 600]
info['fullscr'] = False

win = visual.Window(monSize, fullscr=info['fullscr'],
                    monitor='testMonitor', units='deg')

indices=[0,1]
stim_cycle=cycle([['sweet.jpg','unsweet.jpg'],['unsweet.jpg','sweet.jpg']])

stim_images=stim_cycle.next()

visual_stim1=visual.ImageStim(win, image=N.zeros((300,300)),pos=(0,-0.25), size=(0.25,0.25),units='height')
visual_stim2=visual.ImageStim(win, image=N.zeros((300,300)),pos=(0,0.25), size=(0.25,0.25),units='height')
        
    
visual_stim1.setImage(stim_images[indices[0]])#set which image appears
visual_stim2.setImage(stim_images[indices[1]])#set which image appears
        
frame_rate = win.getActualFrameRate(nIdentical=60, nMaxFrames=10000,
    nWarmUpFrames=10, threshold=1)
print(frame_rate)
# The number of frames you want to display is equal to
# the product of frame-rate and the number of seconds to display
# the stimulus.
# n_frames = frame_rate * n_seconds
start = time.time()
for frameN in range(int(frame_rate*5.0)):
    visual_stim1.draw()
    visual_stim2.draw()
    win.flip()
end = time.time()
print(end - start)