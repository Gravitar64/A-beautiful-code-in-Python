import pygame as pg
from Teil_25_Vektor import Vec, pol2cart
import math


def fib(n):
  if n < 2:
    return n
  return fib(n-1) + fib(n-2)



def golden_spiral(n):
  ausgl = Vec(22, 23)
  G=(1+5**.5)/2
  w=int(G**(4*(n//4)))
  k=math.pi/180
  return [Vec(G**(j/90)*math.cos(j*k)-w/2,G**(j/90)*math.sin(j*k)-w/2)*3+ausgl+offset for j in range(n*90)]


pg.init()
SCALE = 20
auflösung = Vec(1000, 1000)
screen = pg.display.set_mode(auflösung)
offset = auflösung / 3 

weitermachen = True
clock = pg.time.Clock()
boxes = [Vec(0,0), Vec(-1,0), Vec(-1,1), Vec(1,0), Vec(-1,-5), Vec(-9,-5), Vec(-9,3), Vec(4,-5)]
points = golden_spiral(8)


while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  for n,b in enumerate(boxes):
    size = fib(n+1)*SCALE
    pg.draw.rect(screen, pg.Color('grey'), (b*SCALE+offset, (size, size)), 3)
  pg.draw.lines(screen,pg.Color('red'), False, points, 7)
  
  pg.display.update()

pg.quit()
