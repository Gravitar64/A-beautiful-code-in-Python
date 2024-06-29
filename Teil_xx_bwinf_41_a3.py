import itertools as itt
import re
import requests
import time


def mut_zeilen(s, p):
  s1 = s.copy()
  for zei_von, zei_zu in enumerate(p):
    if zei_von == zei_zu:
      continue
    for sp in range(9):
      s1[zei_zu * 9 + sp] = s[zei_von * 9 + sp]
  return s1


def mut_spalten(s, p):
  s1 = s.copy()
  for spa_von, spa_zu in enumerate(p):
    if spa_von == spa_zu:
      continue
    for ze in range(9):
      s1[ze * 9 + spa_zu] = s[ze * 9 + spa_von]
  return s1


def mut_blockspalte(s, p):
  s1 = s.copy()
  for bsp_von, bsp_zu in enumerate(p):
    if bsp_von == bsp_zu:
      continue
    for i in range(27):
      s1[i // 3 * 9 + i % 3 + (bsp_zu * 3)] = s[i //
                                                3 * 9 + i % 3 + (bsp_von * 3)]
  return s1


def mut_blockzeile(s, p):
  s1 = s.copy()
  for bze_von, bze_zu in enumerate(p):
    if bze_von == bze_zu:
      continue
    for i in range(27):
      s1[i % 9 + i // 9 * 9 + bze_zu * 3 * 9] = s[i %
                                                  9 + i // 9 * 9 + bze_von * 3 * 9]
  return s1


def rotiere(s):
  ret = s.copy()
  for ze, sp in perm_rotation:
    ret[ze * 9 + sp] = s[(9 - sp - 1) * 9 + ze]
  return ret


def permutation_möglich():
  def verteilung_zahlen(s): return set(s.count(str(i)) for i in range(1, 10))
  return verteilung_zahlen(s) == verteilung_zahlen(e)


def prüfe_permutationen():
  for p1 in perm_blöcke:
    s1 = mut_blockspalte(s, p1)
    for p2 in perm_blöcke:
      s2 = mut_blockzeile(s1, p2)
      for p3 in perm_zeilen:
        s3 = mut_spalten(s2, p3)
        for p4 in perm_zeilen:
          s4 = mut_zeilen(s3, p4)
          for rot in [False, True]:
            s5 = rotiere(s4) if rot else s4
            if s5 == e or (mapping := umbenennen(s5, e)):
              return p1, p2, p3, p4, rot, mapping


def umbenennen(s1, s2):
  mapping = {}
  for a, b in zip(s1, s2):
    if a == b == '0':
      continue
    if a in mapping and mapping[a] != b:
      return False
    mapping[a] = b
  return mapping


def print_perms(perms):
  for perm, art in zip(perms, 'Blockspalte Blockzeile Spalte Zeile Rot Umb'.split()):
    if art == 'Rot':
      print(f'Rotation   : {perm}')
    elif art == 'Umb':
      if not perm:
        continue
      print(f'Umbenennen : ', end='')
      for i in range(1, 10):
        if perm[str(i)] == str(i):
          continue
        print(f'{i}>{perm[str(i)]}, ', end='')
      print()
    else:
      print(f'{art:<11}: ', end='')
      for a, b in enumerate(perm):
        if a == b:
          continue
        print(f'{int(a)+1}>{int(b)+1}, ', end='')
      print()


perm_blöcke = list(itt.permutations(range(3)))
perm_zeilen = [p1 + p2 + p3 for p1 in perm_blöcke
               for p2 in itt.permutations(range(3, 6))
               for p3 in itt.permutations(range(6, 9))]
perm_rotation = list(itt.product(range(9), repeat=2))


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/sudoku'
for i in range(5):
  datei = f'{URL}{i}.txt'
  print(datei)
  start = time.perf_counter()
  inhalt = re.findall(r'\d+', requests.get(datei).text)
  s, e = inhalt[:81], inhalt[81:]
  if not permutation_möglich():
    print('Keine Permutation möglich')
  elif (perms := prüfe_permutationen()):
    print_perms(perms)
  print(f'Ermittelt in {time.perf_counter()-start:.3f} Sek.')
  print()
