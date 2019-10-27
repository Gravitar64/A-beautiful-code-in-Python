import pygame as pg
import random as rnd


def gruppenbildung(liste, gruppengröße):
  for n in range(0, len(liste), gruppengröße):
    yield liste[n:n+gruppengröße]


namen = 'Andreas Peter Jan Simone Jörg Daniela Klaus Dirk Heike Elke'.split()

BREITE, HÖHE = 1000, 600
pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])

weitermachen = True
clock = pg.time.Clock()

fps = 1
rnd.seed()
while weitermachen:
  clock.tick(fps)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_SPACE:
      fps = 1

  if fps < 50:
    screen.fill((0, 0, 0))
    rnd.shuffle(namen)
    for i, name in enumerate(namen):
      textfläche = pg.font.SysFont('impact', 36).render(
          f'{name}', False, (0, 100, 255))
      screen.blit(textfläche, (0, i*40))
    fps += 1
  else:
    for i, gruppe in enumerate(gruppenbildung(namen, 2)):
      text = ",   ".join(gruppe)
      textfläche = pg.font.SysFont('impact', 36).render(
          f'Gruppe {i+1}:  {text}', False, (0, 255, 255))
      screen.blit(textfläche, (200, i*40))
  pg.display.flip()

pg.quit()
