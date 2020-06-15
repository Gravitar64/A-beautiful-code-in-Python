from itertools import product
import random as rnd

lösungsmenge = list(product(range(6), repeat=4))
GEHEIM = rnd.choice(lösungsmenge)


def treffer(v, g):
  farbe_position = sum(a == b for a, b in zip(v, g))
  farbe = sum(min(v.count(a), g.count(a)) for a in set(g)) - farbe_position
  return '+'*farbe_position + 'o'*farbe


anz, versuch = 0, []
while versuch != GEHEIM:
  anz += 1
  versuch = rnd.choice(lösungsmenge)
  erg = treffer(versuch, GEHEIM)
  print(f'{anz:2}. Lösungsmenge = {len(lösungsmenge):5} Elemente, {versuch}, {erg} ')
  lösungsmenge = [l for l in lösungsmenge if treffer(l, versuch) == erg]