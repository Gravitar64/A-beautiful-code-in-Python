#todo
# en passant nicht umgesetzt


import pygame as pg
from time import perf_counter as pfc
import copy 



def fen2pos(fen):
  global weiss
  i, position = 0, dict()
  pos, farbe, rochade, enpassant, zug50, zugnr = fen.split() 
  for char in pos:
    if char.isnumeric():
      i += int(char)
    elif char.isalpha():
      position[i2pos(i)] = char
      if char in 'kK': kings_pos[char.isupper()]=i2pos(i)
      i += 1
  weiss = farbe == 'w'
  if enpassant != '-':
    spielstatus[weiss]['ep']=enpassant
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
  fig2dat = dict(r='br', n='bn', b='bb', q='bq', k='bk', p='bp',
                 R='wr', N='wn', B='wb', Q='wq', K='wk', P='wp')
  for fig, file in fig2dat.items():
    img = pg.image.load(f'chess_images/{file}.png')
    images[fig] = pg.transform.smoothscale(img, (FELD, FELD))
  return images


def zeichneFiguren(p):
  for pos, fig in p.items():
    screen.blit(FIGS[fig], pos2xy(pos))

def zeichneZielfelder(pos):
  for pos2 in [z[1] for z in züge if z[0] == pos]:
    x,y = pos2xy(pos2)
    pg.draw.circle(screen,pg.Color('bisque4'),(x+50,y+50),8)    

def zügeRochade(weiss,züge):
  global spielstatus
  roch_züge = []
  kingspos = kings_pos[weiss]
  #kurze oder lange Rochade durchtesten
  for option in spielstatus[weiss]['rochade']:
    turmzug = ROCH_FELD[option]['turm']
    #wenn der Turm nicht an den König heranziehen kann, keine Rochade möglich
    if turmzug not in [(z[0], z[1]) for z in züge]: continue
    schach = False
    #wenn der König durch oder ins Schach zieht, keine Rochade möglich
    safe_status = copy.deepcopy(spielstatus)
    for zu in ROCH_FELD[option]['feld']:
      zug = (kingspos, zu, False, False, False)
      zug_ausführen(zug,weiss)
      if imSchach(weiss):
        schach = True
      zug_zurücknehmen(zug,weiss)  
    if not schach:
      roch_züge.append((kingspos, zu, False, False, option))
    spielstatus = safe_status    
  return roch_züge    


def zügeBauern(pos,fig,weiss):
  züge = []
  sp, ze, grundlinie, endlinie = PAWN_MOVE[weiss]
  for i in range(1,3) if pos[1] == grundlinie else range(1,2):
    pos2 = pos_move(pos, (sp*i,ze*i))
    if pos2 not in BRETT or pos2 in position: break
    züge.append((pos, pos2, False, pos2[1] == endlinie, False))
  for r in PAWN_CAPT[weiss]:
    pos2 = pos_move(pos, r)
    if pos2 in BRETT and pos2 in position and position[pos2].isupper() != weiss:
      züge.append((pos, pos2, position[pos2], pos2[1] == endlinie, False))
  return züge    


def zügeFig(pos, fig, weiss):
  züge = []
  if fig in 'pP':
    return zügeBauern(pos,fig,weiss)
  fig = fig.lower()  
  for r in MOVES[fig][1:]:
    for i in range(MOVES[fig][0]):
      r2 = r[0]*(i+1), r[1]*(i+1)
      pos2 = pos_move(pos, r2)
      if pos2 not in BRETT: break
      if pos2 in position and position[pos2].isupper() == weiss: break
      if pos2 in position:
        züge.append((pos, pos2, position[pos2], False, False))
        break
      else:
        züge.append((pos, pos2, False, False, False))
  return züge

def angegriffeneFelder(weiss):
  felder = set()
  for pos, fig in position.items():
    if fig.isupper() == weiss: continue
    if fig in PAWN_CAPT:
      for r in PAWN_CAPT[fig]:
        pos2 = pos_move(pos, r)
        if pos2 in position and position[pos2].isupper() == weiss:
          felder.add(pos2)
    else:
      fig = fig.lower()
      for r in MOVES[fig][1:]:
        for i in range(MOVES[fig][0]):
          r2 = r[0]*(i+1), r[1]*(i+1)
          pos2 = pos_move(pos, r2)
          if pos2 in position:
            if position[pos2].isupper() != weiss: 
              break
            else:
              felder.add(pos2)
              break
  return felder

