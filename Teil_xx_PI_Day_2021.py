import random as rnd 
import math
import curses

stdscr = curses.initscr()

total, coprime = 1_000_000, 0
for i in range(total):
  zuf1, zuf2 = rnd.randint(1,1_000_000), rnd.randint(1,1_000_000)
  coprime += 1 if math.gcd(zuf1, zuf2) == 1 else 0
  pie = math.sqrt(6 * i / coprime)
  stdscr.addstr(0, 0, f'PI               = {math.pi}')
  stdscr.addstr(1, 0, f'PI extrapoliert  = {pie}')
  stdscr.addstr(2, 0, f'Abweichung       = {abs(math.pi-pie)}', curses.A_BOLD)
  stdscr.refresh()
stdscr.getkey()