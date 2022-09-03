import random as rnd
import pygame as pg


def zeige_wald(bäume, brennen):
  for s,z in bäume | brennen:
    color = '#00ff00' if (s,z) in bäume else '#ff0000'
    pg.draw.rect(fenster,color,(s*PIXEL,z*PIXEL,PIXEL,PIXEL))
        

def feuer_nachbarn(bäume, brennen):
  bäume -= brennen
  brennen = {(s+ds, z+dz) for s,z in brennen 
                 for ds in range(-1,2)
                 for dz in range(-1,2)
                 if (s+ds, z+dz) in bäume}
  return bäume-brennen, brennen
    

def sim(bäume, brennen):
  leer = koord - bäume - brennen
  bäume -= brennen
  brennen |= set(rnd.sample(bäume,int(len(bäume)*BRAND)))
  bäume |= set(rnd.sample(leer,int(len(leer)*WACHSTUM)))
  return feuer_nachbarn(bäume, brennen)
  

START_BÄUME = 0.5
WACHSTUM = 0.01          
BRAND = 0.001         
FPS = 40

pg.init()
GR, PIXEL = 80, 10
fenster_b, fenster_h = GR*PIXEL, GR*PIXEL
fenster = pg.display.set_mode((fenster_b, fenster_h))
clock = pg.time.Clock()

koord = {(s,z) for z in range(GR) for s in range(GR)}
bäume = set(rnd.sample(koord, int(GR*GR*START_BÄUME)))
brennen = set() 

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
  
  fenster.fill('#000000')
  bäume, brennen = sim(bäume, brennen)
  zeige_wald(bäume, brennen)

  pg.display.flip()