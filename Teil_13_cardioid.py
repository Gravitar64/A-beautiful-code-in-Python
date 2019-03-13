import pygame as pg
from math import *

TOTAL = 200
faktor = 2.2
breite, höhe = 1150, 1150
zentrum = (breite//2, höhe//2)
zx, zy = zentrum


def i2Punkt(i):
  winkel = tau / TOTAL * i + pi
  x = int(zx + radius * cos(winkel))
  y = int(zy + radius * sin(winkel))
  return (x, y)


pg.init()
screen = pg.display.set_mode((breite, höhe))
screen2 = pg.Surface([breite, höhe])
radius = breite//2-16
farbe = pg.Color(150, 150, 150)

pg.draw.circle(screen2, (255, 255, 255), zentrum, radius, 2)
punkte = []
for i in range(TOTAL):
  punkt = i2Punkt(i)
  punkte.append(punkt)
  pg.draw.circle(screen2, (0, 150, 255), punkt, 4)

clock = pg.time.Clock()
weitermachen = True
while weitermachen:
  clock.tick(70)
  screen.blit(screen2, (0, 0))
  faktor += 0.002
  for event in pg.event.get():
    if event.type == pg.QUIT or \
            (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      weitermachen = False

  for startnr in range(TOTAL):
    zielnr = (startnr * faktor) % TOTAL
    startpunkt = punkte[startnr]
    zielpunkt = i2Punkt(zielnr)
    farbe.hsva = (360/TOTAL * zielnr, 100, 100)
    pg.draw.line(screen, farbe, startpunkt, zielpunkt, 1)

  pg.display.flip()

pg.quit()
