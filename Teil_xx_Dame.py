import pygame as pg
from collections import defaultdict


def bewertung():
  return sum([stein for stein in brett.values()])

# def computer(weiss):
#   bewertete_züge = []
#   züge = generiere_zugliste(weiss)
#   for von,ziele in züge.items():
#     for zu,über,stein,geschlagen in ziele:
#       win = ziehe(weiss,von,zu,über,stein)
#       score = minimax(5, -999999, 999999, weiss, win, über, von, stein)
#       ziehe_rückgängig(weiss,von,zu,über,stein,geschlagen)
#       bewertete_züge.append([score,von,zu,über,stein,geschlagen])
      
#   bewertete_züge.sort(reverse=weiss)
#   score, von,zu,über,stein,geschlagen = bewertete_züge[0]
#   win = ziehe(weiss,von,zu,über,stein)
#   while über:
#     bewertete_züge = []
#     score = minimax(5,-999999, 999999, weiss, win, über, von, stein)
#     bewerte_züge.append([score,von,zu,über,stein,geschlagen])
#     for zu,über,stein,geschlagen in ziele
#   print(f'{"weiss" if weiss else "schwarz"} setzt {von}-{zu} mit der Bewertung {score}')
#   return win  

# # def minimax(tiefe, alpha, beta, weiss, win, über, von, stein):
#   if win:
#     return 99999+tiefe if weiss else -99999-tiefe
#   if tiefe == 0:
#     return bewerten()
#   if über and schlage(weiss, von,stein):
#     züge = schlage(weiss, von,stein)
#   else:
#     weiss = not weiss
#     züge = generiere_zugliste(weiss)
#   value = -999999 if weiss else 999999
#   for von,ziele in züge.items():
#     for zu,über,stein,geschlagen in ziele:
#       win = ziehe(weiss, von,zu,über,stein)
#       score = minimax(tiefe-1, alpha, beta, weiss, win, über, von, stein)
#       ziehe_rückgängig(weiss, von,zu,über,stein,geschlagen)
#     if weiss:
#       value = max(value, score)
#       alpha = max(value, alpha)  
#     else:
#       value = min(value, score)
#       beta = min(value, beta)
#     if alpha >= beta:
#       break
#   return value  

def minimax(tiefe, player, alpha, beta, von, über, stein):
  if tiefe == 5:
    return bewertung()
  if über and schlage(player, von, stein):
    children = schlage(player,von,stein)
  else:
    children = generiere_zugliste(player)
  if player:
    for von, ziele in children.items():
      for zu,über,stein,geschlagen in ziele:
        ziehe(player, von,zu,über,stein)
        if über:
          score = minimax(tiefe+1, player, alpha, beta, von, über, stein)
        else:
          score = minimax(tiefe+1, not player, alpha, beta, von, über, stein)  
        ziehe_rückgängig(player, von,zu,über,stein,geschlagen)
        if tiefe == 0:
          bewertete_züge.append((score,von,zu,über,stein,geschlagen))
        alpha = max(score, alpha)
        if alpha >= beta:
          break
    return alpha
  else:
    for von, ziele in children.items():
      for zu,über,stein,geschlagen in ziele:
        ziehe(player, von,zu,über,stein)
        if über:
          score = minimax(tiefe+1, player, alpha, beta, von, über, stein)
        else:
          score = minimax(tiefe+1, not player, alpha, beta, von, über, stein)  
        ziehe_rückgängig(player, von,zu,über,stein,geschlagen)
        if tiefe == 0:
          bewertete_züge.append((score,von,zu,über,stein,geschlagen))
        beta = min(score,beta)
        if alpha >= beta:
          break
    return beta   

     

def schlage(weiss, von, stein):
  schläge = defaultdict(list)
  for n in richtungen[stein]:
    über = False
    for i in range(1, abs(stein)+1):
      über = von + n * i
      zu = über + n
      if (zu not in brett or über not in brett) or (brett[zu] != 0 and brett[über] != 0):
        break
      if brett[zu] == 0 and brett[über] in steine[not weiss]:
        schläge[von].append([zu, über, stein, brett[über]])
        break
  return schläge


