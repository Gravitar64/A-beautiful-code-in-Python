import random as rnd

def prüfe():
  for gefangener in range(100):
    nächste_schublade = gefangener
    for _ in range(50):
      nächste_schublade = schubladen[nächste_schublade]
      if nächste_schublade == gefangener:
        break 
    else:
      return False
  return True           


gew_zufall = 0.5**100

gewinne, anz = 0, 100_000
schubladen = list(range(100))

for _ in range(anz):
  rnd.shuffle(schubladen)
  if prüfe(): gewinne += 1

gew_strategie = gewinne/anz
print(f'Gewinnwahrscheinlichkeit Zufall    = {gew_zufall}')
print(f'Gewinnwahrscheinlichkeit Strategie = {gew_strategie}')


