from time import perf_counter as pfc
import chessdotcom as chess
from collections import defaultdict

SHIFTS = [52, 53, 53, 53, 53, 53, 53, 52,
	        53, 54, 54, 54, 54, 54, 54, 53,
          53, 54, 54, 54, 54, 54, 54, 53,
          53, 54, 54, 54, 54, 54, 54, 53,
          53, 54, 54, 54, 54, 54, 54, 53,
          53, 54, 54, 54, 54, 54, 54, 53,
          53, 54, 54, 54, 54, 54, 54, 53,
          53, 54, 54, 53, 53, 53, 53, 53]

MAGICS = ['0x0080001020400080', '0x0040001000200040', '0x0080081000200080', '0x0080040800100080',
	        '0x0080020400080080', '0x0080010200040080', '0x0080008001000200', '0x0080002040800100',
          '0x0000800020400080', '0x0000400020005000', '0x0000801000200080', '0x0000800800100080',
          '0x0000800400080080', '0x0000800200040080', '0x0000800100020080', '0x0000800040800100',
          '0x0000208000400080', '0x0000404000201000', '0x0000808010002000', '0x0000808008001000',
          '0x0000808004000800', '0x0000808002000400', '0x0000010100020004', '0x0000020000408104',
          '0x0000208080004000', '0x0000200040005000', '0x0000100080200080', '0x0000080080100080',
          '0x0000040080080080', '0x0000020080040080', '0x0000010080800200', '0x0000800080004100',
          '0x0000204000800080', '0x0000200040401000', '0x0000100080802000', '0x0000080080801000',
          '0x0000040080800800', '0x0000020080800400', '0x0000020001010004', '0x0000800040800100',
          '0x0000204000808000', '0x0000200040008080', '0x0000100020008080', '0x0000080010008080',
          '0x0000040008008080', '0x0000020004008080', '0x0000010002008080', '0x0000004081020004',
          '0x0000204000800080', '0x0000200040008080', '0x0000100020008080', '0x0000080010008080',
          '0x0000040008008080', '0x0000020004008080', '0x0000800100020080', '0x0000800041000080',
          '0x00FFFCDDFCED714A', '0x007FFCDDFCED714A', '0x003FFFCDFFD88096', '0x0000040810002101',
          '0x0001000204080011', '0x0001000204000801', '0x0001000082000401', '0x0001FFFAABFAD1A2']

MOVES = {'k': [1, (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)],
         'q': [8, (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)],
         'r': [8, (-1, 0), (1, 0), (0, 1), (0, -1)],
         'b': [8, (-1, -1), (1, 1), (-1, 1), (1, -1)],
         'n': [1, (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2)],
         'p': [1, (0,1)],
         'P': [1, (0,-1)],
         'pc': [1, (-1,1), (1,1)],
         'Pc': [1, (-1,-1), (1,-1)]}          

for i,m in enumerate(MAGICS):
  MAGICS[i] = int(m,0)

    

def pretty(bb):
  board = bin(bb)[:1:-1]
  output = ''
  for i,char in enumerate(board):
    if not (i % 8): output+= '\n'
    output += '.' if char == '0' else '1'
  return output+'\n'
    
def shitty_hash(masked_composite, square):
  return (masked_composite * MAGICS[square]) >> SHIFTS[square]    

def create_move_bitboards():
  bb = {}
  for fig, vals in MOVES.items():
    richtungen = vals[1:]
    multi = vals[0]
    boards = []
    if fig not in 'pPpcPc': fig = fig.lower()
    for i in range(64):
      b = 0
      s1, z1 = i % 8, i // 8
      for ds,dz in richtungen:
        for n in range(1,multi+1):
          s2, z2 = s1+ds*n, z1+dz*n
          if (s2,z2) not in BRETT: break
          if fig in 'rbq':
            if ds == -1 and s2 == 0: continue
            if ds == 1 and s2 == 7: continue
            if dz == -1 and z2 == 0: continue
            if dz == 1 and z2 == 7: continue
          b |= 1 << z2*8+s2
      if fig == 'p' and z1 == 1:
        b |= 1 << (i+16)
      if fig == 'P' and z1 == 6:
        b |= 1 << (i-16)
      boards.append(b)
    bb[fig] = boards
  return bb

def fen2pos(fen):
  i,position = 0,{}
  pos, farbe, rochade, enpassant, zug50, zugnr = fen.split() 
  for char in pos:
    if char.isnumeric():
      i += int(char)
    elif char.isalpha():
      position[i] = char
      i += 1
  return farbe=='w', position         

def create_pieces_bb(position):
  bb, all_pieces = {}, {}
  w = b = 0
  for i,fig in position.items():
    board = 0 if fig not in bb else bb[fig]
    board |= 1 << i
    bb[fig]=board
    if fig.isupper():
      w |= board
    else:
      b |= board
  all_pieces[True] = w
  all_pieces[False] = b
  occupied = w | b
  return bb, all_pieces, occupied

