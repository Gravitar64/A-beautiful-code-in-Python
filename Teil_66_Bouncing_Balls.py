import pygame as pg
import math

class Vec(tuple):
  """Eigene Vektor-Klasse um 2D-nDimensionale Koordinaten zu hinterlegen und zu addieren, subtrahieren, etc."""
  def __new__(cls, *args):
    return tuple.__new__(cls, args)

  def __add__(self, other):
    if type(other) == 'int' or type(other) == 'float':
      other = tuple(other for _ in range(len(self)))
    return Vec(*tuple(a+b for a, b in zip(self, other)))

  def __sub__(self, other):
    if type(other) == 'int' or type(other) == 'float':
      other = tuple(other for _ in range(len(self)))
    return Vec(*tuple(a-b for a, b in zip(self, other)))

  def __mul__(self, faktor):
    return Vec(*tuple(a*faktor for a in self))

  def __truediv__(self, divisor):
    return Vec(*tuple(a / divisor for a in self))  

  def abstand_euklid(self, other):
    return (sum(abs(a-b)**2 for a,b in zip(self, other)))**0.5

  def dot(self, other):
    return sum(a*b for (a,b) in zip(self, other))

  def normalize(self):
    return self / self.abstand_euklid((0,0))  


def pol2cart(radius, winkel_rad):
  return Vec(radius * math.cos(winkel_rad), radius * math.sin(winkel_rad))

def find_intersection(c,pos):
  ax, ay = pos[0]
  cx, cy = zentrum
  vel = pos[1]
  LAB = vel.abstand_euklid((0,0))
  bx, by = pos[0]+pos[1]
  dx, dy  = vel.normalize()
  area2 = abs( (bx-ax)*(cy-ay) - (cx-ax)*(by-ay) )
  h = area2/LAB
  t = dx*(cx-ax) + dy*(cy-ay)
  dt = math.sqrt( 640**2 - h**2 )
  return Vec(ax + (t+dt) * dx, ay + (t+dt) * dy)

def reflected(b,ip):
  dist_to_circle = b[0].abstand_euklid(ip)
  lenght_moving_vector = b[1].abstand_euklid((0,0))
  rest_lenght = lenght_moving_vector - dist_to_circle
  v = b[1]
  n = (ip - zentrum).normalize()
  b[1] = v - n * 2*v.dot(n)
  v_rest = b[1].normalize()*rest_lenght
  b[0] = ip + v_rest
  return b



pg.init()
BREITE, HÖHE = 1280, 1280
clock = pg.time.Clock()
FPS = 40
zentrum = Vec(BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))
color = pg.Color(0)
balls = [[Vec(x,x), Vec(15,-4)] for x in range(400,600)]
lines = [[b[0]] for b in balls]
x = y = 0

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      quit()
  screen.fill('#000000')
  pg.draw.circle(screen,'#FFFFFF',zentrum,640,2)
  for i,b in enumerate(balls):
    lines[i].append(b[0])
    b[0] += b[1]
    intersect= find_intersection(zentrum, b)
    if b[0].abstand_euklid(intersect) < b[1].abstand_euklid((0,0)):
      b = reflected(b,intersect)
      lines[i].append(intersect)
    color.hsva = ((i*20)%360,100,100,0)
    pg.draw.circle(screen,color,b[0],5)  
    pg.draw.circle(screen,'#00AA00',intersect,5)
  pg.draw.lines(screen,color,False,[b[0] for b in balls])
  # for i,l in enumerate(lines):
  #   color.hsva = ((i*20)%360,100,100,0)
  #   pg.draw.lines(screen, color, False, l ,width=1)
  pg.display.flip()
pg.quit()