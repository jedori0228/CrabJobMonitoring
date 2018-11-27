#!/bin/bash

firstletter=`echo $USER | head -c 1`
mkdir -p /eos/user/$firstletter/$USER/www/SKFlat/ProductionStatus/$SKFlatTag/

while true; do

  for YEAR in 2016 2017
  do
    outname="Status_"$YEAR".html"
    python make_html.py -y $YEAR

    cmd_TAGHERE="sed -i 's/TAGHERE/"$SKFlatTag"/g' "$outname
    cmd_YEARHERE="sed -i 's/YEARHERE/"$YEAR"/g' "$outname
    eval $cmd_TAGHERE
    eval $cmd_YEARHERE

    cp $outname /eos/user/$firstletter/$USER/www/SKFlat/ProductionStatus/$SKFlatTag/
  done

  echo "#####################################################"
  echo "Sleeping...."
  echo "#####################################################"

  sleep 300

done
