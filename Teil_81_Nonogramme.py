from time import perf_counter as pfc
import itertools as itt


def datei_einlesen(datei):
  with open(datei) as f:
    return [[[[ord(buchst)-64 for buchst in zf]
               for zf in zeile.split()]
               for zeile in nonogramm.split('\n')]
               for nonogramm in f.read().split('\n\n')]


def nonogramm_fehlerhaft(nonogramm):
  return sum(map(sum, nonogramm[ZEILEN])) != sum(map(sum, nonogramm[SPALTEN]))


def zeige_spielfeld():
  for zeile in spielfeld:
    print(' '.join(zeile))
  print()


def gen_perm(zf, l):
  perm = []
  for p in itt.combinations(range(l-sum(zf)+1), len(zf)):
    p = [p[0]] + [b-a for a,b in zip(p, p[1:])]
    perm.append(''.join([' '*leer + '#'*zf[i] for i,leer in enumerate(p)]).ljust(l,' '))
  return perm


def prüfe_gültige(perm, sicht, zs):
  vergleich = spielfeld[zs] if sicht == ZEILEN else [spielfeld[z][zs] for z in range(höhe)]
  if all(e == '?' for e in vergleich): return perm
  gültige = []
  for p in perm:
    if not all(a=='?' or a == b for a,b in zip(vergleich, p)): continue
    gültige.append(p)
  return gültige    


def löse_nonogramm(nonogramm):
  speicher = {}
  änderung = True
  while änderung:
    änderung = False
    for sicht, zahlenfolgen in enumerate(nonogramm):
      größe = breite if sicht == ZEILEN else höhe
      for zs, zahlenfolge in enumerate(zahlenfolgen):
        perm = speicher[(sicht,zs)] if (sicht,zs) in speicher else gen_perm(zahlenfolge, größe)
        gültige = prüfe_gültige(perm, sicht, zs)
        speicher[(sicht,zs)] = gültige
        eindeutige = [(i, s[0]) for i, s in enumerate(zip(*gültige)) if len(set(s)) == 1]
        for sz, e in eindeutige:
          z,s = (zs, sz) if sicht == ZEILEN else (sz, zs)
          if spielfeld[z][s] != e:
            spielfeld[z][s] = e
            änderung = True



nonogramme = datei_einlesen('Teil_81_Nonogram_problems.txt')
ZEILEN, SPALTEN = 0, 1

for nonogramm in nonogramme:
  start = pfc()
  if nonogramm_fehlerhaft(nonogramm):
    print('Sorry, das Nonogramm ist fehlerhaft und kann nicht gelöst werden')
    continue
  breite, höhe = len(nonogramm[SPALTEN]), len(nonogramm[ZEILEN])
  spielfeld = [['?'] * breite for _ in range(höhe)]
  löse_nonogramm(nonogramm)
  zeige_spielfeld()
  print(pfc()-start)

