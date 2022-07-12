from datetime import datetime, timedelta
import time

def t2td(d) -> timedelta:
  if type(d) == datetime:
    return timedelta(hours=d.hour, minutes=d.minute, seconds=d.second)
  else:
    hh,mm = map(int, d.split(':'))
    return timedelta(hours=hh, minutes=mm)



start = t2td(input('Arbeitsbeginn (HH:MM): '))
max_soll = t2td("10:45")

while True:
  jetzt = t2td(datetime.now())
  ist = jetzt - start
  soll = t2td("07:45")

  if ist > t2td("6:00"):
    soll += t2td("0:30")
  if ist > t2td("9:00"):
    soll += t2td("0:15")

  saldo = soll - ist if soll > ist else ist - soll

  print(f'  Arbeitszeit inkl. Pausen      =  {soll}')
  print(f'- davon bereits geleistet       =  {ist}')
  print(f'= akt. Saldo                    = {"-" if soll > ist else "+"}{saldo}')
  print()
  print(f'  Feierabend                    = {start + soll} (max. {start + max_soll})')
  time.sleep(1)




