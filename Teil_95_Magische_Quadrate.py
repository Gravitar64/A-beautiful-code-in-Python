import itertools,time


def check(attempt):
  if sum(attempt[i*N+i] for i in range(N)) != summe: return False
  if sum(attempt[i*N+N-1-i] for i in range(N)) != summe:  return False
  return True


def zeilen(pos,quadrat,zahlen):
  base=summe-sum(quadrat[pos*N:pos*N+pos])
  for p in itertools.permutations(zahlen,N-1-pos):
    rest=base-sum(p)
    zahlen2=zahlen-set(p)
    if rest not in zahlen2: continue
    for i in range(pos,N-1):
      quadrat[pos*N+i]=p[i-pos]
    quadrat[pos*N+N-1]=rest
    spalten(pos,quadrat,zahlen2-{rest})


def spalten(pos,quadrat,zahlen):
  if not zahlen:
    if check(quadrat):
      lösungen.append(quadrat)
      #print(f'{anzahl:>4}. {quadrat} {time.time()-start:.1f}')
    return
  base=summe-sum([quadrat[N*i+pos] for i in range(pos+1)])
  for p in itertools.permutations(zahlen,N-2-pos):
    rest=base-sum(p)
    zahlen2=zahlen-set(p)
    if rest not in zahlen2: continue
    for i in range(pos+1,N-1):
      quadrat[pos+i*N]=p[i-pos-1]
    quadrat[pos+N*(N-1)]=rest
    zeilen(pos+1,quadrat,zahlen2-{rest})


start=time.perf_counter()
N=4
lösungen = []
summe = (N**3+N)//2

zeilen(0,[0]*N*N,set(range(1,N*N+1)))
print(f'{len(lösungen):,} mögliche Lösungen für ein {N}x{N} magisches Quadrat mit der Summe von {summe} ({time.perf_counter()-start:.3f} Sek.)')