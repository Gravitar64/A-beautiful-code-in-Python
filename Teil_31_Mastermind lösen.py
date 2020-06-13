from itertools import product
import random as rnd 

LÖSUNGSMENGE = list(product(range(1,7), repeat = 4))
GEHEIM = rnd.choice(LÖSUNGSMENGE)

def treffer(v,g):
  farbe_position = sum(a==b for a,b in zip(v,g))
  farbe = sum(min(v.count(a), g.count(a)) for a in set(g)) - farbe_position
  return '+'*farbe_position + 'o'*farbe

def lösungsmenge_reduzieren(l,v):
  l = [a for a in l if all([ergebnis == treffer(a,versuch) for versuch,ergebnis in v.items()])]
  return l

def maximale_differenz(l,v):
  max_diff = 0
  
  for mögliche_lösung in l:
    diff = sum(abs(a-b) for versuch in v for a,b in zip(mögliche_lösung,versuch) )
    if diff > max_diff:
      max_diff = diff
      best_lösung = mögliche_lösung
  return best_lösung   

def geringste_abweichung(l,v):   
  if not v: return rnd.choice(l)
  v = list(v)
  min_abw = 999999
  referenz = sum(abs(a-b) for v1,v2 in zip(v,v[1:]) for a,b in zip(v1,v2)) / len(v)
  for mögliche_lösung in l:
    abw = sum(abs(a-b) for versuch in v for a,b in zip(mögliche_lösung,versuch)) / len(v) - referenz
    if abw < min_abw:
      min_abw = abw
      best_lösung=mögliche_lösung
  return best_lösung  


def lösung_ermitteln_max_diff(l):
  GEHEIM = rnd.choice(l)
  anz = 0
  versuche = {}
  versuch = []
  while versuch != GEHEIM:
    anz += 1
    versuch = geringste_abweichung(l, versuche)
    versuche[versuch] = treffer(versuch, GEHEIM)
    l = lösungsmenge_reduzieren(l, versuche)
  return anz  

def lösung_ermitteln_rnd(l):
  GEHEIM = rnd.choice(l)
  anz = 0
  versuche = {}
  versuch = []
  while versuch != GEHEIM:
    anz += 1
    versuch = rnd.choice(l)
    versuche[versuch] = treffer(versuch, GEHEIM)
    l = lösungsmenge_reduzieren(l, versuche)
  return anz    

sum1 = sum2 = 0
for i in range(1000):
  sum1 += lösung_ermitteln_rnd(LÖSUNGSMENGE)
  sum2 += lösung_ermitteln_max_diff(LÖSUNGSMENGE)

print(f'{sum1} für Zufallsauswahl, {sum2} für max Diff')
