from datetime import datetime, timedelta
import time


def td(t):
  if type(t) == datetime:
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
  else:
    HH, MM = map(int, t.split(':'))
    return timedelta(hours=HH, minutes=MM)


start = td(input('Arbeitsbeginn (HH:MM): '))
soll  = td('07:45')
max_soll = td('10:45')
pausen = td('00:00')

while True:
  jetzt = td(datetime.now())
  ist = jetzt - start
  pausen = td('00:45') if ist > td('9:00') else td('00:30') if ist > td('6:00') else pausen
  saldo = '+' + str(ist-soll-pausen) if ist >= (soll+pausen) else '-' + str(soll+pausen - ist)

  print(f'  Arbeitszeit inkl. Pausen       =  {soll + pausen}') 
  print(f'- davon bereits geleistet        =  {ist}')
  print(f'= akt. Saldo                     = {saldo}')
  print(f'= Feierabend (start= {start})   = {start + soll + pausen} (max. {start + max_soll})')
  print(f'= akt. Uhrzeit                   = {jetzt}')
  if jetzt > (start + max_soll):
    print(f'ARBEITSZEITVERSTOSS seit {jetzt - (start + max_soll)}')
  time.sleep(1)  


