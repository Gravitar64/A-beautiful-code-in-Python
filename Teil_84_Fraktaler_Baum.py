import pygame as pg
import math

def zeichne_Baum(x, y, θ, tiefe):
  if not tiefe: return
  x2 = x + math.cos(θ) * länge * tiefe
  y2 = y + math.sin(θ) * länge * tiefe
  farbe.hsva = (120, tiefe*sv, tiefe*sv)
  pg.draw.line(fenster, farbe, (x,y), (x2,y2), 1)
  zeichne_Baum(x2, y2, θ-β, tiefe-1)
  zeichne_Baum(x2, y2, θ+β, tiefe-1)


θ, β, länge, tiefe = math.radians(-90), math.radians(20), 10, 14
clock, breite, höhe = pg.time.Clock(), 1920, 1080
fenster = pg.display.set_mode((breite,höhe))
farbe, sv = pg.Color(0), int(100/tiefe)
zeichne_Baum(breite/2,höhe,θ, tiefe)
pg.display.flip()

while True:
  clock.tick(5)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()