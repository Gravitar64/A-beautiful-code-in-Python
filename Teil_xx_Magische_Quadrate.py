import time
import itertools


def print_quadrat():
  for i, z in enumerate(quadrat, start=1):
    print(f'{z:>2} ', end='')
    if not i % N: print()
  print()


def zeilen(pos, zahlen):
  basis = summe - sum(quadrat[pos*N:pos*N+pos])
  for zeile in itertools.permutations(zahlen, N-1-pos):
    rest = basis - sum(zeile)
    zahlen2 = zahlen - set(zeile)
    if rest not in zahlen2: continue
    quadrat[pos*N+pos:pos*N+N] = list(zeile)+[rest]
    if N-2 == pos and sum(quadrat[i*N+N-1-i] for i in range(N)) != summe: return
    spalten(pos, zahlen2-{rest})


def spalten(pos, zahlen):
  if not zahlen:
    if sum(quadrat[i*N+i] for i in range(N)) == summe: pass
    return

  basis = summe - sum(quadrat[i*N+pos] for i in range(pos+1))
  for spalte in itertools.permutations(zahlen, N-2-pos):
    rest = basis - sum(spalte)
    zahlen2 = zahlen - set(spalte)
    if rest not in zahlen2: continue
    for i, z in enumerate(list(spalte)+[rest], start=pos+1):
      quadrat[i*N+pos] = z
    zeilen(pos+1, zahlen2-{rest})


start = time.perf_counter()
N = 4
summe = (N**3+N)//2
quadrat = [0] * N**2
zahlen = set(range(1, N**2+1))
zeilen(0, zahlen)

print_quadrat()
print(time.perf_counter()-start)
