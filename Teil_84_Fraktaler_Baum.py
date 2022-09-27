import pygame as pg
from pygame import Vector2 as Vec


def zeichne_baum(von, 𝜙, verzweigungen):
  if not verzweigungen: return
  zu = Vec(); zu.from_polar((r, 𝜙)); zu = von + zu * verzweigungen
  farbe.hsva = (120, sv*verzweigungen, sv*verzweigungen)
  pg.draw.line(fenster, farbe, von, zu, 3)
  zeichne_baum(zu, 𝜙+𝛽, verzweigungen-1)
  zeichne_baum(zu, 𝜙-𝛽, verzweigungen-1)


FENSTER_G = Vec(1920, 1080)
fenster = pg.display.set_mode(FENSTER_G)
clock = pg.time.Clock()

von, r, 𝜙, 𝛽, verzweigungen = Vec(FENSTER_G.x/2, FENSTER_G.y), 10, 270, 20, 12
farbe, sv = pg.Color(0), int(100/verzweigungen)

zeichne_baum(von, 𝜙, verzweigungen)
pg.display.flip()


while True:
  clock.tick(5)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()
