import pygame as pg
from dataclasses import dataclass
import random as rnd

auflösung = 1000
raster = 20
anzMinen = 50
abstand = auflösung // raster

pg.init()
screen = pg.display.set_mode([auflösung, auflösung])


def ladeBild(dateiname):
  return pg.transform.scale(pg.image.load(dateiname), (abstand, abstand))


def gültig(y, x):
  return y > -1 and y < raster and x > -1 and x < raster


bild_normal = ladeBild('Teil_10_ms_cell_normal.gif')
bild_markiert = ladeBild('Teil_10_ms_cell_marked.gif')
bild_mine = ladeBild('Teil_10_ms_cell_mine.gif')
bild_aufgedeckt = []
for n in range(9):
  bild_aufgedeckt.append(ladeBild(f'Teil_10_ms_cell_{n}.gif'))


matrix = []
benachbarteFelder = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, -1), (1, 0), (1, 1)]


@dataclass
class Cell():
  zeile: int
  spalte: int
  mine: bool = False
  aufgedeckt: bool = False
  markiert: bool = False
  anzMinenDrumrum = int = 0

  def show(self):
    pos = (self.spalte*abstand, self.zeile*abstand)
    if self.aufgedeckt:
      if self.mine:
        screen.blit(bild_mine, pos)
      else:
        screen.blit(bild_aufgedeckt[self.anzMinenDrumrum], pos)
    else:
      if self.markiert:
        screen.blit(bild_markiert, pos)
      else:
        screen.blit(bild_normal, pos)

  def anzMinenErmitteln(self):
    for pos in benachbarteFelder:
      neueZeile, neueSpalte = self.zeile + pos[0], self.spalte + pos[1]
      if gültig(neueZeile, neueSpalte) and matrix[neueZeile*raster+neueSpalte].mine:
        self.anzMinenDrumrum += 1


def floodFill(zeile, spalte):
  for pos in benachbarteFelder:
    neueZeile = zeile + pos[0]
    neueSpalte = spalte + pos[1]
    if gültig(neueZeile, neueSpalte):
      cell = matrix[neueZeile*raster+neueSpalte]
      if cell.anzMinenDrumrum == 0 and not cell.aufgedeckt:
        cell.aufgedeckt = True
        floodFill(neueZeile, neueSpalte)
      else:
        cell.aufgedeckt = True


#Die Objekte werden je Feld angelegt und in der Matrix gespeichert
for n in range(raster*raster):
  matrix.append(Cell(n // raster, n % raster))

#Die Minen werden zufällig verteilt
while anzMinen > 0:
  cell = matrix[rnd.randrange(raster*raster)]
  if not cell.mine:
    cell.mine = True
    anzMinen -= 1

#Die Anzahl der Minen in den benachbarten Feldern werden je Feld ermittelt
for objekt in matrix:
  if not objekt.mine:
    objekt.anzMinenErmitteln()

#Hauptschleife zum Bildschirmzeichnen und zur Auswertung der Ereignisse
clock = pg.time.Clock()
weitermachen = True
while weitermachen:
  #Frames per second setzen
  clock.tick(20)
  #Events auswerten
  for event in pg.event.get():
    #wenn Fenster geschlossen wird
    if event.type == pg.QUIT:
      weitermachen = False
    #wenn Maustaste gedrückt wurde
    if event.type == pg.MOUSEBUTTONDOWN:
      mouseX, mouseY = pg.mouse.get_pos()
      cell = matrix[mouseY // abstand * raster + mouseX // abstand]
      #rechte Maustaste
      if pg.mouse.get_pressed()[2]:
        cell.markiert = not cell.markiert
      #linke Maustaste
      if pg.mouse.get_pressed()[0]:
        cell.aufgedeckt = True
        if cell.anzMinenDrumrum == 0 and not cell.mine:
          floodFill(mouseY // abstand, mouseX // abstand)
        if cell.mine:
          for objekt in matrix:
            objekt.aufgedeckt = True

  for objekt in matrix:
    objekt.show()
  pg.display.flip()

pg.quit()
