from SummarizeCrabStatus import *

JobDirs = [
'/afs/cern.ch/work/j/jskim/SKFlatMaker/ForSubmission/CMSSW_9_4_9_cand2/src/SKFlatMaker/SKFlatMaker/script/CRAB3/v949cand2_1/2017/crab_submission_DATA/crab_projects/',
'/afs/cern.ch/work/j/jskim/SKFlatMaker/ForSubmission/CMSSW_9_4_9_cand2/src/SKFlatMaker/SKFlatMaker/script/CRAB3/v949cand2_1/2017/crab_submission_MC/crab_projects/'
]

Skeleton_path = 'Skeleton_Status.html'
os.system('cp '+Skeleton_path+' tmp_Status.html')
out = open('tmp_Status.html','a')

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
os.system('cp tmp_Status.html Status.html')
