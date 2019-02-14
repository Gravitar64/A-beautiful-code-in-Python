import pygame as pg
from math import *

total = 200
faktor = 0
breite, höhe = 900, 900
center = (breite//2, höhe//2)
r = breite//2-16

pg.init()
screen = pg.display.set_mode([breite, höhe])
screen2 = pg.Surface([breite, höhe])
farbe = pg.Color(150, 150, 150)

points = []
pg.draw.circle(screen2, (255, 255, 255), center, r, 2)
x, y = center
for i in range(total):
  w = 2*pi / total * i
  x1 = int(x + r*cos(w))
  y1 = int(y + r*sin(w))
  pg.draw.circle(screen2, (0, 150, 255), (x1, y1), 4,)
  points.append((x1, y1))


clock = pg.time.Clock()
weitermachen = True
while weitermachen:
  clock.tick(70)
  screen.blit(screen2, (0, 0))
  faktor += 0.002
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      weitermachen = False

  x, y = center
  for i, p in enumerate(points):
    x1, y1 = p
    z = (i * faktor) % total
    w = 2 * pi / total * z
    x2 = int(x + r*cos(w))
    y2 = int(y + r*sin(w))
    farbe.hsva = (360/(2*pi)*w, 100, 100)
    pg.draw.line(screen, farbe, (x1, y1), (x2, y2))

  pg.display.flip()

pg.quit()
