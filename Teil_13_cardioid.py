import pygame as pg
from math import *


def i2Point(i):
  x, y = center
  # tau = 2* pi, +pi um das bild um 180° zu drehen
  w = tau / total * i + pi
  x1 = int(x + r * cos(w))
  y1 = int(y + r * sin(w))
  return (x1, y1)


total = 200
faktor = 0
breite, höhe = 1150, 1150
center = (breite//2, höhe//2)
r = breite//2-16

pg.init()
screen = pg.display.set_mode((breite, höhe))
screen2 = pg.Surface([breite, höhe])
farbe = pg.Color(150, 150, 150)

points = []
pg.draw.circle(screen2, (255, 255, 255), center, r, 2)
x, y = center
for i in range(total):
  point = i2Point(i)
  pg.draw.circle(screen2, (0, 150, 255), point, 4,)
  points.append(point)


clock = pg.time.Clock()
weitermachen = True
while weitermachen:
  clock.tick(70)
  screen.blit(screen2, (0, 0))
  faktor += 0.002
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      weitermachen = False

  for i, p in enumerate(points):
    z = (i * faktor) % total
    farbe.hsva = (360 / total * z, 100, 100)
    pg.draw.line(screen, farbe, p, (i2Point(z)))

  textsurface = pg.font.SysFont('cour', 82).render(
      f'{faktor:6.1f}', False, (farbe))
  screen.blit(textsurface, (3, 10))

  pg.display.flip()

pg.quit()
