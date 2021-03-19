_M_HV = [(0, -1), (0, 1), (-1, 0), (1, 0)]
_M_DI = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

_MOVES = {'r': [7, *_M_HV],
          'b': [7, *_M_DI],
          'k': [1, *_M_HV, *_M_DI],
          'q': [7, *_M_HV, *_M_DI],
          'n': [1, (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2)]}

BRETT = {(s,z): s % 2 == z % 2 for s in range(8) for z in range(8)}          

def zugGenerator(weiss, position):
  züge = []
  pseudo = _pseudoZugGenerator(weiss, position)
  #return züge
  return pseudo

def _pseudoZugGenerator(weiss, position):
  pseudo = []
  for von, fig in position.items():
    if fig.isupper() != weiss: continue
    if fig in 'pP':
      #hier kommt dann später die Zugermittlung für Bauiern rein
      continue
    f = fig.lower()
    richtungen = _MOVES[f][1:]
    multiplikator = _MOVES[f][0]
    for ds, dz in richtungen:
      for m in range(1, multiplikator + 1):
        zu = von[0] + ds * m, von[1] + dz * m
        if zu not in BRETT: break
        if zu in position and position[zu].isupper() == weiss: break
        if zu in position and position[zu].isupper() != weiss:
          pseudo.append((fig, von, zu, position[zu]))
          break
        else:
          pseudo.append((fig, von, zu, False))

  return pseudo      


        
