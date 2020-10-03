from operator import ge
import pygame as pg
from collections import defaultdict

def ziehe(zug):
  stein,von,zu,über,geschlagen = zug
  brett[von] = 0
  brett[zu] = stein

def status_maschine(status, feld):
  global sel_von, am_zug, zugliste
  if not status:
    if feld not in zugliste: return
    sel_von = feld
    return 'von wurde ausgewählt'
  if status == 'von wurde ausgewählt':
    for zug in zugliste[sel_von]:
      if zug[2] == feld:
        ziehe(zug)
        am_zug = not am_zug
        zugliste = generiere_zugliste(am_zug)
        return


def generiere_zugliste(spieler):
  """Liefert eine Liste der gültigen Züge für den spieler (weiss = True, schwarz = False)
  in der Form: Dictionary[Key=von Feld]: Value = [stein,von,zu,über,geschlagen]"""
  zugliste = defaultdict(list)
  for von,stein in brett.items():
    if stein not in steine[spieler]: continue
    for richtung in richtungen[stein]:
      zu = von + richtung
      if zu in brett and brett[zu] == 0:
        zugliste[von].append([stein, von, zu, None, None])
  return zugliste      

def zeichne_brett():
  screen.fill((0,0,0))
  for feld in range(64):
    farbe = (209,139,71) if feld in brett else (254,206,158)
    pg.draw.rect(screen, farbe, (feld2xy(feld), (FELD, FELD)))
  for feld, stein in brett.items():
    if stein == 0: continue
    farbe = (0,0,0) if stein in (-1,-8) else (255,255,255)
    pg.draw.circle(screen, farbe, feld2zentrum(feld), int(FELD*0.2))
  for feld in zugliste:
    pg.draw.rect(screen, (0,50,0), (feld2xy(feld), (FELD, FELD)),7)
  if clickstatus == 'von wurde ausgewählt':
    pg.draw.rect(screen, (255,0,0), (feld2xy(sel_von), (FELD, FELD)),7)
    for zug in zugliste[sel_von]:
      pg.draw.circle(screen, (0,0,100), feld2zentrum(zug[2]), int(FELD*0.1))  

  pg.display.flip()

def feld2xy(feld):
  x = feld % 8 * FELD
  y = feld // 8 * FELD
  return x,y

def xy2feld(pos):
  x,y = pos
  return y // FELD * 8 + x // FELD

def feld2zentrum(feld):
  x,y = feld2xy(feld)
  return x + FELD//2, y + FELD//2

brett = {nr:0 for nr in range(64) if nr // 8 % 2 != nr % 8 % 2}
for feld in brett:
  if feld < 24:
    brett[feld] = -1
  elif feld > 39:
    brett[feld] = 1

am_zug=True
richtungen = {1:[-7,-9],8:[-7,-9,7,9], -1:[7,9], -8:[7,9,-7,-9]}
steine = {True: {1,8}, False: {-1,-8}}
clickstatus = sel_von = None  

AUFLÖSUNG = 800
FELD = AUFLÖSUNG // 8
pg.init()
screen = pg.display.set_mode([AUFLÖSUNG, AUFLÖSUNG])
weitermachen = True
clock = pg.time.Clock()
zugliste = generiere_zugliste(am_zug)

while weitermachen:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      clickstatus = status_maschine(clickstatus, xy2feld(pg.mouse.get_pos()))  
  clock.tick(20)
  zeichne_brett()

pg.quit()    