import itertools as itt
import re
import requests
import time


def mut_zeilen(p):
  return {a*9+i:b*9+i for a,b in enumerate(p) for i in range(9) if a != b}


def mut_spalten(p):
  return {i*9+a:i*9+b for a,b in enumerate(p) for i in range(9) if a != b}
  

def mut_blockspalte(p):
  return {i//3*9+i%3+a*3:i//3*9+i%3+b*3 for a,b in enumerate(p)
          for i in range(27)}
  

def mut_blockzeile(p):
  return {i%9+i//9*9+a*3*9:i%9+i//9*9+b*3*9 for a,b in enumerate(p)
          for i in range(27)}

  
def rotiere(s):
  ret = s.copy()
  for ze, sp in perm_rotation:
    ret[ze*9+sp] = s[(9-sp-1)*9+ze]
  return ret


def mutate(p):
  ret = s.copy()
  for von,zu in p.items():
    ret[zu] = s[von]
  return ret  
  

def konsolidiere(k1,k2):
  ret = {}
  for von,zu in k1.items():
    if zu in k2:
      ret[von] = k2[zu]
      del k2[zu]
    else:
      ret[von] = zu
  ret.update(k2)
  return ret    
        

def permutation_möglich():
  def verteilung_zahlen(s): return set(s.count(str(i)) for i in range(1, 10))
  return verteilung_zahlen(s) == verteilung_zahlen(e)


def prüfe_permutationen():
  for p1 in perm_blöcke:
    s1 = mut_blockspalte(p1)
    for p2 in perm_blöcke:
      s2 = mut_blockzeile(p2)
      k1 = konsolidiere(s1,s2)
      for p3 in perm_zeilen:
        s3 = mut_spalten(p3)
        k2 = konsolidiere(k1,s3)
        for p4 in perm_zeilen:
          s4 = mut_zeilen(p4)
          k3 = konsolidiere(k2,s4)
          buffer = mutate(k3)
          for rot in [False, True]:
            buffer = rotiere(buffer) if rot else buffer
            if buffer == e or (mapping := umbenennen(buffer, e)):
              return p1, p2, p3, p4, rot, mapping


def umbenennen(s1, s2):
  mapping = {}
  for a, b in zip(s1, s2):
    if a == b == '0': continue
    if a in mapping and mapping[a] != b: return False
    mapping[a] = b
  return mapping


def print_perms(perms):
  for perm, art in zip(perms, 'Blockspalte Blockzeile Spalte Zeile Rot Umb'.split()):
    if art == 'Rot':
      print(f'Rotation = {perm}')
    elif art == 'Umb':
      if not perm: continue
      print(f'Umbenennen: ', end='')
      for i in range(1, 10):
        if perm[str(i)] == str(i): continue
        print(f'{i}>{perm[str(i)]}, ', end='')
      print()
    else:
      print(f'{art}: ', end='')
      for a, b in enumerate(perm):
        if a == b:
          continue
        print(f'{int(a)+1}>{int(b)+1}, ', end='')
      print()


perm_blöcke = list(itt.permutations(range(3)))
perm_zeilen = [p1+p2+p3 for p1 in perm_blöcke for p2 in itt.permutations(
    range(3, 6)) for p3 in itt.permutations(range(6, 9))]
perm_rotation = list(itt.product(range(9), repeat=2))


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/sudoku'
for i in range(5):
  datei = f'{URL}{i}.txt'
  print(datei)
  start = time.perf_counter()
  inhalt = re.findall('\d+', requests.get(datei).text)
  s, e = inhalt[:81], inhalt[81:]
  if not permutation_möglich():
    print('Keine Permutation möglich')
    print(time.perf_counter()-start)
    continue
  if (perms := prüfe_permutationen()):
    print_perms(perms)
    print(time.perf_counter()-start)
