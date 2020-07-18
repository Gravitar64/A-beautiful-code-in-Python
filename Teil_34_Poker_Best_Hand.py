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
  def __init__(self, name) -> None:
    self.name = name
    self.pocket = []
    self.rang = ''
    self.score = 0
    self.beste_karten = []


def rang_ermitteln(board, pocket):

  def rückgabewerte(rang, karten):
    return rang, int(str(rang)+''.join([f'{k.wert:02d}' for k in karten])), karten

  def score_ermitteln(karten5, flush, straight):
    # Royal Flush oder Straight Flush
    if flush and straight:
      if max(werte) == 14 and min(werte) == 10:
        return rückgabewerte(9, karten5)
      karten = karten5[1:] + \
          karten5[:1] if werte == {14, 2, 3, 4, 5} else karten5
      return rückgabewerte(8, karten)
    # Four of a Kind
    if 4 in anz2karten:
      return rückgabewerte(7, anz2karten[4] + anz2karten[1])
    # Full House
    if 3 in anz2karten and 2 in anz2karten:
      return rückgabewerte(6, anz2karten[3] + anz2karten[2])
    if flush:
      return rückgabewerte(5, karten5)
    if straight:
      karten = karten5[1:] + \
          karten5[:1] if werte == {14, 2, 3, 4, 5} else karten5
      return rückgabewerte(4, karten)
    # Three of a Kind
    if 3 in anz2karten:
      return rückgabewerte(3, anz2karten[3] + anz2karten[1])
    # Two Pair
    if 2 in anz2karten and len(anz2karten[2]) == 4:
      return rückgabewerte(2, anz2karten[2] + anz2karten[1])
    # One Pair
    if 2 in anz2karten:
      return rückgabewerte(1, anz2karten[2] + anz2karten[1])
    # High Card
    return rückgabewerte(0, karten5)

  karten7 = sorted(board+pocket, key=lambda k: k.wert, reverse=True)
  best_score = best_rang = best_karten = 0
  for karten5 in combinations(karten7, 5):
    farben = {k.farbe for k in karten5}
    flush = len(farben) == 1
    werte = {k.wert for k in karten5}
    straight = len(werte) == 5 and max(werte) - min(werte) == 4

    wert2karten = defaultdict(list)
    anz2karten = defaultdict(list)
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


def string2karten(zeichenkette):
  str2wert = dict(t=10, j=11, q=12, k=13, a=14)
  str2farbe = dict(s='♤', h='♡', c='♧', d='♢')
  karten = []
  zeichenkette = zeichenkette.lower()
  liste_kartenbez = zeichenkette.split()
  for wert, farbe in liste_kartenbez:
    wert = str2wert[wert] if wert in str2wert else int(wert)
    farbe = str2farbe[farbe]
    karten.append(Karte(wert, farbe))
  return karten


# hier startet das Programm
rnd.seed()
RÄNGE = {9: 'Royal Flush', 8: 'Straight Flush', 7: 'Four of a Kind', 6: 'Full House',
         5: 'Flush', 4: 'Straight', 3: 'Three of a Kind', 2: 'Two Pair', 1: 'One Pair', 0: 'High Card'}

deck = Kartendeck()
#spieler_namen = 'Sandra Naujoks,Natalie Hof,Katja Thater,Pius Heinz,Fedor Holz,Hossein Ensan'.split(',')
spieler_namen = 'Fukutu,Infante,Le Chiffre,James Bond'.split(',')

players = [Spieler(name) for name in spieler_namen]
#board = deck.gib(5)
board = string2karten("ah 8s 6s 4s as")
players[0].pocket = string2karten("ks qs")
players[1].pocket = string2karten("8h 8c")
players[2].pocket = string2karten("ac 6h")
players[3].pocket = string2karten("7s 5s")
best_score = 0
print()
print('Board: ', board)
print()
for player in players:
  #player.pocket= deck.gib(2)
  player.rang, player.score, player.beste_karten = rang_ermitteln(
      board, player.pocket)
  print(
      f'{player.pocket}, {player.name:<20}{RÄNGE[player.rang]:<15} {player.beste_karten}')
  if player.score == best_score:
    best_player += [player]
  if player.score > best_score:
    best_score = player.score
    best_player = [player]
print()
for player in best_player:
  print(
      f'Sieger = {player.name} mit {player.beste_karten} = {RÄNGE[player.rang]}')
print()
