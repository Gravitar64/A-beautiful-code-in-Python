import time,itertools

def zähler():
  zähler.zähler += 1
  return zähler.zähler


def print_quadrat():
  print(f'Lösung: {zähler()} nach {time.perf_counter()-start:.2f} Sek.')
  for i,z in enumerate(quadrat):
    if i > 0 and not i%N: print()
    print(f'{z:>2} ',end='')
  print('\n') 


def check():
  if sum(quadrat[i*N+i] for i in range(N)) != summe: return False
  if sum(quadrat[i*N+N-i-1] for i in range(N)) != summe: return False
  return True


def zeilen(nr,zahlen):
  base = summe - sum(quadrat[nr*N:nr*N+nr])
  for p in itertools.permutations(zahlen,N-nr-1):
    rest = base - sum(p)
    zahlen2 = zahlen - set(p)
    if rest not in zahlen2: continue
    quadrat[nr*N+nr:nr*N+N] = list(p)+[rest]
    spalten(nr,zahlen2-{rest})


def spalten(nr, zahlen):
  if not zahlen:
    if check(): print_quadrat()
    return  
  
  base = summe - sum(quadrat[i*N+nr] for i in range(nr+1))
  for p in itertools.permutations(zahlen,N-nr-2):
    rest = base - sum(p)
    zahlen2 = zahlen - set(p)
    if rest not in zahlen2: continue
    for i,n in enumerate(list(p)+[rest],start=nr+1):
      quadrat[i*N+nr] = n
    zeilen(nr+1,zahlen2-{rest})


start = time.perf_counter()
N = 4
zähler.zähler = 0  
summe = (N**3+N)//2
quadrat = [0]*N**2
zeilen(0,set(range(1,N**2+1)))