def könig_im_Schach(weiss):
  kp = kings_pos[weiss]
  for fig,moves in MOVES.items():
    if not weiss: fig = fig.upper()
    for r in moves[1:]:
      for i in range(moves[0]):
        r2 = r[0]*(i+1), r[1]*(i+1)
        pos2 = pos_move(kp, r2)
        if pos2 not in BRETT: break
        if pos2 in position and position[pos2].isupper()==weiss: break
        if pos2 in position and position[pos2] == fig: return True
  for r in PAWN_CAPT[weiss]:
    bauer = 'p' if weiss else 'P'
    pos2 = pos_move(kp, r)
    if pos2 in position and position[pos2] == bauer: return True       






def imSchach(weiss):
  # global spielstatus
  # safe_state = copy.deepcopy(spielstatus)
  # züge = pseudoZugGenerator(not weiss)
  # spielstatus = safe_state
  # return kings_pos[weiss] in {z[1] for z in züge}
  #return kings_pos[weiss] in angegriffeneFelder(weiss)
  return könig_im_Schach(weiss)

def zug_ausführen(z,weiss):
  von,zu,capture,umwandlung,rochade = z
  fig = position[von]
  position[zu] = fig
  del position[von]
  if umwandlung:
    position[zu] = 'Q' if weiss else 'q'
  if fig in 'pP' and abs(von[1] - zu[1]) == 2:
    spielstatus[weiss]['ep'] = (von[0], von[1] - 1 if  weiss else -1)
  if fig in 'kK': 
    kings_pos[weiss] = zu
    spielstatus[weiss]['rochade'] = ''
  if fig in 'Rr' and von in ROCH_TURM[weiss]:
    spielstatus[weiss]['rochade'] = spielstatus[weiss]['rochade'].replace(ROCH_TURM[weiss][von],'')
  if rochade:
      tv, tz = ROCH_FELD[rochade]['turm']
      tfig = position[tv]
      position[tz] = tfig
      del position[tv]
      spielstatus[weiss]['rochade'] = ''

def zug_zurücknehmen(z,weiss):
  von, zu, capture, umwandlung, rochade = z
  fig = position[zu]
  position[von] = fig
  if capture: 
    position[zu] = capture
  else:
    del position[zu]
  if umwandlung:
    position[von] = 'P' if weiss else 'p'
  if fig in 'kK': 
    kings_pos[weiss] = von
  if rochade:
      tv, tz = ROCH_FELD[rochade]['turm']
      tfig = position[tz]
      position[tv] = tfig
      del position[tz] 

def pseudoZugGenerator(weiss):
  pseudo_züge = []
  for pos, fig in position.items():
    if fig.isupper() != weiss: continue
    pseudo_züge.extend(zügeFig(pos, fig, weiss))
  return pseudo_züge

def zugGenerator(weiss):
  global spielstatus
  züge = pseudoZugGenerator(weiss)
  # alle Pseudo-Züge löschen, bei denen man nach dem Zug im Schach steht
  # ob man vorher im Schach stand, spielt dabei keine Rolle, da selbst dann nur noch Züge
  # übrig bleiben, die ein Schach abwehren
  safe_status = copy.deepcopy(spielstatus)
  for z in reversed(züge):
    zug_ausführen(z,weiss)
    if imSchach(weiss): züge.remove(z)
    zug_zurücknehmen(z,weiss)
  spielstatus = safe_status  
  
  # if not imSchach(weiss) and spielstatus[weiss]['rochade']:
  #   züge.extend(zügeRochade(weiss,züge))   
  return züge  
  
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


def minimax(tiefe, maxTiefe, alpha, beta, weiss):
  global spielstatus, counter
  if tiefe == 0:
    bewertete_züge = []
  if tiefe == maxTiefe:
    counter += 1
    return bewerte_position()
  # if win(spieler):
  #   return (99999 if spieler else -99999, None)
  zugliste = zugGenerator(weiss)
  if not zugliste:
    if not imSchach(weiss):
      return 0
    else: 
      return -99999 if weiss else 99999
  for zug in zugliste:
    #safe_status = copy.deepcopy(spielstatus)
    zug_ausführen(zug,weiss)
    wert = minimax(tiefe+1, maxTiefe, alpha, beta, not weiss)
    zug_zurücknehmen(zug,weiss)
    if tiefe == 0:
      bewertete_züge.append((wert,zug))
    #spielstatus = safe_status
    if weiss:
      alpha = max(wert, alpha)
    else:
      beta = min(wert, beta)
    if alpha >= beta:
      break
  if tiefe == 0: 
    return bewertete_züge
  else:
    return alpha if weiss else beta

