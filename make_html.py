from SummarizeCrabStatus import *
from ProxyCheck import *
import datetime
import argparse

parser = argparse.ArgumentParser(description='options')
parser.add_argument('-y', dest='Year', default="2016")
parser.add_argument('-x', dest='email', default="")
args = parser.parse_args()

SKFlatTag = os.environ['SKFlatTag']
CMSSW_BASE =  os.environ['CMSSW_BASE']
user_email = args.email

### function checks proxy is set

Kerb_Stat =  CheckKerbos(user_email)
if Kerb_Stat == 0:
  print "ticket for machine permission is run out: setup new shell or use kinit to reset kerberos"
  sys.exit(10)
  

os.system('touch DoneSamples_'+SKFlatTag+'.txt')

JobDirs = [
CMSSW_BASE+'/src/SKFlatMaker/SKFlatMaker/script/CRAB3/'+SKFlatTag+'/'+args.Year+'/crab_submission_DATA/crab_projects/',
CMSSW_BASE+'/src/SKFlatMaker/SKFlatMaker/script/CRAB3/'+SKFlatTag+'/'+args.Year+'/crab_submission_MC/crab_projects/'
]

Skeleton_path = 'Skeleton_Status.html'
os.system('cp '+Skeleton_path+' '+SKFlatTag+'/tmp_Status.html')
out = open(SKFlatTag+'/tmp_Status.html','a')

JobStartTime = datetime.datetime.now()
timestamp =  JobStartTime.strftime('%Y-%m-%d %H:%M:%S')+' CERN'

print>>out,'''<body>

<p class="Title"> Status of SKFlat {1} Production ({2})</p>
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
'''.format(timestamp,SKFlatTag,args.Year)


for JobDir in JobDirs:

  os.system('ls -1d '+JobDir+'crab_* > '+SKFlatTag+'/tmp.txt')
  lines = open(SKFlatTag+'/tmp.txt').readlines()
  os.system('rm '+SKFlatTag+'/tmp.txt')
  for line in lines:
    line = line.strip('\n')
    SamplePD = line.replace(JobDir,'').replace('crab_','')
    submittion_dir = JobDir.replace('crab_projects/', '')
    print SamplePD

    SummarizeCrabStatus(out,line,SamplePD,submittion_dir)


print>>out,'''</table>




</body>

</html>
'''

out.close()
os.system('mv '+SKFlatTag+'/tmp_Status.html '+SKFlatTag+'/Status_'+args.Year+'.html')

sys.exit(1)
