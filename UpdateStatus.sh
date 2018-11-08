#!/bin/bash

firstletter=`echo $USER | head -c 1`

mkdir -p /eos/user/$firstletter/$USER/www/SKFlat/ProductionStatus/$SKFlatTag/
while true; do
  python make_html.py
  cp Status.html /eos/user/$firstletter/$USER/www/SKFlat/ProductionStatus/$SKFlatTag/
done
