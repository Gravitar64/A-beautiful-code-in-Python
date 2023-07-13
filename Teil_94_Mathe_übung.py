import random
import time
import readchar

input('Spiel starten?')
punkte = 0
start = time.perf_counter()
for _ in range(10):
  a,b,op = random.randint(1,20), random.randint(1,20), random.choice('+ - * /'.split())
  e = eval(f'{a} {op} {b}')
  falsch = random.random() > 0.5
  if falsch: e += random.randint(1,10) if random.random() > 0.5 else -random.randint(1,10)
  print(f'{a} {op} {b} = {e}')
  print('Richtig/Falsch (r/<any key>)? ', end='')
  antwort = readchar.readchar()
  if antwort == 'r' and not falsch or antwort != 'r' and falsch: 
    punkte += 1
    print(f'{antwort} = KORREKT')
  else:
    print(f'{antwort} = FALSCH')  

print(punkte)
print(time.perf_counter()-start+20*(10-punkte))