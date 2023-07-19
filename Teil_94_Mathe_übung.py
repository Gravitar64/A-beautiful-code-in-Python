import random as rnd
import time
import readchar


delta = lambda: rnd.randint(-5, 5) if rnd.choice([1, 0]) else 0
r = lambda: rnd.randint(1, 10)


readchar.readchar()
start = time.perf_counter()
anz = fehler = 10

for _ in range(anz):
  a, b, op, d = r(), r(), rnd.choice('+ - *'.split()), delta()
  e = eval(f'{a} {op} {b}') + d
  print(f'{a} {op} {b} = {e} ')
  antwort = readchar.readchar()
  if antwort == 'r' and d or antwort != 'r' and not d: continue
  fehler -= 1

z1 = time.perf_counter()-start
z2 = z1 + fehler * 10
print(f'{z1:.2f} Sek. + Fehler = {fehler} x 10 Sek. = {z2:.2f}')