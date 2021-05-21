import random as rnd
from collections import defaultdict
import time
rnd.seed()


def deck_erstellen():
  deck = [(w, f) for f in '♤♡♧♢' for w in range(2, 15)]
  rnd.shuffle(deck)
  return deck


def gib(deck, anz):
  return [deck.pop() for _ in range(anz)]


def rückgabewerte(rang, karten):
  return rang, int(str(rang)+''.join([f'{k[0]:02d}' for k in karten])), karten


def zeige(karten):
  ergebnis = ''
  karten_namen = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
  for w, f in karten:
    name = str(w) if w < 10 else karten_namen[w]
    ergebnis += name+f+' '
  return ergebnis




def score_ermitteln(board, pocket):
  
  def finde_kicker(anz_kicker, verbrauchte_werte):
    karten = []
    for k in karten7:  
      if k[0] in verbrauchte_werte: continue
      karten.append(k)
      if len(karten) == anz_kicker:
        return karten
  
  karten7 = sorted(board+pocket, key=lambda k: k[0], reverse=True)
  werte = defaultdict(list)
  farben = defaultdict(list)
  for k in karten7:
    werte[k[0]].append(k)
    farben[k[1]].append(k)
  anz2werte = defaultdict(list)
  for v in werte.values():
    anz2werte[len(v)] += v
  if 14 in werte:
    werte[1] = werte[14]

  flush = flush_farbe = False
  for f, k in farben.items():
    if len(k) > 4:
      flush = True
      flush_farbe = f
      break

  straight = straight_high = False
  c = 0
  for i in range(min(werte), max(werte)+1):
    if i not in werte:
      c = 0
    else:
      c += 1
      if c > 4:
        straight = True
        straight_high = i
        break

  # Royale Flush und Straigth Flush
  if flush and straight:
    flush_werte = {k[0] for k in farben[flush_farbe]}
    if {10, 11, 12, 13, 14}.issubset(flush_werte):
      return rückgabewerte(9, farben[flush_farbe][:5])
    c = 0
    #hier kann kein Straight Flush mit 5,4,3,2,A gefunden werden, da A=1 gesetzt wird und 1 nicht in flush_werte enthalten ist
    for i in reversed(range(min(werte), max(werte)+1)):
      if i not in flush_werte:
        c = 0
      else:
        c += 1
        if c == 5:
          return rückgabewerte(8, [(w, flush_farbe) for w in reversed(range(i, i+5))])
  # Four of a Kind
  if 4 in anz2werte:
    return rückgabewerte(7, anz2werte[4] + finde_kicker(1,{anz2werte[4][0][0]}))
  # Full House
  # könnte in [3] stecken (2 x Drilling), dann den ersten Drilling und vom 2ten Drilling 2 Karten
  if 3 in anz2werte and len(anz2werte[3]) == 6:
    return rückgabewerte(6, anz2werte[3][:5])
  # könnte aber auch aus einem Drilling in [3] und einem Paar in [2] bestehen
  if 3 in anz2werte and 2 in anz2werte:
    return rückgabewerte(6, anz2werte[3][:3]+anz2werte[2][:2])
  if flush:
    return rückgabewerte(5, farben[flush_farbe][:5])
  if straight:
    karten = []
    for i in reversed(range(straight_high-4, straight_high+1)):
      karten.append(werte[i][0])
    return rückgabewerte(4, karten)
  # Three of a Kind
  if 3 in anz2werte:
    return rückgabewerte(3, anz2werte[3][:3]+finde_kicker(2,{anz2werte[3][0][0]}))
  # Two Pair
  if 2 in anz2werte and len(anz2werte[2]) > 3:
    return rückgabewerte(2, anz2werte[2][:4]+finde_kicker(1,{anz2werte[2][0][0], anz2werte[2][2][0]}))
  # One Pair
  if 2 in anz2werte:
    return rückgabewerte(1, anz2werte[2][:2]+finde_kicker(3,{anz2werte[2][0][0]}))
  # High Card
  return rückgabewerte(0, karten7[:5])


time_start = time.perf_counter()
hand_stat = defaultdict(int)
loops = 100_000
for _ in range(loops):
  deck = deck_erstellen()
  pocket = gib(deck, 2)
  board = gib(deck, 5)
  rang, score, karten = score_ermitteln(board, pocket)
  if rang == 8 and karten[0][0] == 5:
    print(zeige(pocket),zeige(board),zeige(karten))
  hand_stat[rang] += 1
for i in reversed(range(10)):
  print(f'Rang {i} {hand_stat[i]:8d} = {hand_stat[i]/loops*100:8.3f}%')
print(f'{time.perf_counter()-time_start:.2f} Sek')
