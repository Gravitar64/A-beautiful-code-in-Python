import random as rnd
import itertools as itt
import pygame as pg
from time import perf_counter as pfc


def i2sz(i):
  return i % ZELLEN, i // ZELLEN


def create_new_forest(ZELLEN):
  return [BAUM if rnd.random() <= START_BÄUME else LEER for _ in range(ZELLEN*ZELLEN)]


def display_forest(forest):
  for i,b in enumerate(forest):
    if b == LEER: continue
    s,z = i2sz(i)
    color = '#00ff00' if b == BAUM else '#ff0000'
    pg.draw.rect(fenster,color,(s*PIXEL,z*PIXEL,PIXEL,PIXEL))    
      

def feuer_nachbarn(i,f):
  f[i] = LEER
  s,z = i2sz(i)
  for ds,dz in itt.product(range(-1,2), range(-1,2)):
    s2, z2 = s+ds, z+dz
    i2 = z2*ZELLEN + s2
    if s2 < 0 or s2 >= ZELLEN or z2 <0 or z2 >= ZELLEN or f[i2] != BAUM: continue
    f[i2] = BRENNT
    

def sim(forest):
  forest2 = forest.copy()
  for i, b in enumerate(forest):
    if b == LEER and rnd.random() <= WACHSTUM:
      forest2[i] = BAUM
    elif b == BAUM and rnd.random() <= BRAND:
      forest2[i] = BRENNT
    elif b == BRENNT:
      feuer_nachbarn(i, forest2)
  return forest2


LEER, BAUM, BRENNT  = 0,1,2 
START_BÄUME = 0.5
WACHSTUM = 0.01          
BRAND = 0.001           


pg.init()
ZELLEN, PIXEL = 80, 10
fenster_b, fenster_h = ZELLEN*PIXEL, ZELLEN*PIXEL
fenster = pg.display.set_mode((fenster_b, fenster_h))
clock = pg.time.Clock()
FPS = 15

forest = create_new_forest(ZELLEN)

frames = gesamt = 0
while True:
  clock.tick(FPS)
  frames += 1
  
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
  
  fenster.fill('#000000')
  
  start = pfc()
  forest = sim(forest)
  gesamt += pfc() - start
  print(gesamt/frames)
  
  display_forest(forest)
  pg.display.flip()