with open("Teil_65_puzzle1.txt") as f:
  puzzle = [[int(nr) for nr in zeile.split()] for zeile in f][2:]

kanten = {1:[(0,2)], 2:[(1,1)], 3:[(1,0)], 4:[(2,2)], 5:[(4,1)], 
          6:[(4,0)], 7:[(6,1), (3,2)], 8:[(7,0)]}

def dfs(lösung,benutzt,tiefe):
  if tiefe == 9: return lösung
  for i in range(9):
    if i in benutzt: continue
    for _ in range(3):
      puzzle[i] = puzzle[i][1:] + puzzle[i][:1]
      if tiefe == 0:
        l = dfs(lösung + [puzzle[i]], benutzt.union({i}), tiefe+1)
      else:  
        if sum([puzzle[i][k]+lösung[p][k] for p,k in kanten[tiefe]])  != 0: continue
        l = dfs(lösung + [puzzle[i]], benutzt.union({i}), tiefe+1)
      if l: 
        return l
      
print(dfs([], set(), 0))