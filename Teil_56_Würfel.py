# Bedingte Wahrscheinlichkeit
#
# In Anlehnung an Prof. Edmund Weitz, HAW Hamburg
# https://www.youtube.com/watch?v=ePulos20frg

aufgabe = """
Aufgabenstellung:

Wir haben 3 Würfel mit der Augenzahl 1-6

Welches der folgenden Ergebnisse hat die höchste Wahrscheinlichkeit?

a = Die Gesamtaugenzahl ist größer als 9
b = Die Gesamtaugenzahl ist kleiner als 9
c = Mindestens 2 Würfel haben die gleiche Augenzahl

"""
print(aufgabe)

from itertools import product

def wahrscheinlichkeit(bedingung):
  mächtigkeit = sum(map(bedingung, omega))
  return mächtigkeit / len(omega) * 100

würfel = 3
omega = list(product(range(1,7), repeat = würfel))

a = wahrscheinlichkeit(lambda wurf: sum(wurf) > 9)
b = wahrscheinlichkeit(lambda wurf: sum(wurf) < 9)
c = wahrscheinlichkeit(lambda wurf: len(set(wurf)) < 3)

print(f'Wahrscheinlichkeit a) = {a:0.1f}%')
print(f'Wahrscheinlichkeit b) = {b:0.1f}%')
print(f'Wahrscheinlichkeit c) = {c:0.1f}%')