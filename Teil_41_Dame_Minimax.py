import pygame as pg
from collections import defaultdict


def feld2xy(feld):
  x = feld % 8 * FELD
  y = feld // 8 * FELD
  return x, y


def feld2zentrum(feld):
  x, y = feld2xy(feld)
  return x + FELD//2, y + FELD//2


def generiere_zugliste(spieler):
  zugliste, schlagzüge_gesamt = defaultdict(list), defaultdict(list)
  for von, stein in brett.items():
    if stein not in steine[spieler]:
      continue
    schlagzüge_gesamt.update(generiere_schläge(
        spieler, von, stein, [], defaultdict(list)))
    if schlagzüge_gesamt:
      continue
    for richtung in richtungen[stein]:
      for n in range(1, abs(stein)+1):
        zu = von + richtung * n
        if zu not in brett or brett[zu] != 0:
          break
        zugliste[von].append([zu, von, stein, None, None])
  return schlagzüge_gesamt if schlagzüge_gesamt else zugliste


def generiere_schläge(spieler, von, stein, zug, schlagzüge_von):
  sackgasse = True
  for richtung in richtungen[stein]:
    for n in range(1, abs(stein)+1):
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
      anz_steine[not spieler] -= 1

  if zu in letzte_reihe[spieler] and abs(stein) == 1:
    brett[zu] *= 8


def ziehe_rückgängig(spieler, zug):
  for i in reversed(range(0, len(zug), 5)):
    zu, von, stein, über, geschlagen = zug[i:i+5]
    brett[von] = stein
    brett[zu] = 0
    if über:
      brett[über] = geschlagen
      anz_steine[not spieler] += 1


def bewerte_position():
  return sum(wert for wert in brett.values())


def win(spieler):
  return anz_steine[not spieler] == 0


def minimax(tiefe, alpha, beta, spieler):
  if tiefe == 0:
    return (bewerte_position(), None)
  if win(spieler):
    return (99999 if spieler else -99999, None)
  zugliste = generiere_zugliste(spieler)
  if not zugliste:
    return (-99999 if spieler else 99999, None)
  beste_bewertung = -999999 if spieler else 999999
  for züge in zugliste.values():
    for zug in züge:
      ziehe(spieler, zug)
      wert, _ = minimax(tiefe-1, alpha, beta, not spieler)
      ziehe_rückgängig(spieler, zug)
      if spieler:
        if wert > beste_bewertung:
          beste_bewertung = wert
          bester_zug = zug
          alpha = max(wert, alpha)
      else:
        if wert < beste_bewertung:
          beste_bewertung = wert
          bester_zug = zug
          beta = min(wert, beta)
      if alpha >= beta:
        break
  return beste_bewertung, bester_zug


brett = {nr: 0 for nr in range(64) if nr // 8 % 2 != nr % 8 % 2}
for feld in brett:
  if feld < 24:
    brett[feld] = -1
  elif feld > 39:
    brett[feld] = 1


am_zug = True
steine = {True: {1, 8}, False: {-1, -8}}
richtungen = {1: [-7, -9], -1: [7, 9], -8: [7, 9, -7, -9], 8: [7, 9, -7, -9]}
letzte_reihe = {True: {1, 3, 5, 7}, False: {56, 58, 60, 62}}
anz_steine = {True: sum(1 for stein in brett.values() if stein > 0),
              False: sum(1 for stein in brett.values() if stein < 0)}
zugliste = generiere_zugliste(am_zug)
clickstatus = feld1 = computerzug = bewertung = None
for von, züge in zugliste.items():
  for zug in züge:
    print(f'von: {von} -> {zug}')


AUFLÖSUNG = 800
FELD = AUFLÖSUNG // 8
pg.init()
screen = pg.display.set_mode([AUFLÖSUNG, AUFLÖSUNG])
weitermachen = True
clock = pg.time.Clock()


def zeichne_brett():
  screen.fill((0, 0, 0))
  for feld in range(64):
    farbe = (209, 139, 71) if feld in brett else (254, 206, 158)
    pg.draw.rect(screen, farbe, (feld2xy(feld), (FELD, FELD)))
  for feld, stein in brett.items():
    if stein == 0:
      continue
    farbe = (0, 0, 0) if stein in (-1, -8) else (255, 255, 255)
    pg.draw.circle(screen, farbe, feld2zentrum(feld), int(FELD*0.2))
    if abs(stein) == 8:
      farbe = (0, 0, 0) if stein > 0 else (255, 255, 255)
      pg.draw.circle(screen, farbe, feld2zentrum(feld), int(FELD*0.05))

  if not clickstatus:
    for von in zugliste:
      pg.draw.rect(screen, (0, 50, 0), (feld2xy(von), (FELD, FELD)), 7)
  if clickstatus == 'feld1 selektiert':
    pg.draw.rect(screen, (255, 0, 0), (feld2xy(feld1), (FELD, FELD)), 7)
    for zug in zugliste[feld1]:
      pg.draw.circle(screen, (0, 0, 100), feld2zentrum(zug[0]), int(FELD*0.1))
  if clickstatus == 'zeige computerzug':
    for i in range(0, len(computerzug), 5):
      pg.draw.line(screen, (0, 0, 230), feld2zentrum(
          computerzug[i+1]), feld2zentrum(computerzug[i]), 10)
      pg.draw.circle(screen, (0, 0, 230), feld2zentrum(
          computerzug[-5]), int(FELD*0.1))
  pg.display.flip()


def status_maschine(status, pos):
  global feld1, am_zug, zugliste, bewertung, computerzug
  sprung = None
  x, y = pos
  feldnr = y // FELD * 8 + x // FELD
  if not status:
    if feldnr not in zugliste:
      return
    feld1 = feldnr
    return 'feld1 selektiert'
  if status == 'feld1 selektiert':
    for zug in zugliste[feld1]:
      if feldnr == zug[0]:
        if len(zug) == 5:
          ziehe(am_zug, zug)
          return 'computer'
        else:
          sprung = zug[:5]
          zugliste[feldnr].append(zug[5:])
    if not sprung:
      return
    ziehe(am_zug, sprung)
    feld1 = feldnr
    return 'feld1 selektiert'
  if status == 'computer':
    am_zug = not am_zug
    bewertung, computerzug = minimax(6, -999999, 999999, am_zug)
    print(bewertung)
    return 'zeige computerzug'
  if status == 'zeige computerzug':
    ziehe(am_zug, computerzug)
    am_zug = not am_zug
    zugliste = generiere_zugliste(am_zug)
    return


while weitermachen:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      pos = pg.mouse.get_pos()
      clickstatus = status_maschine(clickstatus, pos)
  clock.tick(20)
  zeichne_brett()
  if clickstatus == 'computer':
    clickstatus = status_maschine(clickstatus, (0, 0))

pg.quit()
