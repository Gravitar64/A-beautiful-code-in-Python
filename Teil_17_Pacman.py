from pygame_functions import *
import random as rnd
import threading
from Teil_17_Vector import Vector


grid = [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
        9,1,1,1,1,1,1,1,1,1,1,1,1,9,9,1,1,1,1,1,1,1,1,1,1,1,1,9,
        9,1,9,9,9,9,1,9,9,9,9,9,1,9,9,1,9,9,9,9,9,1,9,9,9,9,1,9,
        9,2,9,9,9,9,1,9,9,9,9,9,1,9,9,1,9,9,9,9,9,1,9,9,9,9,2,9,
        9,1,9,9,9,9,1,9,9,9,9,9,1,9,9,1,9,9,9,9,9,1,9,9,9,9,1,9,
        9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,
        9,1,9,9,9,9,1,9,9,1,9,9,9,9,9,9,9,9,1,9,9,1,9,9,9,9,1,9,
        9,1,9,9,9,9,1,9,9,1,9,9,9,9,9,9,9,9,1,9,9,1,9,9,9,9,1,9,
        9,1,1,1,1,1,1,9,9,1,1,1,1,9,9,1,1,1,1,9,9,1,1,1,1,1,1,9,
        9,9,9,9,9,9,1,9,9,9,9,9,0,9,9,0,9,9,9,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,9,9,9,0,9,9,0,9,9,9,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,0,0,0,0,0,0,0,0,0,0,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,0,9,9,9,7,7,9,9,9,0,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,0,9,0,0,0,0,0,0,9,0,9,9,1,9,9,9,9,9,9,
        5,0,0,0,0,0,1,0,0,0,9,0,0,0,0,0,0,9,0,0,0,1,0,0,0,0,0,6,
        9,9,9,9,9,9,1,9,9,0,9,0,0,0,0,0,0,9,0,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,0,9,9,9,9,9,9,9,9,0,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,0,0,0,0,0,0,0,0,0,0,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,0,9,9,9,9,9,9,9,9,0,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,0,9,9,9,9,9,9,9,9,0,9,9,1,9,9,9,9,9,9,
        9,1,1,1,1,1,1,1,1,1,1,1,1,9,9,1,1,1,1,1,1,1,1,1,1,1,1,9,
        9,1,9,9,9,9,1,9,9,9,9,9,1,9,9,1,9,9,9,9,9,1,9,9,9,9,1,9,
        9,1,9,9,9,9,1,9,9,9,9,9,1,9,9,1,9,9,9,9,9,1,9,9,9,9,1,9,
        9,2,1,1,9,9,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,9,9,1,1,2,9,
        9,9,9,1,9,9,1,9,9,1,9,9,9,9,9,9,9,9,1,9,9,1,9,9,1,9,9,9,
        9,9,9,1,9,9,1,9,9,1,9,9,9,9,9,9,9,9,1,9,9,1,9,9,1,9,9,9,
        9,1,1,1,1,1,1,9,9,1,1,1,1,9,9,1,1,1,1,9,9,1,1,1,1,1,1,9,
        9,1,9,9,9,9,9,9,9,9,9,9,1,9,9,1,9,9,9,9,9,9,9,9,9,9,1,9,
        9,1,9,9,9,9,9,9,9,9,9,9,1,9,9,1,9,9,9,9,9,9,9,9,9,9,1,9,
        9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,
        9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]

directions = {0:(1,0), 1:(-1,0), 2:(0,-1), 3:(0,1)}
dir_invers = {v:k for (k,v) in directions.items()}
grid_save = grid.copy()
dots = {}

class Dot:
  def __init__(self, pos, image):
    self.pos = pos
    self.grid = pos2grid(self.pos)
    self.i = grid2i(self.grid)
    self.sprite = makeSprite(image)
    moveSprite(self.sprite,pos,centre=True)

