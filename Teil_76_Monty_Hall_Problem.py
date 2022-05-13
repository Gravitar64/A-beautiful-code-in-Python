import random as rnd
from time import perf_counter as pfc

start = pfc()
gew_ow = gew_mw = 0
sim = 1_000_000
türen = {0,1,2}

for _ in range(sim):
  auto = rnd.randrange(3)
  wahl = rnd.randrange(3)
  if auto == wahl:
    gew_ow += 1
  ziege = (türen - {auto, wahl}).pop()
  wahl  = (türen - {wahl, ziege}).pop()
  if auto == wahl:
    gew_mw += 1

print(f'{sim:,.0f} Simulationen in {pfc()-start:.2f} Sek.')
print(f'Gewinnwahrscheinlichkeit ohne Wechsel = {gew_ow/sim*100:.2f} %')
print(f'Gewinnwahrscheinlichkeit mit Wechsel  = {gew_mw/sim*100:.2f} %')