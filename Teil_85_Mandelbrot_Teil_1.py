import pygame as pg


def zeichne_fractal(x1, x2, y1, y2, max_iter):
  schritt_x = (x2-x1) / breite
  schritt_y = (y2-y1) / höhe
  for y in range(höhe):
    for x in range(breite):
      c = complex(x1 + x*schritt_x, y1 + y*schritt_y)
      z = 0
      for i in range(max_iter):
        z = z**2 + c
        if abs(z) > 2:
          break
      farbe = 255 / max_iter * i
      fenster.set_at((x, y), (farbe, farbe, farbe))


pg.init()
größe = breite, höhe = 800, 600
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()

x1, x2 = -2, 1
y1, y2 = -1, 1
max_iter = 30

zeichne_fractal(x1, x2, y1, y2, max_iter)
pg.display.flip()

while True:
  clock.tick()
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()
