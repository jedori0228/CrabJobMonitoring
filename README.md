# CrabJobMonitoring

Example : https://jskim.web.cern.ch/jskim/Public/CrabJobMonitoring/Status.html

You must set cmssw enviroment variables first (i.e., cmsenv), with your crab-submission working directory.

create a python file, based on python/MonitConfig.py

E.g., python/MyConfig.py

Edit python/MyConfig.py, and then


```
source setup.sh
RunMonitoring.py -i MyConfig
```