class Actor:
  def __init__(self,pos):
    self.pos = pos
    self.richtung = Vector(1,0)
    self.frame = 0
    self.dir = 0
    self.dir_buffer = None
    self.grid = pos2grid(self.pos)
    self.i = grid2i(self.grid)
  
  def changeAnimationFrame(self):
    sprite, animations, je_richtung = self.sprites[self.modus]
    if je_richtung:
      self.frame = (self.frame+1) % animations + self.dir * animations
    else:
      self.frame = (self.frame+1) % animations  
    changeSpriteImage(sprite,self.frame)

  def show(self):
    showSprite(self.sprites[self.modus][0])
  
  def dirGültig(self,dir):
    richtung = Vector(*directions[dir])
    sp, ze = richtung + self.grid
    i = ze * spalten + sp
    return grid[i] != 9

  def inSync(self,pos):
    pos2 = i2xy(xy2i(pos))
    return pos == pos2
  
  def changeDir(self,i):
    self.dir = i
    self.richtung = Vector(*directions[i])

  def changeMode(self, modus):
    sprite, _, _ = self.sprites[self.modus]
    hideSprite(sprite)
    self.modus = modus
    self.frame = 0 
    sprite, _, _ = self.sprites[self.modus]
    moveSprite(sprite,self.pos, centre= True)

    

class Ghosts(Actor):
  def __init__(self,tileset,pos):
    Actor.__init__(self,pos)
    self.sprites = {'jagd':[makeSprite(tileset,8),2,True],
                    'flucht':[makeSprite("ghost_flucht.png",2),2,False],
                    'blink':[makeSprite("ghost_blink.png",4),4,False],
                    'die':[makeSprite("ghost_die.png",4),1, True]
                    }
    self.modus = "jagd"
  
  def update(self):
    if self.inSync(self.pos):
      if grid[self.i] in (5,6):
        self.i = self.i+27 if grid[self.i] == 5 else self.i-27
        self.pos = i2xy(self.i)
        self.pos += self.richtung
        self.grid = pos2grid(self.pos)
        return
      while True:
        dir = rnd.randrange(3)
        vx, vy = self.richtung
        if dir == 0:
          vx, vy = vy, -vx
        elif dir == 2:
          vx, vy = -vy, vx  
        dir = dir_invers[(vx, vy)]
        if self.dirGültig(dir):
          self.changeDir(dir)
          break
    self.pos += self.richtung
    self.grid = pos2grid(self.pos)
    self.i = grid2i(self.grid)
    moveSprite(self.sprites[self.modus][0],self.pos,centre=True)
    
  
class Pacman(Actor):
  def __init__(self,pos):
    Actor.__init__(self,pos)
    self.sprites = {'run':[makeSprite("pacman_tileset2.png",12),3,True],
                    'die':[makeSprite("pacman_die.png",12),12,False]}
    self.modus = 'run'
    

  def update(self):
    if self.inSync(self.pos):
      if grid[self.i] in (5,6):
        self.i = self.i+27 if grid[self.i] == 5 else self.i-27
        self.pos = i2xy(self.i)
        self.pos += self.richtung
        self.grid = pos2grid(self.pos)
        return
      if self.dir_buffer != None:
        if self.dirGültig(self.dir_buffer):
          self.changeDir(self.dir_buffer)
          self.dir_buffer = None
      if not self.dirGültig(self.dir):
        return
    self.pos += self.richtung
    self.grid = pos2grid(self.pos)
    self.i = grid2i(self.grid)
    moveSprite(self.sprites[self.modus][0],self.pos,centre=True)
    
  def eatDot(self):
    global grid
    if grid[self.i] in (1,2):
      if grid[self.i] == 2:
        changeGhostMode('flucht')
      grid[self.i] = 0
      killSprite(dots[self.i].sprite)
      del dots[self.i]
    if not dots:
      changeGameStatus('nextLevel')
      timer2 = threading.Timer(1.2, nextPacman)
      timer2.start()
      grid = grid_save.copy()
      dotsAufbauen()



