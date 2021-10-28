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


def pol2cart(w, von):
  r = 1
  x, y = von
  w_rad = math.radians(w)
  dx, dy = r * math.cos(w_rad), r * math.sin(w_rad)
  return round(x+dx, 1), round(y+dy, 1)


def verschiebe(nachher):
  for (x, y), *args in vorher:
    for (x1, y1), *args in nachher:
      dx, dy = x-x1, y-y1
      yield {frozenset(((vx+dx, vy+dy), (zx+dx, zy+dy))) for (vx, vy), (zx, zy) in nachher}


def solve():
  maxÜbereinst = 0
  for ziel in verschiebe(nachher):
    if (l :=len(vorher & ziel)) > maxÜbereinst:
      maxÜbereinst, bestZiel = l, ziel
  return bestZiel


l = dateiLesen('Teil_68_streichhoelzer0.txt')
vorher, nachher = genKoordinaten(l)
ziel = solve()
gleich, löschen, setzen = vorher & ziel, vorher - ziel, ziel - vorher
print(f'Anzahl übereinstimmender Streichhölzer = {len(gleich)}')
print(f'Anzahl zu verschiebender Streichhölzer = {len(löschen)}')
