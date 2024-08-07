import pygame as pg
import random as rnd


def generiere_felder():
  b = bild.copy()
  breite, höhe = scr_b / spalten, scr_h / zeilen
  felder = [b.subsurface((s * breite, z * höhe, breite, höhe))
            for z in range(zeilen) for s in range(spalten)]
  pg.draw.rect(felder[-1], '#3274B3', (0, 0, breite, höhe))
  return felder, len(felder) - 1, breite, höhe


def i2pos(i):
  return i % spalten * breite, i // spalten * höhe


def pos2i(x, y):
  return int(x // breite + y // höhe * spalten)


def vertausche(feld):
  global leer
  felder[feld], felder[leer] = felder[leer], felder[feld]
  leer = feld


def generiere_nachbarn():
  s, z = leer % spalten, leer // spalten
  return [s1 + z1 * spalten for s1, z1 in ((s + 1, z), (s - 1, z), (s, z - 1), (s, z + 1))
          if -1 < s1 < spalten and -1 < z1 < zeilen]


def mischen():
  for _ in range(spalten * zeilen * 10):
    vertausche(rnd.choice(generiere_nachbarn()))


scr_b = scr_h = 1000
spalten = zeilen = 4
screen = pg.display.set_mode((scr_b, scr_h))
bild = pg.image.load('teil_071_katze.jpg')
bild = pg.transform.smoothscale(bild, (scr_b, scr_h))
felder, leer, breite, höhe = generiere_felder()


clock = pg.time.Clock()
FPS = 40

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
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
      felder, leer, breite, höhe = generiere_felder()

  for i, feld in enumerate(felder):
    screen.blit(feld, i2pos(i))
    pg.draw.rect(screen, '#ffffff', (*i2pos(i), breite, höhe), 3)
  pg.display.flip()
