import random as rnd
from collections import Counter, defaultdict
from itertools import combinations
import time
import unittest as ut
rnd.seed()


SUITS = '♤ ♡ ♧ ♢'.split()
RÄNGE = ['High Card', 'Pair', 'Two Pairs', 'Three of a kind', 'Straight', 'Flush', 'Full House',
         'Four of a kind', 'Straight Flush', 'Royal Flush']


class Karte:
  def __init__(self, wert, farbe):
    self.wert = wert
    self.farbe = farbe
    self.name = self._name_ermitteln()

  def _name_ermitteln(self):
    k_namen = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    return str(self.wert) + self.farbe if self.wert < 10 else k_namen[self.wert] + self.farbe

class Kartendeck:
  def __init__(self):
    self.karten = self._neu_gemischt()

  def _neu_gemischt(self):
    karten = [Karte(w, f) for f in SUITS for w in range(2, 15)]
    rnd.shuffle(karten)
    return karten

  def geben(self, anz):
    return [self.karten.pop() for _ in range(anz)]


def zeige_karten(karten):
  text = ''
  for k in karten:
    text += k.name + ' '
  return text


def rückgabewerte(rang, karten):
  return rang, int(str(rang)+''.join([f'{k.wert:02d}' for k in karten])), karten


def rang_ermitteln(board, pocket):

  def score_ermitteln(karten5):

    def is_flush():
      if len(farben) == 1:
        ränge[5] = karten5
        return True
    def is_straight():  
      if len(werte) == 5 and max(werte) - min(werte) == 4:
        ränge[4] = karten5
        return True
      if werte == {14, 2, 3, 4, 5}:
        ränge[4] = karten5[1:]+karten5[0:1]
        return True
    def is_royal_flush():
      if ränge[5] and ränge[4] and max(werte) == 14 and min(werte) == 10:
        ränge[9] = karten5
        return True
    def is_straight_flush():
      if ränge[5] and ränge[4]:
        ränge[8] = karten5
        return True
    def is_four_of_a_kind():
      if 4 in anzahl:
        ränge[7] = karten5
        return True
    def is_full_house():
      if [3,2] in anzahl:
        ränge[6] = karten5
        return True
    def is_three_of_a_kind():
      if werte_anz.most_common(1)[0][1] == 3:
        ränge[3] = karten5
        return True
    def is_two_pairs():
      anz = []
      for w,a in werte_anz.most_common(2):
        anz.append(a)
      if anz == [2,2]:
        ränge[2] = karten5
    def is_one_pair():
      if werte_anz.most_common(1)[0][1] == 2:
        ränge[1] = karten5
        return True


    is_flush()
    is_straight()
    if is_royal_flush():
      return rückgabewerte(9, ränge[9])
    if is_straight_flush():
      return rückgabewerte(8, ränge[8])
    if is_four_of_a_kind():
      return rückgabewerte(7, ränge[7])
    if is_full_house():
      return rückgabewerte(6, ränge[6])
    if ränge[5]:
      return rückgabewerte(5, ränge[5])
    if ränge[4]:
      return rückgabewerte(4, ränge[4])
    if is_three_of_a_kind(): 
      return rückgabewerte(3, ränge[3])
    if is_two_pairs(): 
      return rückgabewerte(2, ränge[2])
    if is_one_pair(): return rückgabewerte(1, ränge[1])
    return rückgabewerte(0, karten5)

    

  karten7 = sorted(board+pocket, key=lambda k: k.wert, reverse=True)
  mögliche_karten = combinations(karten7, 5)
  best_score = 0
  for karten5 in mögliche_karten:
    werte = {k.wert for k in karten5}
    werte_anz = Counter(karten5)
    anzahl = [a for a in werte_anz.values()]
    farben = {k.farbe for k in karten5}
    ränge = {key: False for key in range(10)}
    rang, score, karten = score_ermitteln(karten5)
    if score > best_score:
      best_score = score
      best_karten = karten
      best_rang = rang
  return best_rang, best_score, best_karten


