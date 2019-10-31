import pygame as pg
import random as rnd
import sys

sys.setrecursionlimit(4000)


class Zelle:
  def __init__(self, spalte, zeile):
    self.spalte = spalte
    self.zeile = zeile
    self.besucht = False
    self.wände = {'l': True, 'r': True, 'o': True, 'u': True}

  def show(self):
    x, y = self.spalte * ZELLEN_GRÖßE, self.zeile * ZELLEN_GRÖßE
    for key, val in self.wände.items():
      if not val:
        continue
      if key == 'l':
        pg.draw.line(screen, f_linie, (x, y), (x, y+ZELLEN_GRÖßE))
      if key == 'r':
        pg.draw.line(screen, f_linie, (x+ZELLEN_GRÖßE, y),
                     (x+ZELLEN_GRÖßE, y+ZELLEN_GRÖßE))
      if key == 'o':
        pg.draw.line(screen, f_linie, (x, y), (x+ZELLEN_GRÖßE, y))
      if key == 'u':
        pg.draw.line(screen, f_linie, (x, y+ZELLEN_GRÖßE),
                     (x+ZELLEN_GRÖßE, y+ZELLEN_GRÖßE))

  def mark(self):
    x, y = self.spalte * ZELLEN_GRÖßE, self.zeile * ZELLEN_GRÖßE
    x, y = x + ZELLEN_GRÖßE/2, y + ZELLEN_GRÖßE / 2
    pg.draw.circle(screen, f_markierung, (x, y), ZELLEN_GRÖßE // 3)


def ereignis_quit():
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      return True


def i2sz(i):
  return i % SPALTEN, i // SPALTEN


def nachbarn(zelle):
  nachb = []
  for key, val in richt.items():
    ds, dz = val
    s, z = zelle.spalte, zelle.zeile
    s1, z1 = s + ds, z + dz
    if (s1, z1) in raster:
      nachb.append((key, s1, z1))
  rnd.shuffle(nachb)
  return nachb


def richt_invers(richt):
  ri = {'l': 'r', 'r': 'l', 'o': 'u', 'u': 'o'}
  return ri[richt]


def labyrinth_erstellen(zelle, richtung):
  zelle.besucht = True
  zelle.wände[richtung] = False
  nachb = nachbarn(zelle)
  if not nachb:
    return
  for richt, s, z in nachb:
    if raster[(s, z)].besucht:
      continue
    zelle.wände[richt] = False
    labyrinth_erstellen(raster[(s, z)], richt_invers(richt))


def mögliche_richtungen(zelle):
  richt = []
  richtungen = 'l r o u'.split()
  for r in richtungen:
    if zelle.wände[r]:
      continue
    richt.append(r)
  return richt


weg = []


def finde_weg(zelle, found):
  zelle.besucht = True
  s, z = zelle.spalte, zelle.zeile
  if (s, z) == (SPALTEN-1, ZEILEN-1):
    weg.append((raster[(s, z)]))
    return True
  for r in mögliche_richtungen(zelle):
    ds, dz = richt[r]
    s1, z1 = s+ds, z+dz
    if (s1, z1) in raster and not raster[(s1, z1)].besucht:
      found = finde_weg(raster[(s1, z1)], found)
    if found:
      weg.append((raster[(s, z)]))
      return True
  return found


BREITE, HÖHE = 1001, 1001
ZELLEN_GRÖßE = 20
SPALTEN, ZEILEN = BREITE // ZELLEN_GRÖßE, HÖHE // ZELLEN_GRÖßE
ANZ_ZELLEN = SPALTEN * ZEILEN
richt = {'l': (-1, 0), 'r': (1, 0), 'o': (0, -1), 'u': (0, 1)}


pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
f_hintergrund = pg.Color('Black')
f_linie = pg.Color('White')
f_markierung = pg.Color('gold2')


rnd.seed()
raster = {}
for i in range(ANZ_ZELLEN):
  s, z = i2sz(i)
  raster[(s, z)] = Zelle(s, z)

screen.fill(f_hintergrund)
labyrinth_erstellen(raster[(0, 0)], 'l')
for zelle in raster.values():
  zelle.show()

while not ereignis_quit():
  pg.display.flip()

for i in range(ANZ_ZELLEN):
  s, z = i2sz(i)
  raster[(s, z)].besucht = False

finde_weg(raster[(0, 0)], False)
weg.reverse()

clock = pg.time.Clock()
i = 0
while not ereignis_quit():
  clock.tick(5)
  weg[i].mark()
  i = min(i+1, len(weg)-1)
  pg.display.flip()

pg.quit()
