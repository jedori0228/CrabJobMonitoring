#!/usr/bin/env python

import os
import subprocess
from MonitConfig import *
import pickle
from ReadCrabStatus import ReadCrabStatus
from CrabJobStatus import CrabJobStatus

MonitWD = os.environ['MonitWD']
CrabDirs = CRABInfo['CrabDirs']
MonitName = CRABInfo['MonitName']

NewJobStatus = []
NewJobStatus_filename = MonitWD+'/pkl/JobStatus_'+MonitName+'.pkl'
NewJobStatus_file = open(NewJobStatus_filename,'wb')

for CrabDir in CrabDirs:

  if not os.path.isdir(CrabDir):
    print "@@@@ Dir not exists : "+CrabDir
    continue

  Dirs = subprocess.check_output('ls -1d '+CrabDir+'/crab_*',shell=True).strip('\n').split('\n')
  for Dir in Dirs:

    crab_dir = Dir.split('/')[-1]
    this_Sample = crab_dir.replace('crab_','')
    crablog = open(Dir+'/crab.log').readlines()
    this_TimeStamp = ''
    for line in crablog:
      if 'Task name' in line:
        this_TimeStamp = line.split()[-1].split(':')[0]
        break
    print '@@@@ '+this_Sample+'\t'+this_TimeStamp
    if len(crablog)>10000:
      #### if we keep runing crab status, the file size of crab.log goes really hig
      os.system(Dir+'/crab.log')

    ThisCrabStatus = CrabJobStatus()

    #### Now, run ReadCrabStatus()
    CrabStatus = subprocess.check_output('crab status -d '+Dir,shell=True).split('\n')
    ThisCrabStatus = ReadCrabStatus( CrabStatus )

    #### if has failed job, resubmit
    if ThisCrabStatus.JobFailed > 0:
      print '--> has '+str(ThisCrabStatus.JobFailed)+' failed jobs, resubmitting...'
      os.system('crab resubmit -d '+Dir)

    #ThisCrabStatus.Print()
    NewJobStatus.append(ThisCrabStatus)

pickle.dump(NewJobStatus, NewJobStatus_file)
NewJobStatus_file.close()

#print '@@@@ New status :'
#print NewJobStatus