def rang_ermitteln2(karten):

  def is_royal_flush():
    if not ränge[4] or not ränge[5] or ränge[5][0].wert != 14 or ränge[5][4].wert != 10:
      return
    ränge[9] = ränge[5]
    return True

  def is_straight_flush():
    if not ränge[4] or not ränge[5]:
      return
    flush_farbe = ränge[5][0].farbe
    if len(farben_werte[flush_farbe]) < 5: return
    best5 = []
    for i in reversed(range(1, 15)):
      if i in werte:
        for k in werte[i]:
          if k.farbe == flush_farbe:
            best5.append(k)
            break
        else:
          best5 = []
        if len(best5) == 5:
          ränge[8] = best5
          return True
      else:
        best5 = []

  def is_flush():
    for farbe in 'shdc':
      if len(farben[farbe]) > 4:
        ränge[5] = farben[farbe][:5]
        return True

  def is_straight():
    if len(werte) < 5:
      return
    best5 = []
    for w in werte:
      if not best5:
        best5 = werte[w][0]
        last_w = w
      else:
        if w - last_w == 1:
          best5.appemd(werte[w][0])
          last_w = w
          if len(best5) == 5:
            ränge[4] = best5
            return True
        else:
          best5 = []

    for i in reversed(range(1, 15)):
      if i in werte:
        best5.append(werte[i][0])
        if len(best5) == 5:
          ränge[4] = best5
          return True
      else:
        best5 = []

  def is_four_of_a_kind():
    for karten in werte.values():
      if len(karten) != 4:
        continue
      best5 = karten
      for k in karten7:
        if k.wert == best5[0].wert:
          continue
        best5.append(k)
        ränge[7] = best5
        return True

  def is_full_house():
    best5 =[]
    for karten in werte.values():
      if len(karten) != 3:
        continue
      best5 = karten
      break
    if not best5: return
    for karten in werte.values():
      if len(karten) < 2 or karten[0].wert == best5[0].wert:
        continue
      best5 += karten[:2]
      ränge[6] = best5
      return True

  def is_three_of_a_kind():
    best5 =[]
    for karten in werte.values():
      if len(karten) != 3: continue
      best5.extend(karten)
      break
    if not best5: return
    for k in karten7:
      if k.wert == best5[0].wert: continue
      best5.append(k)
      if len(best5) < 5: continue
      ränge[3] = best5
      return True 
  
  def is_two_pairs():
    best5 =[]
    for karten in werte.values():
      if len(karten) != 2: continue
      best5.extend(karten)
      if len(best5) == 4: break
    if len(best5) != 4 : return
    for k in karten7:
      if k.wert == best5[0].wert or k.wert == best5[2].wert: continue
      best5.append(k)
      if len(best5) == 5: 
        ränge[2] = best5
        return True
      

  def is_one_pair():
    best5 = []
    for karten in werte.values():
      if len(karten) != 2: continue
      best5.extend(karten)
      break
    if len(best5) != 2 : return
    for k in karten7:
      if k.wert == best5[0].wert: continue
      best5.append(k)
      if len(best5) == 5: 
        ränge[1] = best5
        return True            

  ränge = defaultdict(lambda: False)
  werte = defaultdict(list)
  farben = defaultdict(list)
  farben_werte = defaultdict(list)
  for w,s in karten:
    werte[w].append((w,s))
    farben[s].append((w,s))
    farben_werte[s].append(w)
    if w == 14: farben_werte[s].append(1)
  if 14 in werte:
    werte[1].append(werte[14][0])
  
  is_flush()
  is_straight()
  if is_royal_flush():
    return rückgabewerte(9, ränge[9])
  if is_straight_flush():
    return rückgabewerte(8, ränge[8])
  if is_four_of_a_kind():
    return rückgabewerte(7, ränge[7])
  if is_full_house():
    return rückgabewerte(6, ränge[6])
  if ränge[5]:
    return rückgabewerte(5, ränge[5])
  if ränge[4]:
    return rückgabewerte(4, ränge[4])
  if is_three_of_a_kind(): 
    return rückgabewerte(3, ränge[3])
  if is_two_pairs(): 
    return rückgabewerte(2, ränge[2])
  if is_one_pair():
    return rückgabewerte(1, ränge[1]) 
  return rückgabewerte(0, karten7[:5])

def deck_erstellen():
  deck = []
  for w in range(2,15):
    for s in 'shdc':
      deck.append((w,s))
  rnd.shuffle(deck)
  return deck

def geben(deck, anz):
  karten = []
  for i in range(anz):      
    karten.append(deck.pop())
  return karten

# time_start = time.perf_counter()
# for _ in range(100_000):
#   deck = Kartendeck()
#   pocket = deck.geben(2)
#   board = deck.geben(5)
#   rang, score, karten = rang_ermitteln2(board, pocket)
# print(time.perf_counter()- time_start)

deck = deck_erstellen()
pocket = geben(deck,2)
board = geben(deck,5)
karten = sorted(pocket + board, key=lambda x: x[0], reverse=True)
print(karten)
werte = sorted(list({w for w,s in karten}),reverse = True)
binary = [a-b==1 for a,b in zip(werte,werte[1:])]
print(binary)