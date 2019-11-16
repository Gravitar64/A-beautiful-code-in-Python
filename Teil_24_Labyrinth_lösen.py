import pygame as pg 
import random as rnd 
import sys

sys.setrecursionlimit(4000)

BREITE = HÖHE = 1000
SPALTEN = ZEILEN = 60
ZE_BH = BREITE // SPALTEN

delta_linien = {'l': [(0,0), (0,ZE_BH)], 'r': [(ZE_BH, 0), (ZE_BH, ZE_BH)],
                'o': [(0,0), (ZE_BH, 0)], 'u': [(0, ZE_BH), (ZE_BH, ZE_BH)]}
delta_nachbarn = {'l':(-ZE_BH, 0), 'r': (ZE_BH,0), 'o': (0,-ZE_BH), 'u':(0,ZE_BH)}                
richtung_invers = {'l':'r', 'r':'l', 'o':'u', 'u':'o'}
pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
farbe_hintergrund = pg.Color('Black')
farbe_linie = pg.Color('White')
farbe_suche = pg.Color('darkorchid4')
farbe_weg = pg.Color('gold2')

raster = {}
for i in range(SPALTEN*ZEILEN):
  pos = i % SPALTEN * ZE_BH, i // SPALTEN * ZE_BH
  raster[pos] = {b for b in 'lrou'}

def add_pos(pos1, pos2):
  return pos1[0]+pos2[0], pos1[1]+pos2[1]  

def zeichne_zelle(pos, wände):
  for wand in wände:
    delta_von, delta_bis = delta_linien[wand]
    von = add_pos(pos,delta_von)
    bis = add_pos(pos,delta_bis)
    pg.draw.line(screen, farbe_linie, von, bis, 2) 
    
def pg_quit():
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
      return True 

def nachbarn_ermitteln(pos):
  nachb = []
  for richtung, delta in delta_nachbarn.items():
    neue_pos = add_pos(pos, delta)
    if neue_pos not in raster: continue
    nachb.append((richtung, neue_pos))
  rnd.shuffle(nachb)
  return nachb  


def labyrinth_erstellen(pos_aktuell, richtung_von):
  besucht.add(pos_aktuell)
  raster[pos_aktuell].remove(richtung_von)
  nachb = nachbarn_ermitteln(pos_aktuell)
  for richtung_nach, pos_neu in nachb:
    if pos_neu in besucht: continue
    raster[pos_aktuell].remove(richtung_nach)
    labyrinth_erstellen(pos_neu, richtung_invers[richtung_nach])


def mögliche_richtungen(pos):
  richtungen = []
  for richtung, delta in delta_nachbarn.items():
    neue_pos = add_pos(pos, delta)
    if neue_pos not in raster: continue
    if richtung in raster[pos]: continue
    richtungen.append(neue_pos)
  return richtungen  

ziel = ((SPALTEN-1)*ZE_BH, (ZEILEN-1)*ZE_BH)
weg = []
def labyrinth_lösen(pos_aktuell):
  besucht.append(pos_aktuell)
  if pos_aktuell == ziel:
    weg.append(pos_aktuell)
    return True
  for pos_neu in mögliche_richtungen(pos_aktuell):
    if pos_neu in besucht: continue
    if labyrinth_lösen(pos_neu):
      weg.append(pos_neu)
      return True




besucht = set()
labyrinth_erstellen((0,0), 'l')
besucht = []
labyrinth_lösen((0,0))


while not pg_quit():
  screen.fill(farbe_hintergrund)
  for pos, wände in raster.items():
    zeichne_zelle(pos, wände)
  pg.display.flip()

i = 0
while not pg_quit():
  pos = besucht[i]
  pg.draw.rect(screen, farbe_suche, (pos, (ZE_BH, ZE_BH)))
  for pos, wände in raster.items():
    zeichne_zelle(pos, wände)
  pg.display.flip()
  i = min(i+1, len(besucht)-1)

i = 0
clock = pg.time.Clock()
while not pg_quit():
  clock.tick(5)
  x,y = weg[i]
  x,y = x + ZE_BH // 2, y + ZE_BH // 2
  pg.draw.circle(screen, farbe_weg, (x,y), ZE_BH // 6)
  for pos, wände in raster.items():
    zeichne_zelle(pos, wände)
  pg.display.flip()
  i = min(i+1, len(weg)-1)    

pg.quit()    





