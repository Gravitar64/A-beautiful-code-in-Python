#pygame ab Version 2.0 wird benötigt
#Installation im Terminal mit 
#   --> pip install pygame (windows) 
#   --> pip3 install pygame (mac)
#   --> sudo apt-get install python3-pygame (Linux Debian/Ubuntu/Mint)

import pygame as pg


pg.init()
BREITE, HÖHE = 1000,1000
FPS = 40
zentrum = (BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  screen.fill((0,0,0))
  #ab hier wird mit 40 FPS das Bild im Hintergrund gezeichnet 
  

  

  #und hier wird das im Hintergrund gezeichnete Bild angezeigt
  pg.display.flip()

pg.quit()
