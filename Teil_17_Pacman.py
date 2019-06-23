import Teil_17_pygame_functions as pgf
import random as rnd
import threading


grid = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
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


class Dot():
  def __init__(self, pos, image):
    self.x, self.y = pos
    self.sprite = pgf.makeSprite(image)
    pgf.moveSprite(self.sprite, self.x, self.y, centre=True)


class Actor():
  def __init__(self, name, pos):
    self.x, self.y = pos
    self.vx, self.vy = 1, 0
    self.dir = 0
    self.frame = 0
    self.name = name
    self.animationFrames = 0
    self.modus = 'jagd'
    self.i = 355

  def show(self):
    pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
    pgf.showSprite(self.sprite)

  def changeAnimationFrame(self):
    _, animationFrames, richtungsabhängig = self.sprites[self.modus]
    if richtungsabhängig:
      self.frame = (self.frame + 1) % animationFrames + \
          self.dir * animationFrames
    else:
      self.frame = (self.frame + 1) % animationFrames
    pgf.changeSpriteImage(self.sprite, self.frame)

  def update(self):
    self.x += self.vx
    self.y += self.vy
    sp, ze = (self.x - rasterxy // 2) // rasterxy, (self.y - rasterxy // 2) // rasterxy
    self.i = ze * spalten + sp

  def changeDir(self, dir):
    if self.richtungGültig(dir):
      self.dir = dir
      self.vx, self.vy = richtungen[dir]
      return True

  def aufRaster(self):
    sp, ze = (self.x - rasterxy // 2) // rasterxy, (self.y -
                                                    rasterxy // 2) // rasterxy
    x2, y2 = sp * rasterxy + rasterxy // 2, ze * rasterxy + rasterxy // 2
    return self.x == x2 and self.y == y2

  def richtungGültig(self, dir):
    sp, ze = (self.x - rasterxy // 2) // rasterxy, (self.y -
                                                    rasterxy // 2) // rasterxy
    vx, vy = richtungen[dir]
    sp += vx
    ze += vy
    i = ze * spalten + sp
    return grid[i] != 9

  def warp(self):
    if grid[self.i] in  (5,6):
      if grid[self.i] == 5:
        self.i += 27
      else:
        self.i -= 27
      sp, ze = self.i % spalten, self.i // spalten
      self.x, self.y = sp * rasterxy + rasterxy // 2, ze * rasterxy + rasterxy // 2
      return True

  def ändereModus(self, modus):
    pgf.hideSprite(self.sprite)
    self.modus = modus
    self.sprite = self.sprites[modus][0]
    self.frame = 0    



class Pacman(Actor):
  def __init__(self, name, pos):
    Actor.__init__(self, name, pos)
    self.sprites = {'jagd': [pgf.makeSprite('./Teil_17_Pacman_Tileset.png', 12), 3, True],
                    'tot': [pgf.makeSprite('./Teil_17_pacman_die.png', 12), 12, False]}
    self.sprite = self.sprites[self.modus][0]
    self.keybuffer = 0

  def bewegungslogik(self):
    if self.aufRaster():
      self.punkteFressen()
      if self.warp():
        return
      self.changeDir(self.keybuffer)
      if not self.richtungGültig(self.dir):
        self.vx, self.vy = 0, 0

  def punkteFressen(self):
    if grid[self.i] == 2:
      ändereModusGeister('flucht')
    if grid[self.i] in (1,2):
      grid[self.i] = 0
      pgf.killSprite(dots[self.i].sprite)
      del dots[self.i]      


class Ghosts(Actor):
  def __init__(self, name, tileset, pos):
    Actor.__init__(self, name, pos)
    self.sprites = {'jagd': [pgf.makeSprite(tileset, 8), 2, True],
                    'tot': [pgf.makeSprite('./Teil_17_Ghost_die.png', 4), 1, True],
                    'blink': [pgf.makeSprite('./Teil_17_Ghost_blink.png', 4), 4, False],
                    'flucht': [pgf.makeSprite('./Teil_17_Ghost_flucht.png', 2), 2, False]}
    self.sprite = self.sprites[self.modus][0]

  def bewegungslogik(self):
    if self.aufRaster():
      if self.warp():
        return
      while True:
        while True:
          neueRichtung = rnd.randrange(4)
          if self.dir == 0 and neueRichtung != 1 or \
             self.dir == 1 and neueRichtung != 0 or \
             self.dir == 2 and neueRichtung != 3 or \
             self.dir == 3 and neueRichtung != 2:
            break
        if self.changeDir(neueRichtung):
          break

def ändereModusGeister(modus):
  for actor in actors:
    if actor.name == 'pacman': continue
    actor.ändereModus(modus)
  if modus == 'flucht':
    timer1 = threading.Timer(5,ändereModusGeister,('blink',)).start()  
    timer2 = threading.Timer(8,ändereModusGeister,('jagd',)).start()

def punkteSetzen():
  dots = {}
  for i, zahl in enumerate(grid):
    if zahl == 1:
      sp, ze = i % spalten, i // spalten
      x, y = sp * rasterxy + rasterxy // 2, ze * rasterxy + rasterxy // 2
      dots[i] = Dot((x, y), './Teil_17_dot.png')
      pgf.showSprite(dots[i].sprite)
    elif zahl == 2:
      sp, ze = i % spalten, i // spalten
      x, y = sp * rasterxy + rasterxy // 2, ze * rasterxy + rasterxy // 2
      dots[i] = Dot((x, y), './Teil_17_dot_big.png')
      pgf.showSprite(dots[i].sprite)
  return dots


richtungen = {0: (1, 0), 1: (-1, 0), 2: (0, -1), 3: (0, 1)}
breite, höhe = 672, 744
pgf.screenSize(breite, höhe)
rasterxy = 24
pgf.setBackgroundImage('./Teil_17_Spielfeld.png')
pgf.setAutoUpdate(False)
spalten, zeilen = breite // rasterxy, höhe // rasterxy

pacman = Pacman('pacman', (336, 564))
blinky = Ghosts('blinky', './Teil_17_Blinky_tileset.png', (360, 276))
pinky = Ghosts('pinky', './Teil_17_pinky_tileset.png', (300, 348))
inky = Ghosts('inky', './Teil_17_inky_tileset.png', (348, 348))
clyde = Ghosts('clyde', './Teil_17_clyde_tileset.png', (396, 348))
nextAnimation = pgf.clock() + 100

actors = [pacman, blinky, pinky, clyde, inky]
dots = punkteSetzen()

while True:
  pgf.tick(120)
  if pgf.keyPressed('right'):
    pacman.keybuffer = 0
  elif pgf.keyPressed('left'):
    pacman.keybuffer = 1
  elif pgf.keyPressed('up'):
    pacman.keybuffer = 2
  elif pgf.keyPressed('down'):
    pacman.keybuffer = 3
  for actor in actors:
    if pgf.clock() > nextAnimation:
      actor.changeAnimationFrame()
    actor.bewegungslogik()
    actor.update()
    actor.show()
    if actor.name != 'pacman':
      if actor.i == pacman.i:
        if actor.modus in ('flucht', 'blink'):
          actor.ändereModus('tot')
        if actor.modus == 'jagd':
          pacman.ändereModus('tot')  
  if pgf.clock() > nextAnimation:
    nextAnimation += 100

  pgf.updateDisplay()
  if pgf.keyPressed('ESC'):
    break
