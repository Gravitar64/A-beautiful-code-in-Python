import pygame as pg
import random as rnd
import sys

sys.setrecursionlimit(4000)


BREITE = HÖHE = 1000
SPALTEN = ZEILEN = 30
ZELLE_BH = BREITE // SPALTEN

ri_inv = {'l': 'r', 'r': 'l', 'o': 'u', 'u': 'o'}
ri_sz = {'l': (-1, 0), 'r': (1, 0), 'o': (0, -1), 'u': (0, 1)}
ri_xy = {'l': [(0, 0), (0, ZELLE_BH)],
         'r': [(ZELLE_BH, 0), (ZELLE_BH, ZELLE_BH)],
         'o': [(0, 0), (ZELLE_BH, 0)],
         'u': [(0, ZELLE_BH), (ZELLE_BH, ZELLE_BH)]}


def add_pos(pos1, pos2):
  return pos1[0]+pos2[0], pos1[1]+pos2[1]


def pg_quit():
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
      (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
      return True


class Zelle:
  def __init__(self, pos):
    self.posXY = pos[0]*ZELLE_BH, pos[1] * ZELLE_BH
    self.besucht = False
    self.wände = {c for c in 'lrou'}

  def anzeigen(self):
    for wand in self.wände:
      delta_von, delta_bis = ri_xy[wand]
      von = add_pos(self.posXY, delta_von)
      bis = add_pos(self.posXY, delta_bis)
      pg.draw.line(screen, farbe_wand, von, bis, 2)


pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
farbe_wand = pg.Color('White')
farbe_hintergrund = pg.Color('Black')

raster = {}
for i in range(SPALTEN * ZEILEN):
  posSZ = i % SPALTEN, i // SPALTEN
  raster[posSZ] = Zelle(posSZ)


def nachbarn(posSZ):
  nachb = []
  for richtung, deltaSZ in ri_sz.items():
    neue_posSZ = add_pos(posSZ, deltaSZ)
    if neue_posSZ not in raster: continue
    nachb.append((richtung, neue_posSZ))
  rnd.shuffle(nachb)
  return nachb


def labyrinth_erstellen(posSZ_aktuell, richtung_von):
  akt_zelle = raster[posSZ_aktuell]
  akt_zelle.besucht = True
  akt_zelle.wände.remove(richtung_von)
  nachb = nachbarn(posSZ_aktuell)
  for richtung_nach, posSZ_neu in nachb:
    if raster[posSZ_neu].besucht: continue
    akt_zelle.wände.remove(richtung_nach)
    labyrinth_erstellen(posSZ_neu, ri_inv[richtung_nach])


labyrinth_erstellen((0, 0), 'l')

while not pg_quit():
  screen.fill(farbe_hintergrund)
  for zelle in raster.values():
    zelle.anzeigen()
  pg.display.flip()

pg.quit()
