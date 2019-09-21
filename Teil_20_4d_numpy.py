import numpy as np
from math import sin, cos
import pygame as pg

SCALE = 500
WINDOW = [800, 600]
TRANSFORM = np.array([400, 300, 300, 300])


def drehen4D(winkels, objekt):
  x, y, z, w = np.radians(winkels)
  if x:
    sin_rad = sin(x)
    cos_rad = cos(x)
    drehmatrix = np.array([[1, 0, 0, 0],
                           [0, cos_rad, sin_rad, 0],
                           [0, -sin_rad, cos_rad, 0],
                           [0, 0, 0, 1]])
    objekt = np.matmul(objekt, drehmatrix)
  if y:
    sin_rad = sin(y)
    cos_rad = cos(y)
    drehmatrix = np.array([[cos_rad, 0, -sin_rad, 0],
                           [0, 1, 0, 0],
                           [sin_rad, 0, cos_rad, 0],
                           [0, 0, 0, 1]])
    objekt = np.matmul(objekt, drehmatrix)
  if z:
    sin_rad = sin(z)
    cos_rad = cos(z)
    drehmatrix = np.array([[cos_rad, sin_rad, 0, 0],
                           [-sin_rad, cos_rad, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
    objekt = np.matmul(objekt, drehmatrix)
  if w:
    sin_rad = sin(w)
    cos_rad = cos(w)
    drehmatrixXW = np.array([[cos_rad,0,0,sin_rad],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [-sin_rad, 0, 0, cos_rad],
                           ])
    drehmatrixYW = np.array([[1,0,0,0],
                             [0, cos_rad, 0, -sin_rad],
                             [0,0,1,0],
                             [0, sin_rad, 0, cos_rad]
                           ])
    drehmatrixZW = np.array([[1,0,0,0],
                           [0, 1, 0, 0],
                           [0, 0, cos_rad, -sin_rad],
                           [0, 0, sin_rad, cos_rad],
                           ])                                              
    objekt = np.matmul(objekt, drehmatrixXW)
  return objekt  


pg.init()
screen = pg.display.set_mode(WINDOW)
hyperCube = np.array([[-1, -1, -1, -1], [1, -1, -1, -1], [1, 1, -1, -1], [-1, 1, -1, -1],
             [-1, -1, 1, -1], [1, -1, 1, -1], [1, 1, 1, -1], [-1, 1, 1, -1],
             [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
             [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1]])


weitermachen = True
clock = pg.time.Clock()
x = y = z = w = 0
while weitermachen:
  screen.fill((0, 0, 0))
  clock.tick(80)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      weitermachen = False
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_x and pg.key.get_mods() & pg.KMOD_SHIFT:
        x -= 0.1
      elif event.key == pg.K_x:
        x += 0.1
      if event.key == pg.K_y and pg.key.get_mods() & pg.KMOD_SHIFT:
        y -= 0.1
      elif event.key == pg.K_y:
        y += 0.1
      if event.key == pg.K_z and pg.key.get_mods() & pg.KMOD_SHIFT:
        z -= 0.1
      elif event.key == pg.K_z:
        z += 0.1
      if event.key == pg.K_w and pg.key.get_mods() & pg.KMOD_SHIFT:
        w -= 0.1
      elif event.key == pg.K_w:
        w += 0.1
      if event.key == pg.K_SPACE:
        x = y = z = w = 0
  hyperCube = drehen4D([x, y, z, w], hyperCube)
  projektion2D = []
  for punkt in hyperCube:
    w1 = 2 / (4- punkt[3])
    persp_projektion3D = np.array([[w1, 0, 0, 0],
                                 [0, w1, 0, 0],
                                 [0, 0, w1, 0],
                                 [0, 0, 0, 0]])
    pos = np.matmul(punkt, persp_projektion3D)
    z1 = 2 / (4 - punkt[2])
    persp_projektion2D = np.array([[z1, 0, 0, 0],
                                 [0, z1, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0]])
    pos = np.matmul(pos, persp_projektion2D)                             
    pos = pos * SCALE + TRANSFORM
    projektion2D.append(pos[:2])

  for pos in projektion2D:
    pg.draw.circle(screen, (255, 255, 255), pos, 7)
  for i in range(4):
    pg.draw.line(screen, (255, 255, 255),
                 projektion2D[i], projektion2D[(i+1) % 4], 1)
    pg.draw.line(screen, (255, 255, 255),
                 projektion2D[i+4], projektion2D[(i+1) % 4+4], 1)
    pg.draw.line(screen, (255, 255, 255),
                 projektion2D[i], projektion2D[i+4], 1)
    pg.draw.line(screen, (255, 255, 255),
                 projektion2D[i+8], projektion2D[(i+1) % 4+8], 1)
    pg.draw.line(screen, (255, 255, 255),
                 projektion2D[i+12], projektion2D[(i+1) % 4+12], 1)
    pg.draw.line(screen, (255, 255, 255),
                 projektion2D[i+8], projektion2D[(i+12)], 1)
    pg.draw.line(screen, (255, 255, 255), projektion2D[i], projektion2D[i+8],1)
    pg.draw.line(screen, (255, 255, 255), projektion2D[i+4], projektion2D[i+12],1)
  pg.display.flip()


pg.quit()
