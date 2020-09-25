import pygame as pg


def generiere_zugliste(weiss):
  züge, schläge = [], []
  for von,stein in brett.items():
    if stein not in steine[weiss]: continue
    for n in richtungen[brett[von]]:
      über = False
      for i in range(1,abs(brett[von])+1):  
        zu = von+n*i
        if zu not in brett or brett[zu] != 0: break
        züge.append([[von, zu, über]])
      for i in range(1,abs(brett[von])+1): 
        über = von+n*i
        zu = über + n
        if zu not in brett or über not in brett: break
        if brett[zu] != 0 and brett[über] != 0: break
        if brett[zu] == 0 and brett[über] in steine[not weiss]:
          schläge.append([[von, zu, über]])
          break
  return züge if not schläge else schläge


def ziehe(zug):
  for von, zu, über in zug:
    brett[zu], brett[von] = brett[von], 0
    if über:
      brett[über] = 0
    if zu in umwandlung[weiss] and abs(brett[zu]) == 1:
      brett[zu] *= 8


def feld_zentrum(feld):
  s, z = feld % 8, feld // 8
  zentrum = ZELLE // 2
  return (s * ZELLE + zentrum, z * ZELLE + zentrum)


def xy2cell(pos):
  x, y = pos
  return y // ZELLE * 8 + x // ZELLE


def cell2xy(i):
  return i % 8 * ZELLE, i // 8 * ZELLE


brett = {i: 0 for i in range(64) if i % 8 % 2 != i // 8 % 2}
for i in range(64):
  if i not in brett: continue
  if i < 24:
    brett[i] = -1
  if i > 39:
    brett[i] = 1
richtungen = {1: (-7, -9), -1: (7, 9), -8: (-7,-9,9,7), 8: (-7,-9,9,7)}
steine = {True: {1, 8}, False: (-1, -8)}
umwandlung = {True: {1, 3, 5, 7}, False: {56, 58, 60, 62}}


weiss = True

AUFLÖSUNG = 800
ZELLE = AUFLÖSUNG // 8
pg.init()
screen = pg.display.set_mode([AUFLÖSUNG, AUFLÖSUNG])
weitermachen = True
clock = pg.time.Clock()
züge = generiere_zugliste(weiss)
von = 0
while weitermachen:
  clock.tick(20)
  screen.fill((0, 0, 0))
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      if von:
        zu = xy2cell(pg.mouse.get_pos())
        for zug in züge:
          if zug[0][0] == von and zug[0][1] == zu: 
            ziehe(zug)
            weiss = not weiss#
            züge = generiere_zugliste(weiss)
            von = 0
      von = xy2cell(pg.mouse.get_pos())
  for i in range(64):
    color = (209, 139, 71) if i in brett else (254, 206, 158)
    pg.draw.rect(screen, color, (cell2xy(i), (ZELLE, ZELLE)))
    if i in brett and brett[i] != 0:
      color = (255, 255, 255) if brett[i] > 0 else (0, 0, 0)
      pg.draw.circle(screen, color, feld_zentrum(i), int(ZELLE*0.2))
      if abs(brett[i]) == 8:
        color = (255, 255, 255) if brett[i] -8 else (0, 0, 0)
        pg.draw.circle(screen, color, feld_zentrum(i), int(ZELLE*0.1))
    for zug in züge:
      pg.draw.rect(screen, (0,50,0), (cell2xy(zug[0][0]), (ZELLE, ZELLE)), 5)
      if von == zug[0][0]:
        pg.draw.circle(screen, (0,0,100), feld_zentrum(zug[0][1]), int(ZELLE*0.1) )
  pg.display.flip()

pg.quit()
