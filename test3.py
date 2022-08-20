from datetime import datetime, timedelta

def datetime2timedelta(d) -> timedelta:
  return timedelta(hours=d.hour, minutes=d.minute, seconds=d.second)

def hm2timedelta(h,m) -> timedelta:
  return timedelta(hours=h, minutes=m)

a1 = datetime2timedelta(datetime.now())
a2 = datetime2timedelta(datetime.now())

print(a1+a2)

