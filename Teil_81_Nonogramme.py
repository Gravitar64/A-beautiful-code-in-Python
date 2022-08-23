import itertools as itt
from time import perf_counter as pfc


def datei_einlesen(datei):
  with open(datei) as f:
    return [[[[ord(buchst)-64 for buchst in zf]
               for zf in zeile.split()]
               for zeile in nonogramm.split('\n')]
               for nonogramm in f.read().split('\n\n')]


def nonogramm_fehlerhaft(n):
  return sum(map(sum, n[ZEILEN])) != sum(map(sum, n[SPALTEN]))


def zeige_spielfeld():
  for zeile in spielfeld:
    print(' '.join(zeile))
  print()


def gen_permutationen(zf, l):
  permutationen = []
  max_leer = l - sum(zf) + 1
  for v in itt.combinations(range(max_leer), len(zf)):
    v = [v[0]] + [b-a for a, b in zip(v, v[1:])]
    permutationen.append(''.join([' '*leer + '#'*zf[i]
                                  for i, leer in enumerate(v)]).ljust(l, ' '))
  return permutationen


def prüfe_gültig(perm, sicht, i):
  vergleich = spielfeld[i] if sicht == ZEILEN else [spielfeld[z][i] for z in range(höhe)]
  if all(e == '?' for e in vergleich): return perm
  gültige = []
  for p in perm:
    if not all(vergleich[i] == '?' or vergleich[i] == e for i, e in enumerate(p)): continue
    gültige.append(p)
  return gültige


def löse(nonogramm):
  speicher = {}
  änderung = True
  while änderung:
    änderung = False
    for sicht, zahlenfolgen in enumerate(nonogramm):
      größe = breite if sicht == ZEILEN else höhe
      for zs, zahlenfolge in enumerate(zahlenfolgen):
        permutationen = speicher.get((sicht,zs), gen_permutationen(zahlenfolge, größe))
        gültige = prüfe_gültig(permutationen, sicht, zs)
        speicher[(sicht, zs)] = gültige
        eindeutige = [(i,s[0]) for i,s in enumerate(zip(*gültige)) if len(set(s)) == 1]
        for sz, e in eindeutige:
          z,s = (zs,sz) if sicht == ZEILEN else (sz,zs)
          if spielfeld[z][s] != e:
            spielfeld[z][s] = e
            änderung = True


nonogramme = datei_einlesen('Teil_81_Nonogram_problems.txt')
ZEILEN, SPALTEN = 0, 1

for nonogramm in nonogramme:
  start = pfc()
  if nonogramm_fehlerhaft(nonogramm):
    print('Sorry, das Nonogramm ist feherhaft und kann nicht gelöst werden')
    continue
  breite, höhe = len(nonogramm[SPALTEN]), len(nonogramm[ZEILEN])
  spielfeld = [['?']*breite for _ in range(höhe)]
  löse(nonogramm)
  zeige_spielfeld()
  print(pfc()-start)