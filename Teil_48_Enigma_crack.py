import Teil_44_Enigma as eni
from itertools import groupby, permutations, product
from collections import defaultdict
import string
import time
import pickle
verschlüsselt = 'TLZHWCKAGXNJJUIEHKMGFE'
crib = 'WUEBYYNULLSEQSNULLNULL'


def brute_force(verschlüsselt, crib):
  for ukw in (1,2,3):
    for walz in permutations(range(1, 6), 3):
      print(ukw, walz)
      for walzpos in product(string.ascii_uppercase, repeat=3):
        walzpos = ''.join(walzpos)
        e.setup(ukw, walz, walzpos, [1, 1, 1], "")
        entschlüsselt = eni.umwandeln(e, verschlüsselt, crib)
        if crib in entschlüsselt:
          print('CRACKED!!!!!')
          print(walz, walzpos)
          return

def brute_force2(verschlüsselt, crib):
  for i, id in enumerate(nachschlagTabelle):
    entschlüsselt = umwandeln2(id, i, verschlüsselt,  crib)
    if crib in entschlüsselt:
      print('CRACKED!!!!!')
      print(entschlüsselt)
      print(id)
      return

def umwandeln2(id, i, text, crib=''):
  text_u = ''
  for n,c in enumerate(text):
    c = ord(c)-65
    text_u += nachschlagTabelle[id][c]
    if crib and text_u[-1] != crib[n]:
      return ''
    i += 1
    id = nachschlag_i[i]
  return text_u

def set2id(ukw,walz,walzpos):
  s = str(ukw)
  for w in walz:
    s += str(w)
  return s + ''.join(walzpos)

def baue_nachschlag_tabelle():
  nachschlag_tabelle = defaultdict(str)
  for buchst in string.ascii_uppercase:
    for ukw in (1,2,3):
      for walz in permutations(range(1,6), 3):
        print(buchst,ukw,walz)
        walzpos = 'AAA'
        e.setup(ukw, walz, walzpos, [1,1,1], "")
        while True:
          nachschlag_tabelle[set2id(ukw,walz,walzpos)] += eni.umwandeln(e,buchst)
          walzpos = e.walzen_positionen
          if walzpos == 'AAA': 
            break
  with open('Teil_xx_Enigma_lookup.pkl','wb') as f:
    pickle.dump(nachschlag_tabelle, f)
          

def crib_positionen(verschlüsselt, crib):
  pos = []
  for offset in range(len(verschlüsselt)-len(crib)+1):
    if all([verschlüsselt[offset+i] != crib[i] for i in range(len(crib))]):
      pos.append(offset)
  return pos


def get_graph(v, c, offset):
  g = defaultdict(set)
  for i in range(len(c)):
    g[v[i+offset]].add((c[i], i))
    g[c[i]].add((v[i+offset],i))
  return g


def dfs(graph, start, end):
  fringe = [(start, [])]
  while fringe:
    state, path = fringe.pop()
    if path and state == end:
      yield path
      continue
    for next_state in graph[state]:
      if next_state[0] in path:
        continue
      fringe.append((next_state[0], path+[next_state[0]]))




e = eni.Enigma()
e.setup(2,[1,2,3],'CAT',[1,1,1],"")

for p in crib_positionen(verschlüsselt, crib):
  print(verschlüsselt)
  print(crib)
  g = get_graph(verschlüsselt, crib, p)
  cycles = [tuple([node]+path) for node in g for path in dfs(g, node, node)]
for c in cycles:
  if len(c) < 4:
    continue
  print(c)
#baue_nachschlag_tabelle()

with open('Teil_xx_Enigma_lookup.pkl','rb') as f:
  nachschlagTabelle = pickle.load(f)

print(len(nachschlagTabelle))  

nachschlag_id, nachschlag_i = {}, {}
for i,id in enumerate(nachschlagTabelle.keys()):
  nachschlag_i[i] = id
  nachschlag_id[id] = i


# time_start = time.perf_counter()
# print(umwandeln2('WETTERBERICHTXDERXNEUENXSAISON',2,[1,2,3],'CAT'))
# print(time.perf_counter()-time_start)

# time_start = time.perf_counter()
# print(eni.umwandeln(e,"WETTERBERICHTXDERXNEUENXSAISON"))  
# print(time.perf_counter()-time_start)

# for pos in list(nachschlagTabelle.keys())[:16901]:
#   print(pos)

# time_start = time.perf_counter()
# brute_force(verschlüsselt, crib)
# print(time.perf_counter()-time_start)

time_start = time.perf_counter()
brute_force2(verschlüsselt, crib)
print(time.perf_counter()-time_start)