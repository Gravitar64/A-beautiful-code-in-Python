import pygame as pg
import random as rnd
import math


class Kristallisationskeim():
  def __init__(self):
    self.x = rnd.randrange(breite)
    self.y = rnd.randrange(höhe)
    self.orientierung = rnd.randrange(360)
    self.geschwindigkeit = [rnd.randrange(1, 4) for _ in range(4)]
    self.richtungen = self.ermittel_richtungen(self.orientierung)
    self.farbe = [self.orientierung/360*255]*3
    self.pixel = {(self.x, self.y)}

  def ermittel_richtungen(self, grad):
    richtungen = []
    for richtung in [0, 90, 180, 270]:
      phi = math.radians(grad+richtung)
      richtungen.append((math.cos(phi), math.sin(phi)))
    return richtungen

  def wachse(self):
    neu = set()
    for x, y in self.pixel:
      for geschw, (dx, dy) in zip(self.geschwindigkeit, self.richtungen):
        for multi in range(1, geschw+1):
          x2, y2 = int(x+dx*multi), int(y+dy*multi)
          if 0 <= x2 < breite and 0 <= y2 < höhe and pxarray[x2, y2] == 0:
            fenster.set_at((x2, y2), self.farbe)
            neu.add((x2, y2))
    self.pixel = neu


pg.init()
größe = breite, höhe = 1000, 1000
fenster = pg.display.set_mode(größe)
fenster.fill('black')
pxarray = pg.PixelArray(fenster)
keime = [Kristallisationskeim() for _ in range(200)]


clock = pg.time.Clock()
FPS = 40

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()

  for keim in keime:
    keim.wachse()

  pg.display.flip()
