from itertools import product
import random as rnd

LÖSUNGSMENGE = list(product(range(1, 7), repeat=4))
GEHEIM = rnd.choice(LÖSUNGSMENGE)


def treffer(v, g):
  farbe_position = sum(a == b for a, b in zip(v, g))
  farbe = sum(min(v.count(a), g.count(a)) for a in set(g)) - farbe_position
  return '+'*farbe_position + 'o'*farbe


def lösungsmenge_reduzieren(l, v):
  return [a for a in l if all([ergebnis == treffer(a, vers) for vers, ergebnis in v.items()])]


anz, versuche, versuch = 0, {}, []
while versuch != GEHEIM:
  anz += 1
  erg = treffer(versuch:= rnd.choice(LÖSUNGSMENGE), GEHEIM)
  versuche[versuch] = erg
  print(f'{anz:2}. Lösungsmenge = {len(LÖSUNGSMENGE):4} Elemente, {versuch}, {erg} ')
  LÖSUNGSMENGE = lösungsmenge_reduzieren(LÖSUNGSMENGE, versuche)