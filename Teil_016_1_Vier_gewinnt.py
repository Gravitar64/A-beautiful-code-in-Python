spielfeld = {}  # Key = (spalte, zeile), Value = 'O' oder 'X'

SPALTEN = 7
ZEILEN = 6
ZELLEN = SPALTEN * ZEILEN
RICHTUNGEN = [(-1, -1), (0, -1), (1, -1), (-1, 0),
              (1, 0), (-1, 1), (0, 1), (1, 1)]


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

def gewonnen(spieler):
  stein = 'O' if spieler else 'X'
  for pos in spielfeld:
    for richtung in RICHTUNGEN:
      vier_in_einer_reihe = True
      for i in range(4):
        spalte, zeile = pos
        delta_spalte, delta_zeile = richtung
        p1 = (spalte + delta_spalte*i, zeile + delta_zeile*i)
        if p1 in spielfeld and spielfeld[p1] == stein: continue
        vier_in_einer_reihe = False
        break  
      if vier_in_einer_reihe:
        return True

spieler = True
while True:
  printSpielfeld()
  while True:
    spalte = int(input('Ihr Zug (Spalte 0-6): '))
    if spalteGültig(spalte):
      break
  zeile = findeTiefsteZeile(spalte)
  spielfeld[(spalte, zeile)] = 'O' if spieler else 'X'
  if gewonnen(spieler):
    printSpielfeld()
    print('GEWONNEN!!!')
    break
  spieler = not spieler
