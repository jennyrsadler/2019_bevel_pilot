# PST Practice 

#this is a set of practice trials for the probabilistic learning task for bevel pilot testing
#this is done OUT OF SCANNER

#the pkl file contains all study data as a back up including what files were used, useful for sanity checks
#the csv file is easier to read
#the log file also has onsets, but it has the time from when the .py file was initalized more accurate should be used for analysis

#Imports
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
#import pdb

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
subdata['expt_title']='sidepiece_prob'

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
subdata['cond']='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/practice_onset_files/conds'
subdata['quit_key']='q'

#######################################
dataFileName='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/%s_%s_practice_subdata.log'%(info['participant'],subdata['datestamp'])
logging.console.setLevel(logging.INFO)
logfile=logging.LogFile(dataFileName,level=logging.DATA)
ratings_and_onsets = []
key_responses=[]
correct_response=[]
flip=[]
#######################################
# Serial connection and commands setup
#ser = serial.Serial(
#                    port=info['port'],
#                    baudrate=19200,
#                    parity=serial.PARITY_NONE,
#                    stopbits=serial.STOPBITS_ONE,
#                    bytesize=serial.EIGHTBITS
#                   )
#if not ser.isOpen():
#    ser.open()
#
time.sleep(1)

#global settings aka Input parameters, make sure these match with the effciciency calculation
delivery_time=0.5
cue_time=2.0
wait_time=1.0
fix=int(2)

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

scan_trigger_text = visual.TextStim(win, text='Waiting for task to begin', pos=(0, 0))

#Direction text
example_images=['ex1.jpg','ex2.jpg']
example_stim1=visual.ImageStim(win, image=N.zeros((300,300)),pos=(0.25,0.30), size=(0.25,0.35),units='height')
example_stim2=visual.ImageStim(win, image=N.zeros((300,300)),pos=(-0.25,0.30), size=(0.25,0.35),units='height')
example_stim1.setImage(example_images[0])#set which image appears
example_stim2.setImage(example_images[1])#set which image appears
example_stim1.draw()
example_stim2.draw()
scan_trigger_text = visual.TextStim(win, text='During this game, you will see three pairs of shapes. Each shape has a probability with which it is correct. Your goal is to figure out which shape has a higher probability of being correct in each pair. Use the arrow keys to choose a shape. After you choose, you will receive written feedback. Try to choose correctly as much as possible.', pos=(0, -1.75), height=0.8)

#set onset times
onsets=[]
f=open(subdata['onset'],'r')
x = f.readlines()
for i in x:
    onsets.append(i.strip())
print(onsets)
onsets=[float(i) for i in onsets]
print(onsets, 'onsets')

#set condition order 
cond=[]
f=open(subdata['cond'],'r')
x = f.readlines()
for i in x:
    cond.append(i.strip())
print(cond)
cond=[float(i) for i in cond]
print(cond, 'cond')

#for this the trial conditions are created randomly each time so it doesn't really matter, the length is what matters
trialcond=N.loadtxt(subdata['cond'], dtype='int')
print(trialcond,'trial conditions')
ntrials=len(trialcond)


# specify lists of stimulus positions and their corresponding responses:
positions = [(0.25,0), (-0.25,0)]
positions_eng = ['right','left']
positions_scan=['2','1']
pos_ind = [0,1]

#these are indexed on img_index
stim_images1=['a.jpg','b.jpg']
stim_images2=['c.jpg','d.jpg']
stim_images3=['e.jpg','f.jpg']

img_index=[0,1]


#probabilities for each pair
prob1=[0.8, 0.2]
prob2=[0.7, 0.3]
prob3=[0.6, 0.4]

inv_prob1=[0.2, 0.8]
inv_prob2=[0.3, 0.7]
inv_prob3=[0.4, 0.6]


#stim list is on the stim index
stim_list=[stim_images1, stim_images2, stim_images3]
stim_index=[0,1,2]

prob_list=[prob1, prob2, prob3]
inv_prob_list=[inv_prob1, inv_prob2, inv_prob3]
prob_index=[0,1,2]


#Index for feedback 
indices=[0,1]

feedback =['Correct','Incorrect']
feedback_index = [0, 1] 

