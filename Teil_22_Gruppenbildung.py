import random as rnd 

teilnehmer = "Constantin Peter Jan Simone Jörg Daniela Klaus Dirk Heike Elke".split()

rnd.seed()
rnd.shuffle(teilnehmer)

def gruppenbildung(liste, gruppengröße):
  for n in range(0, len(liste), gruppengröße):
    yield liste[n:n+gruppengröße]

for zähler, gruppe in enumerate(gruppenbildung(teilnehmer, 5)):
  print(f'Gruppe {zähler+1}: {", ".join(gruppe)}')