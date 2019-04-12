import os

class CrabJobStatus:

  def __init__(self):

    self.Empty = True
    self.SubmitFail = False
    self.Started = False

    self.Sample = ''
    self.TimeStamp = ''
    self.Scheduler = ''

    self.JobUnsubmitted = 0
    self.JobCooloff = 0
    self.JobIdle = 0
    self.JobRunning = 0
    self.JobFailed = 0
    self.JobTransferring = 0
    self.JobFinished = 0.
    self.JobTotal = -1.

  def AllDone(self):
    if (not self.Empty) and (self.JobFinished==self.JobTotal):
      return True
    else:
      return False

  def Print(self):
    print self.Sample+'\t'+self.TimeStamp+'\t'+str(self.JobUnsubmitted)+'\t'+str(self.JobCooloff)+'\t'+str(self.JobIdle)+'\t'+str(self.JobRunning)+'\t'+str(self.JobFailed)+'\t'+str(self.JobTransferring)+'\t'+str(self.JobFinished)+'\t'+str(self.JobTotal)
