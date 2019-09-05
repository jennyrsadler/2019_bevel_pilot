"""
Created May 2018
@author: JRS, script kiddie from gracer
"""

#!/usr/bin/python
#get onsets

import numpy
import os
import glob

handles=[]

basepath='/Users/jennygilbert/Documents/niblunc/bevel_task/Output/logs/task_files'
os.chdir(basepath)


ignore = ['DATA 	Keypress: o','Level post injecting via pump at address']

#files = [file for file in os.listdir(".") if (file.lower().endswith('.log'))]
#files.sort(key=os.path.getmtime)

#get the global info about the run. 
for file in glob.glob(os.path.join(basepath,'bevel67_run02*.log')):
    print(file)

    sub=file.split('/')[9].split('_')[1]
    run=file.split('/')[9].split('_')[2]
    print([sub,run])
    
#   open the script and read in log data
    with open(file,'r') as infile:
        img_onsets=[]
        #AB_img_onsets=[]
        #CD_img_onsets=[]
        #EF_img_onsets=[]
        sweet_onset=[]
        bitter_onset=[]
        neu_onset=[]
        #sweet_expected_onset=[]
        #sweet_PE_onset=[]
        #bitter_expected_onset=[]
        #bitter_PE_onset=[]
        #RT=[]
        start_time=None
        
        for x in infile.readlines():
#            if x.find('Keypress: q'):
#                continue
            
            if not x.find(ignore[0])>-1 or x.find(ignore[1])>-1:
                
                l_s=x.strip().split()
                #print l_s
                
                if x.find('Level start key press')>-1:#find the start
                    l_s=x.strip().split()
                    start_time=float(l_s[0])
                    
                #if x.find('at time= ')>1:
                    #l_s=x.strip().split()
                    #RT.append(l_s[5])
                    
                if x.find('position')>-1:
                    l_s=x.strip().split()
                    #print(l_s)
                    img_onsets.append(float(l_s[0]))
                   # img_onsets.append(l_s[2]) #fix this to pull only time 
                    #if l_s[2] == 'a.jpg' or l_s[2] == 'b.jpg':
                        #AB_img_onsets.append(l_s[2])
                        #AB_img_onsets.append(float(l_s[0]))
                    #if l_s[2] == 'c.jpg' or l_s[2] == 'd.jpg':
                        #CD_img_onsets.append(l_s[2])
                        #CD_img_onsets.append(float(l_s[0]))
                    #if l_s[2] == 'e.jpg' or l_s[2] == 'f.jpg':
                        #EF_img_onsets.append(l_s[2])
                        #EF_img_onsets.append(float(l_s[0]))
                if x.find('Level injecting via pump at address ')>-1:#find the tasty image
                    l_s=x.strip().split()
                    #print(l_s)
                    if l_s[7] == '1':
                        sweet_onset.append(l_s[0])
#                   expected sweet
                    #if l_s[7] == '1' and l_s[16] == 'a.jpg':
                        #sweet_expected_onset.append(l_s[0])
                    #if l_s[7] == '1' and l_s[16] == 'c.jpg':
                        #sweet_expected_onset.append(l_s[0])                    
                    #if l_s[7] == '1' and l_s[16] == 'e.jpg':
                        #sweet_expected_onset.append(l_s[0])                       

#                   unexpected sweet                    
                    #if l_s[7] == '1' and l_s[16] == 'b.jpg':
                        #sweet_PE_onset.append(l_s[0])
                    #if l_s[7] == '1' and l_s[16] == 'd.jpg':
                        #sweet_PE_onset.append(l_s[0])                    
                    #if l_s[7] == '1' and l_s[16] == 'f.jpg':
                        #sweet_PE_onset.append(l_s[0]) 

                        
                    if l_s[7] == '2':
                        bitter_onset.append(l_s[0])              
#                   expected bitter                                         
                    #if l_s[7] == '2' and l_s[16] == 'b.jpg':
                        #bitter_expected_onset.append(l_s[0])
                    #if l_s[7] == '2' and l_s[16] == 'd.jpg':
                        #bitter_expected_onset.append(l_s[0])               
                    #if l_s[7] == '2' and l_s[16] == 'f.jpg':
                        #bitter_expected_onset.append(l_s[0])                    
#                   unexpected bitter
                    #if l_s[7] == '2' and l_s[16] == 'a.jpg':
                        #bitter_PE_onset.append(l_s[0])
                    #if l_s[7] == '2' and l_s[16] == 'c.jpg':
                        #bitter_PE_onset.append(l_s[0])
                    #if l_s[7] == '2' and l_s[16] == 'e.jpg':
                        #bitter_PE_onset.append(l_s[0])