def generiere_zugliste(weiss):
  züge, schläge = defaultdict(list), {}
  for von, stein in brett.items():
    if stein not in steine[weiss]: continue
    schläge.update(schlage(weiss, von, stein))
    if schläge: continue
    for n in richtungen[stein]:
      for i in range(1, abs(stein)+1):
        zu = von+n*i
        if zu not in brett or brett[zu] != 0:
          break
        züge[von].append([zu, False, brett[von], None])
  return züge if not schläge else schläge


def ziehe(weiss, von, zu, über, stein):
  brett[von], brett[zu] = 0, stein
  if über:
    brett[über] = 0
    anz_steine[not weiss] -= 1
  if zu in umwandlung[weiss] and abs(stein) == 1:
    brett[zu] *= 8
  return anz_steine[not weiss] == 0  


def ziehe_rückgängig(weiss, von, zu, über, stein, geschlagen):
  brett[von], brett[zu] = stein, 0
  if über:
    brett[über] = geschlagen
    anz_steine[not weiss] += 1
  if zu in umwandlung[weiss] and abs(stein) == 1:
    brett[von] = stein


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

for i in brett:
  if i < 24: brett[i] = -1
  if i > 39: brett[i] = 1
richtungen = {1: (-7, -9), -1: (7, 9), -8: (-7, -9, 9, 7), 8: (-7, -9, 9, 7)}
steine = {True: {1, 8}, False: (-1, -8)}
anz_steine = {True:12, False:12}
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
      if state == 'von':
        feld2 = xy2cell(pg.mouse.get_pos())
        if feld2 in {f for f, _, _, _ in züge[feld1]}:
          state = 'zu'
        else:
          state = None
      if not state:
        feld1 = xy2cell(pg.mouse.get_pos())
        if feld1 in züge:
          state = 'von'
    if state == 'zu':
      for zu, über, stein, _ in züge[feld1]:
        if zu == feld2:
          win = ziehe(weiss, feld1, feld2, über, stein)
          if über and schlage(weiss, feld2, stein):
            züge = schlage(weiss, feld2, stein)
            feld1 = feld2
            state = 'von'
            break
          else:
            state = None
            weiss = not weiss
            bewertete_züge = []
            erg = minimax(0, weiss, -99999, 99999, None, None, None)
            bewertete_züge.sort(reverse=weiss)
            score,von,zu,über,stein,geschlagen = bewertete_züge[0]
            print(score)
            ziehe(weiss,von,zu,über,stein)
            weiss = not weiss
            züge = generiere_zugliste(weiss)
            break

  for i in range(64):
    color = (209, 139, 71) if i in brett else (254, 206, 158)
    pg.draw.rect(screen, color, (cell2xy(i), (ZELLE, ZELLE)))
  for i in brett:
    if brett[i] != 0:
      color = (255, 255, 255) if brett[i] > 0 else (0, 0, 0)
      pg.draw.circle(screen, color, feld_zentrum(i), int(ZELLE*0.2))
      if abs(brett[i]) == 8:
        color = (255, 255, 255) if brett[i] - 8 else (0, 0, 0)
        pg.draw.circle(screen, color, feld_zentrum(i), int(ZELLE*0.05))
      if i in züge:
        pg.draw.rect(screen, (0, 50, 0), (cell2xy(i), (ZELLE, ZELLE)), 7)
  if state == 'von':
    pg.draw.rect(screen, (255, 0, 0), (cell2xy(feld1), (ZELLE, ZELLE)), 7)
    for zu, _, _, _ in züge[feld1]:
      pg.draw.circle(screen, (0, 0, 100), feld_zentrum(zu), int(ZELLE*0.1))
  pg.display.flip()

pg.quit()
