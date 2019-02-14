import pygame as pg
from math import *


def endPosBerechnen(pos, θ, L):
  x1, y1 = pos
  x2 = int(x1 + L*sin(θ))
  y2 = int(y1 + L*cos(θ))
  return(x2, y2)


def draw(p1, p2, m):
  pg.draw.line(screen, (255, 255, 255), p1, p2, 3)
  pg.draw.circle(screen, (255, 0, 0), p2, m)


breite, höhe = 900, 600
θ1 = θ2 = pi / 2
L1 = L2 = höhe // 3
m1 = m2 = 10
θ1_1 = θ1_2 = θ2_1 = θ2_2 = 0
g = 1.0

aPos1 = (breite//2, höhe//3)
ePos1 = endPosBerechnen(aPos1, θ1, L1)
aPos2 = ePos1
ePos2 = endPosBerechnen(aPos2, θ2, L2)
altePos = ePos2

pg.init()
screen = pg.display.set_mode([breite, höhe])
screen2 = pg.Surface([breite, höhe])
clock = pg.time.Clock()
weitermachen = True

while weitermachen:
  clock.tick(60)
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      weitermachen = False
  screen.blit(screen2, (0, 0))

  θ1_2 = -g * (2 * m1 + m2) * sin(θ1) - m2 * g * sin(θ1 - 2 * θ2) - \
      2 * sin(θ1 - θ2) * m2 * (θ2_1**2 * L2 + θ1_1**2 * L1 * cos(θ1 - θ2))
  θ1_2 = θ1_2 / (L1 * (2 * m1 + m2 - m2 * cos(2 * θ1 - 2 * θ2)))

  θ2_2 = 2 * sin(θ1 - θ2) * (θ1_1**2 * L1 * (m1 + m2) + g *
                             (m1 + m2) * cos(θ1) + θ2_1**2 * L2 * m2 * cos(θ1 - θ2))
  θ2_2 = θ2_2 / (L2 * (2 * m1 + m2 - m2 * cos(2 * θ1 - 2 * θ2)))

  θ1_1 += θ1_2
  θ1 += θ1_1

  θ2_1 += θ2_2
  θ2 += θ2_1

  ePos1 = endPosBerechnen(aPos1, θ1, L1)
  aPos2 = ePos1
  ePos2 = endPosBerechnen(aPos2, θ2, L2)

  draw(aPos1, ePos1, m1)
  draw(aPos2, ePos2, m2)
  pg.draw.line(screen2, (0, 255, 0), altePos, ePos2, 2)
  altePos = ePos2
  pg.display.flip()

pg.quit()
