import random as rnd
from itertools import combinations
from collections import defaultdict


class Karte(object):
  def __init__(self, wert, farbe) -> None:
    self.wert = wert
    self.farbe = farbe

  def __repr__(self):
    karten_namen = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    name = str(self.wert) if self.wert < 10 else karten_namen[self.wert]
    return name + self.farbe


class Kartendeck(object):
  def __init__(self):
    self.karten = self._neu_gemischt()

  def _neu_gemischt(self):
    karten = [Karte(w, f) for f in '♤♡♧♢' for w in range(2, 15)]
    rnd.shuffle(karten)
    return karten

  def gib(self, anz):
    return [self.karten.pop() for _ in range(anz)]


def score_berechnen(rang, karten):
  ergebnis = str(rang) + ''.join([f'{k.wert:02d}' for k in karten])
  print(ergebnis)


def rang_ermitteln(board, pocket):
  karten7 = board + pocket
  karten7 = sorted(karten7, key=lambda k: k.wert, reverse=True)
  0
  beste_bewertung = -1
  for karten5 in combinations(karten7, 5):
    bewertung, karten = bewerte(karten5)
    if bewertung > beste_bewertung:
      beste_bewertung = bewertung
      beste_karten = karten
  return beste_bewertung, beste_karten


def bewerte(karten):
  werte = {k.wert for k in karten}
  farben = {k.farbe for k in karten}
  flush = len(farben) == 1
  straight = (len(werte) == 5 and max(werte) - min(werte) == 4) or \
      werte == {5, 4, 3, 2, 14}

  wert2karten = defaultdict(list)
  anz2karten = defaultdict(list)
  for k in karten:
    wert2karten[k.wert].append(k)
  for v in wert2karten.values():
    anz2karten[len(v)] += v

  # Royal Flush
  if straight and flush and max(werte) == 14:
    return 9, karten
  # Straight Flush
  if straight and flush:
    if werte == {5, 4, 3, 2, 14}:
      karten = karten[1:] + karten[:1]
    return 8, karten
  # Four of a Kind
  if 4 in anz2karten:
    return 7, anz2karten[4] + anz2karten[1]
  # Full House
  if 3 in anz2karten and 2 in anz2karten:
    return 6, anz2karten[3] + anz2karten[2]
  # Flush
  if flush:
    return 5, karten
  # Straight
  if straight:
    if werte == {5, 4, 3, 2, 14}:
      karten = karten[1:] + karten[:1]
    return 4, karten
  # Three of a Kind
  if 3 in anz2karten:
    return 3, anz2karten[3]+anz2karten[1]
  # Two Pair
  if 2 in anz2karten and len(anz2karten[2]) == 4:
    return 2, anz2karten[2]+anz2karten[1]
  # one Pair
  if 2 in anz2karten:
    return 1, anz2karten[2]+anz2karten[1]
  # High Card
  return 0, karten


deck = Kartendeck()
pocket = deck.gib(2)
board = deck.gib(5)

print(pocket)
print(board)
bester_rang, beste_karten = rang_ermitteln(board, pocket)
print(bester_rang, beste_karten)
print(score_berechnen(bester_rang, beste_karten))