subdata['trialdata']={}

            
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
    
    
    #start the loop
    for trial in range(ntrials):
        #check for quit
        if check_for_quit(subdata,win):
            exptutils.shut_down_cleanly(subdata,win)
            sys.exit()
        
        #empty trial data 
        trialdata={}
        trialdata['onset']=onsets[trial]
        trialdata['cond']=cond[trial]
        
        #shuffle the positions
        shuffle(pos_ind)
        visual_stim1=visual.ImageStim(win, image=N.zeros((300,300)),pos=positions[pos_ind[0]], size=(0.25,0.25),units='height')
        visual_stim2=visual.ImageStim(win, image=N.zeros((300,300)),pos=positions[pos_ind[1]], size=(0.25,0.25),units='height')
        
        #set which pair to use
        #x=int(N.random.choice(stim_index, 1, p=[0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]))
        #print("here is the list")
        #print(stim_list)
        #print(x)
        #stim_img_trial=stim_list[x]
        #print(stim_img_trial)
        
        x=int(trialcond[trial])
        
        stim_img_trial=stim_list[x]
        trial_prob=prob_list[x]
        trial_inv_prob=inv_prob_list[x]
        
        #set which image appears on what side
        visual_stim1.setImage(stim_img_trial[img_index[0]])
        visual_stim2.setImage(stim_img_trial[img_index[1]])
        
        #Indexes
        shuffle(img_index)
        
        master_prob_list=[trial_prob,trial_inv_prob]
        
        shuffle(indices)
        
        #creating a dictory which will store the postion with the image and pump, the image and pump need to match
        mydict={}
        mydict[positions_scan[pos_ind[1]]] = [stim_img_trial[indices[1]], master_prob_list[indices[1]]]
        mydict[positions_scan[pos_ind[0]]] = [stim_img_trial[indices[0]], master_prob_list[indices[0]]]
        
        #which is sweet?
        message=visual.TextStim(win, text='Which is Correct?',pos=(0,5))
        print trial
        t = clock.getTime()
        
        #get the time of the image and log, this log is appending it to the csv file 
        visual_stim1.draw() #making image of the logo appear
        visual_stim2.draw()
        message.draw()
        RT = core.Clock()
        
        logging.log(logging.DATA, "%s at position=%s and %s at position=%s"%(stim_img_trial[img_index[0]],positions_eng[pos_ind[0]],stim_img_trial[img_index[1]],positions_eng[pos_ind[1]]))
        
        while clock.getTime()<trialdata['onset']:
            pass
        win.flip()
        
        RT.reset() # reaction time starts immediately after flip 
        
        while clock.getTime()<(trialdata['onset']+cue_time):#show the image, while clock is less than onset and cue, show cue
            pass
        keys = event.getKeys(timeStamped=RT)
        message=visual.TextStim(win, text='')
        message.draw()
        win.flip()
        
        # get the key press logged, and time stamped 
        
        if len(keys)>0:
            logging.log(logging.DATA, "keypress=%s at time= %f"%(keys[0][0],keys[0][1]))
            print("here are the keys:")
            print(keys)
            t = clock.getTime()
            #back up of the key press
            tempArray = [t, keys[0]]
            key_responses.append(tempArray)
            ratings_and_onsets.append(["keypress=%s"%keys[0][0],t])
            
            
            #If they choose 
            if keys[0][0] == '1':
                #from the dictionary find the image code associated with the key press and determine the right feedback
                image=(mydict['1'][0])
                trial_prob=(mydict['1'][1])
                response=(N.random.choice(feedback, 1, p=trial_prob))
                
                #draw the image they selected
                visual_stim_choice.setImage(image)
                visual_stim_choice.draw()
                print(image)
                print(taste)
                #log the pump used, time, and key press
                print 'Feedback: %s'%response
                logging.log(logging.DATA,"feedback: %s and a keypress of %s and image of %s"%(taste,keys[0][0], image))
                t = clock.getTime()
                ratings_and_onsets.append(["feedback: %s"%response, t, keys[0][0]])
                message=visual.TextStim(win, text='%s'%response, pos=(0, 0), height=2)
                logging.flush()
                
            elif keys[0][0] == '2':
                #from the dictonary get the image associated with the right key press
                image=(mydict['2'][0])
                trial_prob=(mydict['2'][1])
                taste=int(N.random.choice(pump_responses, 1, p=trial_prob))
                print(image)
                print(taste)
                #log the time, keypress, and pump 
                print 'injecting via pump at address %s'%taste
                logging.log(logging.DATA,"injecting via pump at address %d and a keypress of %s and image of %s"%(taste,keys[0][0], image))
                t = clock.getTime()
                ratings_and_onsets.append(["injecting via pump at address %d"%taste, t])
                logging.flush()
        else:
            taste=0
            t = clock.getTime()
            logging.log(logging.DATA,"Key Press Missed!")
            keys=keys.append(['MISS',t])
            message=visual.TextStim(win, text='Please answer quicker', pos=(0, 0), height=2)#this lasts throught the taste
            message.draw()
            win.flip()

        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time):
            pass
        
        message=visual.TextStim(win, text='+', pos=(0, 0), height=2)#this lasts throught the wait
        message.draw()
        win.flip()
        t = clock.getTime()
        ratings_and_onsets.append(["wait", t])

        #trialdata['dis']=[ser.write('0DIS\r'),ser.write('1DIS\r')]
        #print(trialdata['dis'])
        
        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
            pass

      
        
        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
            pass

        message=visual.TextStim(win, text='+', pos=(0, 0), height=2)#lasts through the jitter 
        message.draw()
        win.flip()
        t = clock.getTime()
        ratings_and_onsets.append(["jitter", t])

        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
            pass
        
        t = clock.getTime()
        ratings_and_onsets.append(['end time', t])
        logging.log(logging.DATA,"finished")
        subdata['trialdata'][trial]=trialdata
        
      
        
        print(key_responses)
        
    win.close()


run_block(fix)

#subdata['key_responses']=keys_responses

subdata.update(info)
f=open('/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/%s_%s_posttest_subdata.log'%(info['participant'],subdata['datestamp']))
pickle.dump(subdata,f)
f.close()

myfile = open('/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/%s_%s_posttest_subdata.csv'%(info['participant'],subdata['datestamp'],'wb'))
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(['event','data'])
for row in ratings_and_onsets:
    wr.writerow(row)


core.quit()
