import random as rnd
from time import perf_counter as pfc

start = pfc()
gew_ow = gew_mw = 0
anz_simulationen = 1_000_000
türen = {0,1,2}

for _ in range(anz_simulationen):
  auto, wahl  = rnd.randrange(3), rnd.randrange(3)
  if auto == wahl:
    gew_ow += 1
  ziege = (türen - {auto, wahl}).pop()
  wahl  = (türen - {wahl, ziege}).pop()
  if auto == wahl:
    gew_mw += 1

print(f'{anz_simulationen:,.0f} Simulationen in {pfc()-start:.2f} Sek.')
print(f'Gewinnquote ohne Wechsel = {gew_ow/anz_simulationen*100:.2f} %')    
print(f'Gewinnquote mit Wechsel  = {gew_mw/anz_simulationen*100:.2f} %')