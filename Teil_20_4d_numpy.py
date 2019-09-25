import numpy as np
from math import sin, cos
import pygame as pg

def kanten_ermitteln(objekt):
    kanten = []
    for i in range(len(objekt) - 1):
        for j in range(i + 1, len(objekt)):
            abst = round(np.linalg.norm(objekt[i] - objekt[j]), 2)
            if abst != 2.0: continue
            kanten.append((i,j))    
    return kanten

def drehen4D(winkels, objekt):
    x, y, z, w = np.radians(winkels)
    if x:
        sin_rad = sin(x)
        cos_rad = cos(x)
        drehmatrix = np.array([[1, 0, 0, 0], [0, cos_rad, sin_rad, 0],
                               [0, -sin_rad, cos_rad, 0], [0, 0, 0, 1]])
        objekt = objekt @ drehmatrix
    if y:
        sin_rad = sin(y)
        cos_rad = cos(y)
        drehmatrix = np.array([[cos_rad, 0, -sin_rad, 0], [0, 1, 0, 0],
                               [sin_rad, 0, cos_rad, 0], [0, 0, 0, 1]])
        objekt = objekt @ drehmatrix
    if z:
        sin_rad = sin(z)
        cos_rad = cos(z)
        drehmatrix = np.array([[cos_rad, sin_rad, 0, 0], [-sin_rad, cos_rad, 0, 0], 
                               [0, 0, 1, 0], [0, 0, 0, 1]])
        objekt = objekt @ drehmatrix
    if w:
        sin_rad = sin(w)
        cos_rad = cos(w)
        drehmatrixYW = np.array([[1, 0, 0, 0], [0, cos_rad, 0, -sin_rad],
                                 [0, 0, 1, 0], [0, sin_rad, 0, cos_rad]])
        objekt = objekt @ drehmatrixYW
    return objekt

SCALE = 500
WINDOW = [800, 600]
TRANSFORM = np.array([400, 300, 300, 300])
pg.init()
screen = pg.display.set_mode(WINDOW)

tasten = {pg.K_x: 0, pg.K_y: 0, pg.K_z: 0, pg.K_w: 0}
hyperCube = np.array([[-1, -1, -1, -1], [1, -1, -1, -1], [1, 1, -1, -1], [-1, 1, -1, -1], 
                      [-1, -1, 1, -1], [1, -1, 1, -1], [1, 1, 1, -1], [-1, 1, 1, -1], 
                      [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
                      [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1]])
kanten = kanten_ermitteln(hyperCube)

weitermachen = True
clock = pg.time.Clock()
while weitermachen:
    screen.fill((0, 0, 0))
    clock.tick(80)
    for ereignis in pg.event.get():
        if ereignis.type == pg.QUIT:
            weitermachen = False
        if ereignis.type == pg.KEYDOWN and ereignis.key in tasten:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                tasten[ereignis.key] -= 0.1
            else:
                tasten[ereignis.key] += 0.1
    hyperCube = drehen4D(list(tasten.values()), hyperCube)
    projektion2D = []
    for punkt in hyperCube:
        w1 = 4 / (8 - punkt[3])
        persp_projektion3D = np.array([[w1, 0, 0, 0], [0, w1, 0, 0],
                                       [0, 0, w1, 0], [0, 0, 0, 0]])
        pos = punkt @ persp_projektion3D
        z1 = 4 / (8 - punkt[2])
        persp_projektion2D = np.array([[z1, 0, 0, 0], [0, z1, 0, 0],
                                       [0, 0, 0, 0], [0, 0, 0, 0]])
        pos = pos @ persp_projektion2D
        pos = pos * SCALE + TRANSFORM
        projektion2D.append(pos[:2])

    for i1, i2 in kanten:
        pg.draw.line(screen, (255, 255, 255), projektion2D[i1], projektion2D[i2], 1)
    for pos in projektion2D:
        pg.draw.circle(screen, (255, 0, 0), pos, 7)

    pg.display.flip()

pg.quit()
