import os

class CrabJobStatus:

  def __init__(self):

    self._Empty = True
    self._SubmitFail = False
    self._Started = False

    self._Sample = ''
    self._USER = os.environ['USER']
    self._TimeStamp = ''
    self._Scheduler = ''
    self._HOSTNAME = os.environ['HOSTNAME']

    self._Unsubmitted = 0
    self._Cooloff = 0
    self._Idle = 0
    self._Running = 0
    self._Failed = 0
    self._Transferring = 0
    self._Finished = 0.
    self._Held = 0
    self._Total = -1.

  def AllDone(self):
    if (not self._Empty) and (self._Finished==self._Total):
      return True
    else:
      return False

  def SetUSER(self, var):
    self._USER = var
  def USER(self):
    return self._USER

  def SetEmpty(self, var):
    self._Empty = var
  def Empty(self):
    return self._Empty

  def SetSubmitFail(self, var):
    self._SubmitFail = var
  def SubmitFail(self):
    return self._SubmitFail

  def SetStarted(self, var):
    self._Started = var
  def Started(self):
    return self._Started

  def SetSample(self, var):
    self._Sample = var
  def Sample(self):
    return self._Sample

  def SetTimeStamp(self, var):
    self._TimeStamp = var
  def TimeStamp(self):
    return self._TimeStamp

  def SetScheduler(self, var):
    self._Scheduler = var
  def Scheduler(self):
    return self._Scheduler

  def SetHOSTNAME(self, var):
    self._HOSTNAME = var
  def HOSTNAME(self):
    return self._HOSTNAME

  def SetUnsubmitted(self, var):
    self._Unsubmitted = var
  def Unsubmitted(self):
    return self._Unsubmitted

  def SetCooloff(self, var):
    self._Cooloff = var
  def Cooloff(self):
    return self._Cooloff

  def SetIdle(self, var):
    self._Idle = var
  def Idle(self):
    return self._Idle

  def SetRunning(self, var):
    self._Running = var
  def Running(self):
    return self._Running

  def SetFailed(self, var):
    self._Failed = var
  def Failed(self):
    return self._Failed

  def SetTransferring(self, var):
    self._Transferring = var
  def Transferring(self):
    return self._Transferring

  def SetHeld(self, var):
    self._Held = var
  def Held(self):
    return self._Held

  def SetFinished(self, var):
    self._Finished = var
  def Finished(self):
    return self._Finished

  def SetTotal(self, var):
    self._Total = var
  def Total(self):
    return self._Total

  def SetPerct(self, var):
    self._Perct = var
  def Perct(self):
    frac = float(self._Finished)/float(self._Total)
    perc = 100. * frac
    return round(perc,2)
