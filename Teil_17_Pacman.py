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

directions = {0: (1, 0), 1: (-1, 0), 2: (0, -1), 3: (0, 1)}
dir_invers = {v: k for (k, v) in directions.items()}
grid_save = grid.copy()
dots = {}


class Dot:
  def __init__(self, x, y, image):
    self.x, self.y = x, y
    self.sprite = pgf.makeSprite(image)
    pgf.moveSprite(self.sprite, x, y, centre=True)


class Actor:
  def __init__(self, name, pos):
    self.x, self.y = pos
    self.vx, self.vy = 1, 0
    self.frame = 0
    self.dir = 0
    self.dir_buffer = None
    self.name = name

  def changeAnimationFrame(self):
    sprite, animations, je_richtung = self.sprites[self.modus]
    if je_richtung:
      self.frame = (self.frame+1) % animations + self.dir * animations
    else:
      self.frame = (self.frame+1) % animations
    pgf.changeSpriteImage(sprite, self.frame)

  def show(self):
    pgf.showSprite(self.sprite)

  def dirGültig(self, richtung):
    vx, vy = directions[richtung]
    i = xy2i(self.x, self.y)
    sp, ze = i % spalten, i // spalten
    sp += vx
    ze += vy
    i = ze * spalten + sp
    return grid[i] != 9

  def inSync(self, x, y):
    sync_x, sync_y = i2xy(xy2i(x, y))
    return x == sync_x and y == sync_y

  def changeDir(self, i):
    self.dir = i
    self.vx, self.vy = directions[i]

  def changeMode(self, modus):
    pgf.hideSprite(self.sprite)
    self.modus = modus
    self.frame = 0
    self.sprite = self.sprites[self.modus][0]
    pgf.moveSprite(self.sprite, self.x, self.y, centre=True)


class Ghosts(Actor):
  def __init__(self, name, tileset, pos):
    Actor.__init__(self, name, pos)
    self.sprites = {'jagd': [pgf.makeSprite(tileset, 8), 2, True],
                    'flucht': [pgf.makeSprite("Teil_17_ghost_flucht.png", 2), 2, False],
                    'blink': [pgf.makeSprite("Teil_17_ghost_blink.png", 4), 4, False],
                    'die': [pgf.makeSprite("Teil_17_ghost_die.png", 4), 1, True]
                    }
    self.modus = "jagd"
    self.sprite = self.sprites[self.modus][0]

  def update(self):
    if self.inSync(self.x, self.y):
      if warp(self):
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
    pgf.moveSprite(self.sprite, self.x, self.y, centre=True)


class Pacman(Actor):
  def __init__(self, name, pos):
    Actor.__init__(self, name, pos)
    self.sprites = {'jagd': [pgf.makeSprite("Teil_17_pacman_tileset.png", 12), 3, True],
                    'die': [pgf.makeSprite("Teil_17_pacman_die.png", 12), 12, False]}
    self.modus = 'jagd'
    self.sprite = self.sprites[self.modus][0]

  def update(self):
    if self.inSync(self.x, self.y):
      if warp(self):
        return
      if self.dir_buffer != None:
        if self.dirGültig(self.dir_buffer):
          self.changeDir(self.dir_buffer)
          self.dir_buffer = None
      if not self.dirGültig(self.dir):
        return
    self.x, self.y = self.x+self.vx, self.y+self.vy
    pgf.moveSprite(self.sprite, self.x, self.y, centre=True)

  def eatDot(self):
    global grid
    i = xy2i(self.x, self.y)
    if grid[i] in (1, 2):
      if grid[i] == 2:
        changeGhostMode('flucht')
      grid[i] = 0
      pgf.killSprite(dots[i].sprite)
      del dots[i]
    if not dots:
      changeGameStatus('nextLevel')
      timer2 = threading.Timer(1.2, nextPacman)
      timer2.start()
      grid = grid_save.copy()
      dotsAufbauen()


