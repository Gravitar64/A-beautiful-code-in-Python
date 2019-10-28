import pygame as pg
import math


def collatz(n):
  sequenz = []
  while n > 1:
    sequenz.append(n % 2 == 0)
    n = n // 2 if n % 2 == 0 else n * 3 + 1
  sequenz.append(False)
  return sequenz[::-1]


def rotate(winkel):
  winkel = math.radians(winkel)
  x = (math.cos(winkel) - math.sin(winkel)) * SCALE
  y = (math.sin(winkel) + math.cos(winkel)) * SCALE
  return x, -y


BREITE, HÖHE = 1000, 1000
pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
screen.fill((0, 0, 0))
farbe = pg.Color(0)
pg.mouse.set_visible(False)

SCALE = 3
WINKELSCHRITT = 8

for n in range(100_000):
  sequenz = collatz(n)
  start_x, start_y = BREITE // 2.5, HÖHE
  winkel = 0
  for even in sequenz:
    winkel = winkel + WINKELSCHRITT if even else winkel - WINKELSCHRITT * 1.8
    farbe.hsva = (winkel % 360, 100, 70)
    x1, y1 = rotate(winkel)
    ziel_x, ziel_y = start_x + x1, start_y + y1
    pg.draw.line(screen, farbe, (start_x, start_y), (ziel_x, ziel_y), 1)
    start_x, start_y = ziel_x, ziel_y
  if n % 2000 == 0:
    pg.display.flip()

pg.mouse.set_visible(True)

weitermachen = True
while weitermachen:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or (ereignis.type == pg.KEYDOWN and
                                    ereignis.key == pg.K_ESCAPE):
      weitermachen = False
pg.quit()
