# CrabJobMonitoring

Example : https://jskim.web.cern.ch/jskim/Public/CrabJobMonitoring/Status.html

You must set cmssw enviroment variables first (i.e., cmsenv), with your crab-submission working directory.

Create a python file, based on python/Configs/MonitConfig.py

E.g.,

```
source setup.sh
cp python/Configs/MonitConfig.py python/Configs/MyConfig.py
### edit python/Configs/MyConfig.py
RunMonitoring.py -i MyConfig
```
