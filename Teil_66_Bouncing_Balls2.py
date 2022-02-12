import pygame as pg
import math
from collections import deque

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
    return (sum((a-b)**2 for a,b in zip(self, other)))**0.5

  def magnitude(self):
    return (sum(a**2 for a in self)**0.5)  

  def dot(self, other):
    return sum(a*b for (a,b) in zip(self, other))

  def normalize(self):
    return self / self.magnitude() 

class Ball:
  def __init__(self,pos,vel,farbe):
    self.pos = pos
    self.vel = vel
    self.farbe = farbe
    self.magn = self.vel.magnitude()
    self.find_intersection(zentrum)
    
  def find_intersection(self,c):
    ax, ay  = self.pos
    bx, by  = self.pos + self.vel
    cx, cy  = c
    dx, dy  = self.vel.normalize()
    area2 = abs( (bx-ax)*(cy-ay) - (cx-ax)*(by-ay) )
    h = area2/self.magn
    t = dx*(cx-ax) + dy*(cy-ay)
    dt = math.sqrt( R**2 - h**2 )
    self.intercept = Vec(ax + (t+dt) * dx, ay + (t+dt) * dy)

  def reflect(self, dist2circle):
    rest_l = self.magn - dist2circle
    n = (self.intercept - zentrum).normalize()
    self.vel -= n * 2 * self.vel.dot(n)
    vel_rest = self.vel.normalize()*rest_l
    self.pos = self.intercept + vel_rest

  def update(self):
    dist2circle = self.pos.abstand_euklid(self.intercept)
    if  dist2circle > self.magn:
      self.pos += self.vel
    else:
      self.reflect(dist2circle)
      self.find_intersection(zentrum)  
    
pg.init()
BREITE, HÖHE = 1000,1000
R = BREITE // 2
clock = pg.time.Clock()
FPS = 40
zentrum = Vec(BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))
balls = []
for x in range(R-200,R+200):
  color = pg.Color(0)
  color.hsva = (x%360,100,100,0)
  balls.append(Ball(Vec(x,R), Vec(0,10), color))
lines = [[deque(b.pos)] for b in balls]
x  = y = 0
max_trail = 8

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      quit()
  screen.fill('#000000')
  pg.draw.circle(screen,'#FFFFFF',zentrum,R,2)
  for i,b in enumerate(balls):
    b.update()
    lines[i].append(b.pos)
    if len(lines[i]) > max_trail: lines[i].pop(0)
    pg.draw.circle(screen,b.farbe,b.pos,5)
  #pg.draw.lines(screen,color,False,[b.pos for b in balls])
  for i,b in enumerate(balls):
    pg.draw.lines(screen, b.farbe, False, lines[i] ,width=1)
  pg.display.flip()
pg.quit()