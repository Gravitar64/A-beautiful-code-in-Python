import random as rnd

anz_karten = 20
karten = [1] * anz_karten

zähler = 0
while any(karten):
  einsen = [i for i, k in enumerate(karten) if k == 1]
  i = rnd.choice(einsen)
  karten[i] = 0
  if i < anz_karten - 1:
    karten[i + 1] = 0 if karten[i + 1] == 1 else 1
  zähler += 1
  print(f'{zähler:<3} {"".join(map(str,karten))}')
