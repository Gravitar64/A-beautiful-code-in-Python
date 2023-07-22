import itertools
import time


def print_board(board):
  for z in range(n):
    print()
    for s in range(n):
      print(f'{board[z][s]:>2} ', end='')
  print()


def check(board):
  for s in range(n):
    if sum(board[z][s] for z in range(n)) != summe:
      return False
  if sum(board[i][i] for i in range(n)) != summe:
    return False
  if sum(board[i][n-i-1] for i in range(n)) != summe:
    return False
  return True


def löse(zahlen, board):
  if not zahlen and check(board):
    print_board(board)
    print(time.perf_counter()-start)
    lösungen.append(board)
  for zeile in itertools.permutations(zahlen, n-1):
    letzte = summe - sum(zeile)
    zahlen2 = zahlen - set(zeile)
    if letzte < 1 or letzte not in zahlen2: continue
    zahlen2.remove(letzte)
    zeile = list(zeile)+[letzte]
    löse(zahlen2, board+[zeile])
  return


n = 4
start = time.perf_counter()
zahlen = set(range(1, n**2+1))
summe = (n**3+n)//2
lösungen = []

print(f'Magisches Quadrat mit Kantenlänge = {n} und {summe} als Summe')

löse(zahlen, [])
print(f'Anzahl Lösungen = {len(lösungen):,}')
print(time.perf_counter()-start)
