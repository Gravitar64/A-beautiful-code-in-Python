import datetime as dt
import arrow
from dateutil.relativedelta import relativedelta
import locale

locale.setlocale(locale.LC_ALL, 'German')
dat_format = '%a %d.%m.%Y %H:%M'


geburtsdatum = dt.datetime(1964,10,21,12,59)
jetzt = dt.datetime.now()
alter = jetzt-geburtsdatum

start = arrow.now()
start.replace(tzinfo='Europe/Berlin')
end = arrow.get('30.04.2022 13:00','DD.MM.YYYY HH:mm')
print(f'Start-Datetime: {start}')
print(f'End-Datetime : {end}')
print(f'Time-Difference: {end-start}')

jubiläen = []
for k in (500,1_000,22_222,5_000,10_000):
  nächste = ((alter.days // k)+1)*k
  jubiläum = geburtsdatum + dt.timedelta(days=nächste)
  jubiläen.append((nächste, jubiläum))


print(f'\nGeboren am        : {geburtsdatum.strftime(dat_format)}')
print(f'Heute             : {jetzt.strftime(dat_format)}')
print(f'Aktuelles Alter   : {relativedelta(jetzt,geburtsdatum).years} Jahre ({alter})')
for n,j in jubiläen:
  alter = relativedelta(j,geburtsdatum).years
  print(f'   Nächstes Jubiläum : {j.strftime(dat_format)} ({n:,.0f} Tage = {alter}. Jahre)')


