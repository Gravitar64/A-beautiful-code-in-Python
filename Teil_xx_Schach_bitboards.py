from time import perf_counter as pfc
import chessdotcom as chess
from collections import defaultdict
import Teil_xx_Bitboards as bitboards

# TODO enPassant fehlt
# FEAUTURE SLIDING_BB auf minimale Größe optimieren (MAGIC_KEYS Rook 100570->4855 Einträge)

def i2A8(i):
  s, z = i % 8, i//8
  return chr(ord('a')+s)+chr(ord('8')-z)


def fen2pos(fen):
  i, position, roch_state= 0, {}, ['','']
  pos, farbe, rochade, enpassant, zug50, zugnr = fen.split()
  for char in pos:
    if char.isnumeric():
      i += int(char)
    elif char.isalpha():
      position[i] = char
      i += 1
  for char in rochade:
    if char == '-': continue
    roch_state[char.isupper()] += char
  return farbe == 'w', position, roch_state


def pseudo_züge(weiss, position):
  züge = []
  for i, fig in position.items():
    if fig.isupper() != weiss:
      continue
    f = fig.lower()
    if fig in NON_SLIDING_PIECES:
      if fig in 'pP':
        moves = MOVE_BB[fig][i] & ~occupied_bb
        moves |= MOVE_BB[fig + 'c'][i] & all_pieces_bb[not weiss]
        #Bauern auf der Grundlinie
        if (weiss and 47 < i < 56) and \
           i - 8 not in position and \
           i - 16 not in position:
           moves |= SQUARE_BB[i - 16]
        if (not weiss and 7 < i < 16) and \
           i + 8 not in position and \
           i + 16 not in position:
           moves |= SQUARE_BB[i + 16]
      else:  # king and knight
        moves = MOVE_BB[f][i] & ~all_pieces_bb[weiss]
    else:
      blocker = MOVE_BB[f][i] & occupied_bb
      if not blocker:
        continue
      if f in 'rb':
        moves = SLIDING_MOVE_BB[f][blocker+i]
      else:  # Queen
        blocker = MOVE_BB['r'][i] & occupied_bb
        moves = SLIDING_MOVE_BB['r'][blocker+i]
        blocker = MOVE_BB['b'][i] & occupied_bb
        moves |= SLIDING_MOVE_BB['b'][blocker+i]
      moves &= ~all_pieces_bb[weiss]
    if moves:
      züge.append([i, moves, fig])
  return züge


def zuggenerator(weiss, position):
  pseudo = pseudo_züge(weiss, position)
  züge = []
  for von, zus, fig in pseudo:
    for zu in [i for i in range(64) if zus & SQUARE_BB[i]]:
      capture = ziehe(weiss, von, zu, None)
      if not imSchach(weiss):
        züge.append((fig, von, zu, None, capture))
      ziehe_rückgängig(weiss, von, zu, None, capture)
  #Rochade
  if not imSchach(weiss) and roch_state[weiss]:
    züge.extend(gen_rochade_züge(weiss))
  return züge

def gen_rochade_züge(weiss):
  global roch_state
  roch_züge = []
  for roch in roch_state[weiss]:
    mask = ROCH_BB[roch][0]
    könig_zieht_durch = ROCH_BB[roch][1]
    if occupied_bb & mask: continue
    im_schach = False
    kingspos = ONLY1POS[pieces_bb['K' if weiss else 'k']]
    for feld in könig_zieht_durch:
      save_state = roch_state.copy()
      capture = ziehe(weiss, kingspos, feld, None)
      if imSchach(weiss): im_schach = True
      ziehe_rückgängig(weiss, kingspos, feld, None, capture)
      roch_state = save_state
    if not im_schach:
      roch_züge.append(('K' if weiss else 'k', kingspos, feld, roch, None))  
  return roch_züge



def ziehe(weiss, von, zu, rochade):
  global occupied_bb
  capture = position.get(zu, None)
  vonzu = SQUARE_BB[von] | SQUARE_BB[zu]
  pieces_bb[position[von]] ^= vonzu
  all_pieces_bb[weiss] ^= vonzu
  if capture:
    pieces_bb[capture] ^= SQUARE_BB[zu]
    all_pieces_bb[not weiss] ^= SQUARE_BB[zu]
    occupied_bb ^= SQUARE_BB[von]
  else:
    occupied_bb ^= vonzu
  if rochade:
    tvon, tzu = ROCH_BB[rochade][2]
    tvonzu = SQUARE_BB[tvon] | SQUARE_BB[tzu]
    pieces_bb['R' if weiss else 'r'] ^= tvonzu
    all_pieces_bb[weiss] ^= tvonzu
    position[tzu] = position[tvon]
    del position[tvon]

  position[zu] = position[von]
  del position[von]
  return capture


