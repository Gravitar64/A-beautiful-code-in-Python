from datetime import timedelta, datetime

meile = 1.60934

zeit = timedelta(minutes=10, seconds=0)
delta = timedelta(seconds=10)

for _ in range(40):
  pro_meile = zeit/meile
  pro_km = zeit * meile

  print(f'{zeit} pro Meile = {pro_meile.seconds // 60}:{pro_meile.seconds % 60:02d} pro km <-----> {zeit} pro km = {pro_km.seconds // 60}:{pro_km.seconds % 60:02d} pro Meile')
  zeit -= delta
