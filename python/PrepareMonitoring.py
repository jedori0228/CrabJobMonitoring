#!/usr/bin/env python

import os

def PrepareMonitoring(config):

  exec('from '+config+' import UserInfo')

  os.system('mkdir -p '+UserInfo['HTMLDest'])
