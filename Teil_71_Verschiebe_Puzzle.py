import pygame as pg
import random as rnd


def generiere_felder(bild):
  b = bild.copy()
  breite, höhe = screen_breite/spalten, screen_höhe/zeilen
  felder = [b.subsurface((s*breite, z*höhe, breite, höhe))
            for z in range(zeilen) for s in range(spalten)]
  pg.draw.rect(felder[-1], '#3274B3', (0, 0, breite, höhe))
  return felder, len(felder)-1, breite, höhe


def i2pos(i):
  return i % spalten * breite, i // spalten * höhe


def pos2i(x, y):
  return int(x//breite + y//höhe*spalten)


def vertausche(feld):
  global leer
  felder[feld], felder[leer] = felder[leer], felder[feld]
  leer = feld


def get_nachbarn():
  s, z = leer % spalten, leer // zeilen
  return [s1+z1*spalten for s1, z1 in ((s+1, z), (s-1, z), (s, z-1), (s, z+1))
          if -1 < s1 < spalten and -1 < z1 < zeilen]


def mischen():
  for _ in range(spalten*zeilen*10):
    feld = rnd.choice(get_nachbarn())
    vertausche(feld)


screen_breite = screen_höhe = 1000
spalten = zeilen = 3
screen = pg.display.set_mode((screen_breite, screen_höhe))
bild = pg.image.load('Teil_71_katze.jpg')
bild = pg.transform.smoothscale(bild, (screen_breite, screen_höhe))
felder, leer, breite, höhe = generiere_felder(bild)

clock = pg.time.Clock()
FPS = 40

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      if ereignis.button == 3:
        mischen()
      if ereignis.button == 1:
        feld = pos2i(*pg.mouse.get_pos())
        if feld in get_nachbarn():
          vertausche(feld)
    if ereignis.type == pg.MOUSEWHEEL:
      spalten = max(2, spalten + ereignis.y)
      zeilen = max(2, zeilen + ereignis.y)
      felder, leer, breite, höhe = generiere_felder(bild)

  screen.fill((0, 0, 0))
  for i, feld in enumerate(felder):
    pos = i2pos(i)
    screen.blit(feld, pos)
    pg.draw.rect(screen, '#000000', (*pos, breite, höhe), 1)
  pg.display.flip()
