import random as rnd
import pygame as pg


def zeichne_wald(wald, brand):
  for s,z in wald | brand:
    color = '#00ff00' if (s,z) in wald else '#ff0000'
    pg.draw.rect(fenster,color,(s*PIXEL,z*PIXEL,PIXEL,PIXEL))
        

def feuer_nachbarn(wald, brand):
  brand = {(s+ds, z+dz) for s,z in brand 
                 for ds in range(-1,2)
                 for dz in range(-1,2)
                 if (s+ds, z+dz) in wald}
  return wald-brand, brand
    

ANF_BESTAND, WACHSTUM, FEUER = 0.2, 0.01, 0.001
GR, PIXEL = 80, 10
FPS = 25

pg.init()
fenster = pg.display.set_mode((GR*PIXEL, GR*PIXEL))
clock = pg.time.Clock()

koord = {(s,z) for z in range(GR) for s in range(GR)}
wald = set(rnd.sample(koord, int(GR*GR*ANF_BESTAND)))
brand = set() 

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
  
  leer = koord - wald - brand
  wald |= set(rnd.sample(leer,int(len(leer)*WACHSTUM)))
  brand |= set(rnd.sample(wald,int(len(wald)*FEUER)))
  wald, brand = feuer_nachbarn(wald-brand, brand)
      
  fenster.fill('#000000')
  zeichne_wald(wald, brand)
  pg.display.flip()