def print_zug(zug,weiss):
  von, zu, capture, umwandlung, rochade = zug
  fig = position[von]
  if rochade:
    if von[0] - zu[0] > 0:
      return 'O-O'
    else:
      return 'O-O-O'
  return f'{"" if fig in "pP" else fig.upper()}{"x" if capture else ""}{pos2koord(zu)}{"Q" if umwandlung else ""}'

screen = pg.display.set_mode((800, 800))
FELD = 100

BRETT = {i2pos(i): i % 8 % 2 == i // 8 % 2 for i in range(64)}
MOVES = {'k': [1, (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)],
         'q': [8, (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)],
         'r': [8, (-1, 0), (1, 0), (0, 1), (0, -1)],
         'b': [8, (-1, -1), (-1, 1), (1, 1), (1, -1)],
         'n': [1, (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2)]}
PAWN_CAPT = {True: [(-1, -1), (1, -1)], False: [(-1, 1), (1, 1)]}
PAWN_MOVE = {True: (0,-1,6,0), False: (0,1,1,7)}
ROCH_FELD = {'K': {'feld': [(5,7), (6,7)], 'turm':((7,7), (5,7))},
             'Q': {'feld': [(3,7), (2,7)], 'turm':((0,7), (3,7))},
             'k': {'feld': [(5,0), (6,0)], 'turm':((7,0), (5,0))},
             'q': {'feld': [(3,0), (2,0)], 'turm':((0,0), (3,0))}}
ROCH_TURM = {True: {(0,7):'Q', (7,7):'K'}, False: {(0,0):'q', (7,0):'k'}}
FIG_WERTE = dict(P=1, K=99999, Q=9, R=5, B=3, N=3, 
                 p=-1, k=-99999, q=-9, r=-5, b=-3, n=-3)
kings_pos = {True:(0,0), False:(0,0)}
spielstatus = {True: {'rochade':'', 'ep':''}, False: {'rochade':'', 'ep':''}}

FIGS = ladeFiguren()
weiss = True
position = fen2pos('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w  KQkq - 0 1')
#position = fen2pos('r3k2r/8/5Q2/8/8/8/8/R3K2R w KQkq - 0 1')

start = pfc()
counter = 0
bewertete_züge = minimax(0,4,-999999, 999999, weiss)
for bewertung, zug in sorted(bewertete_züge):
  print(f'{print_zug(zug,weiss)}, {pfc()-start:.2f} Sek., Bewertung = {bewertung}, Nodes = {counter:,.0f}')

züge = zugGenerator(weiss)


weitermachen = True
clock = pg.time.Clock()
drag = None

while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.MOUSEBUTTONDOWN and not drag:
      pos1 = xy2pos(pg.mouse.get_pos())
      if pos1 in {z[0] for z in züge}:
        fig = position[pos1]
        drag = FIGS[fig]
        del position[pos1]
    if ereignis.type == pg.MOUSEBUTTONUP and drag:
      pos2 = xy2pos(pg.mouse.get_pos())
      if pos2 in {z[1] for z in züge if z[0] == pos1}:
        zug = [z for z in züge if z[0] == pos1 and z[1] == pos2][0]
        position[pos1] = fig
        zug_ausführen(zug,weiss)
        print(bewerte_position())
        weiss = not weiss
        # start = pfc()
        # counter = 0
        # bewertung, zug = minimax(4,-999999, 999999, weiss)
        # print(f'{print_zug(zug,weiss)}, {pfc()-start:.2f} Sek., Bewertung = {bewertung}, Nodes = {counter:,.0f}')
        # zug_ausführen(zug,weiss)
        # weiss = not weiss
        züge = zugGenerator(weiss)
        if not züge: 
          if imSchach(weiss):
            print('SCHACHMATT')
          else:
            print('PATT')    
      else:
        position[pos1] = fig  
      drag = None
  zeichneBrett(BRETT)
  zeichneFiguren(position)
  if drag:
    zeichneZielfelder(pos1)
    rect = drag.get_rect(center=pg.mouse.get_pos())
    screen.blit(drag, rect)
  pg.display.flip()
