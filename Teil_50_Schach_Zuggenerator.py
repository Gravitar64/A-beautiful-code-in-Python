M_HV = [(1, 0), (-1, 0), (0, 1), (0, -1)]
M_DI = [(1, 1), (-1, -1), (-1, 1), (1, -1)]


MOVES = {'k': [1, *M_HV, *M_DI],
         'q': [7, *M_HV, *M_DI],
         'r': [7, *M_HV],
         'b': [7, *M_DI],
         'n': [1, (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2)],
         'p': [2, (0, 1)],
         'P': [2, (0, -1)],
         'pc': [1, (-1, 1), (1, 1)],
         'Pc': [1, (-1, -1), (1, -1)]}

MOVES_ROCH = {'K': [((5, 7), (6, 7)), ((7, 7), (5, 7))],
              'k': [((5, 0), (6, 0)), ((7, 0), (5, 0))],
              'Q': [((3, 7), (2, 7)), ((0, 7), (3, 7))],
              'q': [((3, 0), (2, 0)), ((0, 0), (3, 0))]}

BRETT = {(s, z): s % 2 == z % 2 for s in range(8) for z in range(8)}


def zugGenerator(weiss, position, roch_state):
  züge = []
  pseudo, königspos = _pseudoZugGenerator(weiss, position)
  #Nur pseudo-Züge, die kein Schach auslösen, werden in die Liste "züge" übernommen
  for zug in pseudo:
    save_state = roch_state.copy()
    zug_ausführen(zug, weiss, position, königspos, roch_state)
    if not _imSchach(weiss, position, königspos):
      züge.append(zug)
    zug_zurücknehmen(zug, weiss, position, königspos)
    roch_state = save_state
  #Falls noch Rochade möglich ist, wird die zugliste um diese Züge erweitert (König zieht 2 Felder und Rochade enthält (K)ingsside, (Q)ueensside
  if roch_state[weiss] and not _imSchach(weiss, position, königspos): 
    _zügeRochade(weiss, züge, position, roch_state, königspos)
  return züge


def _zügeRochade(weiss, züge, position, roch_state, königspos):
  save_königspos = königspos[weiss]
  for roch in roch_state[weiss]:
    turmzug = MOVES_ROCH[roch][1]
    # wenn der Turm nicht an den König heranziehen kann, ist keine Rochade möglich
    if turmzug not in [(z[1], z[2]) for z in züge if not z[3]]:
      continue
    schach = False
    # wenn der König durch oder ins Schach zieht, ist keine Rochade möglich
    for zu in MOVES_ROCH[roch][0]:
      königspos[weiss] = zu
      if _imSchach(weiss, position, königspos):
        schach = True
    königspos[weiss] = save_königspos
    if not schach:
      züge.append(
          ('K' if weiss else 'k', königspos[weiss], zu, False, False, roch))


def _zügeBauern(weiss, fig, von, position, pseudo):
  # Stiller bauernzug
  for ds, dz in MOVES[fig][1:]:
    for m in range(1, MOVES[fig][0] + 1):
      schlagen = umwandlung = rochade = False
      zu = von[0] + ds * m, von[1] + dz * m
      if zu not in BRETT:
        break
      if zu in position:
        break
      # von Grundlinie 2 Felder möglich
      if fig == 'P' and m == 2 and von[1] != 6:
        break
      if fig == 'p' and m == 2 and von[1] != 1:
        break
      # auf der letzten Linie Umwandlung
      if (fig == 'P' and zu[1] == 0) or (fig == 'p' and zu[1] == 7):
        umwandlung = True
      pseudo.append((fig, von, zu, schlagen, umwandlung, rochade))
  # Schlagzug Bauer
  for ds, dz in MOVES[fig+'c'][1:]:
    schlagen = umwandlung = rochade = False
    zu = von[0] + ds, von[1] + dz
    if zu not in BRETT or zu not in position:
      continue
    if position[zu].isupper() != weiss:  # bauer kann schlagen
      schlagen = position[zu]
      if (fig == 'P' and zu[1] == 0) or (fig == 'p' and zu[1] == 7):
        umwandlung = True
      pseudo.append((fig, von, zu, schlagen, umwandlung, rochade))


def _pseudoZugGenerator(weiss, position):
  # zug = fig, von, zu, schlagen(fig), umwandlung(bool), rochade (KQkq)
  pseudo = []
  königspos = [0, 0]
  for von, fig in position.items():
    if fig.isupper() != weiss:
      continue
    if fig in 'pP':
      _zügeBauern(weiss, fig, von, position, pseudo)
    else:
      f = fig.lower()
      for ds, dz in MOVES[f][1:]:
        for m in range(1, MOVES[f][0]+1):
          zu = von[0] + ds * m, von[1] + dz * m
          if zu not in BRETT:
            break
          if zu in position and position[zu].isupper() == weiss:
            break
          if zu in position and position[zu].isupper() != weiss:  # Schlagzug
            pseudo.append((fig, von, zu, position[zu], False, False))
            break
          else:  # stiller Zug
            pseudo.append((fig, von, zu, False, False, False))
      if fig in 'kK':
        königspos[fig.isupper()] = von
  return pseudo, königspos


def _imSchach(weiss, position, königspos):
  von = königspos[weiss]
  # wir simulieren alle Zielfelder - ausgehend vom Königsfeld - jeder mögliche Figur und schauen, ob dort
  # diese feindliche Figur steht
  for figs, moves in MOVES.items():
    if figs in 'pP':
      continue
    for ds, dz in moves[1:]:
      for m in range(1, moves[0]+1):
        zu = von[0] + ds*m, von[1]+dz*m
        if zu not in BRETT:
          break
        # das Zielfeld enthält eine Figur in der eigenen Farbe, die damit die Richtung blockt
        if zu in position and position[zu].isupper() == weiss:
          break
        # das Zielfeld enthält eine Figur in der gegnerischen Farbe 
        if zu in position and position[zu].isupper() != weiss:
          #und diese Figur entspricht der simulierten Figur vom Königsfeld aus gesehen, dann steht der König im Schach
          if position[zu] in figs:
            return True
          #ansonsten steht dort eine andere feindliche Figur, die jedoch die Richtung blockt
          else:
            break


def zug_ausführen(zug, weiss, position, königspos, roch_state):
  fig, von, zu, capture, umwandlung, rochade = zug
  position[zu] = fig
  del position[von]
  if umwandlung:
    position[zu] = 'Q' if weiss else 'q'
  if fig in 'Kk':
    königspos[fig.isupper()] = zu
    roch_state[weiss] = ''
  if fig in 'rR' and roch_state[weiss]:
    if MOVES_ROCH['K' if weiss else 'k'][1][0] == von:
      roch_state[weiss] = roch_state[weiss].replace('K' if weiss else 'k', '')
    if MOVES_ROCH['Q' if weiss else 'q'][1][0] == von:
      roch_state[weiss] = roch_state[weiss].replace('Q' if weiss else 'q', '')
  if rochade:
    tv, tz = MOVES_ROCH[rochade][1]
    position[tz] = fig
    del position[tv]
    roch_state[weiss] = ''



def zug_zurücknehmen(zug, weiss, position, königspos):
  fig, von, zu, capture, umwandlung, rochade = zug
  position[von], position[zu] = fig, capture
  if not capture:
    del position[zu]
  if umwandlung:
    position[von] = 'P' if weiss else 'p'
  if fig in 'Kk':
    königspos[fig.isupper()] = von
  if rochade:
    tv, tz = MOVES_ROCH[rochade][1]
    position[tv] = fig
    del position[tz]
  
