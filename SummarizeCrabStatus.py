import os,sys

def CheckStatus(line, status):

  for st in status:
    if st in line:
      return True
  return False

def SummarizeCrabStatus(out,crabdir, SamplePD):

  SKFlatTag = os.environ['SKFlatTag']

  dones = open('DoneSamples_'+SKFlatTag+'.txt').readlines()
  for done in dones:
    words = done.split()
    if words[0]==done:
      out.write( done.replace(done+'\t','') )
      return 0

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

  ToWrite = ""

  for i in range(0,len(lines)):
    line = lines[i]
    if "Jobs status:" in line:
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

      ToWrite += '    <td align="center"><font color='+color+'>'+num+'</font></td>'+'\n'

    if not ThisStatusExist:

      ToWrite += '    <td align="center"><font color='+color+'>0</font></td>'+'\n'

  ToWrite += '    <td align="center">'+N_Total+'</td>'+'\n'
  if int(Finished)==int(float(N_Total)):
    ToWrite += '    <td align="center">'+str(round(100.*Finished/float(N_Total),2))+'</td>'+'\n'
  else:
    ToWrite += '    <td align="center">'+str(round(100.*Finished/float(N_Total),2))+'</td>'+'\n'
  ToWrite += '  </tr>'+'\n'

  if ( Finished==int(N_Total) ) or ( "Done" in SamplePD ):
    update_dones = open('DoneSamples_'+SKFlatTag+'.txt','a')
    update_dones.write(SamplePD+'\t'+ToWrite)
    update_dones.close()

  out.write(ToWrite)
