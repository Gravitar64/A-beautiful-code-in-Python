import pygame as pg
import random as rnd
import sys

sys.setrecursionlimit(4000)

BREITE, HÖHE = 1001, 1001
ZELLEN_GRÖßE = 100
FPS = 5
SPALTEN, ZEILEN = BREITE // ZELLEN_GRÖßE, HÖHE // ZELLEN_GRÖßE
ANZ_ZELLEN = SPALTEN * ZEILEN
richt = {'l': (-1, 0), 'r': (1, 0), 'o': (0, -1), 'u': (0, 1)}

class Zelle:
  def __init__(self, pos):
    self.pos = pos
    self.besucht = False
    self.wände = {'l': True, 'r': True, 'o': True, 'u': True}

  def show(self):
    s, z = self.pos
    x, y = s * ZELLEN_GRÖßE, z * ZELLEN_GRÖßE
    for key, val in self.wände.items():
      if not val:
        continue
      if key == 'l':
        pg.draw.line(screen, f_linie, (x, y), (x, y+ZELLEN_GRÖßE),2)
      if key == 'r':
        pg.draw.line(screen, f_linie, (x+ZELLEN_GRÖßE, y),
                     (x+ZELLEN_GRÖßE, y+ZELLEN_GRÖßE),2)
      if key == 'o':
        pg.draw.line(screen, f_linie, (x, y), (x+ZELLEN_GRÖßE, y),2)
      if key == 'u':
        pg.draw.line(screen, f_linie, (x, y+ZELLEN_GRÖßE),
                     (x+ZELLEN_GRÖßE, y+ZELLEN_GRÖßE),2)

  def mark(self):
    s,z = self.pos
    x, y = s * ZELLEN_GRÖßE, z * ZELLEN_GRÖßE
    x, y = x + ZELLEN_GRÖßE/2, y + ZELLEN_GRÖßE / 2
    pg.draw.circle(screen, f_markierung, (x, y), ZELLEN_GRÖßE // 3)


def ereignis_quit():
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      return True


def i2sz(i):
  return i % SPALTEN, i // SPALTEN

def add_pos(pos1,pos2):
  return pos1[0]+pos2[0], pos1[1]+pos2[1]


def nachbarn(zelle):
  nachb = []
  for key, val in richt.items():
   pos = add_pos(zelle.pos, val)
   if pos in raster:
      nachb.append((key, pos))
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
  for richt, pos in nachb:
    if raster[pos].besucht:
      continue
    zelle.wände[richt] = False
    labyrinth_erstellen(raster[pos], richt_invers(richt))


def mögliche_richtungen(zelle):
  richt = []
  richtungen = 'l r o u'.split()
  for r in richtungen:
    if zelle.wände[r]:
      continue
    richt.append(r)
  return richt


weg = []
def finde_weg(zelle):
  zelle.besucht = True
  if zelle.pos == (SPALTEN-1, ZEILEN-1):
    weg.append((raster[zelle.pos]))
    return True
  for r in mögliche_richtungen(zelle):
    pos = add_pos(zelle.pos, richt[r])
    if pos not in raster or raster[pos].besucht: continue
    if finde_weg(raster[pos]):
      weg.append((raster[zelle.pos]))
      return True
  



pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
f_hintergrund = pg.Color('Black')
f_linie = pg.Color('White')
f_markierung = pg.Color('gold2')


rnd.seed()
raster = {}
for i in range(ANZ_ZELLEN):
  pos = i2sz(i)
  raster[pos] = Zelle(pos)

screen.fill(f_hintergrund)
labyrinth_erstellen(raster[(0, 0)], 'l')
for zelle in raster.values():
  zelle.show()

while not ereignis_quit():
  pg.display.flip()

for i in range(ANZ_ZELLEN):
  pos = i2sz(i)
  raster[pos].besucht = False

finde_weg(raster[(0, 0)])
weg.reverse()

clock = pg.time.Clock()
i = 0
while not ereignis_quit():
  clock.tick(FPS)
  weg[i].mark()
  i = min(i+1, len(weg)-1)
  pg.display.flip()

pg.quit()
