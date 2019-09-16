import numpy as np 
from math import cos, sin
import pygame as pg 

WINDOW = [800,600]
TRANSFORM = [400, 300]
SKALIERUNG = 120

würfel = np.array([[-1,-1,-1], [1,-1,-1], [1,1,-1,], [-1,1,-1],
                   [-1,-1,1], [1,-1,1], [1,1,1,], [-1,1,1]])

def drehen3D(objekt, winkelwerte):
  wx, wy, wz = np.radians(winkelwerte)
  if wx:
    rotMatrix = np.array([[1,0,0],
                          [0, cos(wx), -sin(wx)],
                          [0, sin(wx), cos(wx)]])                    
    objekt = np.matmul(objekt, rotMatrix)
  if wy:
    rotMatrix = np.array([[cos(wy), 0, sin(wy)],
                          [0, 1, 0],
                          [-sin(wy), 0, cos(wy)]])                    
    objekt = np.matmul(objekt, rotMatrix)
  if wz:
    rotMatrix = np.array([[cos(wz), -sin(wz), 0],
                          [sin(wz), cos(wz), 0],
                          [0, 0, 1]])                    
    objekt = np.matmul(objekt, rotMatrix)
  return objekt    


pg.init()
screen = pg.display.set_mode(WINDOW)

weitermachen = True
clock = pg.time.Clock()
wx = wy = wz = 0

while weitermachen:
  clock.tick(80)
  screen.fill((0,0,0))
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.KEYDOWN:
      if ereignis.key == pg.K_x:
        wx += 0.1
      if ereignis.key == pg.K_y:
        wy += 0.1
      if ereignis.key == pg.K_z:
        wz += 0.1    
  
  #hier zeichnen wir den Würfel
  würfel = drehen3D(würfel,[wx, wy, wz])
  projektion2D = []
  for punkt in würfel:
    z1 = 3 / (4- punkt[2])
    persp_projektion = np.array([[z1,0,0],
                                 [0,z1,0],
                                 [0,0,1]])
    pos = np.matmul(punkt, persp_projektion)                             
    pos = pos[:2]
    projektion2D.append(pos * SKALIERUNG + TRANSFORM)
  for i in range(4):
    p1 = projektion2D[i]
    p2 = projektion2D[(i+1) % 4]
    p3 = projektion2D[i+4]
    p4 = projektion2D[(i+1) % 4 + 4]
    pg.draw.line(screen, (255,255,255), p1, p2, 1)
    pg.draw.line(screen, (255,255,255), p3, p4, 1)
    pg.draw.line(screen, (255,255,255), p1, p3, 1)


  for pos in projektion2D:
    pg.draw.circle(screen, (255,0,0), pos,5)

  pg.display.flip()

pg.quit()      
