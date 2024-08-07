import Teil_17_pygame_functions as pgf
import random as rnd
import threading


spielraster = [ 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,
                9, 1, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 1, 9,
                9, 2, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 2, 9,
                9, 1, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 1, 9,
                9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,
                9, 1, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 1, 9,
                9, 1, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 1, 9,
                9, 1, 1, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 1, 1, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 0, 9, 9, 9, 7, 7, 9, 9, 9, 0, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                5, 0, 0, 0, 0, 0, 1, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 1, 0, 0, 0, 0, 0, 6,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 1, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 1, 9, 9, 9, 9, 9, 9,
                9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,
                9, 1, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 1, 9,
                9, 1, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 1, 9,
                9, 2, 1, 1, 9, 9, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 9, 9, 1, 1, 2, 9,
                9, 9, 9, 1, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 1, 9, 9, 9,
                9, 9, 9, 1, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 1, 9, 9, 9,
                9, 1, 1, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 1, 1, 9,
                9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9,
                9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9,
                9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,
                9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]


def i2xy(i):
  sp, ze = i % spalten, i // spalten
  return sp * raster + raster // 2, ze * raster + raster // 2

def xy2i(x,y):
  sp, ze = (x - raster // 2) // raster, (y - raster // 2) // raster 
  return ze * spalten + sp  


class Punkt:
  def __init__(self, pos, bilddatei):
    self.x, self.y = pos
    self.sprite = pgf.makeSprite(bilddatei)
    pgf.moveSprite(self.sprite,self.x, self.y, centre=True)

class Figur:
  def __init__(self, name, pos):
    self.name = name
    self.x, self.y = pos
    self.richtung = 0
    self.rx, self.ry = 1,0
    self.modus = 'jagd'
    self.bildNr = 0
    self.aufRaster = False
    self.i = 355

  def anzeige(self):
    pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
    pgf.showSprite(self.sprite)

  def bewege(self):
    self.x += self.rx 
    self.y += self.ry
    self.i = xy2i(self.x, self.y)
    x2, y2 = i2xy(self.i)
    self.aufRaster = self.x == x2 and self.y == y2

  def warp(self):
    if spielraster[self.i] not in (5,6): return False
    self.i = self.i + 27 if spielraster[self.i] == 5 else self.i - 27
    self.x, self.y = i2xy(self.i)
    return True    
    
  def richtungGültig(self, richtung):
    rx, ry = richtungen[richtung]
    i = self.i + rx + ry * spalten
    return spielraster[i] != 9

  def ändereModus(self, modus):
    pgf.hideSprite(self.sprite)
    self.modus = modus
    self.sprite = self.sprites[modus][0]
    self.bildNr = 0

  def ändereRichtung(self, richtung):
    if self.richtungGültig(richtung):
      self.richtung = richtung
      self.rx, self.ry = richtungen[richtung]
      return True

  def animiere(self):
    sprite, animationsbilder, richtungsabhängig = self.sprites[self.modus]
    self.bildNr = (self.bildNr + 1) % animationsbilder
    if richtungsabhängig:
      self.bildNr += animationsbilder * self.richtung
    pgf.changeSpriteImage(sprite, self.bildNr)   

class Pacman(Figur):
  def __init__(self, name, pos):
    Figur.__init__(self, name, pos)
    self.sprites = {'jagd': [pgf.makeSprite('Teil_17_Pacman_Tileset.png',12),3,True],
                    'tot' : [pgf.makeSprite('Teil_17_pacman_die.png',12),12,False]}
    self.sprite = self.sprites[self.modus][0]
    self.tastaturspeicher = 0  

  def bewegungslogik(self):
    if not self.aufRaster: return
    if self.warp(): return  
    self.punkteFressen()
    self.ändereRichtung(self.tastaturspeicher)
    if not self.richtungGültig(self.richtung):
      self.rx, self.ry = 0,0

  def punkteFressen(self):
    if spielraster[self.i] not in (1,2): return
    if spielraster[self.i] == 2:
      ändereModusGeister('flucht')
    spielraster[self.i] = 0
    pgf.killSprite(punkte[self.i].sprite)
    del punkte[self.i]


                  

class Geist(Figur):
  def __init__(self, name, pos, bilddatei):
    Figur.__init__(self, name, pos)
    self.sprites = {'jagd': [pgf.makeSprite(bilddatei,8),2,True],
                    'flucht' : [pgf.makeSprite('Teil_17_Ghost_flucht.png',2),2,False],
                    'blink' : [pgf.makeSprite('Teil_17_Ghost_blink.png',4),4,False],
                    'tot' : [pgf.makeSprite('Teil_17_Ghost_die.png',4),1,True]}
    self.sprite = self.sprites[self.modus][0]

  def bewegungslogik(self):
    if not self.aufRaster: return
    if self.warp(): return  
    while True:
      while True: 
        neueRichtung = rnd.randrange(4)
        if self.richtung == 0 and neueRichtung != 1 or \
           self.richtung == 1 and neueRichtung != 0 or \
           self.richtung == 2 and neueRichtung != 3 or \
           self.richtung == 3 and neueRichtung != 2:
          break #abbruch der 2ten While-Schleife
      if self.ändereRichtung(neueRichtung):
        break #abbruch der 1sten While-Schleife


def punkteSetzen():
  punkte = {}
  for i, zahl in enumerate(spielraster):
    if zahl not in (1,2): continue
    punkte[i] = Punkt(i2xy(i),'Teil_17_Punkt.png') if zahl == 1 else Punkt(i2xy(i),'Teil_17_Punkt_gross.png')
    pgf.showSprite(punkte[i].sprite)  
  return punkte

def ändereModusGeister(modus):
  for figur in figuren:
    if figur.name == 'pacman': continue
    if figur.modus != 'tot':
      figur.ändereModus(modus)
  if modus == 'flucht':
    timer1 = threading.Timer(5, ändereModusGeister, ('blink',)).start()    
    timer2 = threading.Timer(8, ändereModusGeister, ('jagd',)).start()  

richtungen = {0:(1,0), 1:(-1,0), 2:(0,-1), 3:(0,1)}
breite, höhe = 672, 744
raster = 24
spalten, zeilen = breite // raster, höhe // raster
pgf.screenSize(breite, höhe)
pgf.setBackgroundImage('Teil_17_Spielfeld.png')
pgf.setAutoUpdate(False)

punkte = punkteSetzen()
pacman = Pacman('pacman', (336,564))
blinky = Geist('blinky', (360,276), 'Teil_17_Blinky_tileset.png')
pinky = Geist('pinky', (300,348), 'Teil_17_pinky_tileset.png')
inky = Geist('inky', (348,348), 'Teil_17_inky_tileset.png')
clyde = Geist('clyde', (396,348), 'Teil_17_clyde_tileset.png')
figuren = [pacman, blinky, pinky, inky, clyde]

nächsteAnimation = pgf.clock() + 100

while True:
  pgf.tick(120)
  if pgf.keyPressed('right'): pacman.tastaturspeicher = 0
  if pgf.keyPressed('left'): pacman.tastaturspeicher = 1 
  if pgf.keyPressed('up'): pacman.tastaturspeicher = 2
  if pgf.keyPressed('down'): pacman.tastaturspeicher = 3
  for figur in figuren:
    if pgf.clock() > nächsteAnimation:
      figur.animiere()
    figur.bewegungslogik()
    figur.bewege()
    figur.anzeige()
    if figur.name != 'pacman':
      if figur.i == pacman.i:
        if figur.modus in ('flucht', 'blink'): figur.ändereModus('tot')
        if figur.modus == ('jagd'): pacman.ändereModus('tot')  
  if pgf.clock() > nächsteAnimation:
    nächsteAnimation += 100

  pgf.updateDisplay()
  if pgf.keyPressed('ESC'):
    break
