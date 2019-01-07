import re, time

start = time.perf_counter()

koordinaten = []
koordNeu = []
with open('AdventOfCode_10.txt') as f:
  for zeile in f:
    pos, vel = re.match(r"position=<(.*)> velocity=<(.*)>", zeile).groups()
    x, y = [int(i) for i in pos.split(',')]
    dx, dy = [int(i) for i in vel.split(',')]
    koordinaten.append([x, y, dx, dy])

def minMaxErmitteln(list):
  x1, y1 = map(min, zip(*list))
  x2, y2 = map(max, zip(*list))  
  return x1, x2, y1, y2


def newPosition(sekunde):
  global koordNeu
  koordNeu = []
  for koord in koordinaten:
    x = koord[0]+koord[2]*sekunde
    y = koord[1]+koord[3]*sekunde
    koordNeu.append((x, y))    
  x1, x2, y1, y2 = minMaxErmitteln(koordNeu)
  return abs(x2-x1) * abs(y2-y1)


minFläche = 10_000_000
for s in range(15_000):
  aktFläche = newPosition(s)
  if aktFläche < minFläche:
    minFläche = aktFläche
    minSekunde = s

newPosition(minSekunde)
minx, maxx, miny, maxy = minMaxErmitteln(koordNeu)
offsX = -minx
offsY = -miny

sp = abs(maxx - minx)+1
ze = abs(maxy - miny)+1
fl = [' '] * sp * ze

for i in koordNeu:
  x = i[0]+offsX
  y = i[1]+offsY
  fl[y*sp+x] = '#'

for i, char in enumerate(fl):
  print(char, end='')
  if (i+1) % sp == 0:
    print()
print(f'Dauer: {time.perf_counter()-start}')
print(minSekunde, minFläche)