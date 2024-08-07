import pygame as pg
import chessdotcom as chess
import Teil_056_Schach_Zuggenerator as zuggen
from pprint import pprint


def sz2xy(sz):
  return sz[0] * FELD, sz[1] * FELD


def xy2sz(xy):
  return xy[0] // FELD, xy[1] // FELD


def zeichneBrett(BRETT):
  for sz, feld in BRETT.items():
    farbe = '#DFBF93' if feld else '#C5844E'
    pg.draw.rect(screen, farbe, (*sz2xy(sz), FELD, FELD))


def fen2position(fen):
  position, s, z, rochaderecht, ep = {}, 0, 0, ['', ''], [set(), set()]
  figurenstellung, zugrecht, rochaderechte, enpassant, zug50, zugnr = fen.split()
  for char in figurenstellung:
    if char.isalpha():
      position[(s, z)] = char
      s += 1
    elif char.isnumeric():
      s += int(char)
    else:
      s, z = 0, z + 1
  for char in rochaderechte:
    if char == '-': break
    rochaderecht[char.isupper()] += char

  weiss = zugrecht == 'w'

  if enpassant != '-':
    sp = ord(enpassant[0]) - 97
    ze = 8 - int(enpassant[1])
    ep[weiss].add((sp, ze))

  return position, weiss, rochaderecht, ep


def ladeFiguren():
  bilder = {}
  fig2datei = dict(r='br', n='bn', b='bb', q='bq', k='bk', p='bp',
                   R='wr', N='wn', B='wb', Q='wq', K='wk', P='wp')
  for fig, datei in fig2datei.items():
    bild = pg.image.load(f'Teil_049_Figuren/{datei}.png')
    bilder[fig] = pg.transform.smoothscale(bild, (FELD, FELD))
  return bilder


def zeichneFiguren(p):
  for sz, fig in p.items():
    screen.blit(FIGUREN[fig], sz2xy(sz))


def zeichneZielfelder(zielfelder):
  for ziel in zielfelder:
    x, y = sz2xy(ziel)
    pg.draw.circle(screen, pg.Color('bisque4'), (x + 50, y + 50), 10)


pg.init()
BREITE, HÖHE = 800, 800
FELD = BREITE // 8
FPS = 40
screen = pg.display.set_mode((BREITE, HÖHE))
FIGUREN = ladeFiguren()
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
# fen = chess.get_random_daily_puzzle().json['fen']
# fen = 'r7/8/8/3k4/8/4P3/8/3K4 w - - 0 1'
position, weiss, rochaderecht, ep = fen2position(fen)
spieler = [False, True]


weitermachen = True
clock = pg.time.Clock()
drag = spielende = False

while weitermachen:
  if spielende: break
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    elif ereignis.type == pg.MOUSEBUTTONDOWN and not drag:
      von = xy2sz(pg.mouse.get_pos())
      if von in {z[1] for z in züge}:
        fig = position.pop(von)
        drag = FIGUREN[fig]
        zielfelder = {z[2] for z in züge if z[1] == von}
    elif ereignis.type == pg.MOUSEBUTTONUP and drag:
      zu = xy2sz(pg.mouse.get_pos())
      if zu in zielfelder:
        zug = [z for z in züge if z[1] == von and z[2] == zu][0]
        position[von] = fig
        zuggen.zug_ausführen(zug, position, königspos, ep)
        weiss = not weiss
      else:
        position[von] = fig
      drag = None

  screen.fill((0, 0, 0))
  zeichneBrett(zuggen.BRETT)
  zeichneFiguren(position)
  if drag:
    rect = drag.get_rect(center=pg.mouse.get_pos())
    screen.blit(drag, rect)
    zeichneZielfelder(zielfelder)
  pg.display.flip()

  if not drag:
    if spieler[weiss]:
      ep[not weiss] = set()
      züge, königspos = zuggen.zugGenerator(weiss, position, rochaderecht, ep)
      if not züge:
        print(f'{"Weiss" if weiss else "Schwarz"} ist ', end='')
        if zuggen.imSchach(weiss, position, königspos[weiss]):
          print('Matt')
        else:
          print('Patt')
        spielende = True
      else:
        beste_bewertung, bester_zug = zuggen.minimax(0, -999999, 999999, weiss, position, rochaderecht, ep.copy())
        zuggen.zug_ausführen(bester_zug, position, königspos, ep)
        weiss = not weiss
    else:
      züge, königspos = zuggen.zugGenerator(weiss, position, rochaderecht, ep)


pg.quit()
