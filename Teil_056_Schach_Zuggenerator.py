_M_HV = [(0, -1), (0, 1), (-1, 0), (1, 0)]
_M_DI = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

_MOVES = {'r': [7, *_M_HV],
          'b': [7, *_M_DI],
          'k': [1, *_M_HV, *_M_DI],
          'q': [7, *_M_HV, *_M_DI],
          'n': [1, (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2)],
          'p': [2, (0, 1)],
          'P': [2, (0, -1)],
          'pc': [1, (-1, 1), (1, 1)],
          'Pc': [1, (-1, -1), (1, -1)]}

_MOVES_ROCH = {'K': [((5, 7), (6, 7)), ((7, 7), (5, 7))],
               'k': [((5, 0), (6, 0)), ((7, 0), (5, 0))],
               'Q': [((3, 7), (2, 7)), ((0, 7), (3, 7))],
               'q': [((3, 0), (2, 0)), ((0, 0), (3, 0))]}

_GRUNDLINIE = [1,6]          

BRETT = {(s,z): s % 2 == z % 2 for s in range(8) for z in range(8)} 

_FIG_WERTE = dict (P=1, K=99999, Q=9, R=5, B=3, N=3,
                   p=-1, k=-99999, q=-9, r=-5, b=-3, n=-3)

MAX_TIEFE = 4                  

def zugGenerator(weiss, position, rochaderecht,ep):
  züge = []
  pseudo, königspos = _pseudoZugGenerator(weiss, position, ep)
  for zug in pseudo:
    if zug[3] and zug[3] in 'kK':
      print(zug)
    zug_ausführen(zug, position, königspos, ep)
    if not imSchach(weiss, position, königspos[weiss]):
      züge.append(zug)
    zug_zurücknehmen(zug, position, königspos,ep)
  if rochaderecht[weiss] and not imSchach(weiss, position, königspos[weiss]):
    _zügeRochade(weiss, züge, position, königspos[weiss], rochaderecht[weiss])
  return züge, königspos

def _zügeRochade(weiss, züge, position, von, rochade):
  for roch in rochade:
    turmzug = _MOVES_ROCH[roch][1]
    if turmzug not in {(z[1], z[2]) for z in züge if not z[3]}: continue
    if all([not imSchach(weiss, position, zu) for zu in _MOVES_ROCH[roch][0]]):
      züge.append(('K' if weiss else 'k', von, _MOVES_ROCH[roch][0][1], False, False, roch, False))  

def imSchach(weiss, position, kpos):
  for figs, moves in _MOVES.items():
    if figs in 'pP': continue
    for ds, dz in moves[1:]:
      for m in range(1, moves[0] + 1):
        zu = kpos[0] + ds * m, kpos[1] + dz * m
        if zu not in BRETT: break
        if zu in position:
          if position[zu].isupper() == weiss:
            break
          else:
            if position[zu].lower() in figs.lower():
              return True
            break  



def zug_ausführen(zug, position, königspos,ep):
  fig, von, zu, capture, umwandlung, rochade, enp = zug
  position[zu] = position.pop(von)
  if umwandlung:
    position[zu] = 'Q' if fig.isupper() else 'q'
  if fig in 'kK':
    königspos[fig.isupper()] = zu
  if rochade:
    tv, tz = _MOVES_ROCH[rochade][1]
    position[tz] = position.pop(tv)
  if enp:
    del position[enp]
  if fig in 'pP' and abs(von[1]-zu[1]) == 2:
    ep[fig.islower()].add((von[0],(von[1]+zu[1])//2))       


def zug_zurücknehmen(zug, position, königspos,ep):
  fig, von, zu, capture, umwandlung, rochade, enp = zug
  position[von] = position.pop(zu)
  if capture and not enp:
    position[zu] = capture
  if umwandlung:
    position[von] = 'P' if fig.isupper() else 'p'
  if fig in 'kK':
    königspos[fig.isupper()] = von
  if rochade:
    tv, tz = _MOVES_ROCH[rochade][1]
    position[tv] = position.pop(tz)
  if enp:
    position[enp] = capture
  if fig in 'pP' and abs(von[1]-zu[1]) == 2:
    ep[fig.islower()].remove((von[0],(von[1]+zu[1])//2))       
       


def _pseudoZugGenerator(weiss, position,ep):
  pseudo, königspos = [], [0,0]
  for von, fig in position.items():
    if fig.isupper() != weiss: continue
    if fig in 'pP':
      _zügeBauern(weiss, fig, von, position, pseudo,ep)
      continue
    f = fig.lower()
    if f == 'k': königspos[weiss] = von
    richtungen = _MOVES[f][1:]
    multiplikator = _MOVES[f][0]
    for ds, dz in richtungen:
      for m in range(1, multiplikator + 1):
        zu = von[0] + ds * m, von[1] + dz * m
        if zu not in BRETT: break
        if zu in position and position[zu].isupper() == weiss: break
        if zu in position and position[zu].isupper() != weiss:
          pseudo.append((fig, von, zu, position[zu], False, False, False))
          break
        else:
          pseudo.append((fig, von, zu, False, False, False, False))
  return pseudo, königspos 

def _zügeBauern(weiss, fig, von, position, pseudo, ep):
  # Stiller Zug
  for ds, dz in _MOVES[fig][1:]:
    for m in range(1,_MOVES[fig][0] + 1):
      zu = von[0], von[1] + dz * m
      if zu not in BRETT or zu in position: break
      if m == 2 and von[1] != _GRUNDLINIE[weiss]: break
      if zu[1] in (0, 7):
        pseudo.append((fig, von, zu, False, True, False, False))
      else:
        pseudo.append((fig, von, zu, False, False, False, False))         
  # Schlagzug
  for ds, dz in _MOVES[fig+'c'][1:]:
    zu = von[0] + ds, von[1] + dz
    if zu not in position: continue
    if position[zu].isupper() == weiss: continue
    if zu[1] in (0, 7):
      pseudo.append((fig, von, zu, position[zu], True, False, False))
    else:
      pseudo.append((fig, von, zu, position[zu], False, False, False))
  #enPassant
  if ep[weiss]:
    for ds, dz in _MOVES[fig+'c'][1:]:
      zu = von[0] + ds, von[1] + dz
      if zu in ep[weiss]:
        pseudo.append((fig, von, zu, 'p' if weiss else 'P', False, False, (zu[0],von[1])))


def bewerte_position(position):
  return sum(_FIG_WERTE[fig] for fig in position.values())

def minimax(tiefe, alpha, beta, weiss, position, rochaderecht,ep):
  if tiefe == MAX_TIEFE:
    return (bewerte_position(position), None)
  zugliste, königspos = zugGenerator(weiss, position, rochaderecht,ep)
  if not zugliste:
    assert(type(königspos[weiss]) == tuple)
    if not imSchach(weiss, position, königspos[weiss]):
      return (0, None)
    else:
      return(-99999+tiefe if weiss else 99999-tiefe, None)
  beste_bewertung = -999999 if weiss else 999999
  ep[not weiss] = set()
  for zug in zugliste:
    safe_roch = rochaderecht.copy()
    zug_ausführen(zug, position, königspos,ep)
    assert(type(königspos[weiss]) == tuple)
    wert, _ = minimax(tiefe+1, alpha, beta, not weiss, position, rochaderecht,ep.copy())
    zug_zurücknehmen(zug, position, königspos,ep)
    rochaderecht = safe_roch
    if weiss:
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

