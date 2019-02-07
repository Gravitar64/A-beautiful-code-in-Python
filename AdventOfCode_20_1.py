richtungen = {'N': (0,-1), 'E':(1,0), 'W':(-1,0), 'S':(0,1)}

def addPos(pos1, pos2):
  return (pos1[0] + pos2[0], pos1[1]+pos2[1])

with open('aoc_20.txt') as f:
  raw = f.readline()
  raw = raw[1:-1]

def printMap():
  minx = min([x[0] for x in map.keys()])
  maxx = max([x[0] for x in map.keys()])
  miny = min([y[1] for y in map.keys()])
  maxy = max([y[1] for y in map.keys()])
  for y in range (miny-1, maxy+2):
    print()
    for x in range (minx-1, maxx+2):
      if (x,y) in map:
        print(map[x,y], end = '')
      else:
        print('#',end='')
  
map = {(0,0) : 'X'}
pos = 0

def mapErstellen(aktPos):
  global pos
  while pos < len(raw):
    zeichen = raw[pos]
    pos += 1
    if zeichen in richtungen:
      aktPos = addPos(aktPos, richtungen[zeichen])
      if zeichen in ('S', 'N'):
        map[aktPos] = '-'
      else:
        map[aktPos] = '|'
      aktPos = addPos(aktPos, richtungen[zeichen])
      map[aktPos] = '.'
    elif zeichen == '(':
      mapErstellen(aktPos)
    elif zeichen == '|':
      return

    
mapErstellen((0,0))
printMap()

