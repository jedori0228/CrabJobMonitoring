from SummarizeCrabStatus import *
import datetime
import argparse

parser = argparse.ArgumentParser(description='options')
parser.add_argument('-y', dest='Year', default="2016")
args = parser.parse_args()

SKFlatTag = os.environ['SKFlatTag']
CMSSW_BASE =  os.environ['CMSSW_BASE']

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

    print SamplePD

    SummarizeCrabStatus(out,line,SamplePD)


print>>out,'''</table>




</body>

</html>
'''

out.close()
os.system('mv '+SKFlatTag+'/tmp_Status.html '+SKFlatTag+'/Status_'+args.Year+'.html')
