#!/usr/bin/env python

import os
import pickle
from ReadCrabStatus import ReadCrabStatus
from CrabJobStatus import CrabJobStatus
from ShellHelper import ShellHelper

def IsAlreadyDone(MyList, sample, timeStamp):

  for js in MyList:
    if (js.Sample()==sample) and (js.TimeStamp()==timeStamp):
      if js.Finished()==js.Total():
        return [True, js]
      else:
        return [False]

  return [False]


def UpdateJobStatus(config):

  exec('from '+config+' import *')

  MonitWD = os.environ['MonitWD']
  CrabDirs = MonitoringInfo['CrabDirs']
  FileName = UserInfo['FileName']

  PrevJobStatus_filename = MonitWD+'/pkl/'+FileName+'.pkl'
  PrevJobStatus = []
  try:
    PrevJobStatus_file = open(PrevJobStatus_filename,'rb')
    PrevJobStatus = pickle.load(PrevJobStatus_file)
  except:
    PrevJobStatus = []

  NewJobStatus = []
  NewJobStatus_filename = MonitWD+'/pkl/New_'+FileName+'.pkl'
  NewJobStatus_file = open(NewJobStatus_filename,'wb')

  for CrabDir in CrabDirs:

    if not os.path.isdir(CrabDir):
      print "@@@@ Dir not exists : "+CrabDir
      continue

    Dirs = ShellHelper('ls -1d '+CrabDir+'/crab_*').strip('\n').split('\n')
    for Dir in Dirs:

      crab_dir = Dir.split('/')[-1]
      this_Sample = crab_dir.replace('crab_','')

      #### Let's write a file which contains sample name and timestamp
      crablog = open(Dir+'/crab.log').readlines()
      if not os.path.isfile(Dir+'/TimeStamp.txt'):
        for line in crablog:
          if 'Task name' in line:
            timestamp_file = open(Dir+'/TimeStamp.txt','w')
            timestamp_file.write(line.split()[-1].split(':')[0])
            timestamp_file.close()
            break
      this_TimeStamp = ShellHelper('cat '+Dir+'/TimeStamp.txt').strip('\n')

      print '@@@@ '+this_Sample+'\t'+this_TimeStamp
      findResult = IsAlreadyDone(PrevJobStatus, this_Sample, this_TimeStamp)

      #### if we keep runing crab status, the file size of crab.log goes really big
      if len(crablog)>10000:
        os.system('rm '+Dir+'/crab.log')
        os.system('touch '+Dir+'/crab.log')

      #### Now, make CrabJobStatus object
      ThisCrabStatus = CrabJobStatus()

      #### check if we have requestcache
      #### if not, this is a submitfailed job
      if not os.path.exists(Dir+'/.requestcache'):
        ThisCrabStatus.SetSubmitFail(True)

      elif findResult[0]:
        ThisCrabStatus = findResult[1]

      #### if we have requestcache, we will get outputs from crab status
      else:
        #### Now, run ReadCrabStatus()
        CrabStatus = ShellHelper('crab status -d '+Dir).split('\n')
        ThisCrabStatus = ReadCrabStatus( CrabStatus )

        #### if has failed job, resubmit
        if ThisCrabStatus.Failed() > 0:
          print '--> has '+str(ThisCrabStatus.Failed())+' failed jobs, resubmitting...'
          os.system('crab resubmit -d '+Dir)

      #### SetSample is also done in ReadCrabStatus()
      #### but in case it failed to find it..
      ThisCrabStatus.SetSample( this_Sample )

      #### Append
      NewJobStatus.append(ThisCrabStatus)

  pickle.dump(NewJobStatus, NewJobStatus_file)
  NewJobStatus_file.close()

  os.system('mv '+NewJobStatus_filename+' '+PrevJobStatus_filename)