#                   rinse
                if x.find('Level RINSE 	25')>-1:
                    neu_onset.append(l_s[0])
                    print(neu_onset)
                
        neu_onsets=(numpy.asarray(neu_onset,dtype=float))-start_time 
        sweet_onsets=(numpy.asarray(sweet_onset,dtype=float))-start_time 
        bitter_onsets=(numpy.asarray(bitter_onset,dtype=float))-start_time
        #sweet_expected_onset=(numpy.asarray(sweet_expected_onset,dtype=float))-start_time
        #sweet_PE_onset=(numpy.asarray(sweet_PE_onset,dtype=float))-start_time
        #bitter_expected_onset=(numpy.asarray(bitter_expected_onset,dtype=float))-start_time
        #bitter_PE_onset=(numpy.asarray(bitter_PE_onset,dtype=float))-start_time
        
        img_onsets=(numpy.asarray(img_onsets,dtype=float))-start_time 
        #AB_img_onsets=(numpy.asarray(AB_img_onsets,dtype=float))-start_time 
        #CD_img_onsets=(numpy.asarray(CD_img_onsets,dtype=float))-start_time 
        #EF_img_onsets=(numpy.asarray(EF_img_onsets,dtype=float))-start_time 

        files2make=['neu','sweet','bitter','sweet_expected','sweet_PE','bitter_expected','bitter_PE', 'img', 'AB', 'CD', 'EF','RT']
        mydict={}
        try:
            for files in files2make:
                path='/Users/jennygilbert/Documents/niblunc/bevel_task/Output/onsets_fsl/%s_%s_%s.txt'%(sub,files,run)
                if os.path.exists(path) == True:
                    print ('exists')
                    break
                else:
                    mydict[files] = path
            
            f_neu=open(mydict['neu'], 'w')
            for t in range(len(neu_onsets)):
                f_neu.write('%f\t2\t1\n'%(neu_onsets[t]))
            f_neu.close()
            
            f_sweet=open(mydict['sweet'], 'w')
            for t in range(len(sweet_onsets)):
                f_sweet.write('%f\t5\t1\n' %(sweet_onsets[t]))
            f_sweet.close()
            
            f_bitter=open(mydict['bitter'], 'w')
            for t in range(len(bitter_onsets)):
                f_bitter.write('%f\t5\t1\n' %(bitter_onsets[t]))
            f_bitter.close()

            #f_sweet_exp=open(mydict['sweet_expected'], 'w')
            #for t in range(len(sweet_expected_onset)):
                #f_sweet_exp.write('%f\t5\t1\n' %(sweet_expected_onset[t]))
            #f_sweet_exp.close()

            #f_sweet_PE=open(mydict['sweet_PE'], 'w')
            #for t in range(len(sweet_PE_onset)):
                #f_sweet_PE.write('%f\t5\t1\n' %(sweet_PE_onset[t]))
            #f_sweet_PE.close()                   

            #f_bitter_exp=open(mydict['bitter_expected'], 'w')
            #for t in range(len(bitter_expected_onset)):
                #f_bitter_exp.write('%f\t5\t1\n' %(bitter_expected_onset[t]))
            #f_bitter_exp.close()            

            #f_bitter_PE=open(mydict['bitter_PE'], 'w')
            #for t in range(len(bitter_PE_onset)):
                #f_bitter_PE.write('%f\t5\t1\n' %(bitter_PE_onset[t]))
            #f_bitter_PE.close()  

            f_img=open(mydict['img'], 'w')
            for t in range(len(img_onsets)):
                f_img.write('%f\t2\t1\n' %(img_onsets[t]))
            f_img.close()              
            
            #f_AB=open(mydict['AB'], 'w')
            #for t in range(len(AB_img_onsets)):
                #f_AB.write('%f\t2\t1\n' %(AB_img_onsets[t]))
            #f_AB.close()  

            #f_CD=open(mydict['CD'], 'w')
            #for t in range(len(CD_img_onsets)):
                #f_CD.write('%f\t2\t1\n' %(CD_img_onsets[t]))
            #f_CD.close()  

            #f_EF=open(mydict['EF'], 'w')
            #for t in range(len(EF_img_onsets)):
                #f_EF.write('%f\t2\t1\n' %(EF_img_onsets[t]))
            #f_EF.close()  

            #f_make=open(path, 'w')
            #for a in zip(RT):
                #f_make.write(str(a)+'\n')
            #f_make.close()

        except KeyError:
            pass                                                         