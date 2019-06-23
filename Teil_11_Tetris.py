import pygame as pg
from dataclasses import dataclass
import random as rnd


BREITE, SPALTEN, ZEILEN = 400, 10, 20
ABSTAND = BREITE // SPALTEN
HÖHE = ABSTAND * ZEILEN
grid = [0] * SPALTEN * ZEILEN
speed = 500
score, level = 0, 1

bilder = []
for n in range(8):
  bilder.append(pg.transform.scale(
      pg.image.load(f'Teil_11_tt3_{n}.gif'), (ABSTAND, ABSTAND)))

pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
TETROMINODOWN = pg.USEREVENT+1
SPEEDUP = pg.USEREVENT+2
pg.time.set_timer(TETROMINODOWN, speed)
pg.time.set_timer(SPEEDUP, 30_000)
pg.key.set_repeat(1, 100)

tetrominoes = [[0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0],
               [0, 0, 7, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 6, 6, 0, 0, 6, 0, 0, 0, 0, 0, 0]]


@dataclass
class Tetrominoe():
  tet: list
  zeile: int = 0
  spalte: int = 3

  def show(self):
    for n, farbe in enumerate(self.tet):
      if farbe > 0:
        y = (self.zeile + n // 4) * ABSTAND
        x = (self.spalte + n % 4) * ABSTAND
        screen.blit(bilder[farbe], (x, y))

  def gültig(self, z, s):
    for n, farbe in enumerate(self.tet):
      if farbe > 0:
        z1 = z + n // 4
        s1 = s + n % 4
        if z1 >= ZEILEN or s1 < 0 or s1 >= SPALTEN or grid[z1 * SPALTEN + s1] > 0:
          return False
    return True

  def update(self, zoff, soff):
    if self.gültig(self.zeile+zoff, self.spalte+soff):
      self.zeile += zoff
      self.spalte += soff
      return True
    return False

  def rotate(self):
    saveTet = self.tet.copy()
    for n, farbe in enumerate(saveTet):
      z = n // 4
      s = n % 4
      self.tet[(2-s)*4+z] = farbe
    if not self.gültig(self.zeile, self.spalte):
      self.tet = saveTet.copy()


def ObjektAufsRaster():
  for n, farbe in enumerate(figur.tet):
    if farbe > 0:
      z = figur.zeile + n // 4
      s = figur.spalte + n % 4
      grid[z*SPALTEN+s] = farbe


def VollständigeZeilenLöschen():
  anzZeilen = 0
  for zeile in range(ZEILEN):
    for spalte in range(SPALTEN):
      if grid[zeile*SPALTEN+spalte] == 0:
        break
    else:
      del grid[zeile*SPALTEN:zeile*SPALTEN+SPALTEN]
      grid[0:0] = [0]*SPALTEN
      anzZeilen += 1
  return anzZeilen**2*100


figur = Tetrominoe(rnd.choice(tetrominoes))

weitermachen = True
clock = pg.time.Clock()
while weitermachen:
  clock.tick(80)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      weitermachen = False
    if event.type == TETROMINODOWN:
      if not figur.update(1, 0):
        ObjektAufsRaster()
        score += VollständigeZeilenLöschen()
        figur = Tetrominoe(rnd.choice(tetrominoes))
    if event.type == SPEEDUP:
      speed = int(speed * 0.8)
      pg.time.set_timer(TETROMINODOWN, speed)
      level += 1
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_LEFT:
        figur.update(0, -1)
      if event.key == pg.K_RIGHT:
        figur.update(0, 1)
      if event.key == pg.K_DOWN:
        figur.update(1, 0)
      if event.key == pg.K_LCTRL:
        figur.rotate()

  screen.fill((0, 0, 0))
  figur.show()
  for n, farbe in enumerate(grid):
    if farbe > 0:
      x = n % SPALTEN * ABSTAND
      y = n // SPALTEN * ABSTAND
      screen.blit(bilder[farbe], (x, y))
  textsurface = pg.font.SysFont('impact', 40).render(
      f'{score:,}', False, (255, 255, 255))
  screen.blit(textsurface, (BREITE // 2 - textsurface.get_width() // 2, 5))
  textsurface = pg.font.SysFont('impact', 20).render(
      f'Level: {level}', False, (150, 150, 150))
  screen.blit(textsurface, (BREITE - textsurface.get_width() - 10, 5))

  pg.display.flip()


pg.quit()
