#pilot task practice: 09/2019
#Copied from taste task original 2/16/2018
#this is the PILOT pre-task practice for the probabilistic learning task for BeveL (a substudy of bevbits, formerly juice)
#the pkl file contains all study data as a back up including what files were used, useful for sanity checks
#the csv file is easier to read
#the log file also has onsets, but it has the time from when the .py file was initalized more accurate should be used for analysis

from psychopy import visual, core, data, gui, event, data, logging
import csv
import time
import serial
import numpy as N
import sys,os,pickle
import datetime
import exptutils
from exptutils import *
import random
from random import shuffle
from itertools import cycle

monSize = [800, 600]
info = {}
info['fullscr'] = False
info['participant'] = 'test'
info['computer']=(os.getcwd()).split('/')[2]
dlg = gui.DlgFromDict(info)
if not dlg.OK:
    core.quit()
########################################
subdata={}

subdata['completed']=0
subdata['cwd']=os.getcwd()

clock=core.Clock()
datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
subdata['datestamp']=datestamp
subdata['expt_title']='bevel_prob_pilot'

subdata['response']={}
subdata['score']={}
subdata['rt']={}
subdata['stim_onset_time']={}
subdata['stim_log']={}
subdata['is_this_SS_trial']={}
subdata['SS']={}
subdata['broke_on_trial']={}
subdata['simulated_response']=False

subdata['onset']='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/practice_onset_files/onsets'
subdata['jitter']='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/practice_onset_files/jitter'
subdata['conds']='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/practice_onset_files/conds'
subdata['quit_key']='q'

#######################################
dataFileName='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/bevel_%s_%s_practice_subdata.log'%(info['participant'],subdata['datestamp'])
logging.console.setLevel(logging.INFO)
logfile=logging.LogFile(dataFileName,level=logging.DATA)
ratings_and_onsets = []
key_responses=[]
correct_response=[]
flip=[]
#######################################

#global settings aka Input parameters, make sure these match with the effciciency calculation
delivery_time=1.0
cue_time=3.0
wait_time=4.0
rinse_time=1.0
fix=int(1)

# HELPER FUNCTIONS. These are pulled from Russ. We don't change these usually.
def show_instruction(instrStim):
    # shows an instruction until a key is hit.
    while True:
        instrStim.draw()
        win.flip()
        if len(event.getKeys()) > 0:
            break
        event.clearEvents()


def show_stim(stim, seconds):
    # shows a stim for a given number of seconds
    for frame in range(60 * seconds):
        stim.draw()
        win.flip()

def check_for_quit(subdata,win):
    k=event.getKeys()
    print 'checking for quit key %s'%subdata['quit_key']
    print 'found:',k
    if k.count(subdata['quit_key']) >0:# if subdata['quit_key'] is pressed...
        print 'quit key pressed'
        return True
    else:
        return False


# MONITOR set up
# set the window size as win
win = visual.Window(monSize, fullscr=info['fullscr'],
                    monitor='testMonitor', units='deg')

# STIMS
fixation_text = visual.TextStim(win, text='+', pos=(0, 0), height=2)

#Direction text (from Doll, Jacobs, Sanfey Frank (2009))
scan_trigger_text = visual.TextStim(win, text='Waiting for scan trigger...', pos=(0, 0))
example_images=['x.jpg','y.jpg']
example_stim1=visual.ImageStim(win, image=N.zeros((300,300)),pos=(0.25,0.25), size=(0.25,0.35),units='height')
example_stim2=visual.ImageStim(win, image=N.zeros((300,300)),pos=(-0.25,0.25), size=(0.25,0.35),units='height')
example_stim1.setImage(example_images[0])#set which image appears
example_stim2.setImage(example_images[1])#set which image appears
example_stim1.draw()
example_stim2.draw()
scan_trigger_text = visual.TextStim(win, text='Two symbols will appear on the screen. You will have 2 seconds to guess which symbol is correct (1=left shape or 2=right shape). Each shape has a certain PROBABILITY of being correct. In each pair, one shape is MORE LIKELY to be correct. Try to learn which shape has the highest CHANCE of being correct in each pair', pos=(0, -2), height=0.75)

#####################
######load in onset files########

onsets=[]
f=open(subdata['onset'],'r')
x = f.readlines()
for i in x:
    onsets.append(i.strip())
print(onsets)
onsets=[float(i) for i in onsets]
print(onsets, 'onsets')

jitter=[]
g=open(subdata['jitter'],'r')
y = g.readlines()
for i in y:
    jitter.append(i.strip())

jitter=[float(i) for i in jitter]
print(jitter, 'jitter')

#for this the trial conditions are created randomly each time so it doesn't really matter, the length is what matters
trialcond=N.loadtxt(subdata['conds'], dtype='int')
print(trialcond,'trial conditions')

ntrials=len(trialcond)
#pump=N.zeros(ntrials)

##########################SET UP INDEXING FOR SHUFFLING IMAGE PAIR, POSITION, and RESPONSE################################################################################

