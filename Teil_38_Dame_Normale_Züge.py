import pygame as pg
from collections import defaultdict

def feld2xy(feld):
  x = feld % 8 * FELD
  y = feld // 8 * FELD
  return x,y

def feld2zentrum(feld):
  x,y = feld2xy(feld)
  return x + FELD//2, y + FELD//2

def generiere_zugliste(spieler):
  zugliste = defaultdict(list)
  for von,stein in brett.items():
    if stein not in steine[spieler]: continue
    for richtung in richtungen[stein]:
      for n in range(1,abs(stein)+1):
        zu = von + richtung * n
        if zu not in brett or brett[zu] != 0:
          break
        zugliste[von].append([zu,von,stein,None,None])
  return zugliste      


brett = {nr:0 for nr in range(64) if nr // 8 % 2 != nr % 8 % 2}
# for feld in brett:
#   if feld < 24:
#     brett[feld] = -1
#   elif feld > 39:
#     brett[feld] = 1
brett[44] = 8
brett[26] = 1

am_zug = True
steine = {True:{1,8}, False:{-1,-8}}
richtungen = {1: [-7,-9], -1:[7,9], -8:[7,9,-7,-9], 8:[7,9,-7,-9]}
zugliste = generiere_zugliste(am_zug)
print(zugliste)
    

AUFLÖSUNG = 800
FELD = AUFLÖSUNG // 8
pg.init()
screen = pg.display.set_mode([AUFLÖSUNG, AUFLÖSUNG])
weitermachen = True
clock = pg.time.Clock()
while weitermachen:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  clock.tick(20)
  screen.fill((0,0,0))
  for feld in range(64):
    farbe = (209,139,71) if feld in brett else (254,206,158)
    pg.draw.rect(screen, farbe, (feld2xy(feld), (FELD, FELD)))
  for feld, stein in brett.items():
    if stein == 0: continue
    farbe = (0,0,0) if stein in (-1,-8) else (255,255,255)
    pg.draw.circle(screen, farbe, feld2zentrum(feld), int(FELD*0.2))

  pg.display.flip()

pg.quit()    