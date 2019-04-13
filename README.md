# CrabJobMonitoring

Example : https://jskim.web.cern.ch/jskim/Public/CrabJobMonitoring/Status.html

You must set cmssw enviroment variables first (i.e., cmsenv), with your crab-submission working directory.

Create a python file, based on python/Configs/MonitConfig.py

E.g., python/Configs/MyConfig.py

Edit python/Configs/MyConfig.py, and then


```
source setup.sh
RunMonitoring.py -i MyConfig
```
