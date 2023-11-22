import math

import time

def chinesischer_restsatz(bedingungen):
  x=0
  gesamt_produkt = math.prod(e[1] for e in bedingungen)
  for rest, teiler in bedingungen:
    mul = 1
    produkt = gesamt_produkt // teiler
    while (mul*produkt)%teiler != rest: mul += 1
    x += mul*produkt
  return x % gesamt_produkt  



start = time.perf_counter()
bedingungen = [(1,3), (0,7), (1,5)]
print(chinesischer_restsatz(bedingungen))
print(f'Ermittelt in {time.perf_counter()-start:.5f} Sek.')