import random as rnd
from time import perf_counter as pfc


def prüfe():
  loop = set()
  for gefangener in range(100):
    if gefangener in loop: continue
    next_box = gefangener
    for count_box in range(50):
      loop.add(next_box)
      next_box = boxes[next_box]
      if next_box == gefangener:
        break
    else:
      return False
  return True

start = pfc()
siege, anz = 0, 100_000
boxes =list(range(100))

for _ in range(anz):
  rnd.shuffle(boxes)
  if prüfe(): siege += 1

strat_zufall_wahrsch = 0.5**100
strat_loop_wahrsch = siege/anz
unterschied = strat_loop_wahrsch / strat_zufall_wahrsch
lichtjahr = 9460730472580.8
länge = unterschied /10 /100 /1000 / lichtjahr
print(f'Bei zufälliger Auswahl der Boxen beträgt die Gewinnwahrscheinlichkeit {strat_zufall_wahrsch}')
print(f'Bei Anwendung der Schleifenstrategie {strat_loop_wahrsch}')
print(f'Der Unterschied der Gewinnwahrscheinlichkeit ist {unterschied:,.0f}')
print(f'Zum Vergleich. Wenn die erste Wahrscheinlichkeit einer Entfernung von 1mm entspricht,')    
print(f'dann entspricht die zweite Wahrscheinlichkeit der Entfernung von {länge:,.0f} Lichtjahren.')    
print(f'Ermittelt in {pfc()-start:.2f} Sekunden.')

