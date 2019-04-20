import os,subprocess

def ShellHelper(cmd):

  out = ''

  N_Trial = 0
  while True:
    N_Trial = N_Trial+1
    try:
      out = subprocess.check_output(cmd,shell=True)
      break
    except:
      print "[ShellHelper.py] Got error from '"+cmd+"'"
      print "[ShellHelper.py] Trying again.. (N_Trial = "+str(N_Trial)+")"

  return out


