import requests
import re
import itertools


def keine_permutation(s1, s2):
  def verteilung_zahlen(s): return set(s.count(str(i)) for i in range(1, 10))
  return verteilung_zahlen(s1) != verteilung_zahlen(s2)


def print_sudoku(s):
  for zeile, spalte in itertools.product(range(9), repeat=2):
    if spalte == 0:
      print()
    print(s[zeile*9+spalte]+" ", end='')
  print()


def rotiere(s):
  ret = s.copy()
  for i in range(9):
    for j in range(9):
      ret[i*9+j] = s[(9-j-1)*9+i]
  return ret    

def blockspalte(a, b):
  return [(i // 3 * 9 + i % 3 + (a * 3),  i // 3 * 9 + i % 3 + (b * 3))
          for i in range(27)]


def blockzeile(a, b):
  return [(i % 9 + i//9*9 + a*3*9, i % 9 + i//9*9 + b*3*9)
          for i in range(27)]


def zeile(a, b):
  return [(i+a*9, i+b*9) for i in range(9)]


def spalte(a, b):
  return [(i*9+a, i*9+b) for i in range(9)]


def permutate(s, perm):
  buffer = s.copy()
  for i, i2 in perm:
    buffer[i], buffer[i2] = buffer[i2], buffer[i]
  return buffer




URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/sudoku'
for i in range(5):
  datei = f'{URL}{i}.txt'
  print(datei)
  sudokus = re.findall('\d+', requests.get(datei).text)
  s1, s2 = sudokus[:81], sudokus[81:]
  if keine_permutation(s1, s2):
    print('Keine Permutation möglich')
    continue
  p = []
  for a, b in itertools.product(range(3), repeat=2):
    p += blockspalte(a, b)
    for c, d in itertools.product(range(3), repeat=2):
      p += blockzeile(c, d)
      for e, f in itertools.product(range(9), repeat=2):
        p += spalte(e, f)
        for g, h in itertools.product(range(9), repeat=2):
          p += zeile(g, h)
          buffer = permutate(s1, p)
          for h in range(2):
            if h == 1: buffer = rotiere(buffer)
            if buffer == s2: print('gefunden')
            
