import pygame as pg
import chessdotcom as chess

def pos2xy(pos):
  return pos[0]*FELD, pos[1]*FELD

def xy2pos(xy):
  return xy[0] // FELD, xy[1] // FELD  

def zeichneBrett():
  for pos, feld in BRETT.items():
    color = '#DFBF93' if feld else '#C5844E'
    pg.draw.rect(screen, color, (*pos2xy(pos), FELD, FELD))

def ladeFiguren():
  images = {}
  fig2file = dict(r='br', n='bn', b='bb', q='bq', k='bk', p='bp',
                  R='wr', N='wn', B='wb', Q='wq', K='wk', P='wp')
  for fig, file in fig2file.items():
    img = pg.image.load(f'Teil_49_Figuren/{file}.png')
    images[fig] = pg.transform.smoothscale(img, (FELD, FELD))
  return images                     

def zeichneFiguren(position):
  for pos, figur in position.items():
    screen.blit(FIGUREN[figur], pos2xy(pos))

def fen2position(fen):
  position, s, z = {}, 0, 0
  pos, amZug, rochade, enpassant, zug50, zugnr = fen.split()
  for char in pos:
    if char.isalpha():
      position[(s,z)] = char
      s += 1
    elif char.isnumeric():
      s += int(char)
    else:
      s,z = 0, z+1 
  return position, amZug      

pg.init()
BREITE, HÖHE = 800, 800
FELD = 100
FPS = 40
zentrum = (BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))

BRETT = {(s,z): s % 2 == z % 2 for s in range(8) for z in range(8)}
FIGUREN = ladeFiguren()
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
#fen = chess.get_random_daily_puzzle().json['fen']
position, amZug = fen2position(fen)
print(f'{"Weiss" if amZug== "w" else "Schwarz"} ist am Zug')
drag = None

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    elif ereignis.type == pg.MOUSEBUTTONDOWN and not drag:
      pos1 = xy2pos(pg.mouse.get_pos())
      if pos1 in position:
        fig = position[pos1]
        drag = FIGUREN[fig]
        del position[pos1]
    elif ereignis.type == pg.MOUSEBUTTONUP and drag:
      pos2 = xy2pos(pg.mouse.get_pos())
      position[pos2] = fig
      drag = None      
  screen.fill((0,0,0))
  zeichneBrett()
  zeichneFiguren(position)
  if drag:
    rect = drag.get_rect(center=pg.mouse.get_pos())
    screen.blit(drag, rect)
  pg.display.flip()

pg.quit()