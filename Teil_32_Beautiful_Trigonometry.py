#pygame ab Version 2.0 wird benötigt
#Installation im Terminal mit --> pip install pygame==2.0.0.dev10 
import pygame as pg
#Vektor-Modul aus meiner YouTube-Reihe wird benötigt
#kann hier über dem Browser kopiert werden 
# https://github.com/Gravitar64/A-beautiful-code-in-Python/blob/master/Teil_25_Vektor.py
from Teil_25_Vektor import Vec, pol2cart
import math

pg.init()
auflösung = Vec(1000,1000)
screen = pg.display.set_mode(auflösung)
zentrum = auflösung / 2
radius = min(auflösung * 0.4)

weitermachen = True
clock = pg.time.Clock()

rotierender_winkel = 0
anz_segemente = 10
while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_KP_PLUS:
      anz_segemente += 1
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_KP_MINUS:
      anz_segemente = max(0, anz_segemente - 1)
     


  screen.fill((0,0,0))
  #ab hier wird mit 40 FPS das Bild im Hintergrund gezeichnet
  pg.draw.circle(screen,pg.Color("darkseagreen4"), zentrum, radius, 3) 
  rotierender_winkel += 0.03
  rotierende_punkt = pol2cart(radius, rotierender_winkel) + zentrum
  pg.draw.circle(screen,pg.Color("darkseagreen4"), rotierende_punkt, 10) 

  for segment_nr in range(anz_segemente):
    delta_winkel = math.pi / anz_segemente
    start_winkel_segment = delta_winkel * segment_nr
    end_winkel_segment = start_winkel_segment + math.pi
    start_linie = pol2cart(radius, start_winkel_segment) + zentrum
    end_linie = pol2cart(radius, end_winkel_segment) + zentrum
    pg.draw.line(screen,pg.Color("gray29"), start_linie, end_linie, 1)
    
    #3 Schritte zur Position des oszilierenden goldenen Punktes
    rotierende_punkt_gegen_uhrzeigersinn = rotierende_punkt.rotate2D(zentrum, -start_winkel_segment)
    projezierter_punkt = Vec(rotierende_punkt_gegen_uhrzeigersinn[0], zentrum[1])
    osz_punkt = projezierter_punkt.rotate2D(zentrum, start_winkel_segment)
    pg.draw.circle(screen,pg.Color("darkgoldenrod1"), osz_punkt, 10) 

  #und hier wird das im Hintergrund gezeichnete Bild angezeigt
  pg.display.flip()

pg.quit()