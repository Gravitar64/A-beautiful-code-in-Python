import numpy as np 
from math import cos, sin
import pygame as pg 

WINDOW = [800,600]
TRANSFORM = [400, 300]
SKALIERUNG = 120

würfel = np.array([[-1,-1,-1,-1], [1,-1,-1,-1], [1,1,-1,-1], [-1,1,-1,-1],
                   [-1,-1,1,-1], [1,-1,1,-1], [1,1,1,-1], [-1,1,1,-1],
                   [-1,-1,-1,1], [1,-1,-1,1], [1,1,-1,1], [-1,1,-1,1],
                   [-1,-1,1,1], [1,-1,1,1], [1,1,1,1], [-1,1,1,1]])

def kanten_ermitteln(objekt):
  kanten=[]
  for i in range(len(objekt)-1):
    for j in range(i+1,len(objekt)):
      abst = round(np.linalg.norm(objekt[i]-objekt[j]),2)
      if abst != 2.0: continue
      kanten.append((i,j))
  return kanten                       

def drehen4D(objekt, winkelwerte):
  wx, wy, wz, ww = np.radians(winkelwerte)
  if wx:
    rotMatrix = np.array([[1,0,0,0],
                          [0, cos(wx), -sin(wx),0],
                          [0, sin(wx), cos(wx),0],
                          [0, 0, 0, 1]])                    
    objekt = objekt @ rotMatrix
  if wy:
    rotMatrix = np.array([[cos(wy), 0, sin(wy),0],
                          [0, 1, 0,0],
                          [-sin(wy), 0, cos(wy),0],
                          [0, 0, 0, 1]])                    
    objekt = objekt @ rotMatrix
  if wz:
    rotMatrix = np.array([[cos(wz), -sin(wz), 0, 0],
                          [sin(wz), cos(wz), 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])                    
    objekt = objekt @ rotMatrix
  if ww:
    rotMatrix = np.array([[1,0,0,0],
                          [0, cos(ww), 0, -sin(ww)],
                          [0,0,1,0],
                          [0, sin(ww), 0, cos(ww)]])
    objekt = objekt @ rotMatrix                        
  return objekt    


pg.init()
screen = pg.display.set_mode(WINDOW)

weitermachen = True
clock = pg.time.Clock()
wx = wy = wz = ww = 0
kanten = kanten_ermitteln(würfel)

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
      if ereignis.key == pg.K_w:
        ww += 0.1  
               
  
  #hier zeichnen wir den Würfel
  würfel = drehen4D(würfel,[wx, wy, wz, ww])
  projektion2D = []
  for punkt in würfel:
    w1 = 4 / (4- punkt[3])
    persp_projektion = np.array([[w1,0,0,0],
                                 [0,w1,0,0],
                                 [0,0,w1,0],
                                 [0,0,0,0]])
    pos = punkt @ persp_projektion  
    z1 = 4 / (4- punkt[2])
    persp_projektion = np.array([[z1,0,0,0],
                                 [0,z1,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0]])
    pos = pos @ persp_projektion                           
    pos = pos[:2]
    projektion2D.append(pos * SKALIERUNG + TRANSFORM)
  

  for i1,i2 in kanten:
    punkt1 = projektion2D[i1]
    punkt2 = projektion2D[i2]
    pg.draw.line(screen,(255,255,255), punkt1, punkt2, 1)
  
  for pos in projektion2D:
    pg.draw.circle(screen, (255,0,0), pos,5)

  pg.display.flip()

pg.quit()      
