import pygame as pg
import numpy as np
import quaternion as quat

x = y = z = 0
tasten = {pg.K_x: x, pg.K_y: y, pg.K_z: z}

#array mit 1 Real- und 3 imaginären Werten (= x,y,z-Koordinaten)
#die ersten 3 Werte sind die x,y,z-Achsen, um die gedreht wird und die
#sich auch mitdrehen, da wir um die lokalen Körperachsen drehen
würfel = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0., -1, -1, -1],
                   [0, 1, -1, -1], [0, 1, 1, -1], [0, -1, 1, -1],
                   [0, -1, -1, 1], [0, 1, -1, 1], [0, 1, 1, 1], [0, -1, 1, 1]])


def drehen3D(objekt, winkelwerte):
    for j, theta in enumerate(winkelwerte):
        #j = 0-2 und damit auch gleich aus objekt[0-2] die Objektachsen
        theta = np.radians(theta)
        axis_angle = (theta * 0.5) * objekt[j] / np.linalg.norm(objekt[j])
        for i, punkt in enumerate(objekt):
            vec = quat.quaternion(*punkt)
            qlog = quat.quaternion(*axis_angle)
            q = np.exp(qlog)
            vec = q * vec * np.conjugate(q)
            objekt[i] = np.array([0, *vec.imag])
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

    #hier zeichnen wir den Würfel
    gedrehterWürfel = drehen3D(würfel, tasten.values())
    projektion2D = []
    for punkt in gedrehterWürfel:
        punkt = punkt[1:]
        z1 = 3 / (4 - punkt[2])
        persp_projektion = np.array([[z1, 0, 0], [0, z1, 0], [0, 0, 1]])
        pos = np.matmul(punkt, persp_projektion)
        pos = pos[:2]
        projektion2D.append(pos * SKALIERUNG + TRANSFORM)
    for i in range(4):
        p1 = projektion2D[i]
        p2 = projektion2D[(i + 1) % 4]
        p3 = projektion2D[i + 4]
        p4 = projektion2D[(i + 1) % 4 + 4]
        pg.draw.line(screen, (255, 255, 255), p1, p2, 1)
        pg.draw.line(screen, (255, 255, 255), p3, p4, 1)
        pg.draw.line(screen, (255, 255, 255), p1, p3, 1)

    for pos in projektion2D:
        pg.draw.circle(screen, (255, 0, 0), pos, 5)

    pg.display.flip()

pg.quit()