def changeGhostMode(modus):
  for ghost in ghosts:
    if ghost.modus != 'die':
      ghost.changeMode(modus)
  if modus == 'flucht':
    timer1 = threading.Timer(5.0, changeGhostMode, ('blink',)) 
    timer2 = threading.Timer(8.0, changeGhostMode, ('jagd',))
    timer1.start()
    timer2.start()
    

def xy2i(pos):
  x,y = pos
  sp = round((x - raster_w / 2) / raster_w)
  ze = round((y - raster_h / 2) / raster_h)
  i = ze*spalten+sp
  return i


def i2xy(i):
  sp, ze = i % spalten, i // spalten
  x = sp * raster_w + raster_w // 2
  y = ze * raster_h + raster_h // 2
  return Vector(x,y)

def sync(pos):
  return i2xy(xy2i(pos))

def pos2grid(pos):
  i = xy2i(pos)
  return Vector(i % spalten, i // spalten)

def grid2i(pos):
  sp, ze = pos
  return ze * spalten + sp  

def nextPacman():
  pacman.pos = sync(Vector(321,420))
  blinky.pos = sync(Vector(335,276))
  pinky.pos = sync(Vector(300,348))
  inky.pos = sync(Vector(348,348))
  clyde.pos = sync(Vector(396,348))
  for ghost in ghosts:
    sprite = ghost.sprites[ghost.modus][0]
    hideSprite(sprite)
    ghost.modus = 'jagd'
    sprite = ghost.sprites[ghost.modus][0]
    moveSprite(sprite,ghost.pos,centre=True)
  pacman.changeMode('run')
  pacman.changeDir(0)
  timer1 = threading.Timer(1.5, changeGameStatus, ('run',))
  timer1.start()

def changeGameStatus(status):
  global game_status
  game_status = status



setAutoUpdate(False)
w = 672
h = 744
spalten, zeilen = w // 24, h // 24
raster_w = 24
raster_h = 24
zellen = spalten * zeilen

screenSize(w,h)
setBackgroundImage("Teil_17_pacman.png")
pacman = Pacman(sync(Vector(321,420)))
blinky = Ghosts("blinky_tileset2.png",sync(Vector(348,276)))
pinky = Ghosts("pinky_tileset2.png",sync(Vector(300,348)))
inky = Ghosts("inky_tileset2.png", sync(Vector(348,348)))
clyde = Ghosts("clyde_tileset2.png", sync(Vector(396,348)))
ghosts = [blinky, pinky, inky, clyde]




def dotsAufbauen():
  global dots
  dots = {}
  for i, zahl in enumerate(grid):
    pos = i2xy(i)
    if zahl == 1: 
      dots[i] = Dot(pos,"dot.png")
    elif zahl == 2:
      dots[i] = Dot(pos,"bit_dot.png")  


nextFrame = clock()
game_status = "run"
dotsAufbauen()
while True:
  if clock() > nextFrame:
    nextFrame += 100
    for ghost in ghosts:
      ghost.changeAnimationFrame()
    pacman.changeAnimationFrame()

  fps = tick(120)
  
  if game_status == "run":
    if keyPressed("right"):
      pacman.dir_buffer = 0
    elif keyPressed("left"):
      pacman.dir_buffer = 1
    elif keyPressed("up"):
      pacman.dir_buffer = 2
    elif keyPressed("down"):
      pacman.dir_buffer = 3   
  
    for dot in dots.values():
      showSprite(dot.sprite)

    pacman.eatDot()
    pacman.update()
    
    for ghost in ghosts:
      ghost.update()
      if ghost.grid == pacman.grid:
        if ghost.modus == "jagd" and pacman.modus == 'run':
          pacman.changeMode('die')
          changeGameStatus('dead')
          timer2 = threading.Timer(1.2, nextPacman)
          timer2.start()

        if ghost.modus in ("flucht", "blink"):
          ghost.changeMode('die')
    
  for ghost in ghosts: ghost.show()
  pacman.show()  
  updateDisplay()
  if keyPressed("ESC"): break