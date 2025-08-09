import pygame as pg
from dataclasses import dataclass
import random as rnd
import time
import sys

sys.setrecursionlimit(100_000)
auflösung = 1000
raster = 20
anzMinen = raster**2 / 10
abstand = auflösung // raster

pg.init()
screen = pg.display.set_mode([auflösung, auflösung])


def ladeBild(dateiname):
  return pg.transform.scale(pg.image.load(dateiname), (abstand, abstand))


def gültig(y, x):
  return y > -1 and y < raster and x > -1 and x < raster


bild_normal = ladeBild("Teil_010_ms_cell_normal.gif")
bild_markiert = ladeBild("Teil_010_ms_cell_marked.gif")
bild_mine = ladeBild("Teil_010_ms_cell_mine.gif")
bild_aufgedeckt = []
for n in range(9):
  bild_aufgedeckt.append(ladeBild(f"Teil_010_ms_cell_{n}.gif"))


matrix = []
benachbarteFelder = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


@dataclass
class Cell:
  zeile: int
  spalte: int
  mine: bool = False
  aufgedeckt: bool = False
  markiert: bool = False
  anzMinenDrumrum: int = 0

  def show(self):
    pos = (self.spalte * abstand, self.zeile * abstand)
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
    self.anzMinenDrumrum = sum(cell.mine for cell in benachbarte_Zellen(self))


def floodFill(cell):
  for nachbar in benachbarte_Zellen(cell):
    if nachbar.anzMinenDrumrum == 0 and not nachbar.aufgedeckt:
      nachbar.aufgedeckt = True
      floodFill(nachbar)
    else:
      nachbar.aufgedeckt = True


def benachbarte_Zellen(cell):
  zellen = []
  for delta_zeile, delta_spalte in benachbarteFelder:
    neueZeile, neueSpalte = cell.zeile + delta_zeile, cell.spalte + delta_spalte
    if not gültig(neueZeile, neueSpalte): continue
    zellen.append(matrix[neueZeile * raster + neueSpalte])
  return zellen


def löse():
  time_start = time.perf_counter()
  änderung = True
  while änderung:
    änderung = False
    for cell in matrix:
      if not cell.aufgedeckt or not cell.anzMinenDrumrum: continue
      nachbarn = benachbarte_Zellen(cell)
      felder_nicht_aufgedeckt, minen = [], cell.anzMinenDrumrum
      for nachbar in nachbarn:
        if nachbar.markiert:
          minen -= 1
        elif not nachbar.aufgedeckt:
          felder_nicht_aufgedeckt.append(nachbar)

      if minen == 0:
        for nachbar in nachbarn:
          if nachbar.markiert or nachbar.aufgedeckt: continue
          nachbar.aufgedeckt = änderung = True
          if not nachbar.anzMinenDrumrum and not nachbar.mine:
            floodFill(nachbar)
      elif len(felder_nicht_aufgedeckt) == minen:
        for feld in felder_nicht_aufgedeckt:
          feld.markiert = änderung = True
  print(f"Gelöst in {(time.perf_counter() - time_start) * 1000:.0f} ms")


# Die Objekte werden je Feld angelegt und in der Matrix gespeichert
for n in range(raster * raster):
  matrix.append(Cell(n // raster, n % raster))

# Die Minen werden zufällig verteilt
while anzMinen > 0:
  cell = matrix[rnd.randrange(raster * raster)]
  if not cell.mine:
    cell.mine = True
    anzMinen -= 1

# Die Anzahl der Minen in den benachbarten Feldern werden je Feld ermittelt
for objekt in matrix:
  if not objekt.mine:
    objekt.anzMinenErmitteln()

# Hauptschleife zum Bildschirmzeichnen und zur Auswertung der Ereignisse
clock = pg.time.Clock()
weitermachen = True
while weitermachen:
  # Frames per second setzen
  clock.tick(20)
  # Events auswerten
  for event in pg.event.get():
    # wenn Fenster geschlossen wird
    if event.type == pg.QUIT:
      weitermachen = False
    # wenn Maustaste gedrückt wurde
    if event.type == pg.MOUSEBUTTONDOWN:
      mouseX, mouseY = pg.mouse.get_pos()
      cell = matrix[mouseY // abstand * raster + mouseX // abstand]
      # rechte Maustaste
      if pg.mouse.get_pressed()[2]:
        cell.markiert = not cell.markiert
      # linke Maustaste
      if pg.mouse.get_pressed()[0]:
        cell.aufgedeckt = True
        if cell.anzMinenDrumrum == 0 and not cell.mine:
          floodFill(cell)
        if cell.mine:
          for objekt in matrix:
            objekt.aufgedeckt = True
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_l:
        löse()

  for objekt in matrix:
    objekt.show()
  pg.display.flip()

pg.quit()
