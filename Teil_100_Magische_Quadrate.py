import itertools


def anz():
  anz.zähler += 1


def gen_zeilen(nr, zahlen):
  rest1 = magische_summe - sum(quadrat[nr * N:nr * N + nr])
  for zeile in itertools.permutations(zahlen, N - 1 - nr):
    rest2 = rest1 - sum(zeile)
    zahlen2 = zahlen - set(zeile)
    if rest2 not in zahlen2: continue
    quadrat[nr * N + nr:nr * N + N] = list(zeile) + [rest2]
    gen_spalten(nr, zahlen2 - {rest2})


def check():
  if sum(quadrat[i] for i in DIAG1) != magische_summe: return False
  if sum(quadrat[i] for i in DIAG2) != magische_summe: return False
  return True


def print_quadrat():
  for i in range(N * N):
    if not i % N: print()
    print(f'{quadrat[i]:>2} ', end='')
  print(f'\nNr. {anz.zähler} \n')


def gen_spalten(nr, zahlen):
  if not zahlen:
    if check():
      anz()
      print_quadrat()
    return

  rest1 = magische_summe - sum(quadrat[i * N + nr] for i in range(nr + 1))
  for spalte in itertools.permutations(zahlen, N - 2 - nr):
    rest2 = rest1 - sum(spalte)
    zahlen2 = zahlen - set(spalte)
    if rest2 not in zahlen2: continue
    for i, z in enumerate(list(spalte) + [rest2], start=nr + 1):
      quadrat[i * N + nr] = z
    gen_zeilen(nr + 1, zahlen2 - {rest2})


N = 5
anz.zähler = 0
magische_summe = (N**3 + N) // 2
quadrat = [0] * N * N
DIAG1 = {i * N + i for i in range(N)}
DIAG2 = {i * N + N - i - 1 for i in range(N)}

gen_zeilen(0, set(range(1, N * N + 1)))