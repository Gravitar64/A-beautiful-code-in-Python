from time import perf_counter as pfc


def prüfe_machbarkeit(hinweise):
  return sum([sum(s) for s in hinweise[0]]) == sum([sum(z) for z in hinweise[1]])


def permutation(einträge, length):
  
  def gen_segment(e, l):
    if not e: return [[2] * l]
    return [[2] * x + e[0] + tail
            for x in range(1, l - len(e) + 2)
            for tail in gen_segment(e[1:], l - x)]

  
  return [x[1:] for x in gen_segment(
          [[1] * i for i in einträge], 
          length + 1 - sum(einträge))]
  


def prüfe_gültigkeit(perm, i, typ):
  if typ == 1:
    vergleich = [grid[y][i] for y in range(höhe)]
  else:
    vergleich = [grid[i][x] for x in range(breite)]
  if all(e == 0 for e in vergleich): return perm
  gültig = []
  for p in perm:
    if not all(vergleich[n] == 0 or vergleich[n] == e for n, e in enumerate(p)):
      continue
    gültig.append(p)
  return gültig


def showGrid(grid):
  for zeile in grid:
    print(' '.join(['?* '[c] for c in zeile]))
  print()


def probleme_einlesen(datei):
  probleme = []

  with open(datei) as f:
    for problem in f.read().split('\n\n'):
      probleme.append([[[ord(c)-64 for c in e] for e in hv.split()]
                       for hv in problem.split('\n')])
  return probleme


def solve(hinweise):
  änderung = True
  verlauf = {}
  while änderung:
    änderung = False
    for vh, h in enumerate(hinweise):
      größe = höhe if vh == 1 else breite
      for i, e in enumerate(h):
        if (vh,i) in verlauf:
          permutations = verlauf[(vh,i)]
        else:
          permutations = permutation(e,größe)
        gültig = prüfe_gültigkeit(permutations, i, vh)
        verlauf[(vh,i)] = gültig
        überdeckung = [all(e[0] == n for n in e) for e in zip(*gültig)]
        for i2, ü in enumerate(überdeckung):
          setze = gültig[0][i2]
          if vh == 0:
            x, y = i2, i
          else:
            x, y = i, i2
          if ü and grid[y][x] == 0:
            grid[y][x] = setze
            änderung = True
  return grid


H, V = 0, 1
probleme = probleme_einlesen('Teil_xx_Nonogram_problems.txt')

for hinweise in probleme:

  start = pfc()
  breite, höhe = len(hinweise[V]), len(hinweise[H])
  print(f'Breite = {breite}, Höhe = {höhe}')
  grid = [[0]*breite for _ in range(höhe)]

  if not prüfe_machbarkeit(hinweise):
    print('Sorry. Dieses Nonogramm ist feherhaft und kann nicht gelöst werden')
    exit()

  showGrid(solve(hinweise))
  print(pfc()-start)
