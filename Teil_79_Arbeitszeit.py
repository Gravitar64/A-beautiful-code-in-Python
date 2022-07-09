from datetime import datetime,timedelta
import time
import curses


def zeitstatus(start, soll, pause_nach_6h, pause_nach_9h):
  jetzt = datetime.now()
  jetzt = timedelta(hours=jetzt.hour, minutes=jetzt.minute,
                    seconds=jetzt.second)
  ist = jetzt - start
  if ist > timedelta(hours=6):
    soll = soll + pause_nach_6h
  if ist > timedelta(hours=9):
    soll = soll + pause_nach_9h
  arbeitsende = start + soll
  saldo = arbeitsende-jetzt if arbeitsende > jetzt else jetzt-arbeitsende
  max_arbeitszeit = timedelta(hours=10, minutes=45)

  stdscr.addstr(0, 0, f'  Start                           :  {start}')
  stdscr.addstr(1, 0, f'+ Arbeitszeit inkl. Pausen        :  {soll}')
  stdscr.addstr(2, 0, f'= Reguläres Arbeitsende           : {start+soll}')
  stdscr.addstr(3, 0, f'- Aktuelle Uhrzeit                : {jetzt}')
  stdscr.addstr(4, 0, f'= Saldo jetzt                     : {"-" if jetzt < arbeitsende else "+"}{saldo}', COLOR_RED if ist < soll else COLOR_GREEN | curses.A_BOLD)

  stdscr.addstr(
      6, 0, f'Spätester Feierabend              : {start+max_arbeitszeit}')
  stdscr.refresh()


H, M = map(int, input('Arbeitsbeginn (HH:MM): ').split(':'))
start = timedelta(hours=H, minutes=M)
soll = timedelta(hours=7, minutes=45)
pause_nach_6h = timedelta(minutes=30)
pause_nach_9h = timedelta(minutes=15)

stdscr = curses.initscr()
curses.curs_set(False)
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
COLOR_RED = curses.color_pair(1)
COLOR_GREEN = curses.color_pair(2)

while True:
  zeitstatus(start, soll, pause_nach_6h, pause_nach_9h)
  time.sleep(1)

curses.endwin()
