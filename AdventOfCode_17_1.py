from dataclasses import dataclass

clay=[]

@dataclass
class Clay():
  fromX : int
  fromY : int
  toX   : int
  toY   : int

maxX, minX, maxY = 0, 1000, 0
with open('aoc_17.txt') as f:
  for zeile in f:
    a, b = zeile.split(', ')
    if a[0] == 'x':
      x1 = x2 = int(a[2:])
      y1,y2 = [int(y) for y in b[2:].split('..')]
    else:
      y1 = y2 = int(a[2:])
      x1,x2 = [int(y) for y in b[2:].split('..')]
    maxX = max(maxX, x2)
    minX = min(minX, x1)
    maxY = max(maxY, y2)
    clay.append(Clay(x1,y1,x2,y2))


minX -= 1
zeilen = maxY+1
spalten = maxX - minX+2

def printMap():
  for i in range(zeilen*spalten):
    pos = (i % spalten, i // spalten)
    if pos in map:
      print(map[pos], end='')
    else:
      print('.', end='')
    if (i+1) % spalten == 0:
      print()
  print()
  
def addPos(pos1,pos2):
  return(pos1[0] + pos2[0], pos1[1]+pos2[1])
  
def gültig(pos):
  if pos[0] < 0 or pos[0] > spalten or pos[1] < 0 or pos[1] > zeilen:
    return False
  return True  
  

for c in clay:
  c.fromX -= minX
  c.toX -= minX

map = {}  
for c in clay:
  for y in range(c.fromY,c.toY+1):
    for x in range(c.fromX, c.toX+1):
      map[(x,y)] = '#'
    
map[(500-minX,0)] = '+'


directions = [(0,1), (-1,0), (1,0)]

def flood(pos):
  for d in directions:
    newPos = addPos(pos, d)
    if newPos in map:
      if map[newPos] == '#':
        continue
    else:  
      if not gültig(newPos):
        return
      map[newPos] = '|'
      printMap()
      flood(newPos)

      
flood((500-minX, 0))      
  
  
      
