"""
Created May 2018
@author: JRS, script kiddie from gracer
"""

#!/usr/bin/python
#get onsets


import numpy
import os
import pdb
import glob

handles=[]

basepath='/Users/jennygilbert/Documents/niblunc/bevel_task/Output/logs/test_files'
os.chdir(basepath)


ignore = ['DATA 	Keypress: o','Level post injecting via pump at address']

#files = [file for file in os.listdir(".") if (file.lower().endswith('.log'))]
#files.sort(key=os.path.getmtime)

#get the global info about the run. 
for file in glob.glob(os.path.join(basepath,'bevel*.log')):
    sub=file.split('/')[9].split('_')[1]
    print(sub)

#   open the script and read in log data
    with open(file,'r') as infile:
        image=[]
        choice=[]
        
        for x in infile.readlines():
            if not x.find(ignore[0])>-1 or x.find(ignore[1])>-1:
                l_s=x.strip().split()
                
                if x.find('position=')>-1:
                    l_s=x.split('Level')
                    image.append(l_s[1])
                    
                if x.find('keypress=left')>-1:
                    choice.append('left')

                if x.find('keypress=right')>-1:
                    choice.append('right')
 
                if x.find('Key Press Missed!')>-1:
                    choice.append('miss')

   
        #neu_onsets=(numpy.asarray(neu_onset,dtype=float))-start_time 
        #sweet_onsets=(numpy.asarray(sweet_onset,dtype=float))-start_time 
        #bitter_onsets=(numpy.asarray(bitter_onset,dtype=float))-start_time
        #sweet_expected_onset=(numpy.asarray(sweet_expected_onset,dtype=float))-start_time
        #sweet_PE_onset=(numpy.asarray(sweet_PE_onset,dtype=float))-start_time
        #bitter_expected_onset=(numpy.asarray(bitter_expected_onset,dtype=float))-start_time
        #bitter_PE_onset=(numpy.asarray(bitter_PE_onset,dtype=float))-start_time
        
        #img_onsets=(numpy.asarray(img_onsets,dtype=float))-start_time 
        #AB_img_onsets=(numpy.asarray(AB_img_onsets,dtype=float))-start_time 
        #CD_img_onsets=(numpy.asarray(CD_img_onsets,dtype=float))-start_time 
        #EF_img_onsets=(numpy.asarray(EF_img_onsets,dtype=float))-start_time 

        files2make=['image','choice']
        mydict={}
        try:
            for files in files2make:
                path='/Users/jennygilbert/Documents/niblunc/bevel_task/Output/prob_learning_test/%s_%s.txt'%(sub,files)
                if os.path.exists(path) == True:
                    print ('exists')
                    break
                else:
                    mydict[files] = path

            f_img=open(mydict['image'], 'w')
            for t in range(len(image)):
                f_img.write('%s\n'%(image[t]))
            f_img.close()
            
            f_choice=open(mydict['choice'], 'w')
            for t in range(len(choice)):
                f_choice.write('%s\n' %(choice[t]))
            f_choice.close()
            



        except KeyError:
            pass                                                         
