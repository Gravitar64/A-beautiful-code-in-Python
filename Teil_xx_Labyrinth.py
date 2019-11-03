import pygame as pg
import random as rnd
import sys

sys.setrecursionlimit(4000)

BREITE, HÖHE = 1001, 1001
SPALTEN = ZEILEN = 30
GRÖßE = BREITE // SPALTEN
FPS = 5
ANZ_ZELLEN = SPALTEN * ZEILEN
ri_sz     = {'l': (-1, 0), 'r': (1, 0), 'o': (0, -1), 'u': (0, 1)}
ri_invers = {'l': 'r', 'r': 'l', 'o': 'u', 'u': 'o'}
ri_xy     = {'l': [(0, 0), (0, GRÖßE)],
             'r': [(GRÖßE, 0), (GRÖßE, GRÖßE)],
             'o': [(0, 0), (GRÖßE, 0)],
             'u': [(0, GRÖßE), (GRÖßE, GRÖßE)]}


class Zelle:
  def __init__(self, pos):
    self.pos = pos
    self.besucht = False
    self.wände = {'l', 'r', 'o', 'u'}

  def show(self):
    s, z = self.pos
    posxy = s * GRÖßE, z * GRÖßE
    for wand in self.wände:
      d_von, d_bis = ri_xy[wand]
      von = add_pos(posxy, (d_von))
      bis = add_pos(posxy, (d_bis))
      pg.draw.line(screen, f_linie, von, bis, 2)
  
  def markiere_suche(self):
    s, z = self.pos
    posxy = s * GRÖßE , z * GRÖßE 
    pg.draw.rect(screen, f_markSuche, (posxy, (GRÖßE, GRÖßE)))

  def markiere_weg(self):
    s, z = self.pos
    posxy = s * GRÖßE + GRÖßE / 2 , z * GRÖßE + GRÖßE / 2
    pg.draw.circle(screen, f_markWeg, posxy, GRÖßE // 5)


def ereignis_quit():
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      return True


def i2sz(i):
  return i % SPALTEN, i // SPALTEN


def add_pos(pos1, pos2):
  return pos1[0]+pos2[0], pos1[1]+pos2[1]


def nachbarn(zelle):
  nachb = []
  for key, val in ri_sz.items():
    pos = add_pos(zelle.pos, val)
    if pos in raster:
      nachb.append((key, pos))
  rnd.shuffle(nachb)
  return nachb


def labyrinth_erstellen(zelle, richtung):
  zelle.besucht = True
  zelle.wände.remove(richtung)
  nachb = nachbarn(zelle)
  if not nachb: return
  for richt, pos in nachb:
    if raster[pos].besucht: continue
    zelle.wände.remove(richt)
    labyrinth_erstellen(raster[pos], ri_invers[richt])


def mögliche_richtungen(zelle):
  mögl_richt = []
  for r in ri_sz:
    if r in zelle.wände: continue
    mögl_richt.append(r)
  return mögl_richt


weg = []
suche = []
def finde_weg(zelle):
  suche.append(zelle)
  zelle.besucht = True
  if zelle.pos == (SPALTEN-1, ZEILEN-1):
    weg.append((raster[zelle.pos]))
    return True
  for r in mögliche_richtungen(zelle):
    pos = add_pos(zelle.pos, ri_sz[r])
    if pos not in raster or raster[pos].besucht: continue
    if finde_weg(raster[pos]):
      weg.append((raster[zelle.pos]))
      return True


pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
f_hintergrund = pg.Color('Black')
f_linie = pg.Color('White')
f_markWeg = pg.Color('gold2')
f_markSuche = pg.Color('darkorchid4')


rnd.seed()
raster = {}
for i in range(ANZ_ZELLEN):
  pos = i2sz(i)
  raster[pos] = Zelle(pos)

screen.fill(f_hintergrund)
labyrinth_erstellen(raster[(0, 0)], 'l')

for i in range(ANZ_ZELLEN):
  pos = i2sz(i)
  raster[pos].besucht = False

finde_weg(raster[(0, 0)])

for zelle in raster.values():
  zelle.show()

#Labyrinth anzeigen bis ESC
while not ereignis_quit():
  pg.display.flip()

#Animiere die Suche
clock = pg.time.Clock()
i = 0
while not ereignis_quit():
  clock.tick(20)
  suche[i].markiere_suche()
  i = min(i+1, len(suche)-1)
  for zelle in raster.values():
    zelle.show()
  pg.display.flip()

#Animiere den gefundenen Weg
i = 0
while not ereignis_quit():
  clock.tick(FPS)
  weg[i].markiere_weg()
  for zelle in raster.values():
    zelle.show()
  i = min(i+1, len(weg)-1)
  pg.display.flip()

pg.quit()
