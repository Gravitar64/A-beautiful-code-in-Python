import random as rnd
from itertools import combinations
from time import perf_counter as pfc


def seite_ermitteln(auf_waage):
  seite = [0]*anz_kugeln
  mitte = len(auf_waage)//2
  for nr in auf_waage:
    seite[nr] = -1 if nr in auf_waage[:mitte] else 1
  return seite


def wiegen(gesucht, seite):
  return gesucht[1] * seite[gesucht[0]]


def statusänderung(wiegung, seite):
  for nr, status in kugeln:
    if wiegung == 0 and seite[nr] == 0: continue
    if (wiegung == 0 and seite[nr] != 0) or (wiegung != 0 and seite[nr] == 0):
      kugeln[nr][1] = '='
    else:
      kugeln[nr][1] = stati[wiegung == seite[nr]].get(status, status)


def kugeln2str(liste):
  return ' '.join([f'{nr}{kugeln[nr][1]}' for nr in liste])
  

def prüfung(v1, v2m, v2lr):
  prüfergebnisse = []
  text = ''
  for nr in range(anz_kugeln):
    gesucht = (nr, rnd.choice((-1, 1)))
    text += f'Gesucht wird {gesucht[0]}{"+" if gesucht[1] == 1 else "-"}\n'
    for k in kugeln: k[1] = '?'
    for n in range(2):
      v = v1 if n == 0 else v2m if wiegung == 0 else v2lr
      seite = seite_ermitteln(v)
      wiegung = wiegen(gesucht, seite)
      statusänderung(wiegung, seite)
      text += f'{wiegung} {kugeln2str(v)}\n' 
      kandidaten = [k[0] for k in kugeln if k[1] != '=']
    text += f'Kandidaten = {kugeln2str(kandidaten)}\n\n'
    prüfergebnisse.append(len(kandidaten) < 4)
  return all(prüfergebnisse), text

def alle_varianten(modus):
  anz_lösungen = 0
  for anz in range(1, anz_kugeln//2+1):
    for v2l in combinations(range(anz_kugeln), anz):
      for v2r in combinations(range(anz_kugeln), anz):
        if set(v2l) & set(v2r): continue
        e, text = prüfung(v1,v2m,v2l+v2r)
        if e:
          anz_lösungen += 1
          if modus > 0:
            print(f'Lösung Nr. {anz_lösungen}  {v2l} <-> {v2r}')
          if modus > 1:
            print(text+'\n\n')
          if modus > 2:
            return
  print(anz_lösungen)        


start = pfc()
anz_kugeln = 12
kugeln = [[nr, '?'] for nr in range(anz_kugeln)]

v1 = range(8)
v2m = [8,9,10,0,1,2]

stati = {True:  {'?': '+', '-': '='},
         False: {'?': '-', '+': '='}}

alle_varianten(3)
print(pfc()-start)
