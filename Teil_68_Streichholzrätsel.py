import math


def dateiLesen(datei):
  listen = []
  with open(datei) as f:
    for e in f.read().split('\n\n'):
      listen.append([list(map(int, (x.split(',')))) for x in e.split('\n')])
  return listen


def genKoordinaten(listen):
  linien = []
  for l in listen:
    for i, e in enumerate(l):
      if len(e) == 1:
        von, w = (0, 0), e[0]
      else:
        nr, w = e
        von = l[nr][1]
      zu = pol2cart(w, von)
      l[i] = (von, zu)
    l = {frozenset(p) for p in l}
    linien.append(l)
  return linien


def addVec(pos, delta):
  return tuple(round(a+b, 1) for a, b in zip(pos, delta))


def pol2cart(w, von):
  r, w_rad = 1, math.radians(w)
  delta = r * math.cos(w_rad), r * math.sin(w_rad)
  return addVec(von, delta)


def verschiebe(nachher):
  for (x, y), *args in vorher:
    for (x1, y1), *args in nachher:
      delta = x-x1, y-y1
      yield {frozenset((addVec(von, delta), addVec(zu, delta))) for von, zu in nachher}


def solve():
  maxÜbereinst = 0
  for ziel in verschiebe(nachher):
    if (l := len(vorher & ziel)) > maxÜbereinst:
      maxÜbereinst, bestZiel = l, ziel
  return bestZiel


for n in range(6):
  l = dateiLesen(f'Teil_68_streichhoelzer{n}.txt')
  vorher, nachher = genKoordinaten(l)
  ziel = solve()
  gleich, löschen, setzen = vorher & ziel, vorher - ziel, ziel - vorher
  print(f'Anzahl zu verschiebender Streichhölzer = {len(löschen)}')