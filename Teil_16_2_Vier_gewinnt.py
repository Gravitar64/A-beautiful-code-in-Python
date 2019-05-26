from collections import defaultdict
spielfeld = {}  # Key = (spalte, zeile), Value = 'O' oder 'X'

SPALTEN = 7
ZEILEN = 6
ZELLEN = SPALTEN * ZEILEN
RICHTUNGEN = [(-1, -1), (0, -1), (1, -1), (-1, 0),
              (1, 0), (-1, 1), (0, 1), (1, 1)]
pos2quads = defaultdict(list)              


def findeQuads():
  quads = {} # key = index, value = Liste [anz rote, gelbe Steine, koordinaten des quads]
  zähler = 0
  for i in range(ZELLEN):
    spalte, zeile = i % SPALTEN, i // SPALTEN
    for richtung in RICHTUNGEN:
      sp_neu, zeile_neu = spalte + richtung[0]*3, zeile + richtung[1]*3
      if -1 < sp_neu < SPALTEN and -1 < zeile_neu < ZEILEN:
        positionen = set()
        for n in range(4):
          sp_neu = spalte + richtung[0]*n
          zeile_neu = zeile + richtung[1]*n
          positionen.add((sp_neu,zeile_neu))
        redundant = False
        for quad in quads.values():
          if quad[2] == positionen:
            redundant = True
        if not redundant:    
          quads[zähler] = [0,0,positionen]
          for position in positionen:
            pos2quads[position].append(zähler)
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

def zugSetzen(pos, spieler):
  win = False
  spielfeld[pos] = 'O' if spieler else 'X'
  for i in pos2quads[pos]:
    if spieler:
      quads[i][0] += 1
      if quads[i][0] == 4:
        win = True
    else:
      quads[i][1] += 1
      if quads[i][1] == 4:
        win = True 
  return win

def zugLöschen(pos, spieler):
  del spielfeld[pos]
  for i in pos2quads[pos]:
    if spieler:
      quads[i][0] -= 1
    else:
      quads[i][1] -= 1

def bewerten():
  score = 0
  for pos in spielfeld:
    for i in pos2quads[pos]:
      if quads[i][0] > 0 and quads[i][1] > 0: continue
      score += 1+quads[i][0]*10
      score -= 1+quads[i][1]*10
  return score    

def zugliste():
  züge = []
  for spalte in range(SPALTEN):
    if not spalteGültig(spalte): continue
    zeile = findeTiefsteZeile(spalte)
    züge.append((spalte, zeile))
  return züge    


def minimax(tiefe, alpha, beta, spieler, win):
  if win:
    return -99999-tiefe if spieler else 99999+tiefe
  if tiefe == 0 or len(spielfeld) == ZELLEN:
    return bewerten()
  if spieler:
    value = -999999
    for zug in zugliste():
      win = zugSetzen(zug, spieler)
      value = max(value, minimax(tiefe-1, alpha, beta, not spieler, win))
      zugLöschen(zug, spieler)
      alpha = max(alpha, value)
      if alpha >= beta:
        break
  else:
    value = 999999
    for zug in zugliste():
      win = zugSetzen(zug, spieler)
      value = min(value, minimax(tiefe-1, alpha, beta, not spieler, win))
      zugLöschen(zug, spieler)
      beta = min(beta, value)
      if alpha >= beta:
        break
  return value

def computer(spieler):
  bewertete_Züge = []
  for zug in zugliste():
    win = zugSetzen(zug, spieler)
    value = minimax(6,-999999, 999999, not spieler, win)
    bewertete_Züge.append((value, zug))
    zugLöschen(zug, spieler)
  bewertete_Züge.sort(reverse=spieler)
  win = zugSetzen(bewertete_Züge[0][1], spieler)
  print(bewertete_Züge)
  print(f'Spieler {1 if spieler else 2} setzt {bewertete_Züge[0][1]}')
  return win  

def human(spieler):
  while True:
    spalte = int(input('Ihr Zug (Spalte 0-6): '))
    if spalteGültig(spalte):
      break
  zeile = findeTiefsteZeile(spalte)
  win = zugSetzen((spalte,zeile), spieler)
  return win

quads = findeQuads()
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
