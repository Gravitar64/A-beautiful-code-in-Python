import time
import sys

sys.setrecursionlimit(5000)
start = time.perf_counter()


clay = set()

with open('adventofcode_17.txt') as f:
  for zeile in f:
    a, b = zeile.split(', ')
    if a[0] == 'x':
      x1 = x2 = int(a[2:])
      y1, y2 = [int(y) for y in b[2:].split('..')]
    else:
      y1 = y2 = int(a[2:])
      x1, x2 = [int(y) for y in b[2:].split('..')]
    for x in range(x1, x2+1):
      for y in range(y1, y2+1):
        clay.add((x, y))

miny = min([p[1] for p in clay])
maxy = max([p[1] for p in clay])
minx = min([p[0] for p in clay])
maxx = max([p[0] for p in clay])


def addPos(pos1, pos2):
  return(pos1[0] + pos2[0], pos1[1]+pos2[1])


LINKS = (-1, 0)
RECHTS = (1, 0)
UNTEN = (0, 1)
fließend = set()
stehend = set()


def flood(pos):
  fließend.add(pos)
  unten = addPos(pos, UNTEN)
  if unten not in clay and unten not in fließend and 1 <= unten[1] <= maxy:
    flood(unten)

  if unten not in clay and unten not in stehend:
    return False

  links = addPos(pos, LINKS)
  rechts = addPos(pos, RECHTS)

  if links not in clay and links not in fließend:
    flood(links)

  if rechts not in clay and rechts not in fließend:
    flood(rechts)    

  if links in clay:
    start = pos
    richtung = RECHTS

  if rechts in clay:
    start = pos
    richtung = LINKS
  
  if links in clay or rechts in clay:
    vollständig = True
    while start not in clay:
      u = addPos(start,UNTEN)
      if u not in clay and u not in stehend:
        vollständig = False
        break
      start = addPos(start,richtung)  
    if vollständig:
      step = -1 if pos[0] > start[0] else 1
      for x in range(pos[0], start[0], step):
        stehend.add((x,pos[1]))
      


flood((500, 0))


print('Part 1: ', len([pos for pos in fließend if miny <= pos[1] <= maxy]))
print('Part 2: ', len(stehend))
print(time.perf_counter()-start)

with open('AdventOfCode_Solution_Tag_17.txt', 'w') as f:
  for y in range(miny, maxy):
    f.write('\n')
    for x in range(minx, maxx):
      pos = (x,y)
      if pos in clay:
        f.write('#')
      elif pos in stehend:
        f.write('~')
      elif pos in fließend:
        f.write('|')
      else:
        f.write(' ')      