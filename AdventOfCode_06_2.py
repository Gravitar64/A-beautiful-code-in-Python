aufgabe = open('AdventOfCode_06.txt').read().split('\n')
zeilen = spalten = 0
koordinaten = []

for zeile in aufgabe:
  x, y = zeile.split(',')
  x, y = int(x), int(y)
  zeilen = max(zeilen, y)
  spalten = max(spalten, x)
  koordinaten.append((x, y))

lösung = 0
for n in range(zeilen*spalten):
  y = n // spalten
  x = n % spalten
  entf = 0
  for i, koordinate in enumerate(koordinaten):
    entf += abs(koordinate[0] - x) + abs(koordinate[1] - y)
  if entf < 10_000:
    lösung += 1

print(lösung)
