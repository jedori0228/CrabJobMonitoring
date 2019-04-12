#!/usr/bin/env python
import os
import datetime
import argparse
import pickle
from MonitConfig import *

  # 'HTMLDest' : '/eos/user/j/jskim/www/HNWR_13TeV/EGammaTnP/CRARBStatus/',
  # 'WEBDir' : '/eos/user/j/jskim/www/',
  # 'URLPrefix' : 'https://jskim.web.cern.ch/jskim/',

HTMLDest = UserInfo['HTMLDest']
WEBDir = UserInfo['WEBDir']
URLPrefix = UserInfo['URLPrefix']
MonitName = CRABInfo['MonitName']
MonitWD = os.environ['MonitWD']

HTMLfilepath = HTMLDest+'/'+MonitName+'.html'
out = open(HTMLfilepath,'w')

MonitURL = URLPrefix+HTMLfilepath.replace(WEBDir,'')
print MonitURL

JobStartTime = datetime.datetime.now()
timestamp =  JobStartTime.strftime('%Y-%m-%d %H:%M:%S')+' CERN'

#### first writhe the header
htmlheaderlines = open(MonitWD+'/tmp/Skeleton_Status.html').readlines()
for line in htmlheaderlines:
  out.write(line)

print>>out,'''<body>

<p class="Title"> Status of {1}</p>
<p class="Clock">Last updated time : {0}</p>

<table border = 1 align="center">
  <tr>
    <th>Sample</th>
    <th>Scheduler</th>
    <th>Unsubmitted</th>
    <th>Cooloff</th>
    <th>Idle</th>
    <th>Running</th>
    <th>Failed</th>
    <th>Transferring</th>
    <th>Finished</th>
    <th>Total</th>
    <th>%</th>
  </tr>
'''.format(timestamp,MonitName)

JobStatus_file = open(MonitWD+'/pkl/JobStatus_'+MonitName+'.pkl', 'rb')
JobStatus = pickle.load(JobStatus_file)

for js in JobStatus:

  ToWrite = '  <tr>'+'\n'

  #### If submissino failed
  ToWrite += '    <td align="left">'+js.Sample+'</td>'+'\n'

  if js.SubmitFail:

    ToWrite += '    <td align="center"><font color=red>SUBMITFAILED</font></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'
    ToWrite += '    <td align="center"></td>'+'\n'

  else :

    ToWrite += '    <td align="centre">'+js.Scheduler+'</td>'+'\n'
    ToWrite += '    <td align="center"><font color=gray>'+str(js.JobUnsubmitted)+'</font></td>'+'\n'
    ToWrite += '    <td align="center"><font color=gray>'+str(js.JobCooloff)+'</font></td>'+'\n'
    ToWrite += '    <td align="center"><font color=gray>'+str(js.JobIdle)+'</font></td>'+'\n'
    ToWrite += '    <td align="center"><font color=orange>'+str(js.JobRunning)+'</font></td>'+'\n'
    ToWrite += '    <td align="center"><font color=red>'+str(js.JobFailed)+'</font></td>'+'\n'
    ToWrite += '    <td align="center"><font color=black>'+str(js.JobTransferring)+'</font></td>'+'\n'
    ToWrite += '    <td align="center"><font color=green>'+str(js.JobFinished)+'</font></td>'+'\n'
    ToWrite += '    <td align="center"><font color=black>'+str(js.JobTotal)+'</font></td>'+'\n'
    ToWrite += '    <td align="center"><font color=black>'+str(round(100.*float(js.JobFinished)/float(js.JobTotal),2))+'</font></td>'+'\n'

  ToWrite += '  </tr>\n'
  out.write(ToWrite)

print>>out,'''</table>




</body>

</html>
'''

out.close()
