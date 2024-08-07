import math


def dateiLesen(dateiname):
  figuren = []
  with open(dateiname) as f:
    for figur in f.read().split('\n\n'):
      figuren.append([list(map(int, (zeile.split(','))))
                     for zeile in figur.split('\n')])
  return figuren


def pol2cart(winkel, von, radius=100):
  winkel_radiant = math.radians(winkel)
  delta = radius * math.cos(winkel_radiant), radius * math.sin(winkel_radiant)
  return addVec(von, delta)


def addVec(pos, delta):
  return tuple(round(a + b, 1) for a, b in zip(pos, delta))


def genKoordinaten(figuren):
  koordinaten = []
  for figur in figuren:
    for i, zeile in enumerate(figur):
      if len(zeile) == 1:
        winkel, von = zeile[0], (0, 0)
      else:
        nr, winkel = zeile
        von = figur[nr][1]
      zu = pol2cart(winkel, von)
      figur[i] = (von, zu)
    figur = {frozenset(streichholz) for streichholz in figur}
    koordinaten.append(figur)
  return koordinaten


def verschiebe(nachher):
  for (x, y), *args in vorher:
    for (x1, y1), *args in nachher:
      delta = x - x1, y - y1
      yield {frozenset(((addVec(von, delta), addVec(zu, delta)))) for von, zu in nachher}


def findeLösung():
  maxÜbereinst = 0
  for verschoben in verschiebe(nachher):
    if (l := len(vorher & verschoben)) > maxÜbereinst:
      maxÜbereinst, bestVerschoben = l, verschoben
  return bestVerschoben


for n in range(6):
  dateiname = f'Teil_068_streichhoelzer{n}.txt'
  figuren = dateiLesen(dateiname)
  vorher, nachher = genKoordinaten(figuren)
  gleich = vorher & nachher
  bestVerschoben = findeLösung()
  gleich = vorher & bestVerschoben
  löschen = vorher - bestVerschoben
  setzen = bestVerschoben - vorher
  alle = vorher | bestVerschoben
  print(f'{dateiname}, Beste Lösung umzulegende Streichhölzer = {len(löschen)}')
