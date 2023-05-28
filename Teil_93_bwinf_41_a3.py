import itertools
import requests


def keine_permutation(s1, s2):
  def verteilung_zahlen(s): return set(list(s).count(i) for i in range(1, 10))
  return verteilung_zahlen(s1.values()) != verteilung_zahlen(s2.values())


def print_sudoku(sod):
  for z, s in itertools.product(range(9), repeat=2):
    if s == 0: print()
    print(sod.get((z,s), '0'), end='')
  print()


def rotiere(sod):
  return {(s,8-z): sod[z,s] for z,s in sod}
  

def blockspalte(sod, a, b):
  return [((z,a), (z,b)) for z,s in sod if s in range(a*3,a*3+3)]


def blockzeile(a, b):
  return [(i % 9 + i//9*9 + a*3*9, i % 9 + i//9*9 + b*3*9)
          for i in range(27)]


def zeile(sod, z1, z2):
  return [((z1,s), (z2,s)) for z,s in sod if z == z1]


def spalte(sod, s1, s2):
  return [((z,s1), (z,s2)) for z,s in sod if s == s1]


def permutate(sod, perm):
  buffer = sod.copy()
  for a, b in perm:
    buffer[a], buffer[b] = buffer[b], buffer[a]
  return buffer

def datei_einlesen(datei):
  dateiinhalt = requests.get(datei).text[1:]
  sudokus = dateiinhalt.split('\r\n\r\n')
  ret = []
  for sudoku in sudokus:
    s_dict = {}
    for z,zeile in enumerate(sudoku.split('\r\n')):
      for s,n in enumerate(zeile.split()):
        if n == '0': continue
        s_dict[(z,s)] = int(n)
    ret.append(s_dict)    
  return ret


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/sudoku'
for i in range(5):
  datei = f'{URL}{i}.txt'
  print(datei)
  s1, s2 = datei_einlesen(datei)
  if keine_permutation(s1, s2):
    print('Keine Permutation möglich')
    continue
  buff = rotiere(s1)
  print_sudoku(s1)
  print_sudoku(buff)
  # p = []
  # for a, b in itertools.product(range(3), repeat=2):
  #   p += blockspalte(a, b)
  #   for c, d in itertools.product(range(3), repeat=2):
  #     p += blockzeile(c, d)
  #     for e, f in itertools.product(range(9), repeat=2):
  #       p += spalte(e, f)
  #       for g, h in itertools.product(range(9), repeat=2):
  #         p += zeile(g, h)
  #         buffer = permutate(s1, p)
  #         for h in range(2):
  #           if h == 1: buffer = rotiere(buffer)
  #           if buffer == s2: print('gefunden')
            
