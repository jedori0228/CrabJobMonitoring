#!/usr/bin/env python
import os
import datetime
import argparse
import pickle

def MakeHTML(config):

  exec('from '+config+' import *')

  HTMLDest = UserInfo['HTMLDest']
  WEBDir = UserInfo['WEBDir']
  URLPrefix = UserInfo['URLPrefix']
  FileName = UserInfo['FileName']
  MonitName = MonitoringInfo['MonitName']
  MonitWD = os.environ['MonitWD']

  HTMLfilepath = HTMLDest+'/'+FileName+'.html'
  out = open(HTMLfilepath,'w')

  MonitURL = URLPrefix+HTMLfilepath.replace(WEBDir,'')
  print "@@@@ URL : "+MonitURL

  JobStartTime = datetime.datetime.now()
  timestamp =  JobStartTime.strftime('%Y-%m-%d %H:%M:%S')+' CERN'

  #### first writhe the header
  htmlheaderlines = open(MonitWD+'/tmp/Skeleton_Status.html').readlines()
  for line in htmlheaderlines:
    out.write(line)

  #### Now, body
  #### Get TableContents from config
  TableContents = MonitoringInfo['TableContents']

  #### First right the headings

  print>>out,'''<body>

<p class="Title">Status of {1}</p>
<p class="Clock">Last updated time : {0}</p>

<table border = 1 align="center">
  <tr>'''.format(timestamp,MonitName)

  for TableContent in TableContents:
    out.write('    <th>'+TableContent.VarName+'</th>\n')
  out.write('  </tr>\n')

  #### Now read JobStatus

  JobStatus = []

  if len(MergeStatus)>0:

    print '@@@@ Mering pkls'
    for pkl in MergeStatus:
      print '@@@@ - '+pkl
      JobStatus_file = open(pkl, 'rb')
      this_JobStatus = pickle.load(JobStatus_file)
      for js in this_JobStatus:
        JobStatus.append(js)

  else:

    print '@@@@ Reading from default pkl'
    print '@@@@ - '+MonitWD+'/pkl/'+FileName+'.pkl'
    JobStatus_file = open(MonitWD+'/pkl/'+FileName+'.pkl', 'rb')
    JobStatus = pickle.load(JobStatus_file)

  for js in JobStatus:

    ToWrite = '  <tr>'+'\n'

    if js.SubmitFail():

      #### If submission failed,
      #### write sample name, write SUBMITFAILED in 'Total', and everything else empty
      for TableContent in TableContents:
        if TableContent.VarName=='Sample':
          program = '''ToWrite += TableContent.GetHTMLLine(str(js.'''+TableContent.VarName+'''()))'''
          exec(program)
        elif TableContent.VarName=='Total':
          ToWrite += '    <td align="center"><font color=red>SUBMITFAILED</font></td>'+'\n'
        else:
          ToWrite += '    <td align="center"></td>'+'\n'

    else:

      #### If jobs running, write them..

      for TableContent in TableContents:
        program = '''ToWrite += TableContent.GetHTMLLine(str(js.'''+TableContent.VarName+'''()))'''
        exec(program)

    ToWrite += '  </tr>\n'
    out.write(ToWrite)

  print>>out,'''</table>




</body>

</html>
'''

  out.close()
