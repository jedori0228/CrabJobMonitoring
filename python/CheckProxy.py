#!/usr/bin/env python

import os,time
from datetime import datetime, timedelta
from TimeTools import ParseTicketTime
import subprocess

time_renewal=12 #### in hours : This is time before ticket renewal stops when email is sent to let user know to renew manually the kerberos ticket

def CheckProxy():

  DoMail=False
  ProxyTimeLeft = ''
  alerting_msg = ''
  status = 0

  HOSTNAME = os.environ['HOSTNAME']
  USER = os.environ['USER']

  ### First check if we have it set
  ProxyInfoCheck = subprocess.call('voms-proxy-info &> /dev/null',shell=True)
  ## if this is 1, means no proxy set
  if ProxyInfoCheck==1:
    DoMail = True
    status = 1
    alerting_msg  = 'GRID proxy is NOT SET\n'
    alerting_msg += "Please log in to "+USER+"@"+HOSTNAME+", and run\n"
    alerting_msg += "voms-proxy-init --voms cms --valid 192:00\n"

  else:

    ProxyTimeLeft = subprocess.check_output('voms-proxy-info | grep "timeleft"',shell=True).split()[2]
    # '191:58:45'

    #### Check if expired
    if ProxyTimeLeft == "00:00:00":
      DoMail = True
      status = 1
      alerting_msg = 'GRID proxy has been EXPIRED\n'
      alerting_msg += "Please log in to "+USER+"@"+HOSTNAME+", and run\n"
      alerting_msg += "voms-proxy-init --voms cms --valid 192:00\n"

    else:
      ProxyTimeLeft_hour = int(ProxyTimeLeft.split(':')[0])

      if ProxyTimeLeft_hour < time_renewal:

        DoMail = True
        status = 1

        alerting_msg += "GRID proxy is EXPIRING SOON\n"
        alerting_msg += "Please log in to "+USER+"@"+HOSTNAME+", and run\n"
        alerting_msg += "voms-proxy-init --voms cms --valid 192:00\n"


  if DoMail:

    import SendEmail
    from MonitConfig import UserInfo

    email_content  = 'GRID Proxy time left (HH:MM:SS) : '+ProxyTimeLeft
    email_content += "\n**********************************************************\n"
    email_content += alerting_msg
    email_content += "**********************************************************\n"

    LogEmail = UserInfo['LogEmail']

    if LogEmail != "":
      SendEmail.SendEmail(LogEmail, LogEmail, '[CrabJobMonitoring] GRID Proxy', email_content)

    #print email_content

  return status
