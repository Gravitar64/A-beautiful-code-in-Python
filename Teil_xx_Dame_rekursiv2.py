import pygame as pg
from collections import defaultdict


def bewertung():
  return sum([stein for stein in brett.values()])


def schlage(spieler,von,stein,zug,züge):
  dead_end = True
  for n in richtungen[stein]:
    for i in range(1, abs(stein)+1):
      über = von + n*i
      zu = über + n
      if über not in brett or zu not in brett or \
         brett[über] in steine[spieler] or \
         (brett[über] != 0 and brett[zu] != 0):
        break
      if brett[über] in steine[not spieler] and brett[zu] == 0:
        dead_end = False
        zug.extend([von,zu,über,stein,brett[über]])
        ziehe(spieler,zug[-5:])
        schlage(spieler, zu, stein, zug.copy(),züge)
        ziehe_rückgängig(spieler,zug[-5:])
        zug = zug[:-5]
        break
  if dead_end and zug:
    züge[zug[0]].append(zug)
  return züge   

        

def generiere_zugliste(spieler):
  züge, schläge = defaultdict(list), defaultdict(list)
  for von,stein in brett.items(): 
    if stein not in steine[spieler]: continue
    schläge.update(schlage(spieler,von,stein,[], defaultdict(list)))
    if schläge: continue
    for n in richtungen[stein]:
      for i in range(1, abs(stein)+1):
        zu = von+n*i
        if zu not in brett or brett[zu] != 0:
          break
        züge[von].append([von, zu, None, stein,  None])
  return schläge if schläge else züge

def ziehe(spieler, zug):
  for i in range(0, len(zug), 5):
    von, zu, über, stein, _ = zug[i:i + 5]
    brett[von] = 0
    brett[zu] = stein
    if über: 
      brett[über] = 0
      anz_steine[not spieler] -= 1
  if zu in umwandlung[spieler] and abs(stein) == 1:
    brett[zu] *= 8
  return anz_steine[not spieler] == 0

def ziehe_rückgängig(spieler, zug):
  for i in reversed(range(0, len(zug), 5)):
    von, zu, über, stein, geschlagen = zug[i:i+5]
    brett[von] = stein
    brett[zu] = 0
    if über:
      brett[über] = geschlagen
      anz_steine[not spieler] += 1

def minimax(tiefe, maxtiefe, alpha, beta, spieler, win):
  if win:
    score = -99999+tiefe if spieler else 99999-tiefe
    return (score, None)
  if tiefe == maxtiefe or 0 in anz_steine.values(): 
    return (bewertung(), None) 
  zugliste = generiere_zugliste(spieler)
  if not zugliste:
    return (-99999 if spieler else 99999, None)
  value = -999999 if spieler else 999999
  for züge in zugliste.values():
    for zug in züge:
      win = ziehe(spieler, zug)
      score,_ = minimax(tiefe+1, maxtiefe, alpha, beta, not spieler, win)
      ziehe_rückgängig(spieler,zug)
      if spieler:
        if score > value:
          bester_zug = zug
          value = score
          alpha = max(value, alpha)
      else:
        if score < value:
          bester_zug = zug
          value = score
          beta = min(value, beta)
      if alpha >= beta:
        break    
  return (value, bester_zug)

 

def bester_zug(spieler):
  score, bester_zug = minimax(0,6,-999999, 999999, spieler, False)
  print(score, bester_zug)
  return bester_zug
  

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

# Teststellung für mehrfachschlagen
# brett[26] = -8
# brett[28] = -8
# brett[33] = 1
# brett[35] = 1
# brett[53] = 1
# brett[46] = 1
# brett[21] = 1
# brett[17] = 1
# brett[19] = 1
# brett[10] = 1

# brett[7] = -1
# brett[62] = -8
# brett[28] = 1
# brett[40] = 1

# brett[62] = -8
# brett[53] = -1
# brett[17] = 1


for i in brett:
  if i < 24: brett[i] = -1
  if i > 39: brett[i] = 1
richtungen = {1: (-7, -9), -1: (7, 9), -8: (-7, -9, 9, 7), 8: (-7, -9, 9, 7)}
steine = {True: {1, 8}, False: (-1, -8)}
anz_steine = {True: sum([1 for feld in brett.values() if feld > 0]),
              False: sum([1 for feld in brett.values() if feld < 0])}
umwandlung = {True: {1, 3, 5, 7}, False: {56, 58, 60, 62}}

weiss = True

AUFLÖSUNG = 800
ZELLE = AUFLÖSUNG // 8
pg.init()
screen = pg.display.set_mode([AUFLÖSUNG, AUFLÖSUNG])
weitermachen = True
clock = pg.time.Clock()
züge = generiere_zugliste(weiss)
state = None

while weitermachen:
  clock.tick(20)
  screen.fill((0, 0, 0))
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      if state == 'zeige_computerzug':
        ziehe(weiss,best)
        weiss = not weiss
        state = None
        züge = generiere_zugliste(weiss)
      if state == 'von':
        feld2 = xy2cell(pg.mouse.get_pos())
        if feld2 in {zug[1] for zug in züge[feld1]}:
          state = 'zu'
        else:
          state = None
      if not state:
        feld1 = xy2cell(pg.mouse.get_pos())
        if feld1 in züge:
          state = 'von'
    if state == 'zu':
      for zug in züge[feld1]:
        if zug[1] == feld2:
          if len(zug) > 5:
            win = ziehe(weiss, zug[:5])
            feld1 = zug[1]
            zug = zug[5:]
            züge[feld1] = [zug]
            state = 'von'
          else:
            ziehe(weiss, zug)
            weiss = not weiss
            best = bester_zug(weiss)
            state = 'zeige_computerzug'
            break

  for i in range(64):
    color = (209, 139, 71) if i in brett else (254, 206, 158)
    pg.draw.rect(screen, color, (cell2xy(i), (ZELLE, ZELLE)))
  for i in brett:
    if brett[i] != 0:
      color = (255, 255, 255) if brett[i] > 0 else (0, 0, 0)
      pg.draw.circle(screen, color, feld_zentrum(i), int(ZELLE * 0.2))
      if abs(brett[i]) == 8:
        color = (255, 255, 255) if brett[i] - 8 else (0, 0, 0)
        pg.draw.circle(screen, color, feld_zentrum(i),
                       int(ZELLE * 0.05))
      if not state and i in züge:
        pg.draw.rect(screen, (0, 50, 0), (cell2xy(i), (ZELLE, ZELLE)),7)
  if state == 'zeige_computerzug':
    for n in range(0,len(best),5):
      pg.draw.line(screen, (0,0,100), feld_zentrum(best[n]), feld_zentrum(best[n+1]),10)
    
  if state == 'von':
    pg.draw.rect(screen, (255, 0, 0), (cell2xy(feld1), (ZELLE, ZELLE)), 7)
    for zug in züge[feld1]:
      pg.draw.circle(screen, (0, 0, 100), feld_zentrum(zug[1]),
                     int(ZELLE * 0.1))
  pg.display.flip()

pg.quit()
