import itertools,time


def print_quadrat(quadrat):
  print(f'Lösung: {anzahl} nach {time.perf_counter()-start:.2f} Sek.')
  for i,z in enumerate(quadrat):
    if i > 0 and not i%N: print()
    print(f'{z:>2} ',end='')
  print('\n')  


def check(quadrat):
  if sum(quadrat[i*N+i] for i in range(N)) != summe: return False
  if sum(quadrat[i*N+N-i-1] for i in range(N)) != summe: return False
  
  if N == 4 and perfect:
    if sum(quadrat[0:2]+quadrat[4:6]) != summe: return False
    if sum(quadrat[2:4]+quadrat[6:8]) != summe: return False
    if sum(quadrat[8:10]+quadrat[12:14]) != summe: return False
    if sum(quadrat[10:12]+quadrat[14:16]) != summe: return False
    if sum(quadrat[5:7]+quadrat[9:11]) != summe: return False
    if sum(quadrat[x] for x in (0,3,12,15)) != summe: return False
    if sum(quadrat[x] for x in (1,7,8,14)) != summe: return False
    if sum(quadrat[x] for x in (2,4,11,13)) != summe: return False
  
  return True


def zeilen(nr, zahlen, quadrat):
  bisherige_summe = sum(quadrat[nr*N:nr*N+nr])
  for z in itertools.permutations(zahlen,N-1-nr):
    rest = summe - bisherige_summe - sum(z)
    zahlen2 = zahlen - set(z)
    if rest not in zahlen2: continue
    quadrat[nr*N+nr:nr*N+N] = list(z)+[rest]
    spalten(nr,zahlen2-{rest},quadrat)


def spalten(nr, zahlen, quadrat):
  if not zahlen:
    if check(quadrat):
      global anzahl
      anzahl += 1
      lösungen.append(quadrat.copy())
      #print_quadrat(quadrat)
    return
  
  bisherige_summe = sum(quadrat[i*N+nr] for i in range(nr+1))
  for z in itertools.permutations(zahlen,N-2-nr):
    rest = summe - bisherige_summe - sum(z)
    zahlen2 = zahlen - set(z)
    if rest not in zahlen2: continue
    for i,zahl in enumerate(list(z)+[rest],start=nr+1):
      quadrat[i*N+nr]=zahl
    zeilen(nr+1,zahlen2-{rest},quadrat)    
  

start = time.perf_counter()
N = 4
perfect = True
summe = (N**3+N)//2
anzahl = 0
lösungen = []
zeilen(0,set(range(1,N**2+1)),[0]*N**2)
print(f'{anzahl} Lösungen für {N}x{N} magische Quadrate mit der Summe {summe} ({time.perf_counter()-start:.2f})')

if N==4 and perfect:
  anzahl = 0
  start = time.perf_counter()
  print('Dürer magische Quadrate mit 15 14 in der untersten Zeile')
  for quadrat in lösungen:
    if quadrat[13] != 15 or quadrat[14] != 14: continue
    anzahl += 1
    print_quadrat(quadrat) 