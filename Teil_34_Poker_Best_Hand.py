import random as rnd
from collections import defaultdict
from itertools import combinations

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

class Spieler(object):
  def __init__(self,name) -> None:
    self.name = name
    self.pocket = []
    self.rang = ''
    self.score = 0
    self.beste_karten = []
      

def rang_ermitteln(board, pocket):

  def rückgabewerte(rang, karten):
    return rang, int(str(rang)+''.join([f'{k.wert:02d}' for k in karten])), karten

  def score_ermitteln(karten5, flush, straight):
    #Royal Flush oder Straight Flush
    if flush and straight:
      if max(werte) == 14 and min(werte) == 10:
        return rückgabewerte(9, karten5)
      karten = karten5[1:]+karten5[:1] if werte == {14, 2, 3, 4, 5} else karten5
      return rückgabewerte(8, karten)
    #Four of a Kind
    if 4 in anz2karten:
      return rückgabewerte(7, anz2karten[4] + anz2karten[1])
    #Full House
    if 3 in anz2karten and 2 in anz2karten:
      return rückgabewerte(6, anz2karten[3]+anz2karten[2])
    #Flush
    if flush:
      return rückgabewerte(5, karten5)
    #Straight
    if straight:
      karten = karten5[1:]+karten5[:1] if werte == {14, 2, 3, 4, 5} else karten5
      return rückgabewerte(4, karten)
    #Three of a Kind
    if 3 in anz2karten:
      return rückgabewerte(3, anz2karten[3] + anz2karten[1][:2])
    #Two Pair
    if 2 in anz2karten and len(anz2karten[2]) == 4:
      return rückgabewerte(2, anz2karten[2] + anz2karten[1])
    #One Pair
    if 2 in anz2karten:
      return rückgabewerte(1, anz2karten[2] + anz2karten[1])
    #High Card
    return  rückgabewerte(0, karten5)

  karten7 = sorted(board+pocket, key=lambda k: k.wert, reverse=True)
  best_score = best_rang = best_karten = 0
  for karten5 in combinations(karten7, 5):
    farben   = {k.farbe for k in karten5}
    flush    = len(farben) == 1
    werte    = {k.wert for k in karten5}
    straight = len(werte) == 5 and max(werte) - min(werte) == 4
    
    wert2karten = defaultdict(list)
    anz2karten  = defaultdict(list)
    for k in karten5:
      wert2karten[k.wert].append(k)
    for v in wert2karten.values():
      anz2karten[len(v)] += v
    rang, score, karten = score_ermitteln(karten5, flush, straight)
    if score > best_score:
      best_score = score
      best_karten = karten
      best_rang = rang
  return best_rang, best_score, best_karten

#hier startet das Programm
rnd.seed()
RÄNGE = {9:'Royal Flush', 8:'Straight Flush', 7:'Four of a Kind', 6:'Full House',
         5:'Flush', 4:'Straight', 3:'Three of a Kind', 2:'Two Pair', 1:'One Pair', 0:'High Card'}

deck = Kartendeck()
spieler_namen = 'Vanessa Liv Pius Fedor'.split()
players = [Spieler(name) for name in spieler_namen]
board = deck.gib(5)
best_score = 0
print()
print('Board: ',board)
print()
for player in players:
  player.pocket= deck.gib(2)
  player.rang, player.score, player.beste_karten = rang_ermitteln(board, player.pocket)
  print (f'{player.pocket}, {player.name:<10}{RÄNGE[player.rang]}')
  if player.score == best_score:
    best_player += [player]  
  if player.score > best_score:
    best_score = player.score
    best_player = [player]
print()
for player in best_player:
  print(f'Sieger = {player.name} mit {player.beste_karten} = {RÄNGE[player.rang]}')
print()  