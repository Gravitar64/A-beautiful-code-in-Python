from itertools import product
import random as rnd 

lösungsmenge = list(product(range(7), repeat = 4))
GEHEIM = rnd.choice(lösungsmenge)
versuch = ''

def treffer(v,g):
  farbe_position = sum(a==b for a,b in zip(v,g))
  farbe = sum(min(v.count(a), g.count(a)) for a in set(g)) - farbe_position
  return '+'*farbe_position + 'o'*farbe

anz = 0
while versuch != GEHEIM:
  anz += 1
  versuch = rnd.choice(lösungsmenge)
  erg = treffer(versuch, GEHEIM)
  print(f'Versuch Nr. {anz} noch {len(lösungsmenge):4} {versuch} {erg}')
  lösungsmenge = [denkbare_lösung for denkbare_lösung in lösungsmenge if treffer(versuch, denkbare_lösung) == erg]


print(f'Lösung in {anz} Versuchen gefunden!')