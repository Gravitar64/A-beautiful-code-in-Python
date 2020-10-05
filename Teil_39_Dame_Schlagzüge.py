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
  zugliste, schlagzüge_gesamt = defaultdict(list), defaultdict(list)
  for von,stein in brett.items():
    if stein not in steine[spieler]: continue
    schlagzüge_gesamt.update(generiere_schläge(spieler, von, stein, [], defaultdict(list)))
    if schlagzüge_gesamt: continue
    for richtung in richtungen[stein]:
      for n in range(1,abs(stein)+1):
        zu = von + richtung * n
        if zu not in brett or brett[zu] != 0:
          break
        zugliste[von].append([zu,von,stein,None,None])
  return schlagzüge_gesamt if schlagzüge_gesamt else zugliste

def generiere_schläge(spieler, von, stein, zug, schlagzüge_von):
  sackgasse = True
  for richtung in richtungen[stein]:
    for n in range(1,abs(stein)+1):
      über = von + richtung * n
      zu = über + richtung
      if über not in brett or zu not in brett or \
        brett[über] in steine[spieler] or \
        (brett[über] != 0 and brett[zu] != 0):
        break
      if brett[über] in steine[not spieler] and brett[zu] == 0:
        sackgasse = False
        sprung = [zu, von, stein, über, brett[über]]
        zug.extend(sprung)
        ziehe(spieler, sprung)
        generiere_schläge(spieler, zu, stein, zug.copy(), schlagzüge_von)
        ziehe_rückgängig(spieler, sprung)
        zug = zug[:-5]
        break
  if sackgasse and zug:
    schlagzüge_von[zug[1]].append(zug)
  return schlagzüge_von        

def ziehe(spieler, zug):
  for i in range(0, len(zug), 5):
    zu, von, stein, über, geschlagen = zug[i:i+5]
    brett[von] = 0
    brett[zu] = stein
    if über:
      brett[über] = 0
  if zu in letzte_reihe[spieler] and abs(stein) == 1:
    brett[zu] *= 8

def ziehe_rückgängig(spieler, zug):
  for i in reversed(range(0, len(zug), 5)):
    zu, von, stein, über, geschlagen = zug[i:i+5]
    brett[von] = stein
    brett[zu] = 0
    if über:
      brett[über] = geschlagen
  





brett = {nr:0 for nr in range(64) if nr // 8 % 2 != nr % 8 % 2}
# for feld in brett:
#   if feld < 24:
#     brett[feld] = -1
#   elif feld > 39:
#     brett[feld] = 1
brett[60] = 1
brett[35] = 8
brett[51] = -1
brett[53] = -1
brett[33] = -1
brett[37] = -1
brett[17] = -1
brett[19] = -1
brett[21] = -1

am_zug = True
steine = {True:{1,8}, False:{-1,-8}}
richtungen = {1: [-7,-9], -1:[7,9], -8:[7,9,-7,-9], 8:[7,9,-7,-9]}
letzte_reihe = {True: {1,3,5,7}, False: {56,58,60,62}}
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