import pygame as pg
import random as rnd


def update(sandkörner):
  sandkörner2 = dict()
  for (x, y), farbe in sandkörner.items():
    a, b, c = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    if b not in sandkörner:
      x, y = b
    elif a not in sandkörner and c not in sandkörner:
      x, y = rnd.choice([a, c])
    elif a not in sandkörner:
      x, y = a
    elif c not in sandkörner:
      x, y = c
    sandkörner2[x, min(höhe // skalierung, y)] = farbe
  return sandkörner2


pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 80

sandkörner = dict()
hue = 0
skalierung = 5

# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  fenster.fill('black')
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()

  if pg.mouse.get_pressed()[0]:
    farbe = pg.Color(0)
    hue = (hue + 1) % 360
    farbe.hsva = hue, 100, 100
    x, y = pg.mouse.get_pos()
    sandkörner[x // skalierung, y // skalierung] = farbe

  for (x, y), farbe in sandkörner.items():
    pg.draw.rect(fenster, farbe, (x * skalierung, y * skalierung, skalierung, skalierung))

  sandkörner = update(sandkörner)

  pg.display.flip()
