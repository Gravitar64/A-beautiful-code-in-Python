from collections import Counter
import pygame as pg
import random as rnd


def nachbarn(pos):
  for x1, y1 in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
    yield pos[0] + x1, pos[1] + y1


def neueGeneration(grid):
  anzNachbarn = Counter([p for pos in grid for p in nachbarn(pos)])
  grid = {pos for pos, anz in anzNachbarn.items() if anz ==
          3 or (anz == 2 and pos in grid)}
  return grid


def show(grid, rect):
  zell_breite, zell_höhe, offs_x, offs_y = rect
  for (x, y) in grid:
    pg.draw.rect(screen, (0, 0, 255), 
                ((x+offs_x)*zell_breite,(y+offs_y)*zell_höhe, zell_breite, zell_höhe))


def zellInfos(grid):
  Xs, Ys = zip(*grid)
  minX, maxX, minY, maxY = min(Xs), max(Xs), min(Ys), max(Ys)
  grid_breite, grid_höhe = (maxX - minX+1), (maxY - minY+1)
  zell_breite = screen_breite / grid_breite
  zell_höhe = screen_höhe / grid_höhe
  return [zell_breite, zell_höhe, -minX, -minY]


pg.init()
screen_breite, screen_höhe = 1000, 1000
screen = pg.display.set_mode([screen_breite, screen_höhe])
spielfeld = {(rnd.randrange(200), rnd.randrange(200)) for _ in range(6000)}
zell_infos = zellInfos(spielfeld)
clock = pg.time.Clock()

weitermachen = True
while weitermachen:
  clock.tick(25)
  screen.fill((0, 0, 0))
  show(spielfeld, zell_infos)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
      weitermachen = False
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_SPACE:
      zell_infos = zellInfos(spielfeld)
  spielfeld = neueGeneration(spielfeld)
  pg.display.flip()
pg.quit()
