#todo
# en passant nicht umgesetzt


import pygame as pg
from time import perf_counter as pfc
import numpy as np
import copy 


def fen2pos(fen):
  global weiss
  i, position = 0, {}
  pos, farbe, rochade, enpassant, zug50, zugnr = fen.split() 
  for char in pos:
    if char.isnumeric():
      i += int(char)
    elif char.isalpha():
      position[i2pos(i)] = FIG2VAL[char]
      if char in 'kK': kings_pos[char.isupper()]=i2pos(i)
      i += 1
  weiss = farbe == 'w'
  for c in rochade:
    if c == '-': continue
    if c.isupper(): 
      spielstatus[True]['rochade'] += c
    else:
      spielstatus[False]['rochade'] += c
  return position


def zeichneBrett(b):
  for pos, feld in b.items():
    color = '#DFBF93' if feld else '#C5844E'
    pg.draw.rect(screen, color, (*pos2xy(pos), FELD, FELD))


def ladeFiguren():
  images = {}
  fig2dat = {-4:'br', -2:'bn', -3:'bb', -5:'bq', -6:'bk', -1:'bp',
             4 :'wr',  2:'wn',  3:'wb',  5:'wq',  6:'wk',  1:'wp'}
  for fig, file in fig2dat.items():
    img = pg.image.load(f'chess_images/{file}.png')
    images[fig] = pg.transform.smoothscale(img, (FELD, FELD))
  return images


def zeichneFiguren(p):
  for pos, f in p.items():
    screen.blit(FIGS[f], pos2xy(pos))

def zeichneZielfelder(pos):
  for pos2 in [züge[0,i][2:4] for i in range(züge_anz[0]) if züge[0,i][:2] == pos]:
    x,y = pos2xy(pos2)
    pg.draw.circle(screen,pg.Color('bisque4'),(x+50,y+50),8)    

def zügeRochade(weiss,züge,tiefe):
  global spielstatus
  kingspos = kings_pos[weiss]
  #kurze oder lange Rochade durchtesten
  for option in spielstatus[weiss]['rochade']:
    turmzug = ROCH_FELD[option]['turm']
    #wenn der Turm nicht an den König heranziehen kann, keine Rochade möglich
    if turmzug not in [züge[tiefe,i][:4] for i in range(züge_anz[tiefe])if not züge[tiefe,i,4]]: continue
    schach = False
    #wenn der König durch oder ins Schach zieht, keine Rochade möglich
    safe_status = copy.deepcopy(spielstatus)
    for zu in ROCH_FELD[option]['feld']:
      kings_pos[weiss] = zu
      if imSchach(weiss): schach = True
      kings_pos[weiss] = kingspos
    if not schach:
      züge[tiefe,züge_anz] = [*kingspos, *zu, False, False, option]
    spielstatus = safe_status    


def zügeBauern(pos,fig,weiss,tiefe):
  sp, ze, grundlinie, endlinie = PAWN_MOVE[fig]
  for i in range(1,3) if pos[1] == grundlinie else range(1,2):
    pos2 = pos_move(pos, (sp*i,ze*i))
    if pos2 not in BRETT or pos2 in position: 
      break
    zug = [*pos, *pos2, False, pos2[1] == endlinie, False]
    safe_state = copy.deepcopy(spielstatus)
    zug_ausführen(zug, weiss)
    if not imSchach(weiss):
      züge[tiefe,züge_anz] = zug
      züge_anz[tiefe] +=1
    zug_zurücknehmen(zug, weiss)
    spielstatus = safe_state
  for r in PAWN_CAPT[fig]:
    pos2 = pos_move(pos, r)
    if pos2 in position and position[pos2]>0 != weiss:
      zug = [*pos, *pos2, position[pos2], pos2[1] == endlinie, False]
      safe_state = copy.deepcopy(spielstatus)
      zug_ausführen(zug, weiss)
      if not imSchach(weiss):
        züge[tiefe,züge_anz] = zug
        züge_anz[tiefe] +=1
      zug_zurücknehmen(zug, weiss)
      spielstatus = safe_state    




def imSchach(weiss):
  kp = kings_pos[weiss]
  for figs,moves in SCHACH_MOVES.items():
    if figs in {-1,1} and figs > 0 == weiss: continue
    for r in moves[1:]:
      for i in range(moves[0]):
        r2 = r[0]*(i+1), r[1]*(i+1)
        pos2 = pos_move(kp, r2)
        if pos2 not in BRETT: break
        if pos2 in position and position[pos2]>0 == weiss: break
        if pos2 in position and position[pos2]>0 != weiss and position[pos2] in figs: return True
        if pos2 in position and position[pos2]>0 != weiss and position[pos2] not in figs: break

