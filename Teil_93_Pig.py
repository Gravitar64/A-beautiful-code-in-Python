import random


def würfeln(i, p):
  while True:
    wurf = random.randint(1, 6)
    p = p+wurf if wurf > 1 else 0
    print(f'Spieler {i}: {wurf} gewürfelt, Punkte = {p:<2} (Max = {max(punkte)})')
    if not p: return p
    if input('Weiterwürfeln? (j/n) ').lower() == 'j': continue
    return p


def rangliste(punkte):
  tabelle = sorted([(-p, s) for s, p in enumerate(punkte,start=1)])
  for p, s in tabelle:
    print(f'Spieler {s} mit {-p} Punkten')
  print()    


while True:
  anz_spieler = input('Wieviele Spieler (2-6)? ')
  if not anz_spieler.isdigit(): continue
  if 1 < (spieler := int(anz_spieler)) < 7: break

punkte = [0]*spieler
while max(punkte) < 50:
  for i, p in enumerate(punkte):
    punkte[i] = würfeln(i+1, p)
    rangliste(punkte)