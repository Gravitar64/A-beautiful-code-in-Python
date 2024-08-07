import pygame as pg


def zeichne_fractal(x1, x2, y1, y2):
  x_s = (x2 - x1) / breite
  y_s = (y2 - y1) / höhe

  for x in range(breite):
    for y in range(höhe):
      c = complex(x1 + x * x_s, y1 + y * y_s)
      z = 0
      for i in range(30):
        z = z**2 + c
        if abs(z) > 2: break
      farbe = 255 / 30 * i
      fenster.set_at((x, y), (farbe, farbe, farbe))


größe = breite, höhe = 900, 600
fenster = pg.display.set_mode(größe, pg.SCALED)
clock = pg.time.Clock()

x1, x2, y1, y2 = -2, 1, -1, 1

zeichne_fractal(x1, x2, y1, y2)
pg.display.flip()


while True:
  clock.tick()
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()
