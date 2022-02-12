import pygame as pg
from clifford.g2c import *

point = up(2*e1+e2)
line = up(3*e1 + 2*e2) ^ up(3*e1 - 2*e2) ^ einf
circle = up(e1) ^ up(-e1 + 2*e2) ^ up(-e1 - 2*e2)

point_refl = circle * point.gradeInvol() * ~circle
line_refl = circle * line.gradeInvol() * ~circle
print(line_refl)



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

# def add_balls(C, R, balls):
#   anz = 2000
#   for x in range(anz):
#     alpha = math.tau / anz * x
#     pos = pol2cart(R, alpha) + C
#     vel = (pos - C).normalize()*7
#     farbe = pg.Color(0)
#     farbe.hsva = (x%360,100,100,0)
#     balls.append(Ball(pos, vel, farbe))



# pg.init()
# BREITE, HÖHE = 1000,1000
# R = BREITE // 2
# clock = pg.time.Clock()
# FPS = 30
# zentrum = Vec(BREITE / 2, HÖHE / 2)
# screen = pg.display.set_mode((BREITE, HÖHE))
# balls = []

# #lines = [[deque(b.pos)] for b in balls]
# x  = y = 0
# max_trail = 8
# drop_R = 100
# old_mouse = pg.mouse.get_pos()
# show_drop = False

# while True:
#   clock.tick(FPS)
#   for ereignis in pg.event.get():
#     if ereignis.type == pg.QUIT:
#       quit()
#     if ereignis.type == pg.MOUSEWHEEL:
#       drop_R += 10 if ereignis.y < 0 else -10
#     if ereignis.type == pg.MOUSEBUTTONDOWN and ereignis.button == 1:
#       add_balls(mousePos, drop_R, balls)
#     if ereignis.type == pg.MOUSEBUTTONDOWN and ereignis.button == 3:
#       balls = [] 
#     if ereignis.type == pg.USEREVENT:
#       show_drop = False     
      

#   screen.fill('#000000')
#   pg.draw.circle(screen,'#FFFFFF',zentrum,R,2)
#   mousePos = pg.mouse.get_pos()
#   if mousePos != old_mouse:
#     pg.time.set_timer(pg.USEREVENT,3000,False)
#     show_drop = True
#     old_mouse = mousePos
#   if show_drop:
#     pg.draw.circle(screen,'#606060',mousePos,drop_R,2)

#   for i,b in enumerate(balls):
#     b.update()
#     # lines[i].append(b.pos)
#     # if len(lines[i]) > max_trail: lines[i].pop(0)
#     pg.draw.circle(screen,b.farbe,b.pos,8)
#   # if balls:
#   #   pg.draw.lines(screen,'#400000',False,[b.pos for b in balls])
#   # for i,b in enumerate(balls):
#   #   pg.draw.lines(screen, b.farbe, False, lines[i] ,width=1)
#   pg.display.flip()
# pg.quit()