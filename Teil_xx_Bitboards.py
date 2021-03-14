from collections import defaultdict

MOVES = {'k': [1, (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)],
         'q': [8, (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)],
         'r': [8, (-1, 0), (1, 0), (0, 1), (0, -1)],
         'b': [8, (-1, -1), (1, 1), (-1, 1), (1, -1)],
         'n': [1, (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2)],
         'p': [1, (0, 1)],
         'P': [1, (0, -1)],
         'pc': [1, (-1, 1), (1, 1)],
         'Pc': [1, (-1, -1), (1, -1)]}

BRETT = {(s,z): s % 2 == z % 2 for s in range(8) for z in range(8)}


def gen_blockerboard(index, blockermask):
  blockerboard = blockermask
  bitindex = 0
  for i in range(64):
    if blockermask & 1 << i:
      if not(index & (1 << bitindex)):
        blockerboard &= ~(1 << i)
      bitindex += 1
  return blockerboard


def gen_blockerboards(move_bb):
  blockerboards = defaultdict(dict)
  for fig in 'rb':
    for feld in range(64):
      blockerboards[fig][feld] = []
      moveboard = move_bb[fig][feld]
      bits = bin(moveboard).count('1')
      for i in range(1 << bits):
        blockerboards[fig][feld].append(gen_blockerboard(i, moveboard))
  return blockerboards


def gen_sliding_move_bb(blockerboards):
  sliding_move_bb = defaultdict(dict)
  for fig in blockerboards:
    for feld, values in blockerboards[fig].items():
      for blocker in values:
        moves, s, z = 0, feld % 8, feld//8
        mult = MOVES[fig][0]
        for ds, dz in MOVES[fig][1:]:
          for m in range(1, mult):
            s2, z2 = s+ds*m, z+dz*m
            if (s2, z2) not in BRETT:
              break
            moves |= 1 << s2 + z2 * 8
            if 1 << s2+z2*8 & blocker:
              break
        sliding_move_bb[fig][blocker+feld] = moves
  return sliding_move_bb


def gen_move_bitboards():
  bb = {}
  for fig, vals in MOVES.items():
    richtungen = vals[1:]
    multi = vals[0]
    boards = []
    if fig not in 'pPpcPc':
      fig = fig.lower()
    for i in range(64):
      b = 0
      s1, z1 = i % 8, i // 8
      for ds, dz in richtungen:
        for n in range(1, multi+1):
          s2, z2 = s1+ds*n, z1+dz*n
          if (s2, z2) not in BRETT:
            break
          if fig in 'rbq':
            if ds == -1 and s2 == 0:
              continue
            if ds == 1 and s2 == 7:
              continue
            if dz == -1 and z2 == 0:
              continue
            if dz == 1 and z2 == 7:
              continue
          b |= 1 << z2*8+s2
      if fig == 'p' and z1 == 1:
        b |= 1 << (i+16)
      if fig == 'P' and z1 == 6:
        b |= 1 << (i-16)
      boards.append(b)
    bb[fig] = boards
  return bb


def gen_pieces_bb(position):
  bb, all_pieces = {}, [0,0]
  w = b = 0
  for i, fig in position.items():
    board = 0 if fig not in bb else bb[fig]
    board |= 1 << i
    bb[fig] = board
    all_pieces[fig.isupper()] |= board
  return bb, all_pieces, all_pieces[0] | all_pieces[1]

def gen_square_bb():
  return [1<<i for i in range(64)] 


def pretty(bb):
  board = bin(bb)[:1:-1]
  board = board+'0'*64
  board = board[:64]
  output = ''
  for i, char in enumerate(board):
    if not (i % 8):
      output += f'\n{8-i//8}  '
    output += '. ' if char == '0' else '1 '
  return output+'\n   A B C D E F G H'

if __name__ == '__main__':
  move = gen_move_bitboards()
  blocker = gen_blockerboards(move)
  slider = gen_sliding_move_bb(blocker)
  

