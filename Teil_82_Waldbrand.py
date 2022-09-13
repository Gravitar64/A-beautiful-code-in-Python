import pygame as pg
import random as rnd


def feuerwalze(bäume, brand):
    return {(s+ds, z+dz) for s,z in brand for ds in range(-1,2) for dz in range(-1,2) if (s+ds, z+dz) in bäume}


def zeichne_wald(bäume, brand):
    for s,z in bäume | brand:
        farbe = '#00ff00' if (s,z) in bäume else '#ff0000'
        pg.draw.rect(fenster, farbe, (s*PIXEL, z*PIXEL, PIXEL, PIXEL))


pg.init()
GR, PIXEL, FPS = 80, 10, 25
ANF_BESTAND, WACHSTUM, BRAND = 0.2, 0.01, 0.0005
fenster = pg.display.set_mode((GR*PIXEL, GR*PIXEL))
clock = pg.time.Clock()

fläche = {(s,z) for s in range(GR) for z in range(GR)}
bäume = set(rnd.sample(fläche, int(len(fläche)*ANF_BESTAND)))
brand = set()


while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()

  leer = fläche - bäume - brand
  bäume |= set(rnd.sample(leer, int(len(leer)*WACHSTUM)))
  brand |= set(rnd.sample(bäume, int(len(bäume)*BRAND)))
  brand = feuerwalze(bäume-brand, brand)
  bäume -= brand

  fenster.fill('#000000')
  zeichne_wald(bäume, brand)
  pg.display.flip()