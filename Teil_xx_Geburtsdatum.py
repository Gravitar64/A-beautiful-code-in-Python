import datetime as dt
from tkinter import N
from dateutil.relativedelta import relativedelta
import locale

locale.setlocale(locale.LC_ALL, 'German')
dat_format = '%a %d.%m.%Y %H:%M'

geburtsdatum = dt.datetime(1995,05,08,12,59)
jetzt = dt.datetime.now()
alter = jetzt-geburtsdatum

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


