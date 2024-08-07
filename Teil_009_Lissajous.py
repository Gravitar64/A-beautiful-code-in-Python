import pygame as pg
from dataclasses import dataclass
import math

auflösung = 1000
spalten = 10
abstand = auflösung // spalten
farbabstand = 360 // (spalten - 1)
radius = (abstand - 20) // 2
pg.init()
screen = pg.display.set_mode([auflösung, auflösung])
matrix = [[0]*spalten for i in range(spalten)]
farbe = pg.Color(0)


@dataclass
class Rotor:
  x: int
  y: int
  speed: float
  horizontal: bool
  hue: int
  winkel: float = 0
  dotX: int = 0
  dotY: int = 0

  def show(self):
    farbe.hsva = (self.hue, 100, 100)
    pg.draw.circle(screen, farbe, (self.x, self.y), radius, 1)
    pg.draw.circle(screen, (255, 255, 255), (self.dotX, self.dotY), 3)
    if self.horizontal:
      pg.draw.line(screen, (50, 50, 50), (self.dotX,
                                          self.dotY), (self.dotX, auflösung))
    else:
      pg.draw.line(screen, (50, 50, 50), (self.dotX,
                                          self.dotY), (auflösung, self.dotY))

  def update(self):
    self.winkel += self.speed
    self.dotX = int(self.x + radius * math.cos(self.winkel))
    self.dotY = int(self.y + radius * math.sin(self.winkel))

  def reset(self):
    self.winkel = 0


@dataclass
class Lissajous:
  verticies: list
  hue: int

  def update(self, pos):
    self.verticies.append(pos)

  def show(self):
    pg.draw.circle(screen, (255, 255, 255), self.verticies[-1], 2)
    if len(self.verticies) > 1:
      farbe.hsva = (self.hue, 100, 100)
      pg.draw.lines(screen, farbe, False, self.verticies, 1)

  # löscht alle Punkte aus der Liste
  def reset(self):
    self.verticies = []


def setup():
  for n in range(spalten):
    x = n*abstand + abstand // 2
    y = abstand // 2
    hue = farbabstand*n
    matrix[0][n] = Rotor(x, y, 0.01*n, True, hue)
    matrix[n][0] = Rotor(y, x, 0.01*n, False, hue)

  for zeile in range(1, spalten):
    for spalte in range(1, spalten):
      hue = (matrix[zeile][0].hue + matrix[0][spalte].hue) // 2
      matrix[zeile][spalte] = Lissajous([], hue)


def draw():

  for n in range(1, spalten):
    matrix[0][n].update()
    matrix[n][0].update()

  for zeile in range(1, spalten):
    for spalte in range(1, spalten):
      x = matrix[0][spalte].dotX
      y = matrix[zeile][0].dotY
      matrix[zeile][spalte].update([x, y])

  for zeile in range(spalten):
    for spalte in range(spalten):
      if zeile == 0 and spalte == 0:
        continue
      matrix[zeile][spalte].show()


setup()

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(20)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      weitermachen = False
  screen.fill((0, 0, 0))
  draw()
  pg.display.flip()
  if matrix[0][1].winkel > math.pi*2:
    for zeile in matrix:
      for objekt in zeile:
        objekt.reset()

pg.quit()
