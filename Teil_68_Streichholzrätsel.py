import math

def dateiLesen(datei):
  figuren = []
  with open(datei) as f:
    for e in f.read().split('\n\n'):
      figuren.append([list(map(int, (x.split(',')))) for x in e.split('\n')])
  return figuren

def addVec(pos, delta):
  return tuple(round(a+b,1) for a,b in zip(pos,delta))

def pol2cart(w, von):
  r, w_rad = 1, math.radians(w)
  delta = r * math.cos(w_rad), r * math.sin(w_rad)
  return addVec(von, delta)

def genKoordinaten(figuren):
  linien = []
  for figur in figuren:
    for i, e in enumerate(figur):
      if len(e) == 1:
        von, w = (0,0), e[0]
      else:
        nr, w = e
        von = figur[nr][1]
      zu = pol2cart(w, von)
      figur[i] = (von,zu)
    figur = {frozenset(p) for p in figur}  
    linien.append(figur)
  return linien

def verschiebe(nachher):
  for (x,y), *args in vorher:
    for (x1,y1), *args in nachher:
      delta = x-x1, y-y1
      yield {frozenset((addVec(von, delta), addVec(zu,delta))) for von,zu in nachher}

def lösung():
  maxÜbereinst = 0
  for ziel in verschiebe(nachher):
    if (l := len(vorher & ziel)) > maxÜbereinst:
      maxÜbereinst, bestZiel = l, ziel
  return bestZiel    


for n in range(6):
  figuren = dateiLesen(f'Teil_68_Streichhoelzer{n}.txt')
  vorher, nachher = genKoordinaten(figuren)
  bestZiel = lösung()
  übereinst = vorher & bestZiel
  löschen = vorher - bestZiel
  setzen = bestZiel - vorher
  print(f'Aufgabe Nr. {n} = {len(löschen)}')