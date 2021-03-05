import pygame as pg

def i2pos(i):
  return i % 8, i // 8

def pos2xy(pos):
  return pos[0]*FELD, pos[1]*FELD

def zeichneBrett():
  for pos, feld in BRETT.items():
    color = '#DFBF93' if feld else '#C5844E'
    pg.draw.rect(screen, color, (*pos2xy(pos), FELD, FELD))  

pg.init()
BREITE, HÖHE = 800, 800
FELD = 100
FPS = 40
zentrum = (BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))

BRETT = {i2pos(i): i // 8 % 2 == i % 8 % 2 for i in range(64)}

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  screen.fill((0,0,0))
  zeichneBrett()
  pg.display.flip()

pg.quit()