from time import perf_counter as pfc
import chessdotcom as chess
from collections import defaultdict
import Teil_xx_Bitboards as bitboards


def i2A8(i):
  s, z = i % 8, i//8
  return chr(ord('a')+s)+chr(ord('8')-z)


def fen2pos(fen):
  i, position, kingspos = 0, {}, [0, 0]
  pos, farbe, rochade, enpassant, zug50, zugnr = fen.split()
  for char in pos:
    if char.isnumeric():
      i += int(char)
    elif char.isalpha():
      if char in 'kK':
        kingspos[char.isupper()] = i
      position[i] = char
      i += 1
  return farbe == 'w', position, kingspos


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
      if fig in 'rb':
        moves = sliding_move_bb[f][blocker]
      else:  # Queen
        blocker = move_bb['r'][i] & occupied_bb
        moves = sliding_move_bb['r'][blocker]
        blocker = move_bb['b'][i] & occupied_bb
        moves |= sliding_move_bb['b'][blocker]
      moves &= ~all_pieces_bb[weiss]
    if moves:
      züge.append([i, moves, fig])
  return züge


def zuggenerator(weiss, position):
  züge = []
  pseudo = pseudo_züge(weiss, position)
  for von, zus, fig in pseudo:
    for zu in [i for i, char in enumerate(bin(zus)[:1:-1]) if char == '1']:
      capture = ziehe(von,zu)
      if not imSchach(weiss):
        züge.append((fig, von, zu))
      else:
        print(f'SCHACH durch {fig} {i2A8(von)} - {i2A8(zu)}')
      ziehe_rückgängig(von,zu,capture)
  return züge


def ziehe(von, zu, capture=None):
  mask = SQUARE_BB[von] | SQUARE_BB[zu]
  pieces_bb[position[von]] ^= mask
  if zu in position: 
    pieces_bb[position[zu]] &= ~mask
    capture = position[zu]
  position[zu] = position[von]
  del position[von]
  return capture
  


def ziehe_rückgängig(von, zu, capture):
  mask = SQUARE_BB[von] | SQUARE_BB[zu]
  pieces_bb[position[zu]] ^= mask
  if von in position: 
    pieces_bb[position[von]] &= ~mask
  position[von] = position[zu]
  if capture:
    position[zu] = capture
  else:
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
    if sliding_move_bb[fig][blocker] & pieces_bb[fig if weiss else fig.upper()]:
      return True
    if sliding_move_bb[fig][blocker] & pieces_bb['q' if weiss else 'Q']:
      return True


NON_SLIDING_PIECES = {'K', 'k', 'p', 'P', 'n', 'N'}
#fen = chess.get_random_daily_puzzle().json['fen']
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
weiss, position, kingspos = fen2pos(fen)

move_bb = bitboards.create_move_bitboards()
pieces_bb, all_pieces_bb, occupied_bb = bitboards.create_pieces_bb(position)
blockerboards = bitboards.gen_blockerboards(move_bb)
sliding_move_bb = bitboards.gen_sliding_move_bb(blockerboards)
SQUARE_BB = bitboards.gen_square_bb()
ONLY1POS = {mask:i for i,mask in enumerate(SQUARE_BB)}


start = pfc()
for i in range(10_000):
  züge = zuggenerator(weiss, position)
print(pfc()-start)

# züge = zuggenerator(weiss, position)
# for fig, von, zu in züge:
#   print(f'{fig} {i2A8(von)} - {i2A8(zu)}')
