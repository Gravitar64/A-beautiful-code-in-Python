with open("Teil_65_puzzle1.txt") as f:
  puzzle = [[int(nr) for nr in zeile.split()] for zeile in f][2:]

kanten = {1:[(0,2)], 2:[(1,1)], 3:[(1,0)],
          4:[(2,2)], 5:[(4,1)], 6:[(4,0)],
          7:[(6,1), (3,2)], 8:[(7,0)]}

def dfs(lösung, benutzt, reihenfolge):
  if reihenfolge == 9: return lösung
  for i, teil in enumerate(puzzle):
    if i in benutzt: continue
    for _ in range(3):
      teil = teil[1:] + teil[:1]
      if reihenfolge > 0 and not all([teil[k]+lösung[p][k] == 0 for p,k in kanten[reihenfolge]]): continue
      if (l := dfs(lösung + [teil], benutzt.union({i}), reihenfolge +1)):
        return l

print(dfs([], set(), 0))