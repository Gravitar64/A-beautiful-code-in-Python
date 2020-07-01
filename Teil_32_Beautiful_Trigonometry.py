import pygame as pg
import math
from Vector import Vec, pol2cart

pg.init()
auflösung = Vec(1000,1000)
screen = pg.display.set_mode(auflösung)
radius = min(auflösung * 0.4)
zentrum = auflösung / 2

weitermachen = True
clock = pg.time.Clock()
rotierenden_winkel = 0
anz_segmente = 0 

while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_KP_PLUS:
      anz_segmente += 1   
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_KP_MINUS:
      anz_segmente = max(0, anz_segmente - 1)   
  screen.fill((0,0,0))
  pg.draw.circle(screen, pg.Color("darkolivegreen1"), zentrum, radius, 1)
  rotierenden_winkel += 0.03
  rotierender_punkt = pol2cart(radius, rotierenden_winkel) + zentrum
  pg.draw.circle(screen, pg.Color("darkolivegreen1"), rotierender_punkt, 5)

  for segment_nr in range(anz_segmente):
    segment_größe = math.pi / anz_segmente
    segment_start_winkel = segment_größe * segment_nr
    segment_end_winkel = segment_start_winkel + math.pi
    linie_start = pol2cart(radius, segment_start_winkel) + zentrum
    linie_end = pol2cart(radius, segment_end_winkel) + zentrum
    pg.draw.line(screen, pg.Color("gray29"),linie_start, linie_end, 1)
    rotierender_punkt_rotiert_ntes_Segment = rotierender_punkt.rotate2D(zentrum, -segment_start_winkel)
    rotierter_punkt_projektion = Vec(rotierender_punkt_rotiert_ntes_Segment[0], zentrum[1])
    osz_punkt = rotierter_punkt_projektion.rotate2D(zentrum, segment_start_winkel)
    pg.draw.circle(screen, pg.Color("darkgoldenrod1"), osz_punkt, 10)
  pg.display.flip()

pg.quit()
