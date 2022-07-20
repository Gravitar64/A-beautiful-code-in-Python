import random as rnd
from itertools import combinations


def leseDatei(dateiname):
  with open(dateiname) as f:
    spieler = [int(x) for x in f][1:]
    return spieler, len(spieler)


def liga(sim):
  anzSiege = 0
  for _ in range(sim):
    tabelle = [0]*anz
    for a,b in combinations(range(anz), 2):
      tabelle[lieferGewinner(a, b, 1)] += 1
    turnierSieger = min([i for i,p in enumerate(tabelle) if p == max(tabelle)])
    if turnierSieger == besterSpieler: anzSiege += 1
  return anzSiege / sim * 100


def lieferGewinner(a,b,n):
  ergSpielerA = 0
  for _ in range(n):
    los = rnd.randrange(spieler[a]+spieler[b])
    ergSpielerA += 1 if los < spieler[a] else -1
  return a if ergSpielerA > 0 else b


def ko(sim,n):
  anzSiege = 0
  for _ in range(sim):
    aktRd = rnd.sample(range(anz),anz)
    while len(aktRd) > 1:
      nextRd = []
      while aktRd:
        a,b = aktRd.pop(), aktRd.pop()
        nextRd.append(lieferGewinner(a,b,n))
      aktRd = nextRd
    if aktRd.pop() == besterSpieler: anzSiege += 1      
  return anzSiege / sim * 100


sim = 10_000
for n in range(1,5):
  dateiname = f'Teil_67_spielstaerken{n}.txt'
  spieler, anz = leseDatei(dateiname)
  besterSpieler = spieler.index(max(spieler))
  print(f'Lösung für Aufgabe {dateiname} mit {sim:,} Simulationsläufen')
  print(f'  Liga: {liga(sim):.1f}%')  
  print(f'  KO  : {ko(sim,1):.1f}%')  
  print(f'  KOx5: {ko(sim,5):.1f}%')
  print() 