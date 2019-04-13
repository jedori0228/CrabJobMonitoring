#!/usr/bin/env python

import os
import subprocess
import pickle
from ReadCrabStatus import ReadCrabStatus
from CrabJobStatus import CrabJobStatus

def UpdateJobStatus(config):

  exec('from '+config+' import *')

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

      print '@@@@ '+this_Sample

      #### if we keep runing crab status, the file size of crab.log goes really big
      crablog = open(Dir+'/crab.log').readlines()
      if len(crablog)>10000:
        os.system('rm '+Dir+'/crab.log')

      #### Now, make CrabJobStatus object
      ThisCrabStatus = CrabJobStatus()

      #### check if we have requestcache
      #### if not, this is a submitfailed job
      if not os.path.exists(Dir+'/.requestcache'):
        ThisCrabStatus.SetSubmitFail(True)

      #### if we have requestcache, we will get outputs from crab status
      else:
        #### Now, run ReadCrabStatus()
        CrabStatus = subprocess.check_output('crab status -d '+Dir,shell=True).split('\n')
        ThisCrabStatus = ReadCrabStatus( CrabStatus )

        #### if has failed job, resubmit
        if ThisCrabStatus.Failed() > 0:
          print '--> has '+str(ThisCrabStatus.Failed())+' failed jobs, resubmitting...'
          os.system('crab resubmit -d '+Dir)

      NewJobStatus.append(ThisCrabStatus)

  pickle.dump(NewJobStatus, NewJobStatus_file)
  NewJobStatus_file.close()

  #print '@@@@ New status :'
  #print NewJobStatus
