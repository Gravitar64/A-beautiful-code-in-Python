# 4-gewinnt
import random as rnd
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
  return spalte > -1 and spalte < SPALTEN and zeile > -1 and zeile < ZEILEN


def quadGültig(pos, vec):
  pos = (pos[0]+vec[0]*3, pos[1]+vec[1]*3)
  return posGültig(pos)


def quadPositionen(pos, vec):
  positionen = [pos]
  for i in range(3):
    pos = (pos[0]+vec[0], pos[1]+vec[1])
    positionen.append(pos)
  return positionen


def findeQuads():
  quads = []
  zähler = 0
  for i in range(ZELLEN):
    pos = i2pos(i)
    for richtung in RICHTUNGEN:
      if quadGültig(pos, richtung):
        quads.append([True, True, 0, 0])
        for position in quadPositionen(pos, richtung):
          pos_zu_quadindex[position].append(zähler)
        zähler += 1
  return quads


def i2pos(i):
  spalte = i % SPALTEN
  zeile = i // SPALTEN
  return (spalte, zeile)


def finde_tiefste_stelle(spalte):
  for zeile in range(ZEILEN):
    if (spalte, zeile) in board:
      return zeile-1
  return zeile


def liefer_gültige_spalten():
  gültige_spalten = []
  for spalte in range(SPALTEN):
    gültige_spalten.append(spalte) if (spalte, 0) not in board else None
  return gültige_spalten


def feld_ändern(player, pos, setzen):
  if setzen:
    board[pos] = 1 if player else 2
  else:
    del board[pos]

  for index in pos_zu_quadindex[pos]:
    quad = quads[index]
    anz_index = 2 if player else 3
    if setzen and not quad[0] and not quad[1]:
      continue
    if setzen:
      quad[anz_index] += 1
    else:
      quad[anz_index] -= 1

  anz1 = quad[2]
  anz2 = quad[3]

  if anz1 > 0 and anz2 > 0:
    quad[0] = quad[1] = False
  if anz1 >= 0 and anz2 == 0:
    quad[0] = True
    quad[1] = False
  if anz2 >= 0 and anz1 == 0:
    quad[1] = True
    quad[0] = False


def gültigeZüge():
  gültig = []
  for spalte in liefer_gültige_spalten():
    zeile = finde_tiefste_stelle(spalte)
    gültig.append((spalte, zeile))
  return gültig


def print_board():
  for i in range(ZELLEN):
    print(board[i2pos(i)], end=' ') if i2pos(
        i) in board else print('_', end=' ')
    print() if (i+1) % SPALTEN == 0 else 0


def bewertung():
  score = 0
  for pos in board:
    for index in pos_zu_quadindex[pos]:
      quad = quads[index]
      if not quad[0] and not quad[1]:
        continue
      if quad[0]:
        score += 1+quad[2]**2
        if quad[2] == 4:
          return 99999
      if quad[1]:
        score -= 1+quad[3]**2
        if quad[3] == 4:
          return -99999
  return score


def bewerteteZüge():
  zugliste = gültigeZüge()
  bewerteteZüge = []
  for pos in zugliste:
    feld_ändern(player, pos, True)
    score = bewertung()
    bewerteteZüge.append([score, pos])
    feld_ändern(player, pos, False)
  return bewerteteZüge


def win():
  for quad in quads:
    if quad[2] == 4 or quad[3] == 4:
      return True


def alphabeta(depth, α, β, player):
  if depth == 0 or win():
    return bewertung()
  if player:
    value = -999999
    for child in gültigeZüge():
      feld_ändern(player, child, True)
      value = max(value, alphabeta(depth-1, α, β, False))
      feld_ändern(player, child, False)
      α = max(α, value)
      if α >= β:
        break  # β cut-off
    return value
  else:
    value = 999999
    for child in gültigeZüge():
      feld_ändern(player, child, True)
      value = min(value, alphabeta(depth-1, α, β, True))
      feld_ändern(player, child, False)
      β = min(β, value)
      if α >= β:
        break  # α cut-off
    return value


quads = findeQuads()
start = time.perf_counter()
player = True

while True:
  zugliste = sorted(bewerteteZüge(), reverse=player)
  for pos in zugliste:
    feld_ändern(player, pos[1], True)
    pos[0] = alphabeta(4, -999999, 999999, not player)
    feld_ändern(player, pos[1], False)

  zugliste.sort(reverse=player)
  best_Zug = zugliste[0][1]
  feld_ändern(player, best_Zug, True)
  print(f'Mein Zug : {best_Zug}')
  if win():
    print(f'Spieler {1 if player else 2} hat gewonnen (Zug: {best_Zug})')
    break
  print_board()
  print('\n'*2)

  player = not player

print(time.perf_counter()-start)