# specify lists of stimulus positions and their corresponding responses:
#set contingency that the sweet is rewarding
positions = [(0.25,0), (-0.25,0)]
positions_eng = ['right','left']
positions_scan=['2','1']
pos_ind = [0,1]

#stim_cycle=cycle([['sweet.jpg','unsweet.jpg'],['unsweet.jpg','sweet.jpg']])
#these are indexed on indicies
stim_images1=['a.jpg','b.jpg']
stim_images2=['c.jpg','d.jpg']
stim_images3=['e.jpg','f.jpg']
stim_list=[stim_images1, stim_images2, stim_images3]

prob1=[0.8, 0.2]
prob2=[0.7, 0.3]
prob3=[0.6, 0.4]
prob_list=[prob1, prob2, prob3]

inv_prob1=[0.2, 0.8]
inv_prob2=[0.3, 0.7]
inv_prob3=[0.4, 0.6]
inv_prob_list=[inv_prob1, inv_prob2, inv_prob3]

#stim list, prob list, and inv_prob list are on prob index
prob_index=[0,1,2]

#this index allows us to switch which key press is associated with which side, while maintaing the image to pump pair
indices=[0,1]

####This is where we set the response
##1 = correct
##2 = incorrect
reinforcer_responses = [1,2]

subdata['trialdata']={}

##########################RUN THE MAIN BLOCK ################################################################################

"""
    The main run block!
"""

