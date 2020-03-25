import os
from CrabJobStatus import CrabJobStatus

def CheckStatus(line, status):

  for st in status:
    if st in line:
      return True
  return False

def ReadCrabStatus(status):

  StatusKeywords = [
  'unsubmitted',
  'cooloff',
  'idle',
  'running',
  'failed',
  'transferring',
  'finished',
  'held',
  'killed',
  ]
  JobNumbers = []
  for i in range(0,len(StatusKeywords)):
    JobNumbers.append(0)

  ThisCrabStatus = CrabJobStatus()
  ThisCrabStatus.SetEmpty(True)

  #### First check if 'SUBMITFAILED'
  IsSUBMITFAILED = False
  for line in status:
    if 'SUBMITFAILED' in line:
      IsSUBMITFAILED = True
      break

  StatusLines = []

  for i in range(0,len(status)):

    line = status[i]
    words = line.split()

    if 'CRAB project directory' in line:

      if 'SKFlatMaker' in line:
        # CRAB project directory:		/afs/cern.ch/work/j/jskim/SKFlatMaker/ForSubmission/Run2Legacy_v4__CMSSW_10_2_18/src/SKFlatMaker/SKFlatMaker/script/CRAB3/Run2Legacy_v4/2016/crab_submission_MC/crab_projects/crab_WRtoNLtoLLJJ_WR2000_N1600_TuneCUETP8M1_13TeV-madgraph-pythia8
        words2 = line.split('/')
        for i_word in range(0,len(words2)):
          if 'crab_submission_' in words2[i_word]:
            ThisCrabStatus.SetYear( words2[i_word-1] )
            break

    if 'Task name' in line:
      # ['Task', 'name:', '190407_012946:jskim_crab_Legacy2016_RunH']

      ThisCrabStatus.SetTimeStamp( words[2].split(':')[0] )

      USER = os.environ['USER'] # actually we can just use ThisCrabStatus.USER()
      ThisCrabStatus.SetSample( words[2].split(':')[1].replace(USER+'_crab_','') )

    elif 'Grid scheduler' in line:
      # ['Grid', 'scheduler', '-', 'Task', 'Worker:', 'crab3@vocms0107.cern.ch', '-', 'crab-prod-tw01']
      ThisCrabStatus.SetScheduler( words[5].replace('crab3@','') )

    elif 'Jobs status' in line:

      line = line.replace('Jobs status:','')
      StatusLines.append( line )
      jswords = line.split('/')

      N_Total = words[len(words)-1].replace(')','').strip('\n')

      j = i+1
      nextline = status[j]
      while CheckStatus(nextline,StatusKeywords):
        StatusLines.append(nextline)
        j = j+1
        nextline = status[j]
      break

  #print StatusLines

  if len(StatusLines)>0:
    ThisCrabStatus.SetStarted( True )

  if IsSUBMITFAILED:
    ThisCrabStatus.SetEmpty( False )
    ThisCrabStatus.SetSubmitFail( True )
    return ThisCrabStatus

  for i in range(0,len(StatusKeywords)):
    st = StatusKeywords[i]
    ThisStatusExist = False

    for line in StatusLines:
      words = line.split()

      if st not in line:
        continue

      Perc = words[1].replace('%','')
      Frac = line.replace(words[0],'').replace(words[1],'').replace('(','').replace(')','').replace('\t','').replace(' ','').strip('\n')
      words_Frac = Frac.split('/')
      num = words_Frac[0]
      den = words_Frac[1]

      ThisCrabStatus.SetTotal( int(den) )

      JobNumbers[i] = int(num)

  ThisCrabStatus.SetUnsubmitted( JobNumbers[0] )
  ThisCrabStatus.SetCooloff( JobNumbers[1] )
  ThisCrabStatus.SetIdle( JobNumbers[2] )
  ThisCrabStatus.SetRunning( JobNumbers[3] )
  ThisCrabStatus.SetFailed( JobNumbers[4] )
  ThisCrabStatus.SetTransferring( JobNumbers[5] )
  ThisCrabStatus.SetFinished( JobNumbers[6] )
  ThisCrabStatus.SetHeld( JobNumbers[7] )
  ThisCrabStatus.SetKilled( JobNumbers[8] )

  return ThisCrabStatus













