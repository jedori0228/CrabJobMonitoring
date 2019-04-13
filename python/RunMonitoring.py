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
  print "Config file is empty"
  exit()

config = 'Configs.'+args.Config

PrepareMonitoring(config)

while True:

  CheckKerberos(config)
  CheckProxy(config)
  UpdateJobStatus(config)
  MakeHTML(config)

  print "#####################################################"
  print "Sleeping...."
  print "#####################################################"

  time.sleep(300)
  os.system('kinit -R')
