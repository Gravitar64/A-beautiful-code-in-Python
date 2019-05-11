import time

board = {}
spalten = []
zeilen = []
blöcke = []
freie_felder = set()


def i2pos(i):
  spalte = i % 9
  zeile = i // 9
  block = zeile // 3 * 3 + spalte // 3
  return (spalte, zeile, block)


def feld_setzen(pos, zahl):
  spalte, zeile, block = pos
  spalten[spalte].remove(zahl)
  zeilen[zeile].remove(zahl)
  blöcke[block].remove(zahl)
  freie_felder.remove(pos)
  board[pos] = zahl


def feld_löschen(pos, zahl):
  spalte, zeile, block = pos
  spalten[spalte].add(zahl)
  zeilen[zeile].add(zahl)
  blöcke[block].add(zahl)
  freie_felder.add(pos)
  board[pos] = 0


def leeres_sudoku_erstellen():
  for i in range(9):
    spalten.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
    zeilen.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
    blöcke.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
  for i in range(81):
    freie_felder.add(i2pos(i))


def sudoku_einlesen(aufgabe):
  for i, buchstabe in enumerate(aufgabe):
    if buchstabe in ('.', '0'):
      board[i2pos(i)] = 0
    else:
      feld_setzen(i2pos(i), int(buchstabe))


def bestes_feld():
  beste_bisherige_anzahl = 9
  for pos in freie_felder:
    spalte, zeile, block = pos
    kandidaten = spalten[spalte] & zeilen[zeile] & blöcke[block]
    anz_kandidaten = len(kandidaten)
    if anz_kandidaten < 2:
      return (pos, kandidaten)
    if anz_kandidaten <= beste_bisherige_anzahl:
      best_feld = (pos, kandidaten)
      beste_bisherige_anzahl = anz_kandidaten
  return best_feld


def löse():
  if not freie_felder:
    return True
  pos, kandidaten = bestes_feld()
  kandidaten = sorted(kandidaten)
  for kandidat in kandidaten:
    feld_setzen(pos, kandidat)
    if löse():
      return True
    feld_löschen(pos, kandidat)


def print_board():
  for i in range(81):
    pos = i2pos(i)
    print(board[pos], end=' ')
    if (i+1) % 9 == 0:
      print()


start = time.perf_counter()
leeres_sudoku_erstellen()
sudoku_einlesen(
    '5......1....4..2...8.2......2....6......3..7.....1....1.3....5....6..4..7........')
löse()
print(time.perf_counter()-start)
print_board()
