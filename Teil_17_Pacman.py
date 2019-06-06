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

directions = {0:(1,0), 1:(-1,0), 2:(0,-1), 3:(0,1)}
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
    self.vx, self.vy = 1,0
    self.frame = 0
    self.dir = 0
    self.dir_buffer = None
  
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
    vx, vy = directions[richtung]
    i = xy2i(self.x, self.y)
    sp, ze = i % spalten, i // spalten
    sp += vx
    ze += vy
    i = ze * spalten + sp
    return grid[i] != 9

  def inSync(self,x,y):
    sync_x, sync_y = i2xy(xy2i(x,y))
    return x == sync_x and y == sync_y
  
  def changeDir(self,i):
    self.dir = i
    self.vx, self.vy = directions[i]

  def changeMode(self, modus):
    sprite, _, _ = self.sprites[self.modus]
    hideSprite(sprite)
    self.modus = modus
    self.frame = 0 
    sprite, _, _ = self.sprites[self.modus]
    moveSprite(sprite,self.x, self.y, centre= True)

    

class Ghosts(Actor):
  def __init__(self,tileset,pos):
    Actor.__init__(self)
    self.sprites = {'jagd':[makeSprite(tileset,8),2,True],
                    'flucht':[makeSprite("ghost_flucht.png",2),2,False],
                    'blink':[makeSprite("ghost_blink.png",4),4,False],
                    'die':[makeSprite("ghost_die.png",4),1, True]
                    }
    self.x,self.y = pos
    self.modus = "jagd"
  
  def update(self):
    if self.inSync(self.x, self.y):
      i = xy2i(self.x, self.y)
      if grid[i] in (5,6):
        i = i+27 if grid[i] == 5 else i-27
        self.x, self.y = i2xy(i)
        self.x, self.y = self.x+self.vx, self.y+self.vy
        return
      while True:
        dir = rnd.randrange(3)
        vx, vy = self.vx, self.vy
        if dir == 0:
          vx, vy = vy, -vx
        elif dir == 2:
          vx, vy = -vy, vx  
        dir = dir_invers[(vx, vy)]
        if self.dirGültig(dir):
          self.changeDir(dir)
          break
    self.x, self.y = self.x+self.vx, self.y+self.vy
    moveSprite(self.sprites[self.modus][0],self.x,self.y,centre=True)
    
  
class Pacman(Actor):
  def __init__(self,pos):
    Actor.__init__(self)
    self.sprites = {'run':[makeSprite("pacman_tileset2.png",12),3,True],
                    'die':[makeSprite("pacman_die.png",12),12,False]}
    self.modus = 'run'
    self.x,self.y = pos

  def update(self):
    if self.inSync(self.x,self.y):
      if self.dir_buffer != None:
        if self.dirGültig(self.dir_buffer):
          self.changeDir(self.dir_buffer)
          self.dir_buffer = None
      if not self.dirGültig(self.dir):
        return
    self.x, self.y = self.x+self.vx, self.y+self.vy
    moveSprite(self.sprites[self.modus][0],self.x,self.y,centre=True)
    
  def eatDot(self):
    global grid
    i = xy2i(self.x, self.y)
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
    

def xy2i(x,y):
  sp = round((x - raster_w / 2) / raster_w)
  ze = round((y - raster_h / 2) / raster_h)
  i = ze*spalten+sp
  return i


def i2xy(i):
  sp, ze = i % spalten, i // spalten
  x = sp * raster_w + raster_w // 2
  y = ze * raster_h + raster_h // 2
  return x,y

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
blinky = Ghosts("blinky_tileset2.png",sync(348,276))
pinky = Ghosts("pinky_tileset2.png",sync(300,348))
inky = Ghosts("inky_tileset2.png", sync(348,348))
clyde = Ghosts("clyde_tileset2.png", sync(396,348))
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