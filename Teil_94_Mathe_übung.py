import random
import time
import readchar


def fifty():
  return random.choice([True, False])


def r(s,e):
 return random.randint(s,e)


readchar.readchar()
fehler = 10
start = time.perf_counter()

for _ in range(10):
  a,b,op, delta = r(1,10), r(1,10), random.choice('+ - *'.split()), r(1,5)
  e = eval(f'{a} {op} {b}') 
  if falsch := fifty(): e += delta if fifty() else -delta
  print(f'{a} {op} {b} = {e} ')
  antwort = readchar.readchar()
  if antwort == 'r' and falsch or antwort != 'r' and not falsch: continue 
  fehler -= 1
   

print(f'{fehler} Fehler')
print(time.perf_counter()-start+20*fehler)