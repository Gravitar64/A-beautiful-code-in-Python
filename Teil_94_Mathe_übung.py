import random
import time
import readchar


def delta():
  if random.choice([True, False]):
    return random.randint(-5,5)
  return 0


def r():
 return random.randint(1,10)


readchar.readchar()
start = time.perf_counter()
anz = fehler = 10

for _ in range(anz):
  a,b,op = r(), r(), random.choice('+ - *'.split())
  e = eval(f'{a} {op} {b}') + (d := delta()) 
  print(f'{a} {op} {b} = {e} ')
  antwort = readchar.readchar()
  if antwort == 'r' and d or antwort != 'r' and not d: continue 
  fehler -= 1
   
zeit = time.perf_counter()-start
print(f'{zeit:.2f} Sek. + Fehler = {fehler} x 10 Sek. = {zeit+fehler*10:.2f}')