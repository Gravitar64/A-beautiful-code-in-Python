n = 9
summe = (n**3+n)//2

print(f'Magisches Quadrat mit Kantenlänge = {n} und {summe} als Summe')

quadrat = [[0]*n for _ in range(n)]
z, s = 0, n//2
for i in range(1, n**2+1):
  quadrat[z][s] = i
  z2, s2 = z-1, s+1
  if z2 < 0: z2 += n
  if s2 == n: s2 = 0
  if quadrat[z2][s2]:
    z += 1
  else:
    z, s = z2, s2

for z in quadrat:
  for n in z:
    print(f'{n:<2} ', end='')
  print()