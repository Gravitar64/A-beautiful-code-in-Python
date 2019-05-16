# 4-gewinnt
from collections import defaultdict
import time

board = {}
RICHTUNGEN = [(-1, -1), (0, -1), (1, -1), (-1, 0),
              (1, 0), (-1, 1), (0, 1), (1, 1)]
SPALTEN = 7
ZEILEN = 6
ZELLEN = SPALTEN * ZEILEN
pos_zu_quadindex = defaultdict(list)


def posGültig(pos):
  spalte, zeile = pos
  return -1 < spalte < SPALTEN and -1 < zeile < ZEILEN


def quadGültig(pos, vec):
  return posGültig((pos[0]+vec[0]*3, pos[1]+vec[1]*3))


def quadPositionen(pos, vec):
  positionen = {pos}
  for i in range(3):
    pos = (pos[0]+vec[0], pos[1]+vec[1])
    positionen.add(pos)
  return positionen


def findeQuads():
  quads = {}
  zähler = 0
  for i in range(ZELLEN):
    pos = i2pos(i)
    for richtung in RICHTUNGEN:
      if not quadGültig(pos, richtung): continue
      quads[zähler] = [0, 0, quadPositionen(pos, richtung)]
      for position in quadPositionen(pos, richtung):
        pos_zu_quadindex[position].append(zähler)
      zähler += 1
  return quads


def i2pos(i):
  return (i % SPALTEN, i // SPALTEN)


def lieferZeile(spalte):
  for zeile in reversed(range(ZEILEN)):
    if (spalte, zeile) not in board:
      return zeile


def lieferSpalten():
  gültige_spalten = []
  for spalte in range(SPALTEN):
    gültige_spalten.append(spalte) if (spalte, 0) not in board else None
  return gültige_spalten


def feld_ändern(player, pos, setzen):
  win = False
  if setzen:
    board[pos] = 'O' if player else 'X'
  else:
    del board[pos]

  for index in pos_zu_quadindex[pos]:
    quad = quads[index]
    if setzen :
      quad[player] += 1
      if quad[player] == 4:
        win = True
    else:
      quad[player] -= 1
  return win

def gültigeZüge():
  gültig = []
  for spalte in lieferSpalten():
    zeile = lieferZeile(spalte)
    gültig.append((spalte, zeile))
  return gültig


def printBoard():
  for i in range(ZELLEN):
    print(board[i2pos(i)], end=' ') if i2pos(
        i) in board else print('.', end=' ')
    print() if (i+1) % SPALTEN == 0 else None


def bewertung():
  score = 0
  for pos in board:
    for index in pos_zu_quadindex[pos]:
      anz1, anz2, _ = quads[index]
      if anz1 > 0 and anz2 >0:
        continue
      score += 1+anz2*10
      score -= 1+anz1*10
  return score


def bewerteteZüge(player):
  zugliste = gültigeZüge()
  bewerteteZüge = []
  for pos in zugliste:
    feld_ändern(player, pos, True)
    score = bewertung()
    bewerteteZüge.append([score, pos])
    feld_ändern(player, pos, False)
  return bewerteteZüge


def alphabeta(depth, α, β, player, win):
  if win:
    return -99999 if player else 99999
  if depth == 0 or len(board) == ZELLEN:
    return bewertung()
  if player:
    value = -999999
    for child in gültigeZüge():
      win = feld_ändern(player, child, True)
      value = max(value, alphabeta(depth-1, α, β, False, win))
      feld_ändern(player, child, False)
      α = max(α, value)
      if α >= β:
        break  # β cut-off
    return value
  else:
    value = 999999
    for child in gültigeZüge():
      win = feld_ändern(player, child, True)
      value = min(value, alphabeta(depth-1, α, β, True, win))
      feld_ändern(player, child, False)
      β = min(β, value)
      if α >= β:
        break  # α cut-off
    return value

def löscheQuads():
  to_del = []
  for index, values in quads.items():
    if values[0] == 0 or values[1] == 0: continue
    to_del.append(index)
    for position in values[2]:
      pos_zu_quadindex[position].remove(index)
  for index in to_del:
    del quads[index]      

def computer():
  zugliste = sorted(bewerteteZüge(player), reverse=player)
  for pos in zugliste:
    win = feld_ändern(player, pos[1], True)
    pos[0] = alphabeta(6, -999999, 999999, not player, win)
    feld_ändern(player, pos[1], False)
  zugliste.sort(reverse=player)
  best_Zug = zugliste[0][1]
  win=feld_ändern(player, best_Zug, True)
  print(zugliste)
  print(f'Spieler {1 if player else 2}: {best_Zug}')
  return win

def human():
  spalte = int(input('Ihr Zug (0-6): '))
  zeile = lieferZeile(spalte)
  win = feld_ändern(player, (spalte, zeile), True)
  return win

def spielende(win):
  if win:
    print(f'Spieler {1 if player else 2} hat gewonnen')
    return True
  if len(board) == ZELLEN:
    print('UNENTSCHIEDEN!!!!')
    return True

quads = findeQuads()
start = time.perf_counter()

player = True
while True:
  if player:
    win = computer()
  else:
    win = computer()  
  printBoard()
  print('\n')
  if spielende(win):
    break
  löscheQuads()
  player = not player

print(time.perf_counter()-start)
