import itertools
import re
import requests
import time


def zeilen():
  ret = []
  for p1 in itertools.permutations(range(3)):
    for p2 in itertools.permutations(range(3, 6)):
      for p3 in itertools.permutations(range(6, 9)):
        ret.append(p1+p2+p3)
  return ret


def blöcke():
  ret = []
  for p1 in itertools.permutations(range(3), 3):
    ret.append(p1)
  return ret


def perm_zeilen(s, p):
  s1 = s.copy()
  for a,b in enumerate(p):
    if a == b: continue
    for i in range(9):
      s1[i+b*9] = s[i+a*9]
  return s1


def perm_spalten(s, p):
  s1 = s.copy()
  for a,b in enumerate(p):
    if a == b:  continue
    for i in range(9):
      s1[i*9+b] = s[i*9+a]
  return s1


def per_blockspalte(s, p):
  s1 = s.copy()
  for a, b in enumerate(p):
    if a == b:
      continue
    for i in range(27):
      s1[i // 3 * 9 + i % 3 + (a * 3)] = s[i // 3 * 9 + i % 3 + (b * 3)]
  return s1


def per_blockzeile(s, p):
  s1 = s.copy()
  for a, b in enumerate(p):
    if a == b:
      continue
    for i in range(27):
      s1[i % 9 + i//9*9 + a*3*9] = s[i % 9 + i//9*9 + b*3*9]
  return s1


def rotiere(s):
  ret = s.copy()
  for i,j in itertools.product(range(9),repeat=2):
    ret[i*9+j] = s[(9-j-1)*9+i]
  return ret


def keine_permutation(s1, s2):
  def verteilung_zahlen(s): return set(s.count(str(i)) for i in range(1, 10))
  return verteilung_zahlen(s1) != verteilung_zahlen(s2)


def permutation_möglich(s):
  for p1 in blöcke():
    s1 = per_blockspalte(s, p1)
    for p2 in blöcke():
      s2 = per_blockzeile(s1, p2)
      for p3 in zeilen():
        s3 = perm_spalten(s2, p3)
        for p4 in zeilen():
          s4 = perm_zeilen(s3, p4)
          for rot in [False, True]:
            s5 = rotiere(s4) if rot else s4
            if s5 == e or (mapping := umbenennen(s5, e)):
              return p1, p2, p3, p4, rot, mapping
              
              
              


def umbenennen(s1, s2):
  mapping = {}
  for a, b in zip(s1, s2):
    if a == b == '0':  continue
    if a in mapping and mapping[a] != b:return False
    mapping[a] = b
  return mapping


def print_perms(perms):
  for perm, art in zip(perms, 'Bl_sp Bl_ze Sp Ze Rot Umb'.split()):
    if art == 'Rot':
      print(f'Rotation = {perm}')
    elif art == 'Umb':
      if not perm: continue
      print(f'Umbenennen: ', end='')
      for i in range(1,10):
        if perm[str(i)] == str(i):  continue
        print(f'{i}>{perm[str(i)]}, ', end='')
      print()
    else:
      print(f'{art}: ', end='')
      for a, b in enumerate(perm):
        if a == b: continue
        print(f'{int(a)+1}>{int(b)+1}, ', end='')
      print()

      
def print_sudoku(sod):
  for i in range(81):
    if not i % 9: print()
    print(f'{sod[i]} ', end='')
  print()      


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/sudoku'
for i in range(5):
  datei = f'{URL}{i}.txt'
  print(datei)
  start = time.perf_counter()
  inhalt = re.findall('\d+', requests.get(datei).text)
  s, e = inhalt[:81], inhalt[81:]
  if keine_permutation(s, e):
    print('Keine Permutation möglich')
    print(time.perf_counter()-start)
    continue
  if (perms := permutation_möglich(s)):
    print_perms(perms)
    print(time.perf_counter()-start)
