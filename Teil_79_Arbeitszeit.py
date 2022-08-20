from datetime import datetime, timedelta
import time
import curses
import playsound


def td(z):
  if type(z) == str:
    HH, MM = map(int, z.split(':'))
    return timedelta(hours=HH, minutes=MM)
  else:
    return timedelta(hours=z.hour, minutes=z.minute, seconds=z.second)

def form(td):
  return f'{str(td):0>8}'    


start = td(input('Arbeitsbeginn (HH:MM): '))
soll = td('7:45')
max_soll = td('10:45')
pausen = td('0:00')
std = curses.initscr()

while True:
  jetzt = td(datetime.now())
  ist = jetzt - start
  pausen = td('0:45') if ist > td('9:00') else td(
      '0:30') if ist > td('6:00') else pausen
  arbeitszeit = soll + pausen
  saldo = '+' + form(ist - arbeitszeit) if ist >= (arbeitszeit) else '-' + form(arbeitszeit - ist)

  std.addstr(0, 0, f'  Arbeitsbeginn                     =  {form(start)}')
  std.addstr(1, 0, f'+ Arbeitszeit inkl. Pausen          =  {form(arbeitszeit)}')
  std.addstr(2, 0, f'= Feierabend                        =  {form(start + arbeitszeit)} (max. {start + max_soll})')
  std.addstr(4, 0, f'- aktuelle Uhrzeit                  =  {form(jetzt)}')
  std.addstr(5, 0, f'= akt. Saldo                        = {saldo}')
  

  
  if jetzt == (start + arbeitszeit):
    playsound.playsound('Teil_79_yabba_dabba_doo.mp3')
  
  time.sleep(1)
  std.refresh()