def zug_ausführen(z,weiss):
  x,y,x1,y1,capture,umwandlung,rochade = z
  fig = position[(x,y)]
  position[(x1,y1)] = fig
  del position[(x,y)]
  if umwandlung:
    position[zu] = 5 if weiss else -5
  if abs(fig) == 6: 
    kings_pos[weiss] = zu
    spielstatus[weiss]['rochade'] = ''
  if abs(fig) == 4 and (x,y) in ROCH_TURM[weiss]:
    spielstatus[weiss]['rochade'] = spielstatus[weiss]['rochade'].replace(ROCH_TURM[weiss][(x,y)],'')
  if rochade:
      tv, tz = ROCH_FELD[rochade]['turm']
      tfig = position[tv]
      position[tz] = tfig
      del position[tv]
      spielstatus[weiss]['rochade'] = ''

def zug_zurücknehmen(z,weiss):
  x,y,x1,y1,capture, umwandlung, rochade = z
  fig = position[(x1,y1)]
  position[(x,y)] = fig
  if capture:
    position[(x1,y1)] = capture
  else:
    del position[(x1,y1)]
  if umwandlung:
    position[(x,y)] = 1 if weiss else -1
  if abs(fig) == 6: 
    kings_pos[weiss] = (x,y)
  if rochade:
      tv, tz = ROCH_FELD[rochade]['turm']
      tfig = position[tz]
      position[tv] = tfig
      del position[tz] 

def zügeFig(weiss, tiefe):
  global spielstatus
  for pos, fig in position.items():
    if fig > 0 != weiss: continue
    if abs(fig) == 1:
      zügeBauern(pos,fig,weiss,tiefe)
    else:
      fig = abs(fig)
      for r in MOVES[fig][1:]:
        for i in range(MOVES[fig][0]):
          r2 = r[0]*(i+1), r[1]*(i+1)
          pos2 = pos_move(pos, r2)
          if pos2 not in BRETT: break 
          if pos2 in position and position[pos2]>0 == weiss: break
          if pos2 in position and position[pos2]>0 != weiss:
            safe_state = copy.deepcopy(spielstatus)
            zug = [*pos, *pos2, position[pos2], 0, 0]
            zug_ausführen(zug, weiss)
            if not imSchach(weiss):
              züge[tiefe,züge_anz] = zug
              züge_anz[tiefe] +=1
            zug_zurücknehmen(zug, weiss)
            spielstatus = safe_state
            break
          else:
            safe_state = copy.deepcopy(spielstatus)
            zug = [*pos, *pos2, 0, 0, 0]
            zug_ausführen(zug, weiss)
            if not imSchach(weiss):
              züge[tiefe,züge_anz] = zug
              züge_anz[tiefe] +=1
            zug_zurücknehmen(zug, weiss)
            spielstatus = safe_state
            


def zugGenerator(weiss,tiefe):
  global spielstatus
  züge_anz[tiefe] = 0
  zügeFig(weiss,tiefe)
  if not imSchach(weiss) and spielstatus[weiss]['rochade']:
    zügeRochade(weiss, tiefe)  
  
def i2pos(i):
  return i % 8, i//8


def pos2xy(pos):
  return pos[0]*FELD, pos[1]*FELD


def xy2pos(pos):
  return pos[0] // FELD, pos[1] // FELD


def pos_move(pos, move):
  return pos[0]+move[0], pos[1]+move[1]


def pos2koord(pos):
  return chr(97+pos[0])+str(8-pos[1])

def bewerte_position():
  return sum(FIG_WERTE[fig] for fig in position.values())

def minimax(tiefe, alpha, beta, weiss):
  global spielstatus, counter
  if tiefe == MAX_TIEFE:
    counter += 1
    return (bewerte_position(), None)
  zugliste = zugGenerator(weiss)
  if not zugliste:
    if not imSchach(weiss):
      return (0, None)
    else: 
      return (-99999+tiefe if weiss else 99999-tiefe, None)
  beste_bewertung = -999999 if weiss else 999999
  for zug in zugliste:
    safe_status = copy.deepcopy(spielstatus)
    zug_ausführen(zug, zugliste[zug], weiss)
    wert, _ = minimax(tiefe+1, alpha, beta, not weiss)
    zug_zurücknehmen(zug, zugliste[zug], weiss)
    spielstatus = safe_status
    if weiss:
      alpha = max(wert, alpha)
      if wert > beste_bewertung:
        beste_bewertung = wert
        bester_zug = zug
    else:
      beta = min(wert, beta)
      if wert < beste_bewertung:
        beste_bewertung = wert
        bester_zug = zug
    if alpha >= beta:
      break
  return beste_bewertung, bester_zug 

