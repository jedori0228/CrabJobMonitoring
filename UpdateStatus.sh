#!/bin/bash

##-- setup crab3 since crab status and resubmittion is needed
source /cvmfs/cms.cern.ch/crab3/crab.sh

python python/PrepareMonitoring.py

while true; do

  #### Check tickets and proxy
  CheckKerberos.py
  CheckProxy.py

  #### update status
  UpdateJobStatus.py

  #### make html
  MakeHTML.py

  echo "#####################################################"
  echo "Sleeping...."
  echo "#####################################################"

  sleep 300
  kinit -R
  
done
