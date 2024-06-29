import pendulum as pnd

pnd.set_locale('de')

geburtstage = [(1964,10,21), (1963,6,4)]
bisher = sum([(pnd.now().date() - pnd.date(*g)).in_days() for g in geburtstage])

for t in range(10_000):
  alter = bisher + t*2
  if len(set(str(alter))) > 2: continue
  jubiläum = pnd.now().date().add(days=t)
  print(f'{alter} Tage, {jubiläum.format("dd DD.MM.YYYY")}')