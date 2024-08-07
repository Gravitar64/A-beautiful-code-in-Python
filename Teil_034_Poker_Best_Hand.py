import random as rnd
from itertools import combinations
from collections import defaultdict 

class Karte(object):
  def __init__(self, wert, farbe) -> None:
    self.wert = wert
    self.farbe = farbe

  def __repr__(self):
    karten_namen = {10:'T', 11:'J', 12:'Q', 13:'K', 14:'A'}
    name = str(self.wert) if self.wert < 10 else karten_namen[self.wert]
    return name + self.farbe  

class Kartendeck(object):
  def __init__(self):
    self.karten = self._neu_gemischt()

  def _neu_gemischt(self):
    karten = [Karte(w,f) for f in '♤♡♧♢' for w in range(2,15)]
    rnd.shuffle(karten)
    return karten

  def gib(self, anz):
    return [self.karten.pop() for _ in range(anz)]


def beste_5_aus_7_ermitteln(pocket, board):
  karten7 = pocket + board
  karten7 = sorted(karten7, key=lambda k:k.wert, reverse = True)
  bester_rang = -1
  for karten5 in combinations(karten7,5):
    rang,karten = bewerte5(karten5)
    if rang > bester_rang:
      bester_rang = rang
      beste_karten = karten
  return bester_rang, beste_karten    
  

def bewerte5(karten5):
  wert2karten = defaultdict(list)
  anz2karten = defaultdict(list)
  for k in karten5:
    wert2karten[k.wert].append(k)
  for v in wert2karten.values():
    anz2karten[len(v)] += v
  werte = {k.wert for k in karten5}  
  straight = (len(werte) == 5 and max(werte) - min(werte) == 4) or \
             werte == {5,4,3,2,14}
  farben = {k.farbe for k in karten5}
  flush = len(farben) == 1            
  
  #Royal Flush
  if straight and flush and min(werte) == 10:
    return 9, karten5
  #Straight Flush
  if straight and flush:
    if werte == {5,4,3,2,14}:
      karten5 = karten5[1:]+karten5[:1]
    return 8, karten5  
  #Four of a Kind
  if 4 in anz2karten:
    return 7, anz2karten[4] + anz2karten[1]  
  #Full House
  if 3 in anz2karten and 2 in anz2karten:
    return 6, anz2karten[3] + anz2karten[2]  
  #Flush
  if flush:
    return 5, karten5
  #Straight
  if straight:
    if werte == {5,4,3,2,14}:
      karten5 = karten5[1:]+karten5[:1]
    return 4, karten5
  #Tree of a Kind
  if 3 in anz2karten:
    return 3, anz2karten[3] + anz2karten[1]  
  #Two Pair
  if 2 in anz2karten and len(anz2karten[2]) == 4:
    return 2, anz2karten[2] + anz2karten[1]  
  #One Pair
  if 2 in anz2karten:
    return 1, anz2karten[2] + anz2karten[1]  
  #High Card
  return 0, karten5

hand_stat = defaultdict(int)
loops = 100_000
for _ in range(loops):
  deck = Kartendeck()
  pocket = deck.gib(2)
  board = deck.gib(5)
  rang, karten = beste_5_aus_7_ermitteln(pocket,board)
  hand_stat[rang] += 1
for i in reversed(range(10)):
  print(f'Rang {i} {hand_stat[i]:8d} = {hand_stat[i]/loops*100:8.3f}%')