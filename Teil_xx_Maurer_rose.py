import pygame as pg, math

BREITE, HÖHE = 600, 600
SCALE = 300
TRANSLATE_X, TRANSLATE_Y = BREITE // 2, HÖHE // 2
pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
weitermachen = True
clock = pg.time.Clock()

n = 1
d = 29

while weitermachen:
    n = (n+0.00003) % 8
    d = (d + 0.00003) % 100
    clock.tick(60)
    screen.fill((0, 0, 0))

    for ereignis in pg.event.get():
        if ereignis.type == pg.QUIT:
            weitermachen = False

    points = []
    for i in range(360):
        k = i * d
        r = math.sin(math.radians(n * k))
        k = math.radians(k)
        x = r * math.cos(k) * SCALE + TRANSLATE_X
        y = r * math.sin(k) * SCALE + TRANSLATE_Y
        points.append((x, y))

    pg.draw.polygon(screen, (191, 62, 255), points, 1)
    pg.display.flip()
pg.quit()