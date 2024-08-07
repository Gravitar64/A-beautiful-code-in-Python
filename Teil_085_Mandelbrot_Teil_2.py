import pygame as pg
import numba
import numpy as np
import math


def pixel2fractal(x, y):
  return x / breite * (x2 - x1), y / höhe * (y2 - y1)


@numba.jit(fastmath=True, parallel=True)
def zeichne_fractal(x1, x2, y1, y2, fractal, max_iter):
  x_s = (x2 - x1) / breite
  y_s = (y2 - y1) / höhe

  for x in numba.prange(breite):
    for y in range(höhe):
      c = complex(x1 + x * x_s, y1 + y * y_s)
      z = 0
      for i in range(max_iter):
        z = z**2 + c
        if z.real ** 2 + z.imag ** 2 > 4: break
      fractal[x][y] = farben[i]
  return fractal


größe = breite, höhe = 900, 600
fenster = pg.display.set_mode(größe, pg.SCALED)
clock = pg.time.Clock()

x1, x2, y1, y2 = -2, 1, -1, 1
fractal = np.full((breite, höhe, 3), (0, 0, 0), dtype=np.uint8)
farben = np.full((20000, 3), (0, 0, 0), dtype=np.uint8)
verschiebe = False
max_iter = 30

for i in range(20000):
  r = int((0.5 * math.sin(0.1 * i + 2.094) + 0.5) * 255)
  g = int((0.5 * math.sin(0.1 * i + 4.188) + 0.5) * 255)
  b = int((0.5 * math.sin(0.1 * i) + 0.5) * 255)
  farben[i] = (r, g, b)


while True:
  clock.tick()
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN and not verschiebe:
      if pg.mouse.get_pressed()[0]:
        mx, my = pg.mouse.get_pos()
        verschiebe = True
    if verschiebe and ereignis.type != pg.MOUSEBUTTONUP:
      mx2, my2 = pg.mouse.get_pos()
      dx, dy = pixel2fractal(mx2 - mx, my2 - my)
      x1 -= dx
      x2 -= dx
      y1 -= dy
      y2 -= dy
      mx, my = mx2, my2
    if verschiebe and ereignis.type == pg.MOUSEBUTTONUP:
      verschiebe = False
    if ereignis.type == pg.MOUSEWHEEL:
      dx, dy = pixel2fractal(breite / 10, höhe / 10)
      if ereignis.y == -1:
        x1 -= dx
        x2 += dx
        y1 -= dy
        y2 += dy
      elif ereignis.y == 1:
        x1 += dx
        x2 -= dx
        y1 += dy
        y2 -= dy
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_UP:
      max_iter *= 2
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_DOWN:
      max_iter /= 2

  fractal = zeichne_fractal(x1, x2, y1, y2, fractal, max_iter)
  pg.surfarray.blit_array(fenster, fractal)
  pg.display.flip()
  pg.display.set_caption(f'FPS = {clock.get_fps():.1f} Iterationen = {max_iter:,.0f}')
