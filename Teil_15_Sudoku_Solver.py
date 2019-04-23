import time


def i2pos(i):
  """Nimmt eine Zahl zwischen 0 und 80 entgegen und liefert ein Tuple 
  mit (spalte, zeile und quadrant) zurück """
  zeile = i // 9
  spalte = i % 9
  quadrant = zeile//3*3+spalte//3
  return (spalte, zeile, quadrant)


def print_board(nr):
  print(f'Position Nr. {nr}')
  for i in range(81):
    pos = i2pos(i)
    print(board[pos], ' ', end='')
    print() if (i+1) % 9 == 0 else None
  print()


def change_board(pos, zahl, setzen):
  '''für (pos,zahl,setzen) wird auf der pos die 
  zahl gesetzt (setzen = True) oder gelöscht (setzen = False)'''
  spalte, zeile, quadrant = pos
  if setzen:
    spalten[spalte].remove(zahl)
    zeilen[zeile].remove(zahl)
    quadrate[quadrant].remove(zahl)
    freie_stellen.remove(pos)
    board[pos] = zahl
  else:
    spalten[spalte].add(zahl)
    zeilen[zeile].add(zahl)
    quadrate[quadrant].add(zahl)
    freie_stellen.add(pos)


def bestes_Feld():
  '''liefert ein Tuple mit (Position, Liste der möglichen Einträge) von dem Feld zurück, 
  dass die geringste Anzahl an möglichen Einträgen enthält'''
  best = 9
  for pos in freie_stellen:
    spalte, zeile, quadrant = pos
    möglichkeiten = spalten[spalte] & zeilen[zeile] & quadrate[quadrant]
    länge = len(möglichkeiten)
    if länge == 1 or not möglichkeiten:
      return (pos, möglichkeiten)
    if länge < best:
      best = länge
      best_feld = (pos, möglichkeiten)
  return best_feld


def solve():
  '''Löst das Sudoku rekursiv indem es in dem Feld mit der geringsten Anzahl an möglichen Einträgen
  eine Zahl einträgt und danach dann solve wieder auftruft. Wenn die Liste der freien Stellen leer
  ist, ist das Sudoku gelöst'''
  pos, möglichkeiten = bestes_Feld()
  if not möglichkeiten:
    return False
  for zahl in möglichkeiten:
    change_board(pos, zahl, True)
    if not freie_stellen or solve():
      return True
    change_board(pos, zahl, False)


# globale Variablen
full_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
sudokus = []
board = {}
freie_stellen = set()
spalten = []
zeilen = []
quadrate = []


def init(sudoku):
  '''generiert aus einem übergebenen String mit der Anfangs-Zahlenverteilung
  ein board-Dictionary mit Key = Tuple(spalte,zeile,quadrant) und Value = Zahl des Feldes
  und die Liste der möglichen Zahlen für jede Spalte, Zeile und jeden Quadranten als Set(). Zusätzlich
  wird ein Set der freien Stellen mit den Tuple für (spalte,zeile,quadrant) angelegt'''

  spalten.clear()
  zeilen.clear()
  quadrate.clear()
  freie_stellen.clear()

  for _ in range(9):
    spalten.append(full_set.copy())
    zeilen.append(full_set.copy())
    quadrate.append(full_set.copy())

  for i, char in enumerate(sudoku):
    pos = i2pos(i)
    freie_stellen.add(pos)
    if char not in ('.', '0'):
      board[pos] = int(char)
      change_board(pos, int(char), True)


with open('Teil_15_Sudoku_top100_hard.txt') as f:
  for nr, sudoku in enumerate(f):
    start = time.perf_counter()
    init(sudoku.rstrip())
    solve()
    zeit = (time.perf_counter() - start)*1_000
    sudokus.append((zeit, nr + 1))


summe_zeit = sum([x for x, y in sudokus])
sudokus.sort(reverse=True)
print(f'{nr+1} Sudokus gelöst in {summe_zeit:.0f} Millisek. (ø {summe_zeit/(nr+1):.0f} ms)')
for i in range(10):
  print(f'{sudokus[i][0]:5,.0f} Millisek. für Nr. {sudokus[i][1]:5d}')
