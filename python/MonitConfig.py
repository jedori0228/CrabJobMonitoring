from HTMLTableRow import HTMLTableRow

UserInfo = {
  'LogEmail' : 'jskim@cern.ch',
  'HTMLDest' : '/eos/user/j/jskim/www/HNWR_13TeV/EGammaTnP/CRARBStatus/',
  'WEBDir' : '/eos/user/j/jskim/www/',
  'URLPrefix' : 'https://jskim.web.cern.ch/jskim/',
}
CRABInfo = {
  'MonitName' : 'EGammaTnPNtuple',
  'CrabDirs' : [
    '/afs/cern.ch/work/j/jskim/EGammaTnP/For2016_CMSSW_10_2_5/src/EgammaAnalysis/TnPTreeProducer/test/CRAB3/crab_2016/',
    '/afs/cern.ch/work/j/jskim/EGammaTnP/For2016_CMSSW_10_2_5/src/EgammaAnalysis/TnPTreeProducer/test/CRAB3/crab_2017/',
  ],

  #### HTMLTableRow(varName, color='black', align='center')
  #### varName are the function names of CrabJobStatus class
  'TableContents' : [
    HTMLTableRow( 'Sample', 'black', 'left' ),
    #HTMLTableRow( 'Scheduler', 'black', 'center' ),
    HTMLTableRow( 'USER', 'black', 'center' ),
    HTMLTableRow( 'Unsubmitted', 'gray', 'center' ),
    HTMLTableRow( 'Cooloff', 'gray', 'center' ),
    HTMLTableRow( 'Idle', 'graa', 'center' ),
    HTMLTableRow( 'Running', 'orange', 'center' ),
    HTMLTableRow( 'Failed', 'red', 'center' ),
    HTMLTableRow( 'Transferring', 'black', 'center' ),
    HTMLTableRow( 'Finished', 'green', 'center' ),
    HTMLTableRow( 'Total', 'black', 'center' ),
    HTMLTableRow( 'Perct', 'black', 'center' ),
  ],
}
