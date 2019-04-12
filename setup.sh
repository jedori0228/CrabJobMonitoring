#!/bin/bash

## Check $CMSSW_BASE
if [[ -z $CMSSW_BASE ]]; then
  echo "@@@@ cmsenv not done yet. Try this again after cmsnev"
  echo "@@@@ this is to make sure we are using python >= 2.7"
  return
fi

## Init Proxy
echo "@@@@ Setting proxy.."
echo "@@@@ type your grid proxy password when asked"
voms-proxy-init --voms cms --valid 192:00
while [[ $? == 1 ]]; do
  printf "\n@@@@ Proxy is not set, do it again\n"
  voms-proxy-init --voms cms --valid 192:00
done

export MonitWD=`pwd`
export PATH=./bin/:./python/:$PATH
export PYTHONPATH=./python/:$PYTHONPATH

mkdir -p pkl
