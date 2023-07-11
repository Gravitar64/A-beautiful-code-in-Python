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
  tabelle = sorted([(p, i+1) for i, p in enumerate(punkte)], reverse=True)
  platz, gleich, vorherige = 0, 1, 999
  for p, s in tabelle:
    if p == vorherige:
      gleich += 1
    else:
      platz += gleich
      gleich = 1
    print(f'Platz {platz}: Spieler {s} mit {p} Punkten')
    vorherige = p
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