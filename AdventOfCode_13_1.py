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

def show():
  for i, c in enumerate(map):
    x = i % spalten
    y = i // spalten
    for cart in carts:
      if x == cart.x and y == cart.y:
        c = 'O'
        break
    print(c, end='')
    if (i+1)%spalten == 0:
      print()




#show()
collision = False
counter = 0
while not collision:
  counter += 1
  carts.sort(key = lambda s: (s.y, s.x))
  for cart in carts:
    i = cart.y * spalten + cart.x
    c = map[i]
    if c in {'/', '\\', '+'}:
      cart.rotate(c)  
    cart.move()
    
    #show()
    
    koord = set()
    for cart in carts:
      k = (cart.x, cart.y)
      if k in koord:
        collision = True
        lösung = k
        break
      else:
        koord.add(k)         
print(time.perf_counter()-start)
print(counter)
print(lösung)

