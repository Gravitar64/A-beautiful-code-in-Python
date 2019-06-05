from pygame_functions import *
import random as rnd

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
        9,9,9,9,9,9,1,9,9,0,9,9,9,6,6,9,9,9,0,9,9,1,9,9,9,9,9,9,
        9,9,9,9,9,9,1,9,9,0,9,0,0,0,0,0,0,9,0,9,9,1,9,9,9,9,9,9,
        5,0,0,0,0,0,1,0,0,0,9,0,0,0,0,0,0,9,0,0,0,1,0,0,0,0,0,5,
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

directions = {0:[1,0], 1:[-1,0], 2:[0,-1], 3:[0,1]}
dir_invers = {(1,0): 0, (-1,0): 1, (0,-1): 2, (0,1):3}

class Dot:
  def __init__(self, x, y, image):
    self.x = x
    self.y = y
    self.sprite = makeSprite(image)
    moveSprite(self.sprite,x,y,centre=True)

class Actor:
  def __init__(self):
    self.vx, self.vy = 1,0
    self.frame = 0
    self.dir = 0
    self.dir_buffer = None
  
  def changeAnimationFrame(self):
    self.frame = (self.frame+1) % self.animations + self.dir * self.animations
    changeSpriteImage(self.sprites,self.frame)

  def dirGültig(self,richtung):
    vx, vy = directions[richtung]
    i = xy2i(self.x, self.y)
    sp, ze = i % spalten, i // spalten
    sp += vx
    ze += vy
    i = ze * spalten + sp
    return grid[i] != 9

  def inSync(self,x,y):
    i = xy2i(x,y)
    sync_x, sync_y = i2xy(i)
    return x == sync_x and y == sync_y
  
  def changeDir(self,i):
    self.dir = i
    self.vx, self.vy = directions[i]
    

class Ghosts(Actor):
  def __init__(self,tileset,pos):
    Actor.__init__(self)
    self.animations = 2
    self.sprites = makeSprite(tileset,8)
    self.x,self.y = pos

  def update(self):
    if self.inSync(self.x, self.y):
      i = xy2i(self.x, self.y)
      if grid[i] == 5 and i == 392:
        i += 27
        self.x, self.y = i2xy(i)
        self.x, self.y = self.x+self.vx, self.y+self.vy
        return
      if grid[i] == 5 and i== 419:
        i -= 27
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
    moveSprite(self.sprites,self.x,self.y,centre=True)
    showSprite(self.sprites)



class Pacman(Actor):
  def __init__(self,tileset,pos):
    Actor.__init__(self)
    self.animations = 3
    self.sprites = makeSprite(tileset,12)
    self.x,self.y = pos

  def update(self):
    if self.inSync(self.x,self.y):
      if self.dir_buffer != None:
        if self.dirGültig(self.dir_buffer):
          self.changeDir(self.dir_buffer)
          self.dir_buffer = None
      else:
        if not self.dirGültig(self.dir):
          return
    self.x, self.y = self.x+self.vx, self.y+self.vy
    moveSprite(self.sprites,self.x,self.y,centre=True)
    showSprite(self.sprites)
  
  def eatDot(self):
    i = xy2i(self.x, self.y)
    if grid[i] == 1 or grid[i] == 2:
      grid[i] = 0
      killSprite(dots[i].sprite)
      del dots[i]



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
  i = xy2i(x,y)
  return i2xy(i)  

setAutoUpdate(False)
w = 672
h = 744
spalten, zeilen = w // 24, h // 24
raster_w = 24
raster_h = 24

screenSize(w,h)
setBackgroundImage("pacman3.png")
pacman = Pacman("pacman_tileset2.png",sync(321,420))
blinky = Ghosts("blinky_tileset2.png",sync(348,276))
pinky = Ghosts("pinky_tileset2.png",sync(300,348))
inky = Ghosts("inky_tileset2.png", sync(348,348))
clyde = Ghosts("clyde_tileset2.png", sync(396,348))
ghosts = [blinky, pinky, inky, clyde]

dots = {}
for i, zahl in enumerate(grid):
  if zahl == 1: 
    x,y = i2xy(i)
    dots[i] = Dot(x,y,"dot.png")
  if zahl == 2:
    x,y = i2xy(i)
    dots[i] = Dot(x,y,"bit_dot.png")  


nextFrame = clock()
while True:
  if clock() > nextFrame:
    nextFrame += 100
    pacman.changeAnimationFrame()
    for ghost in ghosts:
      ghost.changeAnimationFrame()
      
    
  fps = tick(120)
  
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
  
  for ghost in ghosts:
    ghost.update()
  pacman.eatDot()
  pacman.update()
  
    
  # for label in labels:
  #   showLabel(label)
  
  updateDisplay()
  if keyPressed("ESC"): break