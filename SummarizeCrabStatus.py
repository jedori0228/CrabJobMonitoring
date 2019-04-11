import os,sys

def GetSubmittionFile(jobdir):
  
  crabfile = open(jobdir + "/crab.log","r")
  filename=""
  for line in crabfile:
    if "Will use CRAB configuration file" in line:
      line_split = line.split()
      filename = line_split[len(line_split)-1]
      break
  crabfile.close()
  return filename

def CheckStatus(line, status):

  for st in status:
    if st in line:
      return True
  return False

def SummarizeCrabStatus(out,crabdir,SamplePD,submittion_dir):

  SKFlatTag = os.environ['SKFlatTag']

  dones = open('DoneSamples_'+SKFlatTag+'.txt').readlines()
  for a in range(0,len(dones)):
    done = dones[a]
    if "<tr>" not in done:
      continue
    words = done.split()
    if words[0]==SamplePD:

      for b in range(0,len(dones)-a):
        thisline = dones[a+b]
        if "</tr>" in thisline:
          break
        towrite = thisline
        if b==0:
          towrite = thisline.replace(SamplePD+'\t','')
        out.write( towrite )
      return 0
    
  job_submit_file= crabdir +"/.requestcache"
  job_submitted=True
  if not os.path.exists(job_submit_file):
    job_submitted=False
  os.system('crab status -d '+crabdir+' > tmp.txt')
  lines = open('tmp.txt').readlines()
  os.system('rm tmp.txt')

  status = [
  'unsubmitted',
  'cooloff',
  'idle',
  'running',
  'failed',
  'transferring',
  'finished',
  ]
  colors = [
  'gray',
  'gray',
  'gray',
  'orange',
  'red',
  'black',
  'green'
  ]

  StatusLines = []
  N_Total = ""
  scheduler=""
  ToWrite = ""
  JobStarted=False
  for i in range(0,len(lines)):
    line = lines[i]

    if "SUBMITFAILED" in line:
      job_submitted=False
      print "SUBMITFAILED. Resubmitting."
      submittion_file=submittion_dir+"/"+GetSubmittionFile(crabdir)
      os.system("rm -rf " + crabdir)
      print "crab submit -d " + submittion_file
      os.system("crab submit -d " + submittion_file)
    if "Grid scheduler - Task Worker" in line:
      sline=line.split()
      scheduler=sline[5]
    if "Jobs status:" in line:
      JobStarted=True
      StatusLines.append( line.replace('Jobs status:','') )
      words = line.replace('Jobs status:','').split('/')
      N_Total = words[len(words)-1].replace(')','').strip('\n')

      j = i+1
      nextline = lines[j]
      while CheckStatus(nextline,status):
        StatusLines.append(nextline)
        j = j+1
        nextline = lines[j]
      break

  ToWrite  = '  <tr>'+'\n'
  ToWrite += '    <td align="left">'+SamplePD+'</td>'+'\n'
  ToWrite += '    <td align="centre">'+scheduler.replace('crab3@','').replace('.cern.ch','')+'</td>'+'\n'

  Finished = 0
  for i in range(0,len(status)):
    st = status[i]
    color = colors[i]
    ThisStatusExist = False

    for line in StatusLines:
      words = line.split()

      if st not in line:
        continue
      
      ThisStatusExist = True
      Perc = words[1].replace('%','')
      Frac = line.replace(words[0],'').replace(words[1],'').replace('(','').replace(')','').replace('\t','').replace(' ','').strip('\n')
      words_Frac = Frac.split('/')
      num = words_Frac[0]
      den = words_Frac[1]
      if st=="finished":
        Finished = int(num)
      if N_Total!=den:
        print "#### ERROR ####"
        print "N_Total = "+N_Total
        print "den = "+den
        print "---- Printing lines ----"
        print lines
        print "---- Printing StatusLines ----"
        print StatusLines

        
      if job_submitted:
        ToWrite += '    <td align="center"><font color='+color+'>'+num+'</font></td>'+'\n'
  
        if st == "failed":
          if num > 0: 
            print "Resubmitting " + crabdir
            os.system("crab resubmit -d " + crabdir)
      else:
        print "job_submitted FAILED" 
        ToWrite += '    <td align="center"><font color='+color+'> </strike>'+num+'</font></td>'+'\n'

    if not ThisStatusExist:

      ToWrite += '    <td align="center"><font color='+color+'>0</font></td>'+'\n'

  ToWrite += '    <td align="center">'+N_Total+'</td>'+'\n'

  if job_submitted and JobStarted:
    if int(Finished)==int(float(N_Total)):
      ToWrite += '    <td align="center">'+str(round(100.*Finished/float(N_Total),2))+'</td>'+'\n'
    else:
      ToWrite += '    <td align="center">'+str(round(100.*Finished/float(N_Total),2))+'</td>'+'\n'
    ToWrite += '  </tr>'+'\n'

  elif not job_submitted:

    ToWrite += '    <td align="center">FAILED</td>'+'\n'
    ToWrite += '  </tr>'+'\n'

  elif not JobStarted:
    ToWrite += '    <td align="center">SUBMITTING</td>'+'\n'
    ToWrite += '  </tr>'+'\n'

  if job_submitted and JobStarted:

    if ( Finished==int(N_Total) ) or ( "Done" in SamplePD ):
      update_dones = open('DoneSamples_'+SKFlatTag+'.txt','a')
      update_dones.write(SamplePD+'\t'+ToWrite)
      update_dones.close()

  out.write(ToWrite)
