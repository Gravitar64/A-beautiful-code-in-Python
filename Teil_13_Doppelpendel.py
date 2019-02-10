import pygame as pg
from dataclasses import dataclass
import math


@dataclass
class Pendel():
  anfPos: tuple
  θ: float
  L: int
  m: int
  θ1: float = 0
  θ2: float = 0
  endPos: tuple = (0, 0)

  def endPosBerechnen(self):
    x1, y1 = self.anfPos
    x2 = int(x1 + self.L*math.sin(self.θ))
    y2 = int(y1 + self.L*math.cos(self.θ))
    self.endPos = (x2, y2)

  def winkelAktualisieren(self, acc):
    self.θ1 += acc
    self.θ += self.θ1
    self.endPosBerechnen()

  def show(self):
    pg.draw.line(screen, (255, 255, 255), self.anfPos, self.endPos, 3)
    pg.draw.circle(screen, (255, 0, 0), self.endPos, self.m)


pi = 3.14159265
g = 1
breite, höhe = 900, 600
pg.init()
screen = pg.display.set_mode([breite, höhe])
screen2 = pg.Surface([breite,höhe])

p1 = Pendel((breite//2, höhe//3), pi/2, höhe//3, 10)
p1.endPosBerechnen()
p2 = Pendel((p1.endPos), pi/2, höhe//4, 10)
p2.endPosBerechnen()
oldPos = p2.endPos

clock = pg.time.Clock()
weitermachen = True
while weitermachen:
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      weitermachen = False
  clock.tick(60)
  screen.fill((0, 0, 0))
  screen.blit(screen2,(0,0))

  acc1 = (-g*(2*p1.m + p2.m)*math.sin(p1.θ)-p2.m \
          *g*math.sin(p1.θ - 2*p2.θ) - 2*math.sin(p1.θ - p2.θ)*p2.m \
          *(p2.θ1**2*p2.L+p1.θ1**2*p1.L*math.cos(p1.θ-p2.θ))) \
          /(p1.L*(2*p1.m+p2.m-p2.m*math.cos(2*p1.θ-2*p2.θ)))
  acc2 = (2*math.sin(p1.θ-p2.θ)*(p1.θ1**2*p1.L*(p1.m+p2.m) \
          +g*(p1.m+p2.m)*math.cos(p1.θ)+p2.θ1**2*p2.L*p2.m \
          *math.cos(p1.θ-p2.θ))) \
          /(p2.L*(2*p1.m+p2.m-p2.m*math.cos(2*p1.θ-2*p2.θ)))

  p1.winkelAktualisieren(acc1)
  p2.anfPos = p1.endPos
  p2.winkelAktualisieren(acc2)

  p1.show()
  p2.show()
  pg.draw.line(screen2,(0,255,0),oldPos, p2.endPos, 2)
  oldPos = p2.endPos
  pg.display.flip()
