import pygame as pg
import math


def zeichne_baum(x, y, 𝜙, verzweigungen):
  if not verzweigungen: return
  x2 = x + math.cos(𝜙) * r * verzweigungen
  y2 = y + math.sin(𝜙) * r * verzweigungen
  farbe.hsva = (120, sh*verzweigungen, sh*verzweigungen)
  pg.draw.line(fenster, farbe, (x, y), (x2, y2), 3)
  zeichne_baum(x2, y2, 𝜙+𝛽, verzweigungen-1)
  zeichne_baum(x2, y2, 𝜙-𝛽, verzweigungen-1)


pg.init()
fenster_g = fenster_b, fenster_h = 1920, 1080
fenster = pg.display.set_mode(fenster_g)
x, y = fenster_b / 2, fenster_h
𝜙, 𝛽, r, verzweigungen = math.radians(270), math.radians(20), 10, 12
farbe, sh = pg.Color(0), int(100/verzweigungen)


clock = pg.time.Clock()
zeichne_baum(x, y, 𝜙, verzweigungen)
pg.display.flip()

while True:
  clock.tick(5)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
