from time import perf_counter as pfc
import copy


def prüfe_machbarkeit(hinweise):
  return sum([sum(s) for s in hinweise[0]]) == sum([sum(z) for z in hinweise[1]])


def get_permutations(einträge, länge):
  if not einträge:
    return [[False] * länge]
  permutations = []
  for start in range(länge - einträge[0] + 1):
    permutation = []
    for i in range(start):
      permutation.append(False)
    for i in range(start, start + einträge[0]):
      permutation.append(True)
    i = start + einträge[0]
    if i < länge:
      permutation.append(False)
      i += 1
    if i == länge and not einträge:
      permutations.append(permutation)
      break
    sub_start = i
    sub_rows = get_permutations(einträge[1:len(einträge)], länge - sub_start)
    for sub_row in sub_rows:
      sub_permutation = copy.deepcopy(permutation)
      for i in range(sub_start, länge):
        sub_permutation.append(sub_row[i-sub_start])
      permutations.append(sub_permutation)
  return permutations


def prüfe_gültigkeit(perm, i, typ):
  if typ == 1:
    vergleich = [grid[y][i] for y in range(höhe)]
  else:
    vergleich = [grid[i][x] for x in range(breite)]
  if all(e == None for e in vergleich):
    return perm
  gültig = []
  for p in perm:
    if not all(vergleich[n] == None or vergleich[n] == e for n, e in enumerate(p)):
      continue
    gültig.append(p)
  return gültig


def showGrid(grid):
  for y in range(höhe):
    for x in range(breite):
      if grid[y][x] == None:
        print('?', end='')
      elif grid[y][x] == True:
        print('X', end='')
      else:
        print('_', end='')
    print()
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
  while änderung:
    änderung = False
    for vh,h in enumerate(hinweise):
      größe = höhe if vh == 1 else breite
      for i, e in enumerate(h):
        permutations = get_permutations(e, größe)
        gültig = prüfe_gültigkeit(permutations, i, vh)
        überdeckung = [all(e[0] == n for n in e) for e in zip(*gültig)]
        for i2, ü in enumerate(überdeckung):
          setze = gültig[0][i2]
          if vh == 0:
            x,y = i2, i
          else:
            x,y = i, i2  
          if ü and grid[y][x] == None:
            grid[y][x] = setze
            änderung = True
    showGrid(grid)        
  return grid
    


H,V = 0,1
probleme = probleme_einlesen('Teil_xx_Nonogram_problems.txt')

for hinweise in probleme:

  start = pfc()
  breite, höhe = len(hinweise[V]), len(hinweise[H])
  print(f'Breite = {breite}, Höhe = {höhe}')
  grid = [[None]*breite for _ in range(höhe)]

  if not prüfe_machbarkeit(hinweise):
    print('Sorry. Dieses Nonogramm ist feherhaft und kann nicht gelöst werden')
    exit()

  showGrid(solve(hinweise))
  print(pfc()-start)
