import random as rnd

def prüfe():
  rnd.shuffle(schubladen)
  for gefangener in range(100):
    schublade = gefangener
    for _ in range(50):
      schublade = schubladen[schublade]
      if schublade == gefangener:
        break
    else:
      return 0
  return 1      


sim = 100_000
schubladen = list(range(100))

siege = sum([prüfe() for _ in range(sim)])

print(f'Gewinnwahrscheinlichkeit Zufall    = {0.5**100}')
print(f'Gewinnwahrscheinlichkeit Strategie = {siege/sim}')