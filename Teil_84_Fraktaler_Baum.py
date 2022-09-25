import pygame as pg
from Teil_25_Vektor import Vec, pol2cart


def zeichne_baum(von, 𝜙, verzweigungen):
  if not verzweigungen: return
  zu = von + pol2cart(r, 𝜙) * verzweigungen
  farbe.hsva = (120, sh*verzweigungen, sh*verzweigungen)
  pg.draw.line(fenster, farbe, von, zu, 3)
  zeichne_baum(zu, 𝜙+𝛽, verzweigungen-1)
  zeichne_baum(zu, 𝜙-𝛽, verzweigungen-1)


FENSTER_G = BREITE, HÖHE = 1920, 1080
fenster = pg.display.set_mode(FENSTER_G)
𝜙, 𝛽, r, verzweigungen = 270, 20, 14, 12
farbe, sh = pg.Color(0), int(100/verzweigungen)
clock = pg.time.Clock()

zeichne_baum(Vec(BREITE / 2, HÖHE), 𝜙, verzweigungen)
pg.display.flip()

while True:
  clock.tick(5)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
