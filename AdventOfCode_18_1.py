import time

start = time.perf_counter()

mapStart = {}
achtNachbarn = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1,1)]

with open('aoc_18.txt') as f:
  for y, zeile in enumerate(f):
    zeile = zeile.strip()
    for x, char in enumerate(zeile):
      mapStart[(x,y)] = char

spalten = len(zeile)      

def addPos(pos1, pos2) -> tuple:
  return (pos1[0] + pos2[0], pos1[1] + pos2[1])    


def findeNachbarn(pos) -> list:
  nachbarn = []
  for n in achtNachbarn:
    newPos = addPos(pos,n)
    if newPos not in mapStart:
      continue
    nachbarn.append(newPos)
  return nachbarn

def open(pos) -> chr:
  counter = 0
  for p in findeNachbarn(pos):
    if mapStart[p] == '|':
      counter += 1
  return '|' if counter > 2 else '.'

def tree(pos) -> chr:
  counter = 0
  for p in findeNachbarn(pos):
    if mapStart[p] == '#':
      counter += 1
  return '#' if counter > 2 else '|'
  
def lumberyard(pos) -> chr:
  counterLumb, counterTree = 0,0
  for p in findeNachbarn(pos):
    if mapStart[p] == '#':
      counterLumb += 1
    elif mapStart[p] == '|':
      counterTree += 1
  return '#' if counterLumb > 0 and counterTree > 0 else '.'  

def printMap(map):
  i = 0
  for char in map.values():
    print(char, end='')
    if (i+1) % spalten == 0:
      print()
    i += 1  
    
for n in range(10):
  mapEnd = {}
  for pos, typ in mapStart.items():
    if typ == '.':
      mapEnd[pos] = open(pos)
    elif typ == '|':
      mapEnd[pos] = tree(pos)
    elif typ == '#':
      mapEnd[pos] = lumberyard(pos)
  mapStart = mapEnd.copy()


anzTrees = len([t for t in mapStart.values() if t == '|'])
anzLumb  = len([t for t in mapStart.values() if t == '#'])
print(anzTrees * anzLumb)  
print(time.perf_counter() - start)
