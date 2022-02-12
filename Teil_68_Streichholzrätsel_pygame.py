import math
import pygame as pg


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
  return tuple(round(a+b, 1) for a, b in zip(pos, delta))


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


def verschiebe():
  for (x, y) in {von for von,zu in vorher}:
    for (x1, y1) in {von for von,zu in nachher}:
      delta = x-x1, y-y1
      yield (x,y), (x1,y1), {frozenset(((addVec(von, delta), addVec(zu, delta)))) for von, zu in nachher}


def findeLösung():
  maxÜbereinst = 0
  for _,_,verschoben in verschiebe():
    if (l := len(vorher & verschoben)) > maxÜbereinst:
      maxÜbereinst, bestVerschoben = l, verschoben
  return bestVerschoben

def nächsteTransformation():
  return verschiebe()  

def nächsteAufgabe():
  for n in range(6):
    dateiname = f'Teil_68_streichhoelzer{n}.txt'
    figuren = dateiLesen(dateiname)
    yield genKoordinaten(figuren)


def zeichne(koordinaten,delta,transfPunkt,farbe):
  for von,zu in koordinaten:
    v,z = addVec(von,delta), addVec(zu,delta)
    pg.draw.line(screen,farbe,v,z,3)
    pg.draw.circle(screen,'#ff0000',v,6)    
    pg.draw.circle(screen,'#ff0000',z,6)
    if transfPunkt:
      t = addVec(transfPunkt, delta)
      t = addVec(t,(-8,-8))
      pg.draw.rect(screen,'#ffff00', (*t,16,16))
    


transform = set()
gen_ladeAufgabe = nächsteAufgabe()
vorher, nachher = next(gen_ladeAufgabe)
gen_Transform = nächsteTransformation()
vP = nP = False

screen = pg.display.set_mode((1920,1080))
clock = pg.time.Clock()
FPS = 40

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    match ereignis.type:
      case pg.QUIT: quit()
      case pg.KEYDOWN:
        match ereignis.key:
          case pg.K_t: 
            vP, nP, transform = next(gen_Transform)
            alle = vorher | transform
            gleich = vorher & transform
            lösche = vorher - transform
            setze = transform - vorher
          case pg.K_n: 
            vorher, nachher = next(gen_ladeAufgabe)
            vP, nP, transform = False, False, set()
            gen_Transform = nächsteTransformation()
          case pg.K_l: 
            transform = findeLösung()
            vP = nP = (-2000,-2000)
            alle = vorher | transform
            gleich = vorher & transform
            lösche = vorher - transform
            setze = transform - vorher
    
  screen.fill((0,0,0))
  zeichne(vorher,(200,200),vP,'#ffffff')
  zeichne(nachher,(700,200),nP,'#ffffff')
  if transform:
    zeichne(gleich,(1200,200),vP,'#ffffff')
    zeichne(lösche,(1200,200),vP,'#300000')
    zeichne(setze,(1200,200),vP,'#00ff00')
  pg.display.flip()
