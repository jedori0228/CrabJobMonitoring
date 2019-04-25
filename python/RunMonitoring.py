#!/usr/bin/env python

import os
import argparse
import time

from PrepareMonitoring import PrepareMonitoring
from CheckKerberos import CheckKerberos
from CheckProxy import CheckProxy
from UpdateJobStatus import UpdateJobStatus
from MakeHTML import MakeHTML

parser = argparse.ArgumentParser(description='Monitoring')
parser.add_argument('-i', dest='Config', default="")
args = parser.parse_args()

if args.Config=="":
  print '@@@@ Config file is empty'
  print '@@@@ Available Config names :'
  MonitWD = os.environ['MonitWD']
  from ShellHelper import ShellHelper
  cfgFiles = ShellHelper('ls -1 '+MonitWD+'/python/Configs/*.py').split()
  for cfgFile in cfgFiles:
    if '__init__.py' in cfgFile:
      continue
    if '.py' not in cfgFile:
      continue
    print cfgFile.replace(MonitWD+'/python/Configs/','').replace('.py','')
  exit()

config = 'Configs.'+args.Config
exec('from '+config+' import *')

PrepareMonitoring(config)

while True:

  status_Kerberos = CheckKerberos(config)
  status_Proxy = CheckProxy(config)

  if status_Kerberos>1:
    print '@@@@ Kerberos not valid.. Stopiing the monitoring'
    exit()
  if status_Proxy>1:
    print '@@@@ Proxy not valid.. Stopiing the monitoring'
    exit()

  UpdateJobStatus(config)
  MakeHTML(config)

  print "#####################################################"
  print "Sleeping...."
  print "#####################################################"

  time.sleep(MonitoringInfo['RunEvery'])
  os.system('kinit -R')
