from dataclasses import dataclass
import time

start = time.perf_counter()
directions = {'>':[1,0], 'v':[0,1], '<':[-1,0], '^':[0,-1]}

@dataclass
class Cart():
  x : int
  y : int
  dx : int
  dy : int
  dirIndex : int = 0
  deleted : bool = False

  def move(self):
    self.x += self.dx
    self.y += self.dy
  
  def rotate(self,c):
    if c == '/':  
      self.dx, self.dy = -self.dy, -self.dx
    elif c == '\\':
      self.dx, self.dy = self.dy, self.dx
    elif c == '+':  
      if self.dirIndex == 0:
        self.dx, self.dy = self.dy, -self.dx
      elif self.dirIndex == 2:
        self.dx, self.dy = -self.dy, self.dx
      self.dirIndex = (self.dirIndex + 1) % 3  


map = []
carts = []
with open('AdventOfCode_13.txt') as f:
  for y, zeile in enumerate(f):
    zeile = zeile.strip('\n')
    for x, c in enumerate(zeile):
      if c in directions:
        dx, dy = directions[c]
        carts.append(Cart(x,y,dx,dy))
      map.append(c)        
spalten = len(zeile)

counter = 0
while len(carts)>1:
  counter += 1
  carts.sort(key = lambda s: (s.y, s.x))
  for cart in carts:
    i = cart.y * spalten + cart.x
    c = map[i]
    if c in {'/', '\\', '+'}:
      cart.rotate(c)  
    cart.move()

    koord = {}
    toDel = []
    for n, cart in enumerate(carts):
      k = (cart.x, cart.y)
      if k not in koord:
        koord[k] = n      
      else:
        cart.deleted = True 
        carts[koord[k]].deleted = True 
  carts = [a for a in carts if not a.deleted]
  
c = carts[0]
print(time.perf_counter()-start)
print(counter)
print(f'{c.x},{c.y}')
