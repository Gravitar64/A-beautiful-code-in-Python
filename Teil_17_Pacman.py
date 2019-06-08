from pygame_functions import *
import random as rnd
import threading


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

directions = {0:,[(1,0),(0,-1),(0,1)] 1:[(-1,0),(0,-1),(0,1)] 2:[(0,-1),(-1,0),(1,0)] 3:[(0,1),(-1,0),(1,0)]}
dir_invers = {v:k for (k,v) in directions.items()}
grid_save = grid.copy()
dots = {}

class Dot:
  def __init__(self, x,y, image):
    self.x, self.y = x,y
    self.sprite = makeSprite(image)
    moveSprite(self.sprite,x,y,centre=True)

class Actor:
  def __init__(self):
    self.vec = (1,0)
    self.frame = 0
    self.dir = 0
    self.dir_buffer = None
    self.grid_pos = (0,0)
  
  def changeAnimationFrame(self):
    sprite, animations, je_richtung = self.sprites[self.modus]
    if je_richtung:
      self.frame = (self.frame+1) % animations + self.dir * animations
    else:
      self.frame = (self.frame+1) % animations  
    changeSpriteImage(sprite,self.frame)

  def show(self):
    showSprite(self.sprites[self.modus][0])
  
  def dirGültig(self,richtung):
    sp, zi = addVector(self.grid_pos, directions[richtung])
    i = ze * spalten + sp
    return grid[i] != 9

  def inSync(self,pos):
    sync_pos = i2xy(xy2i(pos))
    return sync_pos == pos
  
  def changeDir(self,i):
    self.dir = i
    self.vec = directions[i][0]

  def changeMode(self, modus):
    sprite, _, _ = self.sprites[self.modus]
    hideSprite(sprite)
    self.modus = modus
    self.frame = 0 
    sprite, _, _ = self.sprites[self.modus]
    moveSprite(sprite,self.x, self.y, centre= True)

    

class Ghosts(Actor):
  def __init__(self,name,tileset,pos,target):
    Actor.__init__(self)
    self.sprites = {'jagd':[makeSprite(tileset,8),2,True],
                    'flucht':[makeSprite("ghost_flucht.png",2),2,False],
                    'blink':[makeSprite("ghost_blink.png",4),4,False],
                    'die':[makeSprite("ghost_die.png",4),1, True]
                    }
    self.pos = pos
    self.modus = "jagd"
    self.target = target
    self.name = name
  
  def update(self):
    if self.inSync(self.pos):
      i = xy2i(self.pos)
      if grid[i] in (5,6):
        i = i+27 if grid[i] == 5 else i-27
        self.pos = addVector(i2xy(i), self.vec)
        return
      
      if self.name == 'blinky':
        self.target = xy2grid(pacman.pos)
      elif self.name == 'pinky':
        vx, vy = pacman.vec
        vx *= 4
        vy *= 4
        neue_pos = addVector(pacman.pos, (vx,vy))
        self.target = xy2grid(neue_pos)    
      min_abstand = 999
      for pos in directions[self.dir]
        sp,ze = addVector((i % spalten, i // spalten), pos)
        i = ze * spalten + sp
        if grid[i] != 9:
          abstand = abs(sp-target[0])+abs(ze-target[1])
          if abstand < min_abstand:
            min_abstand = abstand
            best_richtung = dir_invers[(vx, vy)]
        self.changeDir(best_richtung)
          
    self.pos = addVector(self.pos, self.vec)
    self.grid_pos = xy2grid((self.pos)
    moveSprite(self.sprites[self.modus][0],self.x,self.y,centre=True)
    
  
class Pacman(Actor):
  def __init__(self,pos):
    Actor.__init__(self)
    self.sprites = {'run':[makeSprite("pacman_tileset2.png",12),3,True],
                    'die':[makeSprite("pacman_die.png",12),12,False]}
    self.modus = 'run'
    self.pos = pos

  def update(self):
    if self.inSync(pos):
      if self.dir_buffer != None:
        if self.dirGültig(self.dir_buffer):
          self.changeDir(self.dir_buffer)
          self.dir_buffer = None
      if not self.dirGültig(self.dir):
        return
    self.pos = addVector (self.pos, self.vec)
    self.grid_pos = xy2grid(self.pos)
    moveSprite(self.sprites[self.modus][0],self.x,self.y,centre=True)
    
  def eatDot(self):
    global grid
    i = xy2i(self.pos)
    if grid[i] in (1,2):
      if grid[i] == 2:
        changeGhostMode('flucht')
      grid[i] = 0
      killSprite(dots[i].sprite)
      del dots[i]
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
    
def addVector(pos, vec):
  return pos[0]+vec[0], pos[1]+vec[1]

def xy2i(pos):
  sp, ze = pos
  sp = round((x - raster_w / 2) / raster_w)
  ze = round((y - raster_h / 2) / raster_h)
  i = ze*spalten+sp
  return i


def i2xy(i):
  sp, ze = i % spalten, i // spalten
  x = sp * raster_w + raster_w // 2
  y = ze * raster_h + raster_h // 2
  return x,y

def xy2grid(pos):
  x,y = pos
  sp = round((x - raster_w / 2) / raster_w)
  ze = round((y - raster_h / 2) / raster_h)
  return sp, ze  

def sync(x,y):
  return i2xy(xy2i(x,y)) 

def nextPacman():
  pacman.x, pacman.y = sync(321,420)
  blinky.x, blinky.y = sync(335,276)
  pinky.x, pinky.y = sync(300,348)
  inky.x, inky.y = sync(348,348)
  clyde.x, clyde.y = sync(396,348)
  for ghost in ghosts:
    sprite = ghost.sprites[ghost.modus][0]
    hideSprite(sprite)
    ghost.modus = 'jagd'
    sprite = ghost.sprites[ghost.modus][0]
    moveSprite(sprite,ghost.x, ghost.y, centre=True)
  pacman.changeMode('run')
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
setBackgroundImage("pacman3.png")
pacman = Pacman(sync(321,420))
blinky = Ghosts("blinky_tileset2.png",'blinky'sync(348,276), xy2grid(pacman.pos))
pinky = Ghosts("pinky_tileset2.png",'pinky',sync(300,348), (14,14))
inky = Ghosts("inky_tileset2.png", 'inky', sync(348,348), (14,14))
clyde = Ghosts("clyde_tileset2.png", 'clyde', sync(396,348), (14,14))
ghosts = [blinky, pinky, inky, clyde]




def dotsAufbauen():
  global dots
  dots = {}
  for i, zahl in enumerate(grid):
    if zahl == 1: 
      x,y = i2xy(i)
      dots[i] = Dot(x,y,"dot.png")
    if zahl == 2:
      x,y = i2xy(i)
      dots[i] = Dot(x,y,"bit_dot.png")  


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
      gh_sprite = ghost.sprites[ghost.modus][0]
      if touching(gh_sprite, pacman.sprites[pacman.modus][0]):
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