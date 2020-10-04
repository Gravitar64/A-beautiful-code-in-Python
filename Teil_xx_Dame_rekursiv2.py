import pygame as pg
from collections import defaultdict

cl_hellbraun = (254, 206, 158); cl_dunkelbraun = (209, 139, 71); cl_grün = (0, 50, 0)
cl_weiss = (255, 255, 255); cl_schwarz = (0, 0, 0); cl_dunkelblau = (0, 0, 100)
cl_hellblau = (0, 0, 255); cl_rot = (255, 0, 0)


def bewertung():
  return sum([stein for stein in brett.values()])


def generiere_schläge(spieler, von, stein, sequenz, sequenzen):
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
        sequenz.extend([zu, von, stein, über, brett[über]])
        ziehe(spieler, sequenz[-5:])
        generiere_schläge(spieler, zu, stein, sequenz.copy(), sequenzen)
        ziehe_rückgängig(spieler, sequenz[-5:])
        sequenz = sequenz[:-5]
        break
  if dead_end and sequenz:
    sequenzen[sequenz[1]].append(sequenz)
  return sequenzen


def generiere_zugliste(spieler):
  züge, schläge = defaultdict(list), defaultdict(list)
  for von, stein in brett.items():
    if stein not in steine[spieler]:
      continue
    schläge.update(generiere_schläge(
        spieler, von, stein, [], defaultdict(list)))
    if schläge:
      continue
    for n in richtungen[stein]:
      for i in range(1, abs(stein)+1):
        zu = von+n*i
        if zu not in brett or brett[zu] != 0:
          break
        züge[von].append([zu, von, stein, None, None])
  return schläge if schläge else züge


def ziehe(spieler, zug):
  for i in range(0, len(zug), 5):
    zu, von, stein, über, _ = zug[i:i + 5]
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
    zu, von, stein, über, geschlagen = zug[i:i+5]
    brett[von] = stein
    brett[zu] = 0
    if über:
      brett[über] = geschlagen
      anz_steine[not spieler] += 1


def minimax(tiefe, alpha, beta, spieler, win):
  if tiefe == 0:
    return (bewertung(), None)
  if win:
    return (-99999+tiefe if spieler else 99999-tiefe, None)
  zugliste = generiere_zugliste(spieler)
  if not zugliste:
    return (-99999+tiefe if spieler else 99999-tiefe, None)
  value = -999999 if spieler else 999999
  for züge in zugliste.values():
    for zug in züge:
      win = ziehe(spieler, zug)
      score, _ = minimax(tiefe-1, alpha, beta, not spieler, win)
      ziehe_rückgängig(spieler, zug)
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
  return value, bester_zug


def feld_zentrum(feld):
  s, z = feld % 8, feld // 8
  zentrum = ZELLE // 2
  return (s * ZELLE + zentrum, z * ZELLE + zentrum)


def xy2cell(pos):
  x, y = pos
  return y // ZELLE * 8 + x // ZELLE


def cell2xy(i):
  return i % 8 * ZELLE, i // 8 * ZELLE


def zeichne_stein(feld_nr):
  if feld_nr not in brett or brett[feld_nr] == 0:
    return
  farbe = cl_weiss if brett[feld_nr] > 0 else cl_schwarz
  pg.draw.circle(screen, farbe, feld_zentrum(feld_nr), int(ZELLE * 0.2))
  if abs(brett[feld_nr]) == 8:
    farbe = cl_weiss if brett[feld_nr] - 8 else cl_schwarz
    pg.draw.circle(screen, farbe, feld_zentrum(feld_nr), int(ZELLE * 0.05))


def zeichne_brett(status):
  for i in range(64):
    farbe = cl_dunkelbraun if i in brett else cl_hellbraun
    pg.draw.rect(screen, farbe, (cell2xy(i), (ZELLE, ZELLE)))
    zeichne_stein(i)
  if not status:
    for i in züge:
      pg.draw.rect(screen, cl_grün, (cell2xy(i), (ZELLE, ZELLE)), 7)
  if status == 'von ausgewählt':
    pg.draw.rect(screen, cl_rot, (cell2xy(sel_von), (ZELLE, ZELLE)), 7)
    for zug in züge[sel_von]:
      pg.draw.circle(screen, cl_dunkelblau,
                     feld_zentrum(zug[0]), int(ZELLE * 0.1))
  if status == 'zeige computerzug':
    for i in range(0, len(computerzug), 5):
      pg.draw.line(screen, cl_hellblau, feld_zentrum(
          computerzug[i]), feld_zentrum(computerzug[i+1]), 10)
    pg.draw.circle(screen, cl_hellblau, feld_zentrum(
        computerzug[-5]), int(ZELLE * 0.1))
  if numerierung:
    for von in brett:
      color = cl_weiss if brett[von] in steine[False] else cl_schwarz
      font = pg.font.Font(None, 32)
      text = font.render(str(von), True, color)
      text_rect = text.get_rect(center=(feld_zentrum(von)))
      screen.blit(text, text_rect)

  pg.display.flip()


def state_machine(status, feld):
  global züge, sel_von, weiss, computerzug
  erster_schlag = None

  if not status:
    if feld not in züge:
      return
    sel_von = feld
    return 'von ausgewählt'

  if status == 'von ausgewählt':
    for zug in züge[sel_von]:
      if feld == zug[0]:
        if len(zug) == 5:
          ziehe(weiss, zug)
          return 'computer'
        else:
          erster_schlag = zug[:5]
          züge[feld].append(zug[5:])
    if not erster_schlag:
      return
    ziehe(weiss, erster_schlag)
    sel_von = feld
    return 'von ausgewählt'

  if status == 'computer':
    weiss = not weiss
    _, computerzug = minimax(6, -999999, 999999, weiss, False)
    return 'zeige computerzug'

  if status == 'zeige computerzug':
    ziehe(weiss, computerzug)
    weiss = not weiss
    züge = generiere_zugliste(weiss)
    return


brett = {i: 0 for i in range(64) if i % 8 % 2 != i // 8 % 2}
brett[35] = 8
brett[51] = -1
brett[53] = -1
brett[33] = -1
brett[37] = -1
brett[17] = -1
brett[19] = -1
brett[21] = -1
# for i in brett:
#   if i < 24:
#     brett[i] = -1
#   if i > 39:
#     brett[i] = 1

richtungen = {1: (-7, -9), -1: (7, 9), -8: (-7, -9, 9, 7), 8: (-7, -9, 9, 7)}
steine = {True: {1, 8}, False: (-1, -8)}
anz_steine = {True: sum([1 for feld in brett.values() if feld > 0]),
              False: sum([1 for feld in brett.values() if feld < 0])}
umwandlung = {True: {1, 3, 5, 7}, False: {56, 58, 60, 62}}
weiss = True
züge = generiere_zugliste(weiss)
computerzug = []
sel_von = state = None
numerierung = False

AUFLÖSUNG = 800
ZELLE = AUFLÖSUNG // 8
pg.init()
screen = pg.display.set_mode([AUFLÖSUNG, AUFLÖSUNG])
weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(20)
  screen.fill((0, 0, 0))
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      state = state_machine(state, xy2cell(pg.mouse.get_pos()))
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_SPACE:
      numerierung = not numerierung
  zeichne_brett(state)
  if state == 'computer':
    state = state_machine(state, None)
    
pg.quit()