def ziehe_rückgängig(weiss, von, zu, rochade, capture):
  global occupied_bb
  vonzu = SQUARE_BB[von] | SQUARE_BB[zu]
  pieces_bb[position[zu]] ^= vonzu
  all_pieces_bb[weiss] ^= vonzu
  if capture:
    pieces_bb[capture] ^= SQUARE_BB[zu]
    all_pieces_bb[not weiss] ^= SQUARE_BB[zu]
    occupied_bb ^= SQUARE_BB[von]
  else:
    occupied_bb ^= vonzu
  if rochade:
    tvon, tzu = ROCH_BB[rochade][2]
    tvonzu = SQUARE_BB[tvon] | SQUARE_BB[tzu]
    pieces_bb['R' if weiss else 'r'] ^= tvonzu
    all_pieces_bb[weiss] ^= tvonzu
    position[tvon] = position[tzu]
    del position[tzu]

  position[von], position[zu] = position[zu], capture
  if not capture:
    del position[zu]


def imSchach(weiss):
  i = ONLY1POS[pieces_bb['K' if weiss else 'k']]
  if MOVE_BB['n'][i] & pieces_bb.get('n' if weiss else 'N',0):
    return True
  if MOVE_BB['k'][i] & pieces_bb.get('k' if weiss else 'K', 0):
    return True
  if MOVE_BB['Pc' if weiss else 'pc'][i] & pieces_bb.get('p' if weiss else 'P', 0):
    return True
  for fig in 'rb':
    blocker = MOVE_BB[fig][i] & occupied_bb
    if SLIDING_MOVE_BB[fig][blocker+i] & pieces_bb.get(fig if weiss else fig.upper(), 0):
      return True
    if SLIDING_MOVE_BB[fig][blocker+i] & pieces_bb.get('q' if weiss else 'Q', 0):
      return True


NON_SLIDING_PIECES = {'K', 'k', 'p', 'P', 'n', 'N'}
#fen = chess.get_random_daily_puzzle().json['fen']
#fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
#fen = 'r3k2r/1b4bq/2N5/8/8/6n1/7B/R3K2R w KQkq - 0 1'
fen = 'k6r/8/B1N4n/P7/1P2P3/2P4b/5Pq1/8 b - - 0 1'
weiss, position, roch_state = fen2pos(fen)

MOVE_BB = bitboards.gen_move_bitboards()
SLIDING_MOVE_BB = bitboards.gen_sliding_move_bb(MOVE_BB)
SQUARE_BB = bitboards.gen_square_bb()
ONLY1POS = {mask: i for i, mask in enumerate(SQUARE_BB)}
ROCH_BB = {'K': [1 << 61 | 1 << 62, (61,62), (63,61)],
           'Q': [1 << 57 | 1 << 58 | 1 << 59, (59,58), (56,59)],
           'k': [1 << 5 | 1 << 6, (5,6), (7,5)],
           'q': [1<<1 | 1<<2 | 1<<3, (3,2), (0,3)]}
pieces_bb, all_pieces_bb, occupied_bb = bitboards.gen_pieces_bb(position)
save_occ = occupied_bb
save_all = all_pieces_bb.copy()


start = pfc()
for i in range(10_000):
  züge = zuggenerator(weiss, position)
print(pfc()-start)


# züge = zuggenerator(weiss, position)
# for fig, von, zu, rochade, capture in züge:
#   zug = ''
#   if rochade and rochade in 'qQ':
#     zug += 'O-O-O'
#   elif rochade and rochade in 'kK':
#     zug += 'O-O'
#   else:
#     zug += fig.upper() if fig not in 'pP' else ''
#     zug += 'x' if capture else ''
#     zug += i2A8(zu)
#   print(zug)  


# for pos, fig in position.items():
#   print(bitboards.pretty(pieces_bb[fig]))
#   print(fig)

# print(bitboards.pretty(all_pieces_bb[True]))
# print(bitboards.pretty(all_pieces_bb[False]))
# print(bitboards.pretty(occupied_bb))


assert occupied_bb == save_occ
assert all_pieces_bb == save_all
