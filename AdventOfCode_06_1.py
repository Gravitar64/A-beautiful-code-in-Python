from collections import Counter

aufgabe = open('AdventOfCode_06.txt').read().split('\n')
zeilen = spalten = 0
koordinaten = []
infinity = {-1}

for zeile in aufgabe:
  x, y = zeile.split(',')
  x, y = int(x), int(y)
  zeilen = max(zeilen, y)
  spalten = max(spalten, x)
  koordinaten.append((x, y))

grid = [-1] * spalten * zeilen

for n in range(len(grid)):
  y = n // spalten
  x = n % spalten
  entfernungen = []
  for i, koordinate in enumerate(koordinaten):
    entf = abs(koordinate[0] - x) + abs(koordinate[1] - y)
    entfernungen.append((entf, i))
  entfernungen.sort()
  if entfernungen[0][0] < entfernungen[1][0]:
    grid[n] = entfernungen[0][1]
  if x == 0 or y == 0 or x == spalten-1 or y == zeilen - 1:
    infinity.add(entfernungen[0][1])

lösung = Counter(i for i in grid if i not in infinity)
print(lösung)
