import math
import random as rnd

breite_blatt = 800
breite_spalte = breite_blatt / 40
länge = breite_spalte / 6 * 5

streichhölzer_gesamt, streichhölzer_kreuzen = 5_000_000, 0
for _ in range(streichhölzer_gesamt):
  x = rnd.randint(0, breite_blatt)
  winkel = rnd.uniform(0, math.tau)
  x1 = x + länge * math.cos(winkel)
  streichhölzer_kreuzen += x // breite_spalte != x1 // breite_spalte

print(2 * streichhölzer_gesamt * länge / (streichhölzer_kreuzen * breite_spalte))
