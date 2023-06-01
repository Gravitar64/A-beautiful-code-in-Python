import itertools as itt
import re
import requests
import time

def i2koord(i):
  zeile = i // 9
  spalte = i % 9
  blockzeile = zeile // 3
  blockspalte = spalte // 3
  return zeile, spalte, blockzeile, blockspalte


def datei_einlesen(datei):
  inhalt = re.findall('\d+', requests.get(datei).text)
  s = {i2koord(int(i)):int(n) for i,n in enumerate(inhalt[:81]) if n != '0'}
  e = {i2koord(int(i)):int(n) for i,n in enumerate(inhalt[81:]) if n != '0'}
  return s,e
  
  
def permutation_möglich(s1,s2):
  zahlenverteilung = lambda s: {list(s.values()).count(i) for i in range(1,10)}
  return zahlenverteilung(s1) == zahlenverteilung(s2)
  

def prüfe_permutationen(s,e):
  for p1 in perm_blöcke:
    s1 = mut_blockspalten(s, p1)
    for p2 in perm_blöcke:
      s2 = mut_blockzeilen(s1, p2)
      for p3 in perm_zeilen:
        s3 = mut_spalten(s2, p3)  
        for p4 in perm_zeilen:
          s4 = mut_zeilen(s3, p4)
          if s4 == e:
            return p1,p2,p3,p4
            

  
def mut_blockspalten(s,p):
  ret = s.copy()
  for a,b in enumerate(p):
    if a == b: continue
    for ze,sp,bze,bsp in s:
      if bsp != a: continue
      ret[ze,b*3+sp%3,bze,b] = s[ze,sp,bze,bsp]
  return ret


def mut_blockzeilen(s,p):
  ret = s.copy()
  for a,b in enumerate(p):
    if a == b: continue
    for ze,sp,bze,bsp in s:
      if bze != a: continue
      ret[b*3+ze%3,sp,b,bsp] = s[ze,sp,bze,bsp]
  return ret
  

def mut_zeilen(s,p):
  ret = s.copy()
  for a,b in enumerate(p):
    if a == b: continue
    for ze,sp,bze,bsp in s:
      if ze != a: continue
      ret[b,sp,b//3,bsp] = s[ze,sp,bze,bsp]
  return ret


def mut_spalten(s,p):
  ret = s.copy()
  for a,b in enumerate(p):
    if a == b: continue
    for ze,sp,bze,bsp in s:
      if sp != a: continue
      ret[ze,b,bze,b//3] = s[ze,sp,bze,bsp]
  return ret
  
  
                  
  
perm_blöcke = list(itt.permutations(range(3)))
perm_zeilen = [p1+p2+p3 for p1 in perm_blöcke for p2 in itt.permutations(range(3,6)) for p3 in itt.permutations(range(6,9))]
  
    


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/sudoku'
for i in range(5):
  datei = f'{URL}{i}.txt'
  print(datei)
  start = time.perf_counter()
  s,e = datei_einlesen(datei)
  if not permutation_möglich(s, e):
    print('Keine Permutation möglich')
    continue
  print(prüfe_permutationen(s, e))
  print(time.perf_counter() - start)
  
  
  
