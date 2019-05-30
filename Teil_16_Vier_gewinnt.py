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


def quadPositionen(pos, vec):
  positionen = set()
  sp, ze = pos
  rsp, rze = vec
  neue_sp, neue_ze = sp + rsp*3, ze+rze*3
  if neue_sp < 0 or neue_sp >= SPALTEN or neue_ze < 0 or neue_ze >= ZEILEN:
    return False
  for i in range(4):
    positionen.add((sp+rsp*i, ze+rze*i))
  return positionen


def findeQuads():
  zähler = 0
  quads = {}
  bekannte_positionen = set()
  for i in range(ZELLEN):
    for richtung in RICHTUNGEN:
      positionen = quadPositionen(i2pos(i), richtung)
      if not positionen or positionen in bekannte_positionen:
        continue
      quads[zähler] = [0, 0, positionen]  # Anzahl der gelben[0], roten[1] Steine im Quad
      for position in positionen:
        pos_zu_quadindex[position].append(zähler)
      bekannte_positionen.add(frozenset(positionen))
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


def SteinSetzen(player, pos):
  win = False
  board[pos] = 'O' if player else 'X'
  for index in pos_zu_quadindex[pos]:
    quad = quads[index]
    quad[player] += 1
    if quad[player] == 4:
      win = True
  return win

def SteinLöschen(player, pos):
  del board[pos]
  for index in pos_zu_quadindex[pos]:
    quads[index][player] -= 1
  

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
      gelbe, rote, _ = quads[index]
      if gelbe > 0 and rote > 0:
        continue
      score += rote*10
      score -= gelbe*10
  return score


def löscheQuads():
  to_del = []
  for index, values in quads.items():
    if values[0] == 0 or values[1] == 0:
      continue
    to_del.append(index)
    for position in values[2]:
      pos_zu_quadindex[position].remove(index)
  for index in to_del:
    del quads[index]


def computer(spieler):
  win = False
  score, bester_zug = minimax(8, -999999, 999999, spieler, win)
  win = SteinSetzen(spieler, bester_zug)
  print(f'Spieler {1 if spieler else 2} setzt {bester_zug} mit der Bewertung {score}')
  return win


def minimax(tiefe, alpha, beta, spieler, win):
  if win:
    score = -99999-tiefe if spieler else 99999+tiefe
    return (score, None)
  if tiefe == 0 or len(board) == ZELLEN:
    return (bewertung(), None)
  value = -999999 if spieler else 999999
  for zug in gültigeZüge():
    win = SteinSetzen(spieler, zug)
    score,_ = minimax(tiefe-1, alpha, beta, not spieler, win)
    SteinLöschen(spieler,zug)
    if spieler:
      if score > value:
        bester_zug = zug
        value = score
        alpha = max(value, alpha)
    else:
      if score < value:
        bester_zug = zug
        value = score
      beta = min(value, beta)
    if alpha >= beta:
      break
  return (value, bester_zug)

def human(player):
  spalte = int(input(f'Ihr Zug {lieferSpalten()}: '))
  zeile = lieferZeile(spalte)
  win = SteinSetzen(player, (spalte, zeile))
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
    win = human(player)
  else:
    win = computer(player)
  printBoard()
  print('\n')
  if spielende(win):
    break
  löscheQuads()
  player = not player

print(time.perf_counter()-start)