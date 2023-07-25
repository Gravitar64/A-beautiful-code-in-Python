import itertools,time


def print_quadrat(quadrat):
  print(f'Lösung: {len(lösungen)} nach {time.perf_counter()-start:.2f} Sek.')
  for i,z in enumerate(quadrat):
    if i > 0 and not i%N: print()
    print(f'{z:>2} ',end='')
  print('\n')  


def check(quadrat):
  if sum(quadrat[i*N+i] for i in range(N)) != summe: return False
  if sum(quadrat[i*N+N-i-1] for i in range(N)) != summe: return False
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
      lösungen.append(quadrat)
      print_quadrat(quadrat)
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
summe = (N**3+N)//2
lösungen = []
zeilen(0,set(range(1,N**2+1)),[0]*N**2)
print(f'{len(lösungen):,} Lösungen für {N}x{N} magische Quadrate mit der Summe {summe} ({time.perf_counter()-start:.2f})')