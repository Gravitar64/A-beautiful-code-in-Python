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
        0,0,0,0,0,0,1,0,0,0,9,0,0,0,0,0,0,9,0,0,0,1,0,0,0,0,0,0,
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
    self.directions = {0:[1,0], 1:[-1,0], 2:[0,-1], 3:[0,1]}
  
  def changeAnimationFrame(self):
    self.frame = (self.frame+1) % self.animations + self.dir * self.animations
    changeSpriteImage(self.sprites,self.frame)

  def update(self):
    x,y = self.x+self.vx, self.y+self.vy
    i = xy2i(x,y)
    if grid[i] == 9:
      return
    self.x, self.y = x,y 
    if self.vx != 0:
      self.y = self.y // raster_h * raster_h + raster_h//2
    if self.vy != 0:
      self.x = self.x // raster_w * raster_w + raster_w//2  
    moveSprite(self.sprites,self.x,self.y,centre=True)
    showSprite(self.sprites)
    if grid[i] == 1 or grid[i] == 2:
      killSprite(dots[i].sprite)
      del dots[i]
      grid[i] = 0

  def changeDir(self,i):
    vx, vy = self.directions[i]
    self.dir = i
    self.vx, self.vy = vx, vy
    

class Ghosts(Actor):
  def __init__(self,tileset,x,y):
    Actor.__init__(self)
    self.animations = 2
    self.sprites = makeSprite(tileset,8)
    self.vx, self.vy = 0,0
    self.x,self.y = x,y


class Pacman(Actor):
  def __init__(self,tileset,x,y):
    Actor.__init__(self)
    self.animations = 3
    self.sprites = makeSprite(tileset,12)
    self.x,self.y = x,y

def xy2i(x,y):
  sp = x // raster_w
  ze = y // raster_h
  i = ze*spalten+sp
  return i


def i2xy(i):
  sp, ze = i % spalten, i // spalten
  x = sp * raster_w + raster_w // 2
  y = ze * raster_h + raster_h // 2
  return x,y

setAutoUpdate(False)
w = 672
h = 744
spalten, zeilen = w // 24, h // 24
raster_w = 24
raster_h = 24

screenSize(w,h)
setBackgroundImage("pacman3.png")
pacman = Pacman("pacman_tileset2.png",321,420)
blinky = Ghosts("blinky_tileset2.png",342,278)
pinky = Ghosts("pinky_tileset2.png",294,347)
inky = Ghosts("inky_tileset2.png", 342, 347)
clyde = Ghosts("clyde_tileset2.png", 390, 347)
ghosts = [blinky, pinky, inky, clyde]

dots = {}
for i, zahl in enumerate(grid):
  if zahl == 1: 
    x,y = i2xy(i)
    dots[i] = Dot(x,y,"dot.png")
  if zahl == 2:
    x,y = i2xy(i)
    dots[i] = Dot(x,y,"bit_dot.png")  


labels = []
for i, zahl in enumerate(grid):
    sp, ze = i % spalten, i // spalten
    x,y = sp*raster_w, ze*raster_h
    labels.append(makeLabel(str(zahl), 10, x+raster_w/2,y+raster_h/2 , fontColour='white', font='Arial', background='clear'))
    
nextFrame = clock()
while True:
  if clock() > nextFrame:
    nextFrame += 100
    pacman.changeAnimationFrame()
    for ghost in ghosts:
      ghost.changeDir(rnd.randrange(4))
      ghost.changeAnimationFrame()
      
    
  fps = tick(120)
  
  if keyPressed("right"):
    pacman.changeDir(0)
  elif keyPressed("left"):
    pacman.changeDir(1)
  elif keyPressed("up"):
    pacman.changeDir(2)
  elif keyPressed("down"):
    pacman.changeDir(3)      
  
  for dot in dots.values():
   showSprite(dot.sprite)
  
  for ghost in ghosts:
    ghost.update()
  pacman.update()
    
  # for label in labels:
  #   showLabel(label)
  
  updateDisplay()
  if keyPressed("ESC"): break