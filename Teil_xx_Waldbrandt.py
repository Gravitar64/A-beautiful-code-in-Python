import random as rnd
import itertools as itt
import pygame as pg
from time import perf_counter as pfc


def i2sz(i):
  return i % ZELLEN, i // ZELLEN


def create_new_forest(ZELLEN):
  return {i2sz(i):[BAUM,1]  for i in range(ZELLEN*ZELLEN) if rnd.random() <= START_BÄUME}


def display_forest(forest):
  for (s,z),(b,alter) in forest.items():
    farbe.hsva = (122,100,max(100-alter,10))  if b == BAUM else (0,61,100)
    pg.draw.rect(fenster,farbe,(s*PIXEL,z*PIXEL,PIXEL,PIXEL))    
      

def feuer_nachbarn(s,z,f):
  del f[(s,z)]
  for ds,dz in itt.product(range(-1,2), range(-1,2)):
    if not (s+ds, z+dz) in f: continue
    if f[(s+ds, z+dz)][0] != BAUM: continue
    f[(s+ds, z+dz)] = [BRENNT,1]
    

def sim(forest):
  forest2 = forest.copy()
  stichprobe = int(len(KOORD) * WACHSTUM)
  for _ in range(stichprobe):
    pos = rnd.choice(KOORD)
    if (pos) in forest: continue
    forest2[pos] = [BAUM,1]
  
  for pos, b in forest.items():
    if b[0] == BAUM: 
      if rnd.random() <= BRAND:
        forest2[pos] = [BRENNT,1]
      else:
        forest2[pos][1] += 1  
    elif b[0] == BRENNT:
      feuer_nachbarn(*pos, forest2)
  return forest2


LEER, BAUM, BRENNT  = 0,1,2 
START_BÄUME = 0.5
WACHSTUM = 0.01          
BRAND = 0.001         


pg.init()
ZELLEN, PIXEL = 80, 10
KOORD = [(s,z) for s,z in itt.product(range(ZELLEN), range(ZELLEN))]
fenster_b, fenster_h = ZELLEN*PIXEL, ZELLEN*PIXEL
fenster = pg.display.set_mode((fenster_b, fenster_h))
clock = pg.time.Clock()
farbe = pg.Color(0)
FPS = 2

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