import pygame as pg
import numpy as np
from pyquaternion import Quaternion

x = y = z = 0
tasten = {pg.K_x: x, pg.K_y: y, pg.K_z: z}

würfel = np.array([[1., 0, 0], [0, 1, 0], [0, 0, 1], 
                   [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                   [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]])

def drehen3D(objekt, winkelwerte):  
  qs = []
  for i in range(3):
    qs.append(Quaternion(axis=würfel[i], degrees=winkelwerte[i]))  
  q = qs[0] * qs[1] * qs[2]
  for i, punkt in enumerate(objekt):
    objekt[i] = q.rotate(punkt)
  return objekt[3:]


WINDOW = [800, 600]
TRANSFORM = [400, 300]
SKALIERUNG = 120

pg.init()
screen = pg.display.set_mode(WINDOW)

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
    clock.tick(80)
    screen.fill((0, 0, 0))
    for ereignis in pg.event.get():
        if ereignis.type == pg.QUIT:
            weitermachen = False
        if ereignis.type == pg.KEYDOWN and ereignis.key in tasten:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                tasten[ereignis.key] -= 0.1
            else:
                tasten[ereignis.key] += 0.1
    gedrehterWürfel = drehen3D(würfel, list(tasten.values()))
    projektion2D = []
    for punkt in gedrehterWürfel:
        z1 = 3 / (4 - punkt[2])
        persp_projektion = np.array([[z1, 0, 0], [0, z1, 0], [0, 0, 1]])
        pos = np.matmul(punkt, persp_projektion)
        pos = pos[:2]
        projektion2D.append(pos * SKALIERUNG + TRANSFORM)
    for i in range(4):
        p1,p2 = projektion2D[i], projektion2D[(i + 1) % 4]
        p3,p4 = projektion2D[i + 4], projektion2D[(i + 1) % 4 + 4]
        pg.draw.line(screen, (255, 255, 255), p1, p2, 1)
        pg.draw.line(screen, (255, 255, 255), p3, p4, 1)
        pg.draw.line(screen, (255, 255, 255), p1, p3, 1)

    for pos in projektion2D:
        pg.draw.circle(screen, (255, 0, 0), pos, 5)

    pg.display.flip()

pg.quit()
