import random as rnd

gew_ow = gew_mw = 0
sim = 1_000_000
türen = {0,1,2}

for _ in range(sim):
  auto, wahl = rnd.randrange(3), rnd.randrange(3)
  if auto == wahl:
    gew_ow += 1
  ziege = (türen - {auto, wahl}).pop()
  wechsel = (türen - {wahl, ziege}).pop()
  if auto == wechsel:
    gew_mw += 1
    
print(f'Gewinnwahrscheinlichkeit ohne Wechsel = {gew_ow/sim*100:.2f} %')
print(f'Gewinnwahrscheinlichkeit mit  Wechsel = {gew_mw/sim*100:.2f} %')