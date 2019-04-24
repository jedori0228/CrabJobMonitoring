#!/usr/bin/env python

import os
import pickle
from ReadCrabStatus import ReadCrabStatus
from CrabJobStatus import CrabJobStatus
from ShellHelper import ShellHelper

def UpdateJobStatus(config):

  exec('from '+config+' import *')

  MonitWD = os.environ['MonitWD']
  CrabDirs = MonitoringInfo['CrabDirs']
  FileName = UserInfo['FileName']

  NewJobStatus = []
  NewJobStatus_filename = MonitWD+'/pkl/'+FileName+'.pkl'
  NewJobStatus_file = open(NewJobStatus_filename,'wb')

  for CrabDir in CrabDirs:

    if not os.path.isdir(CrabDir):
      print "@@@@ Dir not exists : "+CrabDir
      continue

    Dirs = ShellHelper('ls -1d '+CrabDir+'/crab_*').strip('\n').split('\n')
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
      ThisCrabStatus.SetSample( this_Sample )

      #### check if we have requestcache
      #### if not, this is a submitfailed job
      if not os.path.exists(Dir+'/.requestcache'):
        ThisCrabStatus.SetSubmitFail(True)

      #### if we have requestcache, we will get outputs from crab status
      else:
        #### Now, run ReadCrabStatus()
        CrabStatus = ShellHelper('crab status -d '+Dir).split('\n')
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
