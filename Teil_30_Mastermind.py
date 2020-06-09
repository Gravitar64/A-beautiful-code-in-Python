from itertools import product
import random as rnd 

GEHEIM = rnd.choice(list(product(range(1,7), repeat = 4)))
erg = ''

def treffer(v,g):
  farbe_position = sum(a==b for a,b in zip(v,g))
  farbe = sum(min(v.count(a), g.count(a)) for a in set(g)) - farbe_position
  return '+'*farbe_position + 'o'*farbe

anz = 0
while erg != '++++':
  anz += 1
  versuch = list(map(int,input('Ihr Versuch: ').split()))
  print(erg := treffer(versuch, GEHEIM))

print(f'Lösung in {anz} Versuchen gefunden!')