import itertools,time


def check(quadrat):
  if sum(quadrat[i*N+i] for i in range(N)) != summe: return False
  if sum(quadrat[i*N-i-1] for i in range(N)) != summe: return False
  return True


def lösungsmenge():
  ls = []
  for l in itertools.combinations(range(1,N**2+1),N):
    if sum(l) != summe: continue
    ls.append(set(l))
  return ls  
    

def zeilen(nr, ls, quadrat):
  if nr == N-1:
    füllen(ls,quadrat)
    return
  
  for z in ls:
    l = [x for x in ls if not x&z]
    for p in itertools.permutations(z):
      quadrat[N*nr:N*nr+N] = p
      zeilen(nr+1, l, quadrat)


def füllen(ls,quadrat):
  letzte_zeile = [summe - sum(quadrat[z*N+s] for z in range(N-1)) for s in range(N)]
  if set(letzte_zeile) not in ls: return
  quadrat[N*(N-1):N*N] = letzte_zeile
  if check(quadrat): 
    lösungen.append(quadrat)
    print(f'{len(lösungen)} {quadrat} {time.perf_counter()-start:.2f}')

start = time.perf_counter()
N = 4
summe = (N**3+N)//2
ls = lösungsmenge()
lösungen = []
zeilen(0,ls,[0]*N*N)
print(f'{len(lösungen):,} Lösungen für {N}x{N} magische Quadrate mit der Summe {summe} ({time.perf_counter()-start:.2f})')