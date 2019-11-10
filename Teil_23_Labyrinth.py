import pygame as pg
import random as rnd
import sys

sys.setrecursionlimit(4000)


BREITE, HÖHE = 1000, 1000
SPALTEN = ZEILEN = 30
GRÖßE = BREITE // SPALTEN

ri_inv = {'l': 'r', 'r': 'l', 'o': 'u', 'u': 'o'}
ri_sz = {'l': (-1, 0), 'r': (1, 0), 'o': (0, -1), 'u': (0, 1)}
ri_xy = {'l': [(0, 0), (0, GRÖßE)],
         'r': [(GRÖßE, 0), (GRÖßE, GRÖßE)],
         'o': [(0, 0), (GRÖßE, 0)],
         'u': [(0, GRÖßE), (GRÖßE, GRÖßE)]}


def add_pos(pos1, pos2):
  return pos1[0]+pos2[0], pos1[1]+pos2[1]


def pg_quit():
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
      (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
      return True


class Zelle:
  def __init__(self):
    self.besucht = False
    self.wände = {c for c in 'lrou'}

  def anzeigen(self, pos):
    posXY = list(map(lambda x: x*GRÖßE, pos))
    for wand in self.wände:
      delta_von, delta_bis = ri_xy[wand]
      von = add_pos(posXY, delta_von)
      bis = add_pos(posXY, delta_bis)
      pg.draw.line(screen, farbe_wand, von, bis, 2)


pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
farbe_wand = pg.Color('White')
farbe_hintergrund = pg.Color('Black')

raster = {}
for i in range(SPALTEN * ZEILEN):
  pos = i % SPALTEN, i // SPALTEN
  raster[pos] = Zelle()


def nachbarn(pos):
  nachb = []
  for richtung, delta in ri_sz.items():
    neue_pos = add_pos(pos, delta)
    if neue_pos not in raster: continue
    nachb.append((richtung, neue_pos))
  rnd.shuffle(nachb)
  return nachb


def labyrinth_erstellen(pos, richtung):
  zelle = raster[pos]
  zelle.besucht = True
  zelle.wände.remove(richtung)
  nachb = nachbarn(pos)
  for richt, pos_neu in nachb:
    if raster[pos_neu].besucht: continue
    zelle.wände.remove(richt)
    labyrinth_erstellen(pos_neu, ri_inv[richt])


labyrinth_erstellen((0, 0), 'l')

while not pg_quit():
  screen.fill(farbe_hintergrund)
  for pos, zelle in raster.items():
    zelle.anzeigen(pos)
  pg.display.flip()

pg.quit()
