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
  ]
  JobNumbers = [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  ]

  ThisCrabStatus = CrabJobStatus()
  ThisCrabStatus.Empty = True

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

    if 'Task name' in line:
      # ['Task', 'name:', '190407_012946:jskim_crab_Legacy2016_RunH']

      ThisCrabStatus.TimeStamp = words[2].split(':')[0]

      USER = os.environ['USER']
      ThisCrabStatus.Sample = words[2].split(':')[1].replace(USER+'_crab_','')

    elif 'Grid scheduler' in line:
      # ['Grid', 'scheduler', '-', 'Task', 'Worker:', 'crab3@vocms0107.cern.ch', '-', 'crab-prod-tw01']
      ThisCrabStatus.Scheduler = words[5].replace('crab3@','')

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
    ThisCrabStatus.Started = True

  if IsSUBMITFAILED:
    ThisCrabStatus.Empty = False
    ThisCrabStatus.SubmitFail = True
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

      ThisCrabStatus.JobTotal = den

      JobNumbers[i] = int(num)

  ThisCrabStatus.JobUnsubmitted = JobNumbers[0]
  ThisCrabStatus.JobCooloff = JobNumbers[1]
  ThisCrabStatus.JobIdle = JobNumbers[2]
  ThisCrabStatus.JobRunning = JobNumbers[3]
  ThisCrabStatus.JobFailed = JobNumbers[4]
  ThisCrabStatus.JobTransferring = JobNumbers[5]
  ThisCrabStatus.JobFinished = JobNumbers[6]

  return ThisCrabStatus













