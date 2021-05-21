from itertools import combinations

anz = 0

vs = set()
for n in range(1,7):
  for a in combinations(range(12),n):
    for b in combinations(range(12),n):
      if set(a) & set(b): continue
      if (b,a) in vs: continue
      anz += 1
      vs.add((a,b))

print(anz)
print(len(vs))