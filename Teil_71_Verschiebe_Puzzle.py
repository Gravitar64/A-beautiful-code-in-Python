import pygame as pg
import random as rnd


def i2pos(i):
  return i % spalten * breite, i // spalten * höhe


def pos2i(x, y):
  return int(x//breite + y//höhe*spalten)


def vertausche(feld):
  global leer
  felder[feld], felder[leer] = felder[leer], felder[feld]
  leer = feld


def generiere_nachbarn():
  s, z = leer % spalten, leer // spalten
  return [s1+z1*spalten for s1, z1 in ((s+1, z), (s-1, z), (s, z-1), (s, z+1))
          if -1 < s1 < spalten and -1 < z1 < zeilen]


def generiere_felder(bild):
  b = bild.copy()
  breite, höhe = screen_breite / spalten, screen_höhe / zeilen
  felder = [b.subsurface((s*breite, z*höhe, breite, höhe))
            for z in range(zeilen) for s in range(spalten)]
  pg.draw.rect(felder[-1], '#4068B8', (0, 0, breite, höhe))
  return felder, len(felder)-1, breite, höhe


def mischen():
  for _ in range(spalten*zeilen*10):
    nachb = generiere_nachbarn()
    feld = rnd.choice(nachb)
    vertausche(feld)


spalten = zeilen = 3
screen_breite = screen_höhe = 1000
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
      if ereignis.button == 1:
        pos = pg.mouse.get_pos()
        feld = pos2i(*pos)
        if feld in generiere_nachbarn():
          vertausche(feld)
      if ereignis.button == 3:
        mischen()
    if ereignis.type == pg.MOUSEWHEEL:
      spalten = max(2, spalten + ereignis.y)
      zeilen = max(2, zeilen + ereignis.y)
      felder, leer, breite, höhe = generiere_felder(bild)
  for i, feld in enumerate(felder):
    pos = i2pos(i)
    screen.blit(feld, pos)
    pg.draw.rect(screen, '#000000', (*pos, breite, höhe), 1)

  pg.display.flip()
