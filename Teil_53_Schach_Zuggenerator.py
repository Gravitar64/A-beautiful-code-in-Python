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

def zugGenerator(weiss, position, rochaderecht):
  züge = []
  pseudo, königspos = _pseudoZugGenerator(weiss, position)
  for zug in pseudo:
    zug_ausführen(zug, position, königspos)
    if not imSchach(weiss, position, königspos[weiss]):
      züge.append(zug)
    zug_zurücknehmen(zug, position, königspos)
  if rochaderecht[weiss] and not imSchach(weiss, position, königspos[weiss]):
    _zügeRochade(weiss, züge, position, königspos[weiss], rochaderecht[weiss])  
  return züge, königspos

def _zügeRochade(weiss, züge, position, von, rochade):
  for roch in rochade:
    turmzug = _MOVES_ROCH[roch][1]
    if turmzug not in {(zug[1], zug[2]) for zug in züge if not zug[3]}: continue
    if all([not imSchach(weiss, position, zu) for zu in _MOVES_ROCH[roch][0]]):
      züge.append(('K' if weiss else 'k', von, _MOVES_ROCH[roch][0][1], False, False, roch))


def imSchach(weiss, position, von):
  for figs, moves in _MOVES.items():
    if figs in 'pP': continue
    for ds, dz in moves[1:]:
      for m in range(1, moves[0] + 1):
        zu = von[0] + ds * m, von[1] + dz * m
        if zu not in BRETT: break
        if zu in position:
          if position[zu].isupper() == weiss:
            break
          else:
            if position[zu].lower() in figs:
              return True
            break  



def zug_ausführen(zug, position, königspos):
  fig, von, zu, capture, umwandlung, rochade = zug
  position[zu] = position.pop(von)
  if umwandlung:
    position[zu] = 'Q' if fig.isupper() else 'q'
  if fig in 'kK':
    königspos[fig.isupper()] = zu
  if rochade:
    tv, tz = _MOVES_ROCH[rochade][1]
    position[tz] = position.pop(tv)



def zug_zurücknehmen(zug, position, königspos):
  fig, von, zu, capture, umwandlung, rochade = zug
  position[von] = position.pop(zu)
  if capture:
    position[zu] = capture
  if umwandlung:
    position[von] = 'P' if fig.isupper() else 'p'
  if fig in 'kK':
    königspos[fig.isupper()] = von
  if rochade:
    tv, tz = _MOVES_ROCH[rochade][1]
    position[tv] = position.pop(tz)     


def _pseudoZugGenerator(weiss, position):
  pseudo, königspos = [], [0,0]
  for von, fig in position.items():
    if fig.isupper() != weiss: continue
    if fig in 'pP':
      _zügeBauern(weiss, fig, von, position, pseudo)
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
          pseudo.append((fig, von, zu, position[zu], False, False))
          break
        else:
          pseudo.append((fig, von, zu, False, False, False))
  return pseudo, königspos 

def _zügeBauern(weiss, fig, von, position, pseudo):
  # Stiller Zug
  for ds, dz in _MOVES[fig][1:]:
    for m in range(1,_MOVES[fig][0] + 1):
      zu = von[0], von[1] + dz * m
      if zu not in BRETT or zu in position: break
      if m == 2 and von[1] != _GRUNDLINIE[weiss]: break
      if zu[1] in (0, 7):
        pseudo.append((fig, von, zu, False, True, False))
      else:
        pseudo.append((fig, von, zu, False, False, False))         
  # Schlagzug
  for ds, dz in _MOVES[fig+'c'][1:]:
    zu = von[0] + ds, von[1] + dz
    if zu not in position: continue
    if position[zu].isupper() == weiss: continue
    if zu[1] in (0, 7):
      pseudo.append((fig, von, zu, position[zu], True, False))
    else:
      pseudo.append((fig, von, zu, position[zu], False, False)) 

        
