from time import perf_counter as pfc
import chessdotcom as chess
from collections import defaultdict
import Teil_xx_Bitboards as bitboards

# TODO Fehler bei Bauernzügen von der Grundlinie aus, bei +2 werden blockende Figuren nicht erkannt
# TODO Rochade fehlt
# TODO enPassant fehlt
# FEAUTURE SLIDING_BB auf minimale Größe optimieren (MAGIC_KEYS Rook 100570->4855 Einträge)

def i2A8(i):
  s, z = i % 8, i//8
  return chr(ord('a')+s)+chr(ord('8')-z)


def fen2pos(fen):
  i, position, = 0, {}
  pos, farbe, rochade, enpassant, zug50, zugnr = fen.split()
  for char in pos:
    if char.isnumeric():
      i += int(char)
    elif char.isalpha():
      position[i] = char
      i += 1
  return farbe == 'w', position


def pseudo_züge(weiss, position):
  züge = []
  for i, fig in position.items():
    if fig.isupper() != weiss:
      continue
    f = fig.lower()
    if fig in NON_SLIDING_PIECES:
      if fig in 'pP':
        moves = move_bb[fig][i] & ~occupied_bb
        moves |= move_bb[fig+'c'][i] & all_pieces_bb[not weiss]
      else:  # king and knight
        moves = move_bb[f][i] & ~all_pieces_bb[weiss]
    else:
      blocker = move_bb[f][i] & occupied_bb
      if not blocker:
        continue
      if f in 'rb':
        moves = sliding_move_bb[f][blocker+i]
      else:  # Queen
        blocker = move_bb['r'][i] & occupied_bb
        moves = sliding_move_bb['r'][blocker+i]
        blocker = move_bb['b'][i] & occupied_bb
        moves |= sliding_move_bb['b'][blocker+i]
      moves &= ~all_pieces_bb[weiss]
    if moves:
      züge.append([i, moves, fig])
  return züge


def zuggenerator(weiss, position):
  züge = []
  pseudo = pseudo_züge(weiss, position)
  for von, zus, fig in pseudo:
    for zu in [i for i in range(64) if zus & SQUARE_BB[i]]:
      capture = ziehe(weiss, von, zu)
      if not imSchach(weiss):
        züge.append((fig, von, zu))
      ziehe_rückgängig(weiss, von, zu, capture)
  return züge


def ziehe(weiss, von, zu):
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

  position[zu] = position[von]
  del position[von]
  return capture


def ziehe_rückgängig(weiss, von, zu, capture):
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

  position[von], position[zu] = position[zu], capture
  if not capture:
    del position[zu]


def imSchach(weiss):
  i = ONLY1POS[pieces_bb['K' if weiss else 'k']]
  if move_bb['n'][i] & pieces_bb['n' if weiss else 'N']:
    return True
  if move_bb['k'][i] & pieces_bb['k' if weiss else 'K']:
    return True
  if move_bb['Pc' if weiss else 'pc'][i] & pieces_bb['p' if weiss else 'P']:
    return True
  for fig in 'rb':
    blocker = move_bb[fig][i] & occupied_bb
    if sliding_move_bb[fig][blocker+i] & pieces_bb[fig if weiss else fig.upper()]:
      return True
    if sliding_move_bb[fig][blocker+i] & pieces_bb['q' if weiss else 'Q']:
      return True


NON_SLIDING_PIECES = {'K', 'k', 'p', 'P', 'n', 'N'}
#fen = chess.get_random_daily_puzzle().json['fen']
#fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
fen = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w  KQkq - 0 1'
weiss, position = fen2pos(fen)

move_bb = bitboards.gen_move_bitboards()
pieces_bb, all_pieces_bb, occupied_bb = bitboards.gen_pieces_bb(position)
blockerboards = bitboards.gen_blockerboards(move_bb)
sliding_move_bb = bitboards.gen_sliding_move_bb(blockerboards)
SQUARE_BB = bitboards.gen_square_bb()
ONLY1POS = {mask: i for i, mask in enumerate(SQUARE_BB)}
occ1 = occupied_bb
all_copy = all_pieces_bb.copy()


start = pfc()
for i in range(10_000):
  züge = zuggenerator(weiss, position)
print(pfc()-start)


züge = zuggenerator(weiss, position)
for fig, von, zu in züge:
  print(f'{fig} {i2A8(von)} - {i2A8(zu)}')

# for pos, fig in position.items():
#   print(bitboards.pretty(pieces_bb[fig]))
#   print(fig)

# print(bitboards.pretty(all_pieces_bb[True]))
# print(bitboards.pretty(all_pieces_bb[False]))
# print(bitboards.pretty(occupied_bb))


assert occupied_bb == occ1
assert all_copy == all_pieces_bb
