import random


def würfel(s,p):
  zug = 0
  while True:
    wurf = random.randint(1,6)
    zug = zug+wurf if wurf > 1 else 0
    print(f'Spieler {s+1} hat {wurf} gewürfelt, Punkte Zug = {zug}, Gesamt = {p+zug} (Max = {max(punkte)})')
    if zug and input('Weiterwürfeln (j/n)? ') == 'j': continue
    return zug
    

def rangliste(punkte):
  for p,s in sorted([(p,s) for s,p in enumerate(punkte, start=1)], reverse=True):
    print(f'Spieler {s} mit {p} Punkten')
  print()
    

anz_spieler = int(input("Wieviele Spieler (2-9)? "))
punkte = [0]*anz_spieler

while max(punkte) < 100:
  for s,p in enumerate(punkte):
    punkte[s] += würfel(s,p)
    rangliste(punkte)