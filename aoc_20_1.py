from collections import defaultdict
f=open("adventOfcode_20.txt").read()
dd={"N":(0,-1),"E":(1,0),"S":(0,1),"W":(-1,0)}
p=[]
px,py=x,y=0,0
d=defaultdict(int)
for c in f[1:-2]:
 if c=="(":
  p.append((x, y))
 elif c==")":
  x,y=p.pop()
 elif c=="|":
  x,y=p[-1]
 else:
  dx,dy=dd[c]
  x+=dx
  y+=dy
  d[x,y]=min(d[x,y],d[px,py]+1) if d[x,y] else d[px,py]+1
 px,py=x,y
dv=d.values()
print(d)
print(max(dv))
print(len([x for x in dv if x>=1000]))