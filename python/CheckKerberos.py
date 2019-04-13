#!/usr/bin/env python

import os,time
from datetime import datetime, timedelta
from TimeTools import ParseTicketTime
import subprocess

time_renewal=12 #### in hours : This is time before ticket renewal stops when email is sent to let user know to renew manually the kerberos ticket

def CheckKerberos(config):

  ### Only send email if terminal kerberos ticket is about to expire and user has set email
  DoMail=False
  HOSTNAME = os.environ['HOSTNAME']
  USER = os.environ['USER']

  ### klist show two thinigs;

  ### Valid starting     Expires            Service principal
  ### 04/12/19 12:33:47  04/13/19 13:33:47  krbtgt/CERN.CH@CERN.CH
  ###   renew until 04/17/19 12:33:47
  ### 04/12/19 12:33:48  04/13/19 13:33:47  afs/cern.ch@CERN.CH
  ###                           ^ this can be renewed with 'kinit -R'
  ###   renew until 04/17/19 12:33:47
  ###                       ^ this can be renewed with 'kinit jskim', but we need to type password

  ###-- klist lists kerberos tickets 

  lines_klist = subprocess.check_output('klist').split('\n')
  ticket_info = ''

  ### afs_kerb is used to only check afs ticket
  afs_kerb=False
  ### ticket_is_valid is used to test that kerberos has not expired (would mean som server issue)
  ticket_is_valid=True
  ### renewal_expiring is set if ticket is close to expiring (has 5 days from first running)
  renewal_expiring=False

  ##-- loop over kerberos list
  for line in lines_klist:

    line = line.strip('\n')

    ##-- only look at afs ticket 
    if "afs/cern.ch@CERN.CH" in line:

      words = line.split()
      # ['04/12/19', '13:06:33', '04/13/19', '14:06:33', 'afs/cern.ch@CERN.CH']

      afs_kerb=True
      ticket_info += "\nCurrent ticket AFS:\n"
      ticket_info += line+"\n"

    ## check renew only after we get afs_kerb correctly
    if not afs_kerb:
      continue

    ##-- check expiration of afs ticket 
    if "renew until" in line:

      ticket_info += line+"\n"

      words = line.split()
      # ['renew', 'until', '04/17/19', '12:33:47']

      expiration_time = ParseTicketTime(words[2]+' '+words[3])
      alert_time = datetime.now() + timedelta(hours=time_renewal)

      #### check if renewal date is within time_renewal hours from now, if so send email to let user know

      if expiration_time < datetime.now():
        ticket_is_valid=False

      elif expiration_time < alert_time:

        renewal_expiring=True

      ## we only need two lines, just break
      break

  ##-- status lets the summary code know what the state of the ticket is default 0 (following bash exit code rule)
  status = 0
  alerting_msg = ''
  if not afs_kerb:
    alerting_msg  = "Kerberos ticket is NOT AVAILABLE."
    alerting_msg += "Please log in to "+USER+"@"+HOSTNAME+" to renew the ticket\n"
    DoMail=True
    status= 1
  if not ticket_is_valid:
    alerting_msg  = "Kerberos ticket has been EXPIRED."
    alerting_msg += "Please log in to "+USER+"@"+HOSTNAME+" to renew the ticket\n"
    DoMail=True
    status= 1

  if renewal_expiring: 
    ### ticket is valid and exists, but is close to expiration and will need password to reset
    alerting_msg += "Ticket is expiring soon\n"
    alerting_msg += "Please log in to "++USER+"@"+HOSTNAME+" to renew the ticket\n"
    DoMail=True
    status = 1

  ###################################################
 
  if DoMail:

    import SendEmail
    exec('from '+config+' import UserInfo')

    email_content  = ticket_info
    email_content += "\n**********************************************************\n"
    email_content += alerting_msg
    email_content += "**********************************************************\n"

    LogEmail = UserInfo['LogEmail']

    if LogEmail != "":
      SendEmail.SendEmail(LogEmail, LogEmail, '[CrabJobMonitoring] lxplus Kerberos ticket', email_content)

    #print email_content

  return status