def run_block(fix):

    # Await scan trigger
    while True:
        scan_trigger_text.draw()
        win.flip()
        if 'o' in event.waitKeys():
            logging.log(logging.DATA, "start key press")
            break
        event.clearEvents()

    clock=core.Clock()
    t = clock.getTime()

    #set up the fixation
    ratings_and_onsets.append(['fixation',t])
    logging.log(logging.DATA, "fixation %f"%t)
    show_stim(fixation_text, fix)  # 8 sec blank screen with fixation cross

    #log fixation
    logging.log(logging.DATA, "fixation end %f"%t)
    t = clock.getTime()

    #reset the clock so the onsets are correct (if onsets have the 8 sec in them then you dont need this)
    clock.reset()
    ratings_and_onsets.append(['start',t])
    logging.log(logging.DATA, "START")


    #start the taste loop
    for trial in range(ntrials):
        #check for quit
        if check_for_quit(subdata,win):
            exptutils.shut_down_cleanly(subdata,win)
            sys.exit()
        #empty trial data
        trialdata={}
        trialdata['onset']=onsets[trial]


        #Set which side IMG1 and IMG2 are on.

        #shuffle(pos_ind) <- moved to the end of the script
        visual_stim1=visual.ImageStim(win, image=N.zeros((300,300)),pos=positions[pos_ind[0]], size=(0.25,0.25),units='height')
        visual_stim2=visual.ImageStim(win, image=N.zeros((300,300)),pos=positions[pos_ind[1]], size=(0.25,0.25),units='height')

        #set which image pair to show.
        x= trialcond[trial]
        print(x)

        stim_images=stim_list[x]
        trial_prob=prob_list[x]
        trial_inv_prob=inv_prob_list[x]
        master_prob_list=[trial_prob,trial_inv_prob]

        #Set which shape is IMG1 and IMG2
        visual_stim1.setImage(stim_images[indices[0]])#set which image appears
        visual_stim2.setImage(stim_images[indices[1]])#set which image appears

        #shuffle(indicies) <- moved lower in script

        #creating a dictory which will store the postion with the image and pump, the image and pump need to match
        mydict={}
        mydict[positions_scan[pos_ind[1]]] = [stim_images[indices[1]], master_prob_list[indices[1]]]
        mydict[positions_scan[pos_ind[0]]] = [stim_images[indices[0]], master_prob_list[indices[0]]]

        print(mydict)

        #Question Prompt
        message=visual.TextStim(win, text='Which is Correct?',pos=(0,5))
        print trial
        t = clock.getTime()

        #get the time of the image and log, this log is appending it to the csv file
        visual_stim1.draw()#making image of the logo appear
        visual_stim2.draw()#making image of the logo appear
        message.draw()
        RT = core.Clock()

        #this is logging when the message is shown
        logging.log(logging.DATA, "%s at position=%s and %s at position=%s"%(stim_images[indices[0]],positions_eng[pos_ind[0]],stim_images[indices[1]],positions_eng[pos_ind[1]]))
        logging.flush()

        while clock.getTime()<trialdata['onset']:
            pass
        win.flip()

        RT.reset() # reaction time starts immediately after flip

        while clock.getTime()<(trialdata['onset']+cue_time):#show the image, while clock is less than onset and cue, show cue
            pass

        keys = event.getKeys(keyList=['1','2'],timeStamped=RT)
        print(keys)
        win.flip()

        # get the key press logged, and time stamped

        if len(keys)>0:
            logging.log(logging.DATA, "keypress=%s at time= %f"%(keys[0][0],keys[0][1]))
            print("here are the keys:")
            print(keys)
            t = clock.getTime()
            logging.flush()

            #back up of the key press
            tempArray = [t, keys[0]]
            key_responses.append(tempArray)
            ratings_and_onsets.append(["keypress=%s"%keys[0][0],t])
            if keys[0][0] == '1':
                #draw a box on the left shape
                rectangle_l = visual.Rect(win, pos=(-0.25,0), size=(0.75,0.75),units='height',fillColor=[0, 0, 0],
                lineColor=[1, -1, -1])
                rectangle_l.draw()
                visual_stim1.draw()
                visual_stim2.draw()
                #from the dictionary find the image code associated with the key press
                #taste=int(mydict['left'][1])
                image=(mydict['1'][0])
                trial_prob=(mydict['1'][1])

                #choose the feedback
                taste=int(N.random.choice(reinforcer_responses, 1, p=trial_prob))
                print(taste)
                if taste == 1:
                    message=visual.TextStim(win, text='Correct', pos=(0,5), height=2)
                    message.draw()
                    print 'Reinforcement is correct'
                else:
                    message=visual.TextStim(win, text='Incorrect', pos=(0,5), height=2)
                    message.draw()
                    print 'Reinforcement is incorrect'
                #log the pump used, time, and key press
                print 'Reinforcement is %s'%taste
                logging.log(logging.DATA,"Reinforcement of %s and a keypress of %s for image of %s"%(taste,keys[0][0], image))
                t = clock.getTime()
                ratings_and_onsets.append(["Reinforcement is %s"%taste, t, keys[0][0]])
                logging.flush()

            elif keys[0][0] == '2':
                # show a rectangle on the right
                rectangle_r = visual.Rect(win, pos=(0.25,0), size=(0.75,0.75),units='height',fillColor=[0, 0, 0],
                lineColor=[1, -1, -1])
                rectangle_r.draw()
                visual_stim1.draw()
                visual_stim2.draw()
                #from the dictonary get the image associated with the right key press
                image=(mydict['2'][0])
                trial_prob=(mydict['2'][1])

                #choose the feedback
                taste=int(N.random.choice(reinforcer_responses, 1, p=trial_prob))
                print(taste)
                if taste == 1:
                    message=visual.TextStim(win, text='Correct', pos=(0,5), height=2)
                    message.draw()
                    print 'Reinforcement is correct'
                else:
                    message=visual.TextStim(win, text='Incorrect', pos=(0,5), height=2)
                    message.draw()
                    print 'Reinforcement is incorrect'

                #log the time, keypress, and pump
                print 'Reinforcement is %s'%taste
                logging.log(logging.DATA,"Reinforcement of %s and a keypress of %s for image of %s"%(taste,keys[0][0], image))
                t = clock.getTime()
                ratings_and_onsets.append(["Reinforcement is %s"%taste, t, keys[0][0]])
                logging.flush()
        else:
            taste=0
            t = clock.getTime()
            logging.log(logging.DATA,"Key Press Missed!")
            keys=keys.append(['MISS',t])
            logging.flush()
            message=visual.TextStim(win, text='Please answer quicker', pos=(0, 0), height=2)#this lasts throught the taste
            message.draw()
            win.flip()


        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time):
            pass

        message=visual.TextStim(win, text='', pos=(0, 0), height=2) #this lasts throught the wait
        message.draw()
        win.flip()
        t = clock.getTime()
        ratings_and_onsets.append(["wait", t])


        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
            pass

        message=visual.TextStim(win, text='', pos=(0, 0), height=2)#this lasts throught the rinse
        message.draw()
        win.flip()

        #print 'injecting rinse via pump at address %d'%0
        #t = clock.getTime()
        #ratings_and_onsets.append(['injecting rinse via pump at address %d'%0, t])
        #ser.write('%dRUN\r'%0)
        #logging.log(logging.DATA, "RINSE")
        #logging.flush()



        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time):
            pass

        message=visual.TextStim(win, text='+', pos=(0, 0), height=2)#lasts through the jitter
        message.draw()
        win.flip()
        t = clock.getTime()
        ratings_and_onsets.append(["jitter", t])

        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time+jitter[trial]):
            pass

        t = clock.getTime()
        ratings_and_onsets.append(['end time', t])
        logging.log(logging.DATA,"finished")
        logging.flush()
        subdata['trialdata'][trial]=trialdata



        print(key_responses)

        #shuffle indices for the next trial
        shuffle(indices)
        shuffle(pos_ind)

    win.close()


run_block(fix)

#subdata['key_responses']=keys_responses

subdata.update(info)
f=open('/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/bevel_%s_%s_practice_subdata.pkl'%(info['participant'],subdata['datestamp']),'wb')
pickle.dump(subdata,f)
f.close()

myfile = open('/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/bevel_%s_%s_practice_subdata.csv'%(info['participant'],subdata['datestamp']), 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(['event','data'])
for row in ratings_and_onsets:
    wr.writerow(row)


core.quit()
