import pygame as pg
import random as rnd


def i2pos(i):
  return i % spalten*breite, i//spalten*höhe


def pos2i(x, y):
  return int(x//breite + y//höhe*spalten)


def vertausche(feld):
  global leer
  felder[leer], felder[feld] = felder[feld], felder[leer]
  leer = feld

def get_nachbarn():
  x, y = i2pos(leer)
  n = [pos for pos in ((x+breite, y), (x-breite, y), (x, y+höhe), (x, y-höhe))]
  return [pos2i(x, y) for x, y in n if 0 <= x < screen_breite and 0 <= y < screen_höhe]


def mischen():
  for _ in range(spalten*zeilen*10):
    feld = rnd.choice(get_nachbarn())
    vertausche(feld)


spalten = zeilen = 3
screen_breite = screen_höhe = 800
breite, höhe = screen_breite / spalten, screen_höhe / zeilen
screen = pg.display.set_mode((screen_breite, screen_höhe))


bild = pg.image.load('Teil_71_katze.jpg')
bild = pg.transform.smoothscale(bild, (screen_breite, screen_höhe))
felder = [bild.subsurface((s*breite, z*höhe, breite, höhe))
           for z in range(zeilen) for s in range(spalten)]
pg.draw.rect(felder[-1], '#1BA6A6', (0, 0, breite, höhe))
leer = len(felder)-1

clock = pg.time.Clock()
FPS = 20

while True:
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      if ereignis.button == 1:
        feld = pos2i(*pg.mouse.get_pos())
        if feld in get_nachbarn():
          vertausche(feld)
      if ereignis.button == 3:
        mischen()

  for i, feld in enumerate(felder):
    pos = i2pos(i)
    screen.blit(feld, pos)
    pg.draw.rect(screen, '#000000', (*pos, breite, höhe), 1)
  pg.display.flip()