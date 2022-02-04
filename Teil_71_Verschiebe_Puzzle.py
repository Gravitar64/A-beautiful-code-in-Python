import pygame as pg
import random as rnd 


def i2pos(i):
  return i % spalten*breite, i//spalten*höhe


def pos2i(x, y):
  return int(x//breite + y//höhe*spalten)


def vertausche(leer, kachel):
  kacheln[leer], kacheln[kachel] = kacheln[kachel], kacheln[leer]


def get_nachbarn(empty):
  x, y = i2pos(empty)
  n = [pos for pos in ((x+breite, y), (x-breite, y), (x, y+höhe), (x, y-höhe))]
  return [pos2i(x, y) for x, y in n if 0 <= x < screen_breite and 0 <= y < screen_höhe]


def mischen():
  global leer
  for _ in range(100):
    kachel = rnd.choice(get_nachbarn(leer))
    vertausche(leer, kachel)
    leer = kachel


spalten = zeilen = 3
screen_breite = screen_höhe = 800
breite, höhe = screen_breite / spalten, screen_höhe / zeilen
screen  = pg.display.set_mode((screen_breite, screen_höhe))

bild = pg.image.load('Teil_71_katze.jpg')
bild = pg.transform.smoothscale(bild, (screen_breite, screen_höhe))
kacheln = [bild.subsurface((i*breite, j*höhe, breite, höhe))
           for j in range(zeilen) for i in range(spalten)]
pg.draw.rect(kacheln[-1], '#000000', (0, 0, breite, höhe))
leer = len(kacheln)-1

clock = pg.time.Clock()
FPS = 40

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      if ereignis.button == 1:
        pos = pg.mouse.get_pos()
        i = pos2i(*pos)
        if i in get_nachbarn(leer):
          vertausche(leer, i)
          leer = i
      if ereignis.button == 3:
        mischen()

  for i,kachel in enumerate(kacheln):
    pos = i2pos(i)
    screen.blit(kachel, pos)
  for i in range(spalten):
    pg.draw.rect(screen,'#ffffff',(i*breite,0,breite,screen_höhe),1)  
    pg.draw.rect(screen,'#ffffff',(0,i*höhe,screen_breite,höhe),1)  
  pg.display.flip()