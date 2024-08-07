from collections import defaultdict
spielfeld = {}  # Key = (spalte, zeile), Value = 'O' oder 'X'

SPALTEN = 7
ZEILEN = 6
ZELLEN = SPALTEN * ZEILEN
RICHTUNGEN = [(-1, -1), (0, -1), (1, -1), (-1, 0),
              (1, 0), (-1, 1), (0, 1), (1, 1)]
pos2Index = defaultdict(list)

def quadPositionen(pos, richtung):
  positionen = set()
  sp, ze = pos
  rsp, rze = richtung
  neue_sp, neue_ze = sp + rsp*3, ze+rze*3
  if neue_sp < 0 or neue_sp >= SPALTEN or neue_ze < 0 or neue_ze >= ZEILEN:
    return False
  for i in range(4):
    positionen.add((sp+rsp*i, ze+rze*i))
  return positionen

def quadsErmitteln():
  zähler = 0
  quads = {}
  bekannte_positionen = set()
  for i in range(ZELLEN):
    for richtung in RICHTUNGEN:
      pos = (i % SPALTEN, i // SPALTEN)
      positionen = quadPositionen(pos, richtung)
      if not positionen or positionen in bekannte_positionen: continue
      quads[zähler] = [0,0] # Anzahl der gelben[0], roten[1] Steine im Quad
      for position in positionen:
        pos2Index[position].append(zähler)
      bekannte_positionen.add(frozenset(positionen))
      zähler += 1  
  return quads

def findeTiefsteZeile(spalte):
  for zeile in reversed(range(ZEILEN)):
    if (spalte, zeile) not in spielfeld:
      return zeile


def spalteGültig(spalte):
  if (spalte, 0) in spielfeld:
    return False
  if 0 <= spalte < 7:
    return True


def printSpielfeld():
  for i in range(ZELLEN):
    if i % SPALTEN == 0:
      print()
    pos = (i % SPALTEN, i // SPALTEN)
    if pos in spielfeld:
      print(spielfeld[pos], end=' ')
    else:
      print('.', end=' ')
  print()

def steinSetzen(pos, spieler):
  win = False
  spielfeld[pos] = 'O' if spieler else 'X'
  for i in pos2Index[pos]:
    quads[i][spieler] +=1
    if quads[i][spieler] == 4:
      win = True
  return win

def steinLöschen(pos, spieler):
  del spielfeld[pos]
  for i in pos2Index[pos]:
    quads[i][spieler] -=1

def bewerten():
  score = 0
  for pos in spielfeld:
    for i in pos2Index[pos]:
      gelbe, rote = quads[i]
      if gelbe > 0 and rote > 0: continue
      score += rote*10
      score -= gelbe*10
  return score

def zugliste():
  züge = []
  for spalte in range(SPALTEN):
    if not spalteGültig(spalte): continue
    zeile = findeTiefsteZeile(spalte)
    züge.append((spalte,zeile))
  return züge  

def human(spieler):
  while True:
    spalte = int(input('Ihr Zug (Spalte 0-6): '))
    if spalteGültig(spalte):
      break
  zeile = findeTiefsteZeile(spalte)
  win = steinSetzen((spalte,zeile), spieler)
  return win

def computer(spieler):
  bewertete_züge = []
  for zug in zugliste():
    win = steinSetzen(zug, spieler)
    score = minimax(7, -999999, 999999, spieler, win)
    steinLöschen(zug, spieler)
    bewertete_züge.append((score,zug))
  bewertete_züge.sort(reverse=spieler)
  score, bester_zug = bewertete_züge[0]
  win = steinSetzen(bester_zug, spieler)
  print(bewertete_züge)
  print(f'Spieler {1 if spieler else 2} setzt {bester_zug} mit der Bewertung {score}')
  return win  

def minimax(tiefe, alpha, beta, spieler, win):
  if win:
    return 99999+tiefe if spieler else -99999-tiefe
  if tiefe == 0 or len(spielfeld) == ZELLEN:
    return bewerten()
  spieler = not spieler
  value = -999999 if spieler else 999999
  for zug in zugliste():
    win = steinSetzen(zug, spieler)
    score = minimax(tiefe-1, alpha, beta, spieler, win)
    steinLöschen(zug, spieler)
    if spieler:
      value = max(value, score)
      alpha = max(value, alpha)  
    else:
      value = min(value, score)
      beta = min(value, beta)
    if alpha >= beta:
      break
  return value    

quads = quadsErmitteln()



spieler = True
while True:
  printSpielfeld()
  if spieler:
    win = human(spieler)
  else:
    win = computer(spieler)  
  if win:
    printSpielfeld()
    print('GEWONNEN!!!')
    break
  spieler = not spieler
