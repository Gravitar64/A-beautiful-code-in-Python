from time import perf_counter as pfc
import itertools as itt


def fehlerhaftes_nonogramm(zeilen,spalten):
  return sum(map(sum,spalten)) != sum(map(sum,zeilen))


def gen_permutationen(einträge, länge):
  permutationen = []
  anz_blöcke = len(einträge)
  anz_leer = länge-sum(einträge)-anz_blöcke+1
  for v in itt.combinations(range(anz_blöcke+anz_leer), anz_blöcke):
    v = [v[0]]+[b-a for a,b in zip(v,v[1:])]
    p= ''.join(['2'*pos+'1'*einträge[i] for i,pos in enumerate(v)])
    p+='2'*(anz_leer)
    permutationen.append(p[:länge])
  return permutationen
  

def prüfe_gültigkeit(perm, i, typ):
  vergleich = grid[i] if typ == ZEILEN else [grid[y][i] for y in range(höhe)]
  if all(e == '0' for e in vergleich): return perm
  gültig = []
  for p in perm:
    if not all(vergleich[n] == '0' or vergleich[n] == e  
               for n, e in enumerate(p)):
      continue
    gültig.append(p)
  return gültig


def showGrid(grid):
  for zeile in grid:
    print(' '.join(['?# '[int(c)] for c in zeile]))
  print()


def datei_einlesen(datei):
  nonogramme = []
  with open(datei) as f:
    for nonogramm in f.read().split('\n\n'):
      nonogramme.append([[[ord(c)-64 for c in e] for e in hv.split()]
                       for hv in nonogramm.split('\n')])
  return nonogramme


def löse(nonogramm):
  verlauf = {}
  
  änderung = True
  while änderung:
    änderung = False
    for sicht, hinweise in enumerate(nonogramm):
      größe = höhe if sicht == SPALTEN else breite
      for i, e in enumerate(hinweise):
        permutationen = verlauf[(sicht,i)] if (sicht,i) in verlauf \
                        else gen_permutationen(e,größe)
        gültig = prüfe_gültigkeit(permutationen, i, sicht)
        verlauf[(sicht,i)] = gültig
        treffer = [all(e[0] == n for n in e) for e in zip(*gültig)]
        for i2, t in enumerate(treffer):
          if not t: continue
          if sicht == ZEILEN:
            x, y = i2, i
          else:
            x, y = i, i2
          if grid[y][x] == '0':
            grid[y][x] = gültig[0][i2]
            änderung = True
  return grid

ZEILEN, SPALTEN = 0, 1
nonogramme = datei_einlesen('Teil_81_Nonogram_problems.txt')

for nonogramm in nonogramme:
  start = pfc()
  breite, höhe = len(nonogramm[SPALTEN]), len(nonogramm[ZEILEN])
  print(f'Breite = {breite}, Höhe = {höhe}')
  grid = [['0']*breite for _ in range(höhe)]

  if fehlerhaftes_nonogramm(*nonogramm):
    print('Sorry. Dieses Nonogramm ist feherhaft und kann nicht gelöst werden')
    exit()

  showGrid(löse(nonogramm))
  print(pfc()-start)