import itertools as itt
from time import perf_counter as pfc


def datei_einlesen(datei):
  with open(datei) as f:
    return [[[[ord(buchst)-64 for buchst in zf]
               for zf in zeile.split()]
               for zeile in nonogramm.split('\n')]
               for nonogramm in f.read().split('\n\n')]


def nonogramm_fehlerhaft(zeilen, spalten):
  return sum(map(sum, zeilen)) != sum(map(sum, spalten))


def gen_permutationen(zf, l):
  permutationen = []
  anz_blöcke = len(zf)
  anz_leer = l-sum(zf)-anz_blöcke+1
  for v in itt.combinations(range(anz_blöcke+anz_leer), anz_blöcke):
    v = [v[0]] + [b-a for a, b in zip(v, v[1:])]
    permutationen.append(''.join([' '*leer+'#'*zf[i]
                                  for i, leer in enumerate(v)]).ljust(l, ' '))
  return permutationen


def prüfe_gültig(perm, i, sicht):
  vergleich = grid[i] if sicht == ZEILEN else [grid[z][i] for z in range(höhe)]
  if all(e == '?' for e in vergleich):
    return perm
  gültige = []
  for p in perm:
    if not all(vergleich[i] == '?' or vergleich[i] == e for i, e in enumerate(p)):
      continue
    gültige.append(p)
  return gültige


def löse(nonogramm):
  speicher = {}
  änderung = True
  while änderung:
    änderung = False
    for sicht, zahlenfolgen in enumerate(nonogramm):
      größe = höhe if sicht == SPALTEN else breite
      for i, zahlenfolge in enumerate(zahlenfolgen):
        if (sicht, i) in speicher:
          permutationen = speicher[(sicht, i)]
        else:
          permutationen = gen_permutationen(zahlenfolge, größe)
        gültige = prüfe_gültig(permutationen, i, sicht)
        speicher[(sicht, i)] = gültige
        treffer = [set(s) for s in zip(*gültige)]
        for i2, t in enumerate(treffer):
          if len(t) != 1: continue
          if sicht == ZEILEN:
            z, s = i, i2
          else:
            z, s = i2, i
          if grid[z][s] == '?':
            grid[z][s] = gültige[0][i2]
            änderung = True
  return grid


def zeige_grid(grid):
  for zeile in grid:
    print(' '.join(zeile))
  print()


nonogramme = datei_einlesen('Teil_81_Nonogram_problems.txt')
ZEILEN, SPALTEN = 0, 1


for nonogramm in nonogramme:
  start = pfc()
  if nonogramm_fehlerhaft(*nonogramm):
    print('Sorry, das Nonogramm ist fehlerhaft und kann nicht gelöst werden')
    exit()

  breite, höhe = len(nonogramm[SPALTEN]), len(nonogramm[ZEILEN])
  grid = [['?']*breite for _ in range(höhe)]
  grid = löse(nonogramm)
  print(pfc()-start)
  zeige_grid(grid)