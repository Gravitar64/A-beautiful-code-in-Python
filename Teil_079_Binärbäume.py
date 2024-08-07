import random as rnd
from re import A
from time import perf_counter as pfc


class Knoten:
  def __init__(self, wert):
    self.wert = wert
    self.links = None
    self.rechts = None

  def einfügen(self, wert):
    if wert < self.wert:
      if self.links:
        self.links.einfügen(wert)
      else:
        self.links = Knoten(wert)
    elif wert > self.wert:
      if self.rechts:
        self.rechts.einfügen(wert)
      else:
        self.rechts = Knoten(wert)


def baumSuche(wurzel, wert):
  if not wurzel: return False
  if wert < wurzel.wert:
    aktuell = baumSuche(wurzel.links, wert)
  elif wert > wurzel.wert:
    aktuell = baumSuche(wurzel.rechts, wert)
  else:
    aktuell = None
  return aktuell or wurzel.wert == wert


def baumSortiert(wurzel):
  if not wurzel: return
  baumSortiert(wurzel.links)
  print(wurzel.wert)
  baumSortiert(wurzel.rechts)


def anzKnoten(wurzel):
  if not wurzel: return 0
  links = anzKnoten(wurzel.links)
  rechts = anzKnoten(wurzel.rechts)
  return 1 + links + rechts


ANZ = 100_000
start = pfc()
wurzel = Knoten(ANZ // 2)
for _ in range(ANZ):
  wurzel.einfügen(rnd.randrange(ANZ))
for _ in range(ANZ):
  baumSuche(wurzel, rnd.randrange(ANZ))
zeitKnoten = pfc() - start


start = pfc()
numbers = set()
for _ in range(ANZ):
  numbers.add(rnd.randrange(ANZ))
for _ in range(ANZ):
  rnd.randrange(ANZ) in numbers
zeitSet = pfc() - start

print(f'Binärbaum: Zeit für {ANZ:,} Anlage und Suche = {zeitKnoten:.2f} Sek.')
print(f'Set      : Zeit für {ANZ:,} Anlage und Suche = {zeitSet:.2f} Sek.')
print(f'Faktor Binärbau vs. Set = {zeitKnoten / zeitSet:.2f}x')
