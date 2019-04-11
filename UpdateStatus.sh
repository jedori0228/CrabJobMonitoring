#!/bin/bash

################################
##---- CHANGE ME
user_email="jalmond@cern.ch"
################################

firstletter=`echo $USER | head -c 1`
mkdir -p $SKFlatTag
mkdir -p /afs/cern.ch/user/$firstletter/$USER/www/SKFlat/ProductionStatus/$SKFlatTag/

##-- setup crab3 since crab status and resubmittion is needed
source /cvmfs/cms.cern.ch/crab3/crab.sh

if [ -f "DoneSamples_"+$SKFlatTag+".txt" ];
then
    rm  "DoneSamples_"+$SKFlatTag+".txt"
fi

##-- new script that checks grid proxy and any other setup
python setup_job.py -x $user_email

##-- exit script if grid proxy is not setup
job_status=$?
re='^[0-9]+$'
if ! [[ $job_status =~ $re ]] ; then
    echo "error: Not a number" >&2; exit 1
fi

if [ $job_status -eq 10 ];
then
    echo "Error in setup....  quitting"
    return
fi

while true; do

  echo "Running.............."

  for YEAR in 2018
  do

    echo "Year "$YEAR" is running now.."

    outname=$SKFlatTag"/Status_"$YEAR".html"
    python make_html.py -y $YEAR  -x $user_email 

    job_status=$?
    re='^[0-9]+$'
    if ! [[ $job_status =~ $re ]] ; then
	echo "error: Not a number" >&2; exit 1
    fi

    if [ $job_status -eq 10 ];
    then
	echo "Error in make_html.py....  quitting"
	return
    fi

    cmd_TAGHERE="sed -i 's/TAGHERE/"$SKFlatTag"/g' "$outname
    cmd_YEARHERE="sed -i 's/YEARHERE/"$YEAR"/g' "$outname
    eval $cmd_TAGHERE
    eval $cmd_YEARHERE

    cp $outname /afs/cern.ch/user/$firstletter/$USER/www/SKFlat/ProductionStatus/$SKFlatTag/

  done
  
  cd $CMSSW_BASE/src/SKFlatMaker/SKFlatMaker/script/CRAB3/

  source cleanup_crabdirlogs.sh
  cd -

  echo "#####################################################"
  echo "Sleeping...."
  echo "#####################################################"

  sleep 300
  kinit -R
  
done