def print_zug(zug, att):
  von, zu = zug
  capture, umwandlung, rochade = att
  fig = position[von]
  if rochade:
    if von[0] - zu[0] > 0:
      return 'O-O-O'
    else:
      return 'O-O'
  return f'{"" if fig in "pP" else fig.upper()}{"x" if capture else ""}{pos2koord(zu)}{"Q" if umwandlung else ""}'

screen = pg.display.set_mode((800, 800))
FELD = 100

BRETT = {i2pos(i): i % 8 % 2 == i // 8 % 2 for i in range(64)}
FIG2VAL = dict(k=-6, q=-5, r=-4, b=-3, n=-2, p=-1,
               K= 6, Q= 5, R= 4, B= 3, N= 2, P= 1)
MOVES = {6: [1, (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)],
         5: [8, (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)],
         4: [8, (-1, 0), (1, 0), (0, 1), (0, -1)],
         3: [8, (-1, -1), (-1, 1), (1, 1), (1, -1)],
         2: [1, (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2)]}
PAWN_CAPT = {1: [(-1, -1), (1, -1)], -1: [(-1, 1), (1, 1)]}
PAWN_MOVE = {1: (0,-1,6,0), -1: (0,1,1,7)}
ROCH_FELD = {'K': {'feld': [(5,7), (6,7)], 'turm':((7,7), (5,7))},
             'Q': {'feld': [(3,7), (2,7)], 'turm':((0,7), (3,7))},
             'k': {'feld': [(5,0), (6,0)], 'turm':((7,0), (5,0))},
             'q': {'feld': [(3,0), (2,0)], 'turm':((0,0), (3,0))}}
ROCH_TURM = {True: {(0,7):'Q', (7,7):'K'}, False: {(0,0):'q', (7,0):'k'}}
FIG_WERTE = { 1: 1,  6: 99999,  5: 9,  4: 5, 3 : 3,  2: 3, 
             -1:-1, -6:-99999, -5:-9, -4:-5, -3:-3, -2:-3}
SCHACH_MOVES = {(5,4,-5,-4):MOVES[4], (5,3,-5,-3):MOVES[3], (-2,2): MOVES[2], (-6,6): MOVES[6], -1:[1,(-1,-1),(1,-1)], 1:[1,(-1,1), (1,1)]}

kings_pos = {True:(0,0), False:(0,0)}
spielstatus = {True: {'rochade':'', 'ep':''}, False: {'rochade':'', 'ep':''}}
FIGS = ladeFiguren()
weiss = True
position = fen2pos('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w  KQkq - 0 1')
#position = fen2pos('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
#position = fen2pos('r3k2r/1b4bq/2N5/8/8/6n1/7B/R3K2R w KQkq - 0 1')
MAX_TIEFE = 4
züge = np.zeros([10,400,7],np.int16)
züge_anz = np.zeros([10],np.uint16)
zugGenerator(weiss,0)

weitermachen = True
clock = pg.time.Clock()
drag = None

while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    # if ereignis.type == pg.MOUSEBUTTONDOWN and not drag:
    #   pos1 = xy2pos(pg.mouse.get_pos())
    #   if pos1 in {z[0] for z in züge}:
    #     fig = position[pos1]
    #     drag = FIGS[fig]
    #     del position[pos1]
    # if ereignis.type == pg.MOUSEBUTTONUP and drag:
    #   pos2 = xy2pos(pg.mouse.get_pos())
    #   if pos2 in {z[1] for z in züge if z[0] == pos1}:
    #     zug = [z for z in züge if z[0] == pos1 and z[1] == pos2][0]
    #     position[pos1] = fig
    #     zug_ausführen(zug,züge[zug], weiss)
    #     weiss = not weiss
    #     start = pfc()
    #     counter = 0
    #     bewertung, zug = minimax(0,-999999, 999999, weiss)
    #     print(pfc()-start)
    #     #print(f'{print_zug(zug, züge[zug])}, {pfc()-start:.2f} Sek., Bewertung = {bewertung}, Nodes = {counter:,.0f}')
    #     if not zug:
    #       if imSchach(weiss):
    #         print('SCHACHMATT')
    #       else:
    #         print('PATT')  
    #     zug_ausführen(zug, züge[zug], weiss)
    #     weiss = not weiss
    #     züge = zugGenerator(weiss)
    #     if not züge: 
    #       if imSchach(weiss):
    #         print('SCHACHMATT')
    #       else:
    #         print('PATT')    
    #   else:
    #     position[pos1] = fig  
    #   drag = None
  zeichneBrett(BRETT)
  zeichneFiguren(position)
  if drag:
    zeichneZielfelder(pos1)
    rect = drag.get_rect(center=pg.mouse.get_pos())
    screen.blit(drag, rect)
  pg.display.flip()