def changeGhostMode(modus):
  for actor in actors:
    if actor.name == 'pacman':
      continue
    if actor.modus != 'die':
      actor.changeMode(modus)
  if modus == 'flucht':
    timer_ghost_blink = threading.Timer(5.0, changeGhostMode, ('blink',)).start()
    timer_ghost_jagd = threading.Timer(8.0, changeGhostMode, ('jagd',)).start()
    


def xy2i(x, y):
  sp = round((x - raster_w / 2) / raster_w)
  ze = round((y - raster_h / 2) / raster_h)
  i = ze*spalten+sp
  return i


def i2xy(i):
  sp, ze = i % spalten, i // spalten
  x = sp * raster_w + raster_w // 2
  y = ze * raster_h + raster_h // 2
  return x, y


def sync(x, y):
  return i2xy(xy2i(x, y))


def nextPacman():
  pacman.x, pacman.y = 336, 564
  blinky.x, blinky.y = 336, 276
  blinky.changeDir(0)
  pinky.x, pinky.y = sync(300, 348)
  inky.x, inky.y = sync(348, 348)
  clyde.x, clyde.y = sync(396, 348)
  for actor in actors:
    actor.changeMode('jagd')
  pacman.changeDir(0)
  timer_game_run = threading.Timer(1.5, changeGameStatus, ('run',)).start()


def changeGameStatus(status):
  global game_status
  game_status = status


def dotsAufbauen():
  global dots
  dots = {}
  for i, zahl in enumerate(grid):
    if zahl == 1:
      x, y = i2xy(i)
      dots[i] = Dot(x, y, "Teil_17_dot.png")
    if zahl == 2:
      x, y = i2xy(i)
      dots[i] = Dot(x, y, "Teil_17_dot_big.png")


def warp(actor):
  i = xy2i(actor.x, actor.y)
  if grid[i] in (5, 6):
    i = i+27 if grid[i] == 5 else i-27
    actor.x, actor.y = i2xy(i)
    actor.x, actor.y = actor.x+actor.vx, actor.y+actor.vy
    return True


pgf.setAutoUpdate(False)
w = 672
h = 744
spalten, zeilen = w // 24, h // 24
raster_w = 24
raster_h = 24
zellen = spalten * zeilen

pgf.screenSize(w, h)
pgf.setBackgroundImage("Teil_17_Spielfeld.png")
pacman = Pacman("pacman", (336, 564))
blinky = Ghosts("blinky", "Teil_17_blinky_tileset.png", (360, 276))
pinky = Ghosts("pinky", "Teil_17_pinky_tileset.png", sync(300, 348))
inky = Ghosts("inky", "Teil_17_inky_tileset.png", sync(348, 348))
clyde = Ghosts("clyde", "Teil_17_clyde_tileset.png", sync(396, 348))
actors = [pacman, blinky, pinky, inky, clyde]

nextFrame = pgf.clock()
game_status = "run"
dotsAufbauen()
while True:
  if pgf.clock() > nextFrame:
    nextFrame += 100
    for actor in actors:
      actor.changeAnimationFrame()

  fps = pgf.tick(120)

  if game_status == "run":
    if pgf.keyPressed("right"):
      pacman.dir_buffer = 0
    elif pgf.keyPressed("left"):
      pacman.dir_buffer = 1
    elif pgf.keyPressed("up"):
      pacman.dir_buffer = 2
    elif pgf.keyPressed("down"):
      pacman.dir_buffer = 3

    for dot in dots.values():
      pgf.showSprite(dot.sprite)

    for actor in actors:
      actor.update()
      if actor.name == 'pacman':
        actor.eatDot()
      else:
        if pgf.touching(actor.sprite, pacman.sprite):
          if actor.modus == pacman.modus:
            pacman.changeMode('die')
            changeGameStatus('dead')
            timer2 = threading.Timer(1.2, nextPacman)
            timer2.start()

          if actor.modus in ("flucht", "blink"):
            actor.changeMode('die')

  for actor in actors:
    actor.show()
  pgf.updateDisplay()
  if pgf.keyPressed("ESC"):
    break
