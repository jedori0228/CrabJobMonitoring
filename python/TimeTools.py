from datetime import datetime, timedelta

def ParseTicketTime(s):
  # s should in form of "04/13/19 13:33:47"
  words = s.split()

  days_ = words[0].split('/')
  month_ = int(days_[0])
  day_ = int(days_[1])
  year_ = int(days_[2])+2000

  times_ = words[1].split(':')
  hour_ = int(times_[0])
  minute_ = int(times_[1])
  second_ = int(times_[2])

  return datetime(year=year_, month=month_, day=day_, hour=hour_, minute=minute_, second=second_)
