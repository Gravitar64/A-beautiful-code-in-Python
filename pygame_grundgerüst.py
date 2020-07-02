#pygame ab Version 2.0 wird benötigt
#Installation im Terminal mit --> pip install pygame==2.0.0.dev10 
import pygame as pg
#Vektor-Modul aus meiner YouTube-Reihe wird benötigt
#kann hier über dem Browser kopiert werden 
# https://github.com/Gravitar64/A-beautiful-code-in-Python/blob/master/Teil_25_Vektor.py
from Teil_25_Vektor import Vec, pol2cart

pg.init()
auflösung = Vec(1000,1000)
screen = pg.display.set_mode(auflösung)
zentrum = auflösung / 2

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  screen.fill((0,0,0))
  #ab hier wird mit 40 FPS das Bild im Hintergrund gezeichnet 
  

  

  #und hier wird das im Hintergrund gezeichnete Bild angezeigt
  pg.display.flip()

pg.quit()