def zuggenerator(weiss, position):
  züge, attacked = [], 0
  for i,fig in position.items():
    if fig.isupper() != weiss: continue
    if fig not in 'pP': fig = fig.lower()
    if fig in NON_SLIDING_PIECES:
      if fig in 'pP':
        moves = move_bb[fig][i] & ~occupied_bb
        pawn_captures = move_bb[fig+'c'][i] & all_pieces_bb[not weiss]
        moves |= pawn_captures
        attacked |= pawn_captures
      else: #king and knight  
        moves = move_bb[fig][i] & ~all_pieces_bb[weiss]
        attacked |= moves  
    else:
      blocker = move_bb[fig][i] & occupied_bb
      if not blocker: continue
      if fig in 'rb':
        moves = sliding_move_bb[fig+str(i)+str(blocker)]
      else: #Queen 
        blocker = move_bb['r'][i] & occupied_bb
        moves = sliding_move_bb['r'+str(i)+str(blocker)]
        blocker = move_bb['b'][i] & occupied_bb
        moves |= sliding_move_bb['b'+str(i)+str(blocker)]
      moves &= ~all_pieces_bb[weiss]
      attacked |= moves
    züge.append([i,moves,fig])    
  return züge,attacked

def get_ones_position(bb):
  ones = []
  for i,c in enumerate(bin(bb)[:1:-1]):
    if c == '1': ones.append(i)
  return ones

def i2A8(i):
  s,z = i%8, i//8
  return chr(ord('a')+s)+chr(ord('8')-z)

def imSchach(weiss):
  _ ,attacked = zuggenerator(not weiss, position)
  return pieces_bb['K' if weiss else 'k'] & attacked

def imSchach2(weiss):
  kingpos = pieces_bb['K' if weiss else 'k']
  for i,fig in position.items():
    if fig.isupper() == weiss: continue
    if fig not in 'pP': fig = fig.lower()
    if fig in NON_SLIDING_PIECES:
      if fig in 'pP':
        if move_bb[fig+'c'][i] & kingpos: return True
      else:
        if move_bb[fig][i] & kingpos: return True
    else:
      if fig in 'rRbB':
        hash = move_bb[fig][i] & occupied_bb
        if sliding_move_bb[fig+str(i)+str(hash)] & kingpos: return True
      else:
        hash = move_bb['r'][i] & occupied_bb
        if sliding_move_bb['r'+str(i)+str(hash)] & kingpos: return True
        hash = move_bb['b'][i] & occupied_bb
        if sliding_move_bb['b'+str(i)+str(hash)] & kingpos: return True



#Generate a unique blocker board, given an index (0..2^bits) and the blocker mask 
#for the piece/square. Each index will give a unique blocker board. */
def gen_blockerboard(index, blockermask):
  blockerboard = blockermask
  bitindex = 0
  for i in range(64):
    if blockermask & 1<<i:
      if not(index & (1<<bitindex)):
        blockerboard &= ~(1<<i)
      bitindex += 1
  return blockerboard      

def gen_blockerboards(): 
  blockerboards = defaultdict(dict)
  for fig in 'rb':
    for feld in range(64):
      blockerboards[fig][feld] = []
      moveboard = move_bb[fig][feld]
      bits = len(get_ones_position(moveboard))
      for i in range(1<<bits):
        blockerboards[fig][feld].append(gen_blockerboard(i, moveboard))
  return blockerboards

def gen_sliding_move_bb(blockerboards):
  sliding_move_bb = {}
  for fig in blockerboards:
    for feld, values in blockerboards[fig].items():
      for blocker in values:
        moves, s, z = 0, feld%8, feld//8
        mult = MOVES[fig][0]
        for ds,dz in MOVES[fig][1:]:
          for m in range(1,mult):
            s2,z2 = s+ds*m, z+dz*m
            if (s2,z2) not in BRETT: break
            moves |= 1 << s2+z2*8
            if 1 << s2+z2*8 & blocker: break
        sliding_move_bb[fig+str(feld)+str(blocker)] = moves
  return sliding_move_bb        



BRETT = {(s,z): s % 2 == z % 2 for s in range(8) for z in range(8)}
NON_SLIDING_PIECES = {'K','k','p','P','n','N'}
#fen = chess.get_random_daily_puzzle().json['fen']
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
weiss, position = fen2pos(fen)


move_bb = create_move_bitboards()

pieces_bb, all_pieces_bb, occupied_bb = create_pieces_bb(position)
blockerboards = gen_blockerboards()
sliding_move_bb = gen_sliding_move_bb(blockerboards)

print(len(sliding_move_bb.values()))
print(len(set(sliding_move_bb.values())))


# start = pfc()
# for i in range(10_000):
#   pseudo,attacked = zuggenerator(weiss, position)
#   for von, zus, fig in pseudo:
#     for zu in get_ones_position(zus):
#       imSchach2(weiss)
# print(pfc()-start)

# pseudo, attacked = zuggenerator(weiss, position)
# for von, zus, fig in pseudo:
#   print(f'{fig} {i2A8(von)}')
#   print(pretty(zus))


