import os,sys

def CheckStatus(line, status):

  for st in status:
    if st in line:
      return True
  return False

def SummarizeCrabStatus(out,crabdir, SamplePD):

  os.system('crab status -d '+crabdir+' > tmp.txt')
  lines = open('tmp.txt').readlines()
  os.system('rm tmp.txt')

  status = [
  'unsubmitted',
  'idle',
  'running',
  'failed',
  'transferring',
  'finished',
  ]
  colors = [
  'gray',
  'gray',
  'orange',
  'red',
  'black',
  'green'
  ]

  StatusLines = []
  N_Total = ""
  for i in range(0,len(lines)):
    line = lines[i]
    if "Jobs status:" in line:
      StatusLines.append( line.replace('Jobs status:','') )

      j = i+1
      nextline = lines[j]
      while CheckStatus(nextline,status):
        StatusLines.append(nextline)
        words = nextline.split('/')
        N_Total = words[len(words)-1].replace(')','').strip('\n')
        j = j+1
        nextline = lines[j]
      break

  print>>out, '  <tr>'
  print>>out, '    <td align="left">'+SamplePD+'</td>'

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
        Finished = float(num)
      if N_Total!=den:
        print "#### ERROR ####"
        print "N_Total = "+N_Total
        print "den = "+den
        print "---- Printing lines ----"
        print lines
        print "---- Printing StatusLines ----"
        print StatusLines

      print>>out, '    <td align="center"><font color='+color+'>'+num+'</font></td>'

    if not ThisStatusExist:
      print>>out, '    <td align="center"><font color='+color+'>0</font></td>'

  print>>out, '    <td align="center">'+N_Total+'</td>'
  if int(Finished)==int(float(N_Total)):
    print>>out, '    <td align="center">'+str(round(100.*Finished/float(N_Total),2))+'</td>'
  else:
    print>>out, '    <td align="center">'+str(round(100.*Finished/float(N_Total),2))+'</td>'
  print>>out, '  </tr>'
