import pygame as pg
import math


def collatz(n):
  sequenz = []
  while n > 1:
    sequenz.append(n % 2 == 0)
    n = n // 2 if n % 2 == 0 else n * 3 + 1
  return sequenz[::-1]


def rotate(winkel):
  winkel = math.radians(winkel)
  x = (math.cos(winkel) - math.sin(winkel)) * SCALE
  y = (math.sin(winkel) + math.cos(winkel)) * SCALE
  return x, -y


BREITE, HÖHE = 1500, 1000
pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
screen.fill((0, 0, 0))
SCALE = 3
WINKELSCHRITT = 10

for n in range(10_000):
  sequenz = collatz(n)
  start_x, start_y = BREITE // 2, HÖHE
  winkel = 0
  for even in sequenz:
    winkel = winkel + WINKELSCHRITT if even else winkel - WINKELSCHRITT * 1.8
    x1, y1 = rotate(winkel)
    ziel_x, ziel_y = start_x + x1, start_y + y1
    pg.draw.line(screen, (0, 0, 200),
                 (start_x, start_y), (ziel_x, ziel_y), 1)
    start_x, start_y = ziel_x, ziel_y
  pg.display.flip()

weitermachen = True
while weitermachen:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False

pg.quit()
