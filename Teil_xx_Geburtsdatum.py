import pendulum as pnd

pnd.set_locale('de')

geburtsdatum = pnd.datetime(1964,10,21,12,59)
jetzt = pnd.now()
alter = jetzt-geburtsdatum

jubiläen = []
for k in (500,1_000,22_222,5_000,10_000):
  nächste = ((alter.in_days() // k)+1)*k
  jubiläum = geburtsdatum.add(days=nächste)
  jubiläen.append((nächste, jubiläum))


print()
print(f'Geboren am        : {geburtsdatum.to_rss_string()}')
print(f'Heute             : {jetzt.to_rss_string()}')
print(f'Aktuelles Alter   : {alter.in_years()} Jahre (in Tagen = {alter.in_days():,.0f})')
for n,j in jubiläen:
  alter = geburtsdatum.add(days=n) - geburtsdatum
  print(f'   Nächstes Jubiläum : {j.to_rss_string()} ({n:,.0f} Tage = {alter.in_years()}. Jahre)')


