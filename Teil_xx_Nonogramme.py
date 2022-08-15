from time import perf_counter as pfc
import copy


def prüfe_machbarkeit():
  return sum([sum(s) for s in spalten]) == sum([sum(z) for z in zeilen])


def prüfe_freiheitsgrade(e):
  return size - (sum(e)+len(e)-1)


def get_permutations(einträge, länge):
  if not einträge:  return [[False] * länge]
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

def prüfe_gültigkeit(perm,i,typ):
  if typ == 's':
    vergleich = [grid[i][n] for n in range(höhe)]
  else:
    vergleich = [grid[n][i] for n in range(breite)]
  if all(e==None for e in vergleich): return perm
  gültig = []
  for p in perm:
    if not all(vergleich[i] == None or vergleich[i] == e for i,e in enumerate(p)):
      continue
    gültig.append(p)
  return gültig  

def showGrid(grid):
  for zeile in range(höhe):
    for spalte in range(breite):
      if grid[spalte][zeile] == None:
        print('?',end='')
      elif grid[spalte][zeile] == True:
        print('X',end='')
      else:
        print('_',end='')
    print()
  print()          
      
start = pfc()

spalten = [[3, 4], [1, 2, 1, 1], [1, 3, 2], [
    2, 1, 2], [1, 1], [2, 1], [1, 3], [1, 4], [2], [1]]
zeilen = [[2], [4, 1, 2], [1, 3, 1], [2, 1], [
    2, 1], [2, 1], [3, 2], [1, 4], [1, 2, 1], [3]]
breite, höhe = len(spalten), len(zeilen)
grid = [[None]*breite for _ in range(höhe)]

if not prüfe_machbarkeit():
  print('Sorry. Dieses Nonogramm ist feherhaft und kann nicht gelöst werden')
  exit()



änderung = True
while änderung:
  änderung = False
  
  for i,s in enumerate(spalten):
    permutations = get_permutations(s,breite)
    gültig = prüfe_gültigkeit(permutations,i,'s')
    überdeckung = [all(e[0] == x for x in e) for e in zip(*gültig)]
    for i2,ü in enumerate(überdeckung):
      setze = gültig[0][i2]
      if ü and grid[i][i2] != setze: 
        grid[i][i2] = setze
        änderung = True
   

  for i,s in enumerate(zeilen):
    permutations = get_permutations(s,breite)
    gültig = prüfe_gültigkeit(permutations,i,'z')
    überdeckung = [all(e[0] == x for x in e) for e in zip(*gültig)]
    for i2,ü in enumerate(überdeckung):
      setze = gültig[0][i2]
      if ü and grid[i2][i] != setze: 
        grid[i2][i] = setze
        änderung = True
    
  
print(pfc()-start)
showGrid(grid)