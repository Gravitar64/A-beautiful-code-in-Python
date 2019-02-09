from collections import defaultdict
import time

start = time.perf_counter()

richtungen = {'N': (0, -1), 'E': (1, 0), 'W': (-1, 0), 'S': (0, 1)}


def addPos(pos1, pos2):
  return (pos1[0] + pos2[0], pos1[1]+pos2[1])


with open('AdventOfCode_20.txt') as f:
  raw = f.readline()
  raw = raw[1:-1]


def mapErstellen(aktPos):
  map = defaultdict(int)
  stack = []
  lastPos = aktPos
  for zeichen in raw:
    if zeichen in richtungen:
      aktPos = addPos(aktPos, richtungen[zeichen])
      if aktPos not in map:
        map[aktPos] = map[lastPos]+1
    elif zeichen == '(':
      stack.append(aktPos)
    elif zeichen == ')':
      aktPos = stack.pop()
    elif zeichen == '|':
      aktPos = stack[-1]
    lastPos = aktPos
  return map


map = mapErstellen((0, 0))
lösung1 = max(map.values())
lösung2 = len([x for x in map.values() if x > 999])

print(f'Lösung Tag 20, Teil 1: {lösung1}')
print(f'Lösung Tag 20, Teil 2: {lösung2}')
print(time.perf_counter() - start)
