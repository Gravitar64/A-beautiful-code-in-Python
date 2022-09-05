import random as rnd
import pygame as pg


def feuerwalze(bäume, brand):
    return {(s+ds, z+dz) for s,z in brand for ds in range(-1,2) for dz in range(-1,2) if (s+ds, z+dz) in bäume}
   
   
def zeichne_fläche(bäume, brand):
    for s,z in bäume | brand:
        farbe = '#00ff00' if (s,z) in bäume else '#ff0000'
        pg.draw.rect(fenster,farbe,(s*pixel, z*pixel, pixel, pixel))
    

ANF_BESTAND, WACHSTUM, BRAND = 0.2, 0.01, 0.01
fläche = {(s,z) for s in range(bh) for z in range(bh)}
bäume = set(rnd.sample(list(fläche), int(bh*bh*ANF_BESTAND)))
brand = set()

pg.init()
bh, pixel, FPS = 80, 10, 25
fenster = pg.display.set_mode((bh*pixel, bh*pixel))
clock = pg.time.Clock()

while True:
    clock.tick(FPS)
    for ereignis in pg.event.get():
        if ereignis.type == pg.QUIT: quit()
    
    leer = fläche - bäume - brand
    bäume |= set(rnd.sample(list(leer), int(len(leer)*WACHSTUM)))
    brand |= set(rnd.sample(list(bäume), int(len(bäume)*BRAND)))
    bäume -= brand
    brand = feuerwalze(bäume, brand)
    
    fenster.fill('#000000')
    zeichne_fläche(bäume-brand, brand)
    pg.display.flip()
