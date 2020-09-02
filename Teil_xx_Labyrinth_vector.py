import pygame as pg 
import random as rnd
from Teil_25_Vektor import Vec
import sys

sys.setrecursionlimit(4000)


BREITE = HÖHE = 1000
SPALTEN = ZEILEN = 99
ZE_BH = BREITE // SPALTEN

delta_linien = {'l': [Vec(0,0), Vec(0,ZE_BH)], 'r': [Vec(ZE_BH, 0), Vec(ZE_BH, ZE_BH)],
                'o': [Vec(0,0), Vec(ZE_BH, 0)], 'u': [Vec(0, ZE_BH), Vec(ZE_BH, ZE_BH)]}
delta_nachbarn = {'l':Vec(-ZE_BH, 0), 'r': Vec(ZE_BH,0), 'o': Vec(0,-ZE_BH), 'u':Vec(0,ZE_BH)}                
richtung_invers = {'l':'r', 'r':'l', 'o':'u', 'u':'o'}
pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
farbe_hintergrund = pg.Color('Black')
farbe_linie = pg.Color('White')

raster = {}
for i in range(SPALTEN*ZEILEN):
  pos = Vec(i % SPALTEN, i // SPALTEN) * ZE_BH
  raster[pos] = {b for b in 'lrou'}

def zeichne_zelle(pos, wände):
  for wand in wände:
    delta_von, delta_bis = delta_linien[wand]
    von = pos + delta_von
    bis = pos + delta_bis
    pg.draw.line(screen, farbe_linie, von, bis, 2) 
    
def pg_quit():
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
      return True 

def nachbarn_ermitteln(pos):
  nachb = []
  for richtung, delta in delta_nachbarn.items():
    neue_pos = pos + delta
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

besucht = set()
labyrinth_erstellen(Vec(0,0), 'l')

while not pg_quit():
  screen.fill(farbe_hintergrund)
  for pos, wände in raster.items():
    zeichne_zelle(pos, wände)
  pg.display.flip()

pg.quit()    





