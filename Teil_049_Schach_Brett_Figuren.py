import pygame as pg
import chessdotcom as chess


def sz2xy(sz):
  return sz[0]*FELD, sz[1]*FELD


def xy2sz(xy):
  return xy[0]//FELD, xy[1]//FELD


def zeichneBrett(BRETT):
  for sz, feld in BRETT.items():
    farbe = '#DFBF93' if feld else '#C5844E'
    pg.draw.rect(screen, farbe, (*sz2xy(sz), FELD, FELD))


def fen2position(fen):
  position, s, z = {}, 0, 0
  figurenstellung, zugrecht, rochaderechte, enpassant, zug50, zugnr = fen.split()
  for char in figurenstellung:
    if char.isalpha():
      position[(s, z)] = char
      s += 1
    elif char.isnumeric():
      s += int(char)
    else:
      s, z = 0, z+1
  return position, zugrecht


def ladeFiguren():
  bilder = {}
  fig2datei = dict(r='br', n='bn', b='bb', q='bq', k='bk', p='bp',
                   R='wr', N='wn', B='wb', Q='wq', K='wk', P='wp')
  for fig, datei in fig2datei.items():
    bild = pg.image.load(f'Teil_49_Figuren/{datei}.png')
    bilder[fig] = pg.transform.smoothscale(bild, (FELD, FELD))
  return bilder


def zeichneFiguren(p):
  for sz, fig in p.items():
    screen.blit(FIGUREN[fig], sz2xy(sz))


pg.init()
BREITE, HÖHE = 800, 800
FELD = BREITE // 8
FPS = 40
screen = pg.display.set_mode((BREITE, HÖHE))
BRETT = {(s, z): s % 2 == z % 2 for s in range(8) for z in range(8)}
FIGUREN = ladeFiguren()
#fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# je nach eigesetzter Python-Version (bei mir 3.9.2) und der chess.com-Version 
# (bei mir 21.0.1)
# funktioniert der nachfolgende Aufruf oder es ist noch ein zusätzlicher KEY 
# vor fen notwendig:
#
# also fen = chess.get_random_daily_puzzle().json['puzzle']['fen']

fen = chess.get_random_daily_puzzle().json['fen']
position, zugrecht = fen2position(fen)
print(zugrecht)

weitermachen = True
clock = pg.time.Clock()
drag = None

while weitermachen:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    elif ereignis.type == pg.MOUSEBUTTONDOWN and not drag:
      von = xy2sz(pg.mouse.get_pos())
      if von in position:
        fig = position[von]
        drag = FIGUREN[fig]
        del position[von]
    elif ereignis.type == pg.MOUSEBUTTONUP and drag:
      zu = xy2sz(pg.mouse.get_pos())
      position[zu] = fig
      drag = None

  screen.fill((0, 0, 0))
  zeichneBrett(BRETT)
  zeichneFiguren(position)
  if drag:
    rect = drag.get_rect(center=pg.mouse.get_pos())
    screen.blit(drag, rect)
  # und hier wird das im Hintergrund gezeichnete Bild angezeigt
  pg.display.flip()

pg.quit()
