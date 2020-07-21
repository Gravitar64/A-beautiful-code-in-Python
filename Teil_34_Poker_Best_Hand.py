import random as rnd
from itertools import combinations
from collections import defaultdict
import time


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


def rang_ermitteln(board, pocket):
  karten7 = board + pocket
  karten7 = sorted(karten7, key=lambda k: k.wert, reverse=True)
  best_score = 0
  for karten5 in combinations(karten7, 5):
    score, karten, rang = bewerte(karten5)
    if score > best_score:
      best_score = score
      best_karten = karten
      best_rang = rang
  return best_score, best_karten, best_rang


def score(rang, karten):
  return int(str(rang)+''.join([f'{k.wert:02d}' for k in karten])), karten, rang


def bewerte(karten):
  farben = {k.farbe for k in karten}
  werte = {k.wert for k in karten}
  flush = len(farben) == 1
  straight = len(werte) == 5 and max(werte) - min(werte) == 4
  wert2karten = defaultdict(list)
  anz2karten = defaultdict(list)
  for k in karten:
    wert2karten[k.wert].append(k)
  for value in wert2karten.values():
    anz2karten[len(value)] += value
  # Royale Flush
  if flush and straight and max(werte) == 14:
    return score(9, karten)
  # Straight Flush
  if flush and straight:
    if werte == {5, 4, 3, 2, 14}:
      karten = karten[1:] + karten[:1]
    return score(8, karten)
  # Four of a Kind
  if 4 in anz2karten:
    return score(7, anz2karten[4]+anz2karten[1])
  # Full House
  if 3 in anz2karten and 2 in anz2karten:
    return score(6, anz2karten[3]+anz2karten[2])
  if flush:
    return score(5, karten)
  if straight:
    if werte == {5, 4, 3, 2, 14}:
      karten = karten[1:] + karten[:1]
    return score(4, karten)
  # Three of a Kind
  if 3 in anz2karten:
    return score(3, anz2karten[3]+anz2karten[1])
  # Two Pair
  if 2 in anz2karten and len(anz2karten[2]) == 4:
    return score(2, anz2karten[2]+anz2karten[1])
  # One Pair
  if 2 in anz2karten:
    return score(1, anz2karten[2]+anz2karten[1])
  # High Card
  return score(0, karten)


RANG_NAMEN = {9: 'Royal Flush', 8: 'Straight Flush', 7: 'Four of a Kind', 6: 'Full House', 5: 'Flush',
              4: 'Straight', 3: 'Three of a Kind', 2: 'Two Pair', 1: 'One Pair', 0: 'High Card'}


time_start = time.perf_counter()
rang_anz = defaultdict(int)
loops = 100_000
for _ in range(loops):
  deck = Kartendeck()
  pocket = deck.gib(2)
  board = deck.gib(5)
  best_score, best_karten, rang = rang_ermitteln(board, pocket)
  rang_anz[rang] += 1
for i in reversed(range(10)):
  print(f'{RANG_NAMEN[i]:20} {rang_anz[i]/loops*100:.3f}%')
print(time.perf_counter() - time_start)  
