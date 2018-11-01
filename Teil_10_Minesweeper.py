import pygame as pg
from dataclasses import dataclass
import random as rnd


auflösung = 500
raster = 9
anzMinen = 10
abstand = auflösung // raster

pg.init()
screen = pg.display.set_mode([auflösung, auflösung])
cell_normal = pg.transform.scale(pg.image.load(
    'ms_cell_normal.gif'), (abstand, abstand))
cell_marked = pg.transform.scale(pg.image.load(
    'ms_cell_marked.gif'), (abstand, abstand))
cell_mine = pg.transform.scale(pg.image.load(
    'ms_cell_mine.gif'), (abstand, abstand))
cell_selected = []
for n in range(9):
  cell_selected.append(pg.transform.scale(
      pg.image.load(f'ms_cell_{n}.gif'), (abstand, abstand)))


matrix = []
benachbarteFelder = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, -1), (1, 0), (1, 1)]


@dataclass
class Cell():
  zeile: int
  spalte: int
  mine: bool = False
  selected: bool = False
  flagged: bool = False
  anzMinenDrumrum = int = 0

  def show(self):
    pos = (self.spalte*abstand, self.zeile*abstand)
    if self.selected:
      if self.mine:
        screen.blit(cell_mine, pos)
      else:
        screen.blit(cell_selected[self.anzMinenDrumrum], pos)
    else:
      if self.flagged:
        screen.blit(cell_marked, pos)
      else:
        screen.blit(cell_normal, pos)

  def anzMinenErmitteln(self):
    for pos in benachbarteFelder:
      neueZeile = self.zeile + pos[0]
      neueSpalte = self.spalte + pos[1]
      if neueZeile >= 0 and neueZeile < raster and neueSpalte >= 0 and neueSpalte < raster:
        if matrix[neueZeile*raster+neueSpalte].mine:
          self.anzMinenDrumrum += 1

def floodFill(zeile,spalte):
  for pos in benachbarteFelder:
    neueZeile = zeile + pos[0]
    neueSpalte = spalte + pos[1]
    if neueZeile >= 0 and neueZeile < raster and neueSpalte >= 0 and neueSpalte < raster:
      cell = matrix[neueZeile*raster+neueSpalte]
      if cell.anzMinenDrumrum == 0 and not cell.selected:
        cell.selected = True
        floodFill(neueZeile, neueSpalte)
      else:
        cell.selected = True  


for n in range(raster*raster):
  matrix.append(Cell(n // raster, n % raster))

while anzMinen > 0:
  x = rnd.randrange(raster*raster)
  if not matrix[x].mine:
    matrix[x].mine = True
    anzMinen -= 1

for objekt in matrix:
  objekt.anzMinenErmitteln()

weitermachen = True
while weitermachen:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      weitermachen = False
    if event.type == pg.MOUSEBUTTONDOWN:
      mouseX, mouseY = pg.mouse.get_pos()
      spalte = mouseX // abstand
      zeile = mouseY // abstand
      i = zeile*raster+spalte
      cell = matrix[i]
      if pg.mouse.get_pressed()[2]:
        cell.flagged = not cell.flagged
      if pg.mouse.get_pressed()[0]:
        cell.selected = True
        if cell.anzMinenDrumrum == 0 and not cell.mine:
          floodFill(zeile,spalte)
        if cell.mine:
          for objekt in matrix:
            objekt.selected=True  
          
  for objekt in matrix:
    objekt.show()
  pg.display.flip()

pg.quit()
