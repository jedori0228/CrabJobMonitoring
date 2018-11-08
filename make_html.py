from SummarizeCrabStatus import *
import datetime

SKFlatTag = os.environ['SKFlatTag']
CMSSW_BASE =  os.environ['CMSSW_BASE']

os.system('touch DoneSamples_'+SKFlatTag+'.txt')

JobDirs = [
CMSSW_BASE+'/src/SKFlatMaker/SKFlatMaker/script/CRAB3/'+SKFlatTag+'/2017/crab_submission_DATA/crab_projects/',
CMSSW_BASE+'/src/SKFlatMaker/SKFlatMaker/script/CRAB3/'+SKFlatTag+'/2017/crab_submission_MC/crab_projects/'
]

Skeleton_path = 'Skeleton_Status.html'
os.system('cp '+Skeleton_path+' tmp_Status.html')
out = open('tmp_Status.html','a')

JobStartTime = datetime.datetime.now()
timestamp =  JobStartTime.strftime('%Y-%m-%d %H:%M:%S')+' CERN'

print>>out,'''<body>

<p class="Title"> Status of SKFlat {1} Production </p>
<p class="Clock">Last updated time : {0}</p>

<table border = 1 align="center">
  <tr>
    <th>Sample</th>
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
'''.format(timestamp,SKFlatTag)

for JobDir in JobDirs:

  os.system('ls -1d '+JobDir+'crab_* > tmp.txt')
  lines = open('tmp.txt').readlines()
  os.system('rm tmp.txt')
  for line in lines:
    line = line.strip('\n')
    SamplePD = line.replace(JobDir,'').replace('crab_','')

    SummarizeCrabStatus(out,line,SamplePD)


print>>out,'''</table>




</body>

</html>
'''

out.close()
os.system('mv tmp_Status.html Status.html')
