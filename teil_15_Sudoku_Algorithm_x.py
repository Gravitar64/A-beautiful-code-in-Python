#!/usr/bin/env python3

# Author: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2010 Ali Assaf
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product
import time


def solve_sudoku(size, grid):
  """ An efficient Sudoku solver using Algorithm X.
  """
  R, C = size
  N = R * C
  X = ([("rc", rc) for rc in product(range(N), range(N))] +
       [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
       [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
       [("bn", bn) for bn in product(range(N), range(1, N + 1))])
  Y = dict()
  for r, c, n in product(range(N), range(N), range(1, N + 1)):
    b = r // R * R + c // C  # Box number
    Y[(r, c, n)] = [
        ("rc", (r, c)),
        ("rn", (r, n)),
        ("cn", (c, n)),
        ("bn", (b, n))]
  X, Y = exact_cover(X, Y)
  for i, row in enumerate(grid):
    for j, n in enumerate(row):
      if n:
        select(X, Y, (i, j, n))
  for solution in solve(X, Y, []):
    for (r, c, n) in solution:
      grid[r][c] = n
    yield grid


def exact_cover(X, Y):
  X = {j: set() for j in X}
  for i, row in Y.items():
    for j in row:
      X[j].add(i)
  return X, Y


def solve(X, Y, solution):
  if not X:
    yield list(solution)
  else:
    c = min(X, key=lambda c: len(X[c]))
    for r in list(X[c]):
      solution.append(r)
      cols = select(X, Y, r)
      for s in solve(X, Y, solution):
        yield s
      deselect(X, Y, r, cols)
      solution.pop()


def select(X, Y, r):
  cols = []
  for j in Y[r]:
    for i in X[j]:
      for k in Y[i]:
        if k != j:
          X[k].remove(i)
    cols.append(X.pop(j))
  return cols


def deselect(X, Y, r, cols):
  for j in reversed(Y[r]):
    X[j] = cols.pop()
    for i in X[j]:
      for k in Y[i]:
        if k != j:
          X[k].add(i)


def string2grid(aufgabe):
  grid, zeile = [], []
  for i, char in enumerate(aufgabe):
    if char == '.':
      zahl = 0
    else:
      zahl = int(char)
    zeile.append(zahl)
    if (i+1) % 9 == 0:
      grid.append(zeile)
      zeile = []
  return grid


lösungen = []
start1 = time.perf_counter()
with open('Teil_15_Sudoku_2365_hard.txt') as f:
  for i, zeile in enumerate(f):
    zeile = zeile.rstrip()
    start = time.perf_counter()
    solutions = solve_sudoku((3, 3), string2grid(zeile))
    for solution in solutions:
      pass
    end = time.perf_counter()
    lösungen.append((end-start, i+1))
summe = sum(x for x, y in lösungen)
print(f'Lösung von {i+1:,} Sudokus in {summe:,.2f} Sek. (durchschn. {summe/len(lösungen)*1000:,.2f} Millisek.)\n')
lösungen.sort(reverse=True)
for i in range(10):
  zeit, nr = lösungen[i]
  print(f'Nr. {nr:5d} in {zeit*1000:5,.0f} Millisek.')
