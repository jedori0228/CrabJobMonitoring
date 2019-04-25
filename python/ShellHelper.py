import os,subprocess

def ShellHelper(cmd):

  out = ''

  MAX_TRIAL = 10
  N_Trial = 0
  while True:

    if N_Trial>=MAX_TRIAL:
      break

    N_Trial = N_Trial+1
    try:
      #print "[ShellHelper.py] running '"+cmd+"' ..."
      out = subprocess.check_output('timeout 15 '+cmd,shell=True)
      break
    except KeyboardInterrupt:
      break
    except subprocess.CalledProcessError as e:
      print "[ShellHelper.py] Got error from '"+cmd+"'"
      print "[ShellHelper.py] Exit code = "+str(e.returncode)
      print "[ShellHelper.py] Trying again.. (N_Trial = "+str(N_Trial)+")"

  return out


