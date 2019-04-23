import os,subprocess

def ShellHelper(cmd):

  out = ''

  MAX_TRIAL = 5
  N_Trial = 0
  while True:

    if N_Trial>=MAX_TRIAL:
      break

    N_Trial = N_Trial+1
    try:
      out = subprocess.check_output(cmd,shell=True)
      break
    except:
      print "[ShellHelper.py] Got error from '"+cmd+"'"
      print "[ShellHelper.py] Trying again.. (N_Trial = "+str(N_Trial)+")"

  return out


