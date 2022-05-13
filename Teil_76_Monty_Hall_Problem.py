import random as rnd
from time import perf_counter as pfc

start = pfc()
gew_ohne_wechsel = gew_mit_wechsel = 0
anz_simulationen = 1_000_000

for _ in range(anz_simulationen):
  auto = rnd.randrange(3)
  wahl = rnd.randrange(3)
  if auto == wahl:
    gew_ohne_wechsel += 1
  ziege = ({0, 1, 2} - {auto, wahl}).pop()
  wahl  = ({0, 1, 2} - {wahl, ziege}).pop()
  if auto == wahl:
    gew_mit_wechsel += 1


print(f'{anz_simulationen:,.0f} Simulationen in {pfc()-start:.2f} Sek.')
print(f'Gewinnwahrscheinlichkeit ohne Wechsel = {gew_ohne_wechsel/anz_simulationen*100:.2f} %')
print(f'Gewinnwahrscheinlichkeit mit Wechsel  = {gew_mit_wechsel/anz_simulationen*100:.2f} %')
