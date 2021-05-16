import random as rnd
from itertools import combinations


def seite_ermitteln(versuch):
  seite = [0]*anz_kugeln
  links = set(versuch[:len(versuch)//2])
  for nr in versuch:
    seite[nr] = -1 if nr in links else 1
  return seite


def wiegen(nr, gewicht, seite):
  return gewicht * seite[nr]


def statusänderung(wiegung, seite):
  for nr, status in kugeln:
    if wiegung == 0 and seite[nr] == 0: continue
    if (wiegung == 0 and seite[nr] != 0) or (wiegung != 0 and seite[nr] == 0):
      kugeln[nr][1] = '='
    else:
      kugeln[nr][1] = stati[wiegung == seite[nr]].get(status, status)


def kugel2str(liste):
  return ' '.join([f'{nr}{kugeln[nr][1]}' for nr in liste])


def prüfung(v1, v2m, v2lr):
  text = ''
  prüfungsergebnisse = []
  for nr in range(anz_kugeln):
    for k in kugeln: k[1] = '?'
    gesucht = (nr, rnd.choice((-1, 1)))
    text += f'Gesucht wird {gesucht[0]}{"+" if gesucht[1] == 1 else "-"}\n'
    for n in range(2):
      v = v1 if n == 0 else v2m if wiegung == 0 else v2lr
      seite = seite_ermitteln(v)
      wiegung = wiegen(*gesucht, seite)
      statusänderung(wiegung, seite)
      text += f'{wiegung} {kugel2str(v)}\n'
    kandidaten = [k[0] for k in kugeln if k[1] != '=']
    prüfungsergebnisse.append(len(kandidaten) < 4)
    text += f'Kandidaten = {kugel2str(kandidaten)}\n\n'
  return all(prüfungsergebnisse), text


def prüfe_varianten(modus):
  anz_lösungen = 0
  for anz in range(1, anz_kugeln//2+1):
    for v2l in combinations(range(anz_kugeln), anz):
      for v2r in combinations(range(anz_kugeln), anz):
        if set(v2l) & set(v2r):continue
        e, text = prüfung(v1, v2m, v2l+v2r)
        if e:
          anz_lösungen += 1
          if modus > 0:
            print(f'Lösung Nr. {anz_lösungen} {v2l} <-> {v2r}')
          if modus > 1:
            print(text+'\n\n')
          if modus > 2:
            return
  print(anz_lösungen//2)


stati = {True:  {'?': '+', '-': '='},
         False: {'?': '-', '+': '='}}

anz_kugeln = 12
kugeln = [[nr, '?'] for nr in range(anz_kugeln)]

v1 = [0, 1, 2, 3, 4, 5, 6, 7]
v2m = [8, 9, 10, 0, 1, 2]

prüfe_varianten(3)
