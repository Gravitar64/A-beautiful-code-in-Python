import random as rnd

gew_ow = gew_mw = gew_zufMod = 0
sim = 1_000_000
türen = {0, 1, 2}

for _ in range(sim):
  auto, wahl, moderator = rnd.randrange(3), rnd.randrange(3), rnd.randrange(3)
  if auto == wahl:
    gew_ow += 1
  ziege = (türen - {auto, wahl}).pop()
  wechsel = (türen - {wahl, ziege}).pop()
  if auto == wechsel:
    gew_mw += 1
  if auto == moderator:
    gew_zufMod += 1
  else:
    wechsel = (türen - {wahl, moderator}).pop()
    if wechsel == auto:
      gew_zufMod += 1


print(f'Gewinnwahrscheinlichkeit ohne Wechsel = {gew_ow/sim*100:.2f} %')
print(f'Gewinnwahrscheinlichkeit mit Wechsel (Moderator zeigt Ziege)    = {gew_mw/sim*100:.2f} %')
print(f'Gewinnwahrscheinlichkeit mit Wechsel (Moderator wählt zufällig) = {gew_zufMod/sim*100:.2f} %')
