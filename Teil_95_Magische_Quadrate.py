import itertools
import time


def check(board):
  for z in range(1, n):
    if sum(board[z*n:z*n+n]) != summe: return False
  if sum(board[i*n+i] for i in range(n)) != summe: return False
  if sum(board[i*n+n-i-1] for i in range(n)) != summe: return False
  return True


def rows(nr, zahlen, board):
  for row in itertools.permutations(zahlen, n-1):
    rest = summe-sum(row)
    zahlen2 = zahlen-set(row)
    if rest < 1 or rest not in zahlen2: continue
    board[nr*n:nr*n+n] = list(row)+[rest]
    cols(nr, zahlen2-{rest}, board)


def cols(nr, zahlen, board):
  if not zahlen:
    if check(board):
      print(f'{board} {time.perf_counter()-start:.2f}')
      lösungen.append(board)
    return
  for col in itertools.permutations(zahlen, n-2):
    rest = summe-sum(col)-board[nr]
    zahlen2 = zahlen-set(col)
    if rest < 1 or rest not in zahlen2: continue
    for i, z in enumerate(list(col)+[rest], start=1):
      board[i*n+nr] = z
    cols(nr+1, zahlen2-{rest}, board)


n = 4
start = time.perf_counter()
zahlen = set(range(1, n**2+1))
board = [0]*n*n
summe = (n**3+n)//2
lösungen = []

print(f'Magisches Quadrat mit Kantenlänge = {n} und {summe} als Summe')

rows(0, zahlen, board)
print(f'Anzahl Lösungen = {len(lösungen):,}')
print(time.perf_counter()-start)
