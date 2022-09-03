import random as rnd
import pygame as pg


def zeichne_wald(bäume, brennen):
  for s,z in bäume | brennen:
    color = '#00ff00' if (s,z) in bäume else '#ff0000'
    pg.draw.rect(fenster,color,(s*PIXEL,z*PIXEL,PIXEL,PIXEL))
        

def feuer_nachbarn(bäume, brennen):
  brennen = {(s+ds, z+dz) for s,z in brennen 
                 for ds in range(-1,2)
                 for dz in range(-1,2)
                 if (s+ds, z+dz) in bäume}
  return bäume-brennen, brennen
    

ANF_BESTAND, WACHSTUM, FEUER = 0.2, 0.01, 0.001
GR, PIXEL = 80, 10
FPS = 25

pg.init()
fenster = pg.display.set_mode((GR*PIXEL, GR*PIXEL))
clock = pg.time.Clock()

koord = {(s,z) for z in range(GR) for s in range(GR)}
bäume = set(rnd.sample(koord, int(GR*GR*ANF_BESTAND)))
brennen = set() 

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
  
  leer = koord - bäume - brennen
  bäume |= set(rnd.sample(leer,int(len(leer)*WACHSTUM)))
  brennen |= set(rnd.sample(bäume,int(len(bäume)*FEUER)))
  bäume, brennen = feuer_nachbarn(bäume-brennen, brennen)
      
  fenster.fill('#000000')
  zeichne_wald(bäume, brennen)
  pg.display.flip()