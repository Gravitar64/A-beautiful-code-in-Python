from time import perf_counter as pfc
import itertools as itt
import math


def prüfe_machbarkeit(hinweise):
  return sum([sum(s) for s in hinweise[0]]) == sum([sum(z) for z in hinweise[1]])


def permutation(einträge, länge,vergleich, ist_leer):
  permutationen = []
  anz_blöcke = len(einträge)
  anz_leer = länge-sum(einträge)-anz_blöcke+1
  for v in itt.combinations(range(anz_blöcke+anz_leer), anz_blöcke):
    v = [v[0]]+[b-a for a,b in zip(v,v[1:])]
    p = ''
    abbruch = False
    for i,pos in enumerate(v):
      p += '2'*pos+'1'*einträge[i]
      if not ist_leer:
        for i2,c in enumerate(p):
          if vergleich[i2] != '0' and vergleich[i2] != c:
            abbruch = True
            break
      if abbruch: break    
    else:    
      p+='2'*(anz_leer)
      permutationen.append(p[:länge])
  return permutationen
  

def prüfe_gültigkeit(perm, vergleich):
  return [p for p in perm 
          if all(vergleich[n] == '0' or 
             vergleich[n] == e for n, e in enumerate(p))]


def showGrid(grid):
  for zeile in grid:
    print(' '.join(['?# '[int(c)] for c in zeile]))
  print()


def probleme_einlesen(datei):
  probleme = []
  with open(datei) as f:
    for problem in f.read().split('\n\n'):
      probleme.append([[[ord(c)-64 for c in e] for e in hv.split()]
                       for hv in problem.split('\n')])
  return probleme

def get_anz_perm(h,n):
  k = len(h)
  m = sum(h)
  return math.comb(n-m+1,k)


def gen_sortierte_hinweise(hinweise,verlauf):
  erg = []
  for vh,hi in enumerate(hinweise): 
    größe = höhe if vh == 1 else breite
    for i,h in enumerate(hi):
      if (vh,i) in verlauf:
        anz = len(verlauf[(vh,i)])
      else:
        anz = get_anz_perm(h,größe)
      erg.append((anz,vh,i,h))    
  return sorted(erg)
  



def solve(hinweise):
  verlauf = {}
  
  änderung = True
  while änderung:
    änderung = False
    einträge = gen_sortierte_hinweise(hinweise,verlauf)
    for _,vh,i,e in einträge:
      größe = höhe if vh == 1 else breite
      vergleich = grid[i] if vh == 0 else [grid[y][i] for y in range(höhe)]
      ist_leer = all(e == '0' for e in vergleich)
      if (vh,i) in verlauf:
        if not ist_leer:
          verlauf[(vh,i)] = prüfe_gültigkeit(verlauf[(vh,i)], vergleich)
      else:
        verlauf[(vh,i)] = permutation(e,größe,vergleich,ist_leer)
      treffer = [all(e[0] == n for n in e) for e in zip(*verlauf[(vh,i)])]
      for i2, ü in enumerate(treffer):
        if not ü: continue
        if vh == 0:
          x, y = i2, i
        else:
          x, y = i, i2
        if grid[y][x] == '0':
          grid[y][x] = verlauf[(vh,i)][0][i2]
          änderung = True
  return grid

H, V = 0, 1
probleme = probleme_einlesen('Teil_xx_Nonogram_problems.txt')

for hinweise in probleme:
  start = pfc()
  breite, höhe = len(hinweise[V]), len(hinweise[H])
  print(f'Breite = {breite}, Höhe = {höhe}')
  grid = [['0']*breite for _ in range(höhe)]

  if not prüfe_machbarkeit(hinweise):
    print('Sorry. Dieses Nonogramm ist feherhaft und kann nicht gelöst werden')
    exit()

  showGrid(solve(hinweise))
  print(pfc()-